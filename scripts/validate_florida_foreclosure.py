#!/usr/bin/env python3
"""Semantic validation for data/florida-foreclosure.json.

Contract-v2 / Phase-7C invariants:
- Florida authorities and federal overlays are distinct provenance layers.
- Every numeric clock resolves to verified current authority.
- Sale, certificate of sale, title, writ, sheriff execution, and physical possession are distinct.
- Former owner, bona fide tenant, other tenant, and unknown occupant are distinct.
- Chapter 83's residential-eviction writ clock cannot leak into general foreclosure possession.
- Null means unresolved/not safely generalized, never "no deadline".
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "florida-foreclosure.json"
REGISTRY = ROOT / "data" / "datasets.json"
FEDERAL = ROOT / "data" / "housing-federal.json"
FLORIDA_HOUSING = ROOT / "data" / "states" / "florida.json"

ALLOWED_STATUS = {"verified", "partially_verified", "unverified", "deprecated", "needs_refresh", "verified_federal_overlay_only"}
LEGAL_TYPES = {"statute", "regulation", "court_rule", "case_law", "agency_guidance", "government_form"}
CURRENT_RULE_HOSTS = {"www-media.floridabar.org", "acis.flcourts.gov", "flcourts-media.flcourts.gov", "www.flcourts.gov", "flcourts.gov"}


def https(url):
    p = urlparse(url or "")
    return p.scheme == "https" and bool(p.netloc)


def load_federal_overlay_ids() -> set[str]:
    data = json.loads(FEDERAL.read_text(encoding="utf-8"))
    return {x.get("id") for x in data.get("overlays", []) if x.get("id")}


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
        atype = a.get("authority_type")
        source = a.get("source_url")
        parsed = urlparse(source or "")
        if atype not in LEGAL_TYPES:
            errors.append(f"{aid}: invalid authority type")
        if a.get("jurisdiction") != "Florida":
            errors.append(f"{aid}: Florida subject authority must identify Florida jurisdiction")
        if not https(source):
            errors.append(f"{aid}: source must be HTTPS")
        if not a.get("supports"):
            errors.append(f"{aid}: missing supported proposition")
        if a.get("status") not in ALLOWED_STATUS:
            errors.append(f"{aid}: invalid status")
        try:
            datetime.strptime(a.get("last_verified", ""), "%Y-%m-%d")
        except ValueError:
            errors.append(f"{aid}: malformed verification date")

        if aid.startswith("fl-r-") and atype != "court_rule":
            errors.append(f"{aid}: Florida rule authority must be classified court_rule")
        if aid.startswith("fl-form-") and atype != "government_form":
            errors.append(f"{aid}: Florida form authority must be classified government_form")
        if atype in {"court_rule", "government_form"} and a.get("status") == "verified" and parsed.netloc not in CURRENT_RULE_HOSTS:
            errors.append(f"{aid}: verified current rule/form must use an official/current Florida court or Florida Bar source")
        if atype == "statute" and a.get("status") == "verified" and parsed.netloc not in {"www.leg.state.fl.us", "leg.state.fl.us"}:
            errors.append(f"{aid}: verified Florida statute must use official Florida Legislature source")
        match = re.search(r"StatuteYear=(\d{4})", source or "")
        if match and a.get("status") == "verified" and int(match.group(1)) < 2026:
            errors.append(f"{aid}: archived statute year cannot support a current verified proposition")

    federal_ids = load_federal_overlay_ids()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registered = {x.get("id") for x in registry.get("datasets", [])}
    florida_routes = set(json.loads(FLORIDA_HOUSING.read_text(encoding="utf-8")).get("document_routes", {}))

    for rid, route in data.get("routes", {}).items():
        status = route.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{rid}: invalid route status")

        refs = route.get("authorities", [])
        for ref in refs:
            if ref not in by_id:
                errors.append(f"{rid}: unknown authority {ref}")
        if status == "verified" and not refs:
            errors.append(f"{rid}: verified Florida route lacks Florida authority")
        if status == "verified":
            for ref in refs:
                if by_id.get(ref, {}).get("status") != "verified":
                    errors.append(f"{rid}: verified route uses nonverified authority {ref}")

        overlays = route.get("federal_overlays", [])
        for overlay in overlays:
            if overlay not in federal_ids:
                errors.append(f"{rid}: unknown federal overlay {overlay}")
            if overlay in by_id:
                errors.append(f"{rid}: federal overlay {overlay} must not be stored as Florida legal authority")

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
            if cref not in by_id:
                errors.append(f"{rid}: numeric clock authority does not resolve: {cref}")
            elif by_id[cref].get("status") != "verified":
                errors.append(f"{rid}: numeric clock authority must resolve to verified Florida authority")

        if route.get("immediate_clock") is None:
            text = " ".join([route.get("description", ""), *route.get("exceptions", [])]).lower()
            for unsafe in ("there is no deadline", "no deadline applies", "no notice is required"):
                if unsafe in text:
                    errors.append(f"{rid}: null clock rendered as negative legal conclusion")

    for overlay in data.get("federal_overlays", []):
        if overlay not in federal_ids:
            errors.append(f"unknown dataset-level federal overlay: {overlay}")

    for dep in data.get("dataset_dependencies", []):
        if dep not in registered:
            errors.append(f"unresolved dataset dependency: {dep}")
    for ref in data.get("cross_dataset_refs", []):
        dataset = ref.get("dataset")
        if dataset not in registered:
            errors.append(f"cross-dataset reference points to unknown dataset: {dataset}")
        if dataset == "florida-housing":
            for route_id in ref.get("routes", []):
                if route_id not in florida_routes:
                    errors.append(f"cross-dataset Florida housing route does not resolve: {route_id}")

    for key, resource in data.get("resources", {}).items():
        if not https(resource.get("url")):
            errors.append(f"resource {key}: source must be HTTPS")
        if resource.get("verified") is not True:
            errors.append(f"resource {key}: resource must be explicitly verified before publication")
        try:
            datetime.strptime(resource.get("last_verified", ""), "%Y-%m-%d")
        except ValueError:
            errors.append(f"resource {key}: malformed verification date")

    routes = data.get("routes", {})
    required_routes = (
        "judicial_sale",
        "certificate_of_sale",
        "sale_objection",
        "certificate_of_title",
        "redemption",
        "post_sale_former_owner",
        "post_sale_writ_of_possession",
        "post_sale_sheriff_execution",
        "post_sale_bona_fide_tenant",
        "post_sale_other_tenant",
        "post_sale_other_occupant",
        "appeal_stay_postsale",
        "post_sale_document_router",
    )
    for required in required_routes:
        if required not in routes:
            errors.append(f"missing distinct foreclosure event route: {required}")

    objection = routes.get("sale_objection", {}).get("immediate_clock") or {}
    if objection and (objection.get("value") != 10 or "certificate of sale" not in objection.get("trigger", "").lower()):
        errors.append("sale objection clock must remain tied to 10 days after filing certificate of sale")

    if routes.get("redemption", {}).get("immediate_clock") is not None:
        errors.append("redemption must remain event-based/null rather than a generic numeric days-after-sale clock")

    post_sale_routes = (
        "certificate_of_title",
        "post_sale_former_owner",
        "post_sale_writ_of_possession",
        "post_sale_sheriff_execution",
        "post_sale_bona_fide_tenant",
        "post_sale_other_tenant",
        "post_sale_other_occupant",
        "appeal_stay_postsale",
    )
    for rid in post_sale_routes:
        if routes.get(rid, {}).get("immediate_clock") is not None:
            errors.append(f"{rid}: post-sale possession/title clock must remain null unless independently established")

    # Foreclosure possession cannot borrow the separate Chapter 83 eviction writ clock.
    for rid in post_sale_routes:
        route = routes.get(rid, {})
        if "fl-83-62" in route.get("authorities", []):
            errors.append(f"{rid}: foreclosure possession improperly cites §83.62")
        text = json.dumps(route).lower()
        if "statewide foreclosure" in text and "24" in text:
            errors.append(f"{rid}: local/eviction 24-hour timing may not be generalized statewide")
    if "fl-r-civ-p-1-580" not in routes.get("post_sale_writ_of_possession", {}).get("authorities", []):
        errors.append("post-sale writ route must use current Rule 1.580")
    writ_text = json.dumps(routes.get("post_sale_writ_of_possession", {})).lower()
    if "affidavit" not in writ_text or "sheriff" not in writ_text:
        errors.append("post-sale writ route must preserve Rule 1.580(b) third-party affidavit safeguard")

    cert_text = json.dumps(routes.get("certificate_of_title", {})).lower()
    for unsafe in ("immediate physical removal", "immediate lockout", "automatically removed"):
        if unsafe in cert_text:
            errors.append("certificate of title must not be rendered as immediate physical eviction")

    former = routes.get("post_sale_former_owner", {})
    bona = routes.get("post_sale_bona_fide_tenant", {})
    other = routes.get("post_sale_other_tenant", {})
    unknown = routes.get("post_sale_other_occupant", {})
    if "ptfa" in former.get("federal_overlays", []):
        errors.append("former mortgagor route must not automatically receive PTFA tenant protection")
    if "ptfa" not in bona.get("federal_overlays", []):
        errors.append("bona fide tenant post-sale route must preserve PTFA overlay")
    if bona.get("id") in {former.get("id"), other.get("id"), unknown.get("id")}:
        errors.append("occupant classifications must remain distinct")
    if unknown.get("immediate_clock") is not None or "unknown" not in json.dumps(unknown).lower():
        errors.append("unknown occupant must remain null-safe and identification-first")

    router_text = json.dumps(routes.get("post_sale_document_router", {})).lower()
    for phrase in ("certificate of sale is not a certificate of title", "certificate of title is not a writ", "writ of possession is not completed physical"):
        if phrase not in router_text:
            errors.append(f"post-sale document router missing separation invariant: {phrase}")

    appeal_text = json.dumps(routes.get("appeal_stay_postsale", {})).lower()
    if "does not itself create a stay" not in appeal_text:
        errors.append("appeal/stay route must state that appeal does not itself create a stay")

    redemption_text = json.dumps(routes.get("redemption", {})).lower()
    if "possession" not in redemption_text:
        errors.append("redemption route must expressly distinguish redemption from possession")

    return errors


def main() -> int:
    errors = validate(json.loads(DATA.read_text(encoding="utf-8")))
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Florida foreclosure semantic validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
