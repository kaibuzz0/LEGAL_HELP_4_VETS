#!/usr/bin/env python3
"""Semantic validator for structured state legal data.

JSON Schema handles shape. This module enforces legal-data relationships that are
unsafe to express as loose prose: deadline triggers, authority provenance,
status vocabulary, jurisdiction inheritance, null semantics, and program/law
classification.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "data" / "states"
ALLOWED_STATUS = {"verified", "pilot_partially_verified", "partially_verified", "unverified", "needs_refresh", "deprecated"}
AUTHORITY_STATUS = {"verified", "partially_verified", "unverified", "needs_refresh", "deprecated"}
PROGRAM_TYPES = {"government_program", "LSV-H", "SSVF"}
REFRESH_DAYS = 365


def valid_https(value: str | None) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def authority_date(authority: dict) -> str | None:
    return authority.get("last_verified") or authority.get("verified_date")


def clock_value(clock: dict) -> object:
    return clock.get("value", clock.get("deadline_value"))


def clock_trigger(clock: dict) -> object:
    return clock.get("trigger", clock.get("deadline_trigger"))


def clock_authority(clock: dict) -> object:
    return clock.get("computation_authority", clock.get("time_computation_authority"))


def stale_authority_ids(data: dict, as_of: date | None = None, max_age_days: int = REFRESH_DAYS) -> list[str]:
    as_of = as_of or date.today()
    stale = []
    for authority in data.get("primary_authorities", []):
        checked = authority_date(authority)
        if not checked:
            continue
        if (as_of - parse_date(checked)).days > max_age_days and authority.get("status") not in {"deprecated", "needs_refresh"}:
            stale.append(authority.get("id", "<missing-id>"))
    return stale


def validate_state(data: dict, filename: str = "<memory>") -> list[str]:
    errors: list[str] = []
    state = data.get("state")
    state_status = data.get("status")
    if not state:
        errors.append(f"{filename}: missing state")
    if state_status not in ALLOWED_STATUS:
        errors.append(f"{filename}: unknown state status {state_status!r}")

    authorities = data.get("primary_authorities", [])
    ids = [a.get("id") for a in authorities]
    duplicates = sorted({x for x in ids if x and ids.count(x) > 1})
    if duplicates:
        errors.append(f"{filename}: duplicate authority IDs: {duplicates}")
    known_ids = {x for x in ids if x}

    for authority in authorities:
        aid = authority.get("id", "<missing-id>")
        if authority.get("status") not in AUTHORITY_STATUS:
            errors.append(f"{filename}:{aid}: unknown authority status")
        checked = authority_date(authority)
        if not checked:
            errors.append(f"{filename}:{aid}: authority lacks verification date")
        else:
            try:
                parse_date(checked)
            except ValueError:
                errors.append(f"{filename}:{aid}: malformed verification date")
        url = authority.get("source_url") or authority.get("url")
        if not valid_https(url):
            errors.append(f"{filename}:{aid}: malformed or missing HTTPS source URL")
        if not authority.get("jurisdiction"):
            errors.append(f"{filename}:{aid}: authority lacks jurisdiction")
        if not authority.get("authority_type"):
            errors.append(f"{filename}:{aid}: authority lacks authority_type")

    routes = data.get("document_routes", {})
    if not isinstance(routes, dict):
        errors.append(f"{filename}: document_routes must be an object")
        return errors

    for route_id, route in routes.items():
        status = route.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{filename}:{route_id}: unknown route status {status!r}")
        # State-law routes inherit the state's jurisdiction unless they explicitly override it.
        if not (route.get("jurisdiction") or state):
            errors.append(f"{filename}:{route_id}: state-law route lacks jurisdiction")

        refs = route.get("authorities", [])
        if status == "verified" and route_id != "va_home_loan_default" and not refs:
            errors.append(f"{filename}:{route_id}: verified route lacks authority")
        unknown_refs = sorted(set(refs) - known_ids)
        if unknown_refs:
            errors.append(f"{filename}:{route_id}: unknown authority references {unknown_refs}")

        for field in ("required_actions", "optional_actions"):
            for action in route.get(field, []):
                if not isinstance(action, dict) or action.get("type") not in {"legal_requirement", "practical_action", "optional_action", "legal_help"} or not action.get("text"):
                    errors.append(f"{filename}:{route_id}: {field} action lacks classification/text")

        clocks = []
        if "immediate_clock" in route:
            clocks.append(("immediate_clock", route.get("immediate_clock")))
        clocks.extend(("other_clock", c) for c in route.get("other_clocks", []))
        for clock_name, clock in clocks:
            if clock is None:
                continue  # Unknown means unknown; it is never interpreted as no deadline.
            if not isinstance(clock, dict):
                errors.append(f"{filename}:{route_id}:{clock_name}: clock must be object or null")
                continue
            value = clock_value(clock)
            trigger = clock_trigger(clock)
            if value is not None and not trigger:
                errors.append(f"{filename}:{route_id}:{clock_name}: deadline value lacks triggering event")
            if value is not None and not clock_authority(clock):
                errors.append(f"{filename}:{route_id}:{clock_name}: deadline value lacks computation authority")
            display = str(clock.get("display", "")).lower()
            if clock is None and "no deadline" in display:
                errors.append(f"{filename}:{route_id}:{clock_name}: null converted to no-deadline conclusion")

    for key, resource in data.get("resources", {}).items():
        if resource is None:
            continue
        url = resource.get("url")
        if url and not valid_https(url):
            errors.append(f"{filename}:resource:{key}: malformed URL")

    # Federal assistance programs must not be represented as state legal authority.
    for authority in authorities:
        if authority.get("authority_type") in PROGRAM_TYPES and authority.get("jurisdiction") == state:
            errors.append(f"{filename}:{authority.get('id')}: federal program mislabeled as state legal authority")

    return errors


def load_public_state_files() -> list[Path]:
    return sorted(p for p in STATE_DIR.glob("*.json") if p.name not in {"schema.json", "_template.json"})


def main() -> int:
    failures = []
    warnings = []
    for path in load_public_state_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        failures.extend(validate_state(data, path.name))
        stale = stale_authority_ids(data)
        if stale:
            warnings.append(f"{path.name}: authorities need refresh review: {', '.join(stale)}")
    for warning in warnings:
        print("WARNING:", warning)
    for failure in failures:
        print("ERROR:", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
