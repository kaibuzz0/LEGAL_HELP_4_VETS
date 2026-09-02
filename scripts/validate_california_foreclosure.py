#!/usr/bin/env python3
"""Semantic validation for data/california-foreclosure.json.

The foreclosure layer lives outside data/states/, so it must not be a validator blind spot.
Null clocks mean unknown/not verified, never no deadline.
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "california-foreclosure.json"
ALLOWED_STATUS = {"verified", "partially_verified", "unverified", "deprecated", "needs_refresh", "verified_federal_overlay_only"}
LEGAL_TYPES = {"statute", "regulation", "court_rule", "case_law", "agency_guidance", "government_form"}


def https(url):
    p = urlparse(url or "")
    return p.scheme == "https" and bool(p.netloc)


def validate(data: dict) -> list[str]:
    errors = []
    if data.get("state") != "California" or data.get("layer") != "foreclosure":
        errors.append("dataset must identify California foreclosure layer")
    authorities = data.get("authorities", [])
    ids = [a.get("id") for a in authorities]
    if len([x for x in ids if x]) != len(set(x for x in ids if x)):
        errors.append("duplicate authority IDs")
    by_id = {a["id"]: a for a in authorities if a.get("id")}
    for a in authorities:
        aid = a.get("id", "<missing>")
        if a.get("status") not in ALLOWED_STATUS:
            errors.append(f"{aid}: invalid authority status")
        if a.get("authority_type") not in LEGAL_TYPES:
            errors.append(f"{aid}: invalid/missing legal authority type")
        if a.get("jurisdiction") not in {"California", "Federal", "United States"}:
            errors.append(f"{aid}: invalid/missing jurisdiction")
        if not https(a.get("source_url")):
            errors.append(f"{aid}: source must be HTTPS")
        if not a.get("supports"):
            errors.append(f"{aid}: missing supported proposition")
        try:
            datetime.strptime(a.get("last_verified", ""), "%Y-%m-%d")
        except ValueError:
            errors.append(f"{aid}: missing/malformed verification date")

    for rid, route in data.get("routes", {}).items():
        status = route.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{rid}: invalid route status")
        refs = route.get("authorities", [])
        for ref in refs:
            if ref not in by_id:
                errors.append(f"{rid}: unknown authority {ref}")
        if status == "verified" and not refs:
            errors.append(f"{rid}: verified route lacks authority")
        if status == "verified":
            for ref in refs:
                if by_id.get(ref, {}).get("status") != "verified":
                    errors.append(f"{rid}: verified route uses nonverified authority {ref}")
        clocks = []
        if route.get("clock") is not None:
            clocks.append(route.get("clock"))
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
            if cref not in by_id:
                errors.append(f"{rid}: clock authority does not resolve: {cref}")
            elif by_id[cref].get("status") != "verified":
                errors.append(f"{rid}: verified clock uses nonverified authority {cref}")
        if route.get("clock") is None:
            joined = " ".join(route.get("warnings", [])).lower()
            if "no deadline" in joined and "not no deadline" not in joined:
                errors.append(f"{rid}: null clock must not be interpreted as no deadline")

    # Architectural invariants.
    if data["routes"].get("hoa_foreclosure", {}).get("clock") is not None:
        errors.append("HOA foreclosure must remain null until independently verified")
    if data["routes"].get("tax_foreclosure", {}).get("clock") is not None:
        errors.append("tax foreclosure must remain null until independently verified")
    return errors


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: California foreclosure semantic validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
