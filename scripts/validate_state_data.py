#!/usr/bin/env python3
"""Semantic validator for structured state legal data.

JSON Schema handles shape. This module enforces cross-field legal-data invariants:
authority provenance, route verification, deadline traceability, jurisdiction,
null safety, and separation of legal authority from assistance resources.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "data" / "states"
FEDERAL_OVERLAY_FILE = ROOT / "data" / "housing-federal.json"
ALLOWED_SCHEMA_VERSIONS = {"1.1", "1.2"}
ALLOWED_STATUS = {"verified", "pilot_partially_verified", "partially_verified", "unverified", "needs_refresh", "deprecated"}
AUTHORITY_STATUS = {"verified", "partially_verified", "unverified", "needs_refresh", "deprecated"}
LEGAL_AUTHORITY_TYPES = {"statute", "regulation", "court_rule", "case_law", "agency_guidance", "government_form"}
PROGRAM_AUTHORITY_TYPES = {"government_program"}
ACTION_TYPES = {"legal_requirement", "procedural_requirement", "practical_action", "optional_strategy", "referral", "emergency_action", "optional_action", "legal_help"}
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


def clock_value(clock: dict):
    return clock.get("value", clock.get("deadline_value"))


def clock_unit(clock: dict):
    return clock.get("unit", clock.get("deadline_unit"))


def clock_trigger(clock: dict):
    return clock.get("trigger", clock.get("deadline_trigger"))


def clock_authority(clock: dict):
    return clock.get("computation_authority", clock.get("time_computation_authority"))


def federal_overlay_ids() -> set[str]:
    if not FEDERAL_OVERLAY_FILE.exists():
        return set()
    data = json.loads(FEDERAL_OVERLAY_FILE.read_text(encoding="utf-8"))
    return {item.get("id") for item in data.get("overlays", []) if item.get("id")}


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
    schema_version = data.get("schema_version")
    state = data.get("state")
    state_status = data.get("status")
    strict_12 = schema_version == "1.2"

    if schema_version and schema_version not in ALLOWED_SCHEMA_VERSIONS:
        errors.append(f"{filename}: unsupported schema_version {schema_version!r}")
    if not state:
        errors.append(f"{filename}: missing state")
    if state_status not in ALLOWED_STATUS:
        errors.append(f"{filename}: unknown state status {state_status!r}")

    authorities = data.get("primary_authorities", [])
    ids = [a.get("id") for a in authorities]
    duplicates = sorted({x for x in ids if x and ids.count(x) > 1})
    if duplicates:
        errors.append(f"{filename}: duplicate authority IDs: {duplicates}")
    authority_by_id = {a.get("id"): a for a in authorities if a.get("id")}
    known_ids = set(authority_by_id)

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
        if strict_12 and not authority.get("supports"):
            errors.append(f"{filename}:{aid}: authority lacks supported proposition")

    routes = data.get("document_routes", {})
    if not isinstance(routes, dict):
        errors.append(f"{filename}: document_routes must be an object")
        return errors

    overlay_ids = federal_overlay_ids()
    for route_id, route in routes.items():
        status = route.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{filename}:{route_id}: unknown route status {status!r}")
        route_jurisdiction = route.get("jurisdiction") or state
        if not route_jurisdiction:
            errors.append(f"{filename}:{route_id}: state-law route lacks jurisdiction")

        refs = route.get("authorities", [])
        overlay_refs = route.get("federal_overlays", [])
        unknown_refs = sorted(set(refs) - known_ids)
        if unknown_refs:
            errors.append(f"{filename}:{route_id}: unknown authority references {unknown_refs}")
        unknown_overlays = sorted(set(overlay_refs) - overlay_ids)
        if unknown_overlays:
            errors.append(f"{filename}:{route_id}: unknown federal overlay references {unknown_overlays}")

        # 1.1 compatibility preserves the historical VA route exception; 1.2 removes it.
        if status == "verified" and not refs and not overlay_refs:
            if not (schema_version == "1.1" and route_id == "va_home_loan_default"):
                errors.append(f"{filename}:{route_id}: verified route lacks authority or verified overlay")

        for ref in refs:
            authority = authority_by_id.get(ref)
            if not authority:
                continue
            if authority.get("authority_type") not in LEGAL_AUTHORITY_TYPES:
                errors.append(f"{filename}:{route_id}: resource/program authority {ref!r} cannot support state-law proposition")
            if status == "verified" and authority.get("status") != "verified":
                errors.append(f"{filename}:{route_id}: verified route references non-verified authority {ref!r}")
            if authority.get("status") == "deprecated" and status == "verified":
                errors.append(f"{filename}:{route_id}: verified route references deprecated authority {ref!r}")
            aj = authority.get("jurisdiction")
            if aj and route_jurisdiction and aj not in {route_jurisdiction, "Federal", "United States"}:
                errors.append(f"{filename}:{route_id}: authority {ref!r} has wrong jurisdiction {aj!r}")

        for field in ("required_actions", "optional_actions"):
            for action in route.get(field, []):
                if not isinstance(action, dict) or action.get("type") not in ACTION_TYPES or not action.get("text"):
                    errors.append(f"{filename}:{route_id}: {field} action lacks classification/text")
                    continue
                if action.get("type") in {"legal_requirement", "procedural_requirement"}:
                    aref = action.get("authority")
                    if not aref or aref not in known_ids:
                        errors.append(f"{filename}:{route_id}: legal/procedural action lacks valid authority")

        clocks = []
        if "immediate_clock" in route:
            clocks.append(("immediate_clock", route.get("immediate_clock")))
        clocks.extend(("other_clock", c) for c in route.get("other_clocks", []))
        for clock_name, clock in clocks:
            if clock is None:
                continue  # Null is unknown. No negative legal conclusion is inferred.
            if not isinstance(clock, dict):
                errors.append(f"{filename}:{route_id}:{clock_name}: clock must be object or null")
                continue
            value = clock_value(clock)
            if value is None:
                continue
            trigger = clock_trigger(clock)
            comp_ref = clock_authority(clock)
            if not trigger:
                errors.append(f"{filename}:{route_id}:{clock_name}: deadline value lacks triggering event")
            if not clock_unit(clock):
                errors.append(f"{filename}:{route_id}:{clock_name}: deadline value lacks unit/computation description")
            if not comp_ref:
                errors.append(f"{filename}:{route_id}:{clock_name}: deadline value lacks computation authority")
            elif comp_ref not in known_ids:
                errors.append(f"{filename}:{route_id}:{clock_name}: deadline computation authority {comp_ref!r} does not exist")
            else:
                comp = authority_by_id[comp_ref]
                if comp.get("authority_type") not in LEGAL_AUTHORITY_TYPES:
                    errors.append(f"{filename}:{route_id}:{clock_name}: deadline computation reference is not legal authority")
                if clock.get("verified") is True and comp.get("status") != "verified":
                    errors.append(f"{filename}:{route_id}:{clock_name}: verified deadline uses non-verified authority")
            if clock.get("verified") is not True:
                errors.append(f"{filename}:{route_id}:{clock_name}: numeric deadline must be explicitly verified")
            if not str(clock.get("display", "")).strip():
                errors.append(f"{filename}:{route_id}:{clock_name}: numeric deadline lacks human-reviewed display text")

    for key, resource in data.get("resources", {}).items():
        if resource is None:
            continue
        url = resource.get("url")
        if url and not valid_https(url):
            errors.append(f"{filename}:resource:{key}: malformed URL")

    for authority in authorities:
        if authority.get("authority_type") in PROGRAM_AUTHORITY_TYPES and authority.get("jurisdiction") == state:
            errors.append(f"{filename}:{authority.get('id')}: program mislabeled as state legal authority")

    return errors


def load_public_state_files() -> list[Path]:
    return sorted(p for p in STATE_DIR.glob("*.json") if p.name not in {"schema.json", "_template.json"})


def main() -> int:
    failures = []
    warnings = []
    states = load_public_state_files()
    for path in states:
        data = json.loads(path.read_text(encoding="utf-8"))
        state_errors = validate_state(data, path.name)
        failures.extend(state_errors)
        stale = stale_authority_ids(data)
        if stale:
            warnings.append(f"{path.name}: authorities need refresh review: {', '.join(stale)}")
        if not state_errors:
            print(f"PASS: {data.get('state', path.stem)}")
    for warning in warnings:
        print("WARNING:", warning)
    for failure in failures:
        print("ERROR:", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
