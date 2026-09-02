#!/usr/bin/env python3
"""Semantic validation for data/florida-foreclosure.json."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "florida-foreclosure.json"
REGISTRY = ROOT / "data" / "datasets.json"
ALLOWED_STATUS = {"verified", "partially_verified", "unverified", "deprecated", "needs_refresh", "verified_federal_overlay_only"}
LEGAL_TYPES = {"statute", "regulation", "court_rule", "case_law", "agency_guidance", "government_form"}


def https(url):
    p = urlparse(url or "")
    return p.scheme == "https" and bool(p.netloc)


def validate(data: dict) -> list[str]:
    errors = []
    if data.get("dataset_id") != "florida-foreclosure" or data.get("state") != "Florida" or data.get("subject") != "housing_foreclosure":
        errors.append("dataset must identify Florida housing_foreclosure subject layer")
    if data.get("status") not in ALLOWED_STATUS:
        errors.append("dataset has invalid status")
    authorities = data.get("authorities", [])
    by_id = {a.get("id"): a for a in authorities if a.get("id")}
    if len(by_id) != len(authorities):
        errors.append("authority IDs must be present and unique")
    for a in authorities:
        aid = a.get("id", "<missing>")
        if a.get("authority_type") not in LEGAL_TYPES:
            errors.append(f"{aid}: invalid authority type")
        if a.get("jurisdiction") != "Florida":
            errors.append(f"{aid}: Florida subject authority must identify Florida jurisdiction")
        if not https(a.get("source_url")):
            errors.append(f"{aid}: source must be HTTPS")
        if not a.get("supports"):
            errors.append(f"{aid}: missing supported proposition")
        if a.get("status") not in ALLOWED_STATUS:
            errors.append(f"{aid}: invalid status")
        try:
            datetime.strptime(a.get("last_verified", ""), "%Y-%m-%d")
        except ValueError:
            errors.append(f"{aid}: malformed verification date")
    for rid, route in data.get("routes", {}).items():
        status = route.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{rid}: invalid route status")
        for ref in route.get("authorities", []):
            if ref not in by_id:
                errors.append(f"{rid}: unknown authority {ref}")
        if status == "verified" and not route.get("authorities"):
            errors.append(f"{rid}: verified route lacks authority")
        clocks = []
        if route.get("immediate_clock") is not None:
            clocks.append(route["immediate_clock"])
        clocks.extend(route.get("other_clocks", []))
        for clock in clocks:
            if not isinstance(clock, dict):
                errors.append(f"{rid}: clock must be object or null")
                continue
            if clock.get("value") is None:
                continue
            for field in ("unit", "trigger", "computation_authority", "display"):
                if not clock.get(field):
                    errors.append(f"{rid}: numeric clock missing {field}")
            if clock.get("verified") is not True:
                errors.append(f"{rid}: numeric clock must be explicitly verified")
            cref = clock.get("computation_authority")
            if cref not in by_id or by_id.get(cref, {}).get("status") != "verified":
                errors.append(f"{rid}: numeric clock authority must resolve to verified Florida authority")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registered = {d.get("id") for d in registry.get("datasets", [])}
    for dep in data.get("dataset_dependencies", []):
        if dep not in registered:
            errors.append(f"unresolved dataset dependency: {dep}")
    # Contract-v2 event separation: unresolved sale/title/possession clocks remain null.
    for rid in ("judicial_sale", "post_sale", "post_sale_possession"):
        route = data.get("routes", {}).get(rid, {})
        if route.get("immediate_clock") is not None:
            errors.append(f"{rid}: clock must remain null until independently verified")
    return errors


def main() -> int:
    errors = validate(json.loads(DATA.read_text(encoding="utf-8")))
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: Florida foreclosure semantic validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
