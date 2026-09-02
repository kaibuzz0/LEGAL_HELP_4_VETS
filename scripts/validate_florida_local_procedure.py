#!/usr/bin/env python3
"""Semantic validation for Florida county/circuit housing procedure overlays.

Local procedure is intentionally non-statewide:
- every proposition has an explicit county;
- clerk/sheriff/informational pages are operational guidance, not state law;
- local timing never becomes a statewide legal deadline;
- foreclosure possession cannot silently inherit Chapter 83's eviction writ clock.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "florida-local-procedure.json"
REGISTRY = ROOT / "data" / "datasets.json"
FORECLOSURE = ROOT / "data" / "florida-foreclosure.json"
HOUSING = ROOT / "data" / "states" / "florida.json"

ALLOWED_STATUS = {"verified", "partially_verified", "unverified", "needs_refresh", "deprecated"}
ALLOWED_COUNTIES = {"Hillsborough", "Orange", "Duval"}
SOURCE_TYPES = {
    "local_court_rule",
    "administrative_order",
    "clerk_filing_procedure",
    "sheriff_execution_practice",
    "local_form_requirement",
    "informational_guidance",
}
LEGAL_LOCAL_TYPES = {"local_court_rule", "administrative_order", "local_form_requirement"}
HOSTS = {
    "Hillsborough": {"hillsclerk.com", "www.hillsclerk.com", "teamhcso.com", "www.teamhcso.com", "fljud13.org", "www.fljud13.org", "hcfl.gov", "www.hcfl.gov"},
    "Orange": {"myorangeclerk.com", "www.myorangeclerk.com", "ocso.com", "www.ocso.com", "ninthcircuit.org", "www.ninthcircuit.org", "orangecountyfl.net", "www.orangecountyfl.net"},
    "Duval": {"duvalclerk.com", "www.duvalclerk.com", "jaxsheriff.org", "www.jaxsheriff.org", "jud4.org", "www.jud4.org", "jacksonville.gov", "www.jacksonville.gov"},
}


def https(url: str | None) -> bool:
    p = urlparse(url or "")
    return p.scheme == "https" and bool(p.netloc)


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    if data.get("dataset_id") != "florida-local-procedure":
        errors.append("dataset_id must be florida-local-procedure")
    if data.get("state") != "Florida" or data.get("state_code") != "FL":
        errors.append("dataset must identify Florida / FL")
    if data.get("subject") != "housing_local_procedure":
        errors.append("subject must be housing_local_procedure")
    if data.get("status") not in ALLOWED_STATUS:
        errors.append("dataset has invalid status")
    if data.get("default_county") is not None:
        errors.append("local router must not default to a county")

    sources = data.get("sources", [])
    ids = [s.get("id") for s in sources]
    if len(set(ids)) != len(ids) or any(not x for x in ids):
        errors.append("local source IDs must be present and unique")
    by_id = {s["id"]: s for s in sources if s.get("id")}

    for source in sources:
        sid = source.get("id", "<missing>")
        county = source.get("county")
        stype = source.get("source_type")
        url = source.get("url")
        parsed = urlparse(url or "")

        if county not in ALLOWED_COUNTIES:
            errors.append(f"{sid}: local source lacks an allowed explicit county")
        if stype not in SOURCE_TYPES:
            errors.append(f"{sid}: invalid local source type {stype!r}")
        if source.get("official") is not True:
            errors.append(f"{sid}: verified local source must be official")
        if not https(url):
            errors.append(f"{sid}: local source must use HTTPS")
        if county in HOSTS and parsed.netloc.lower() not in HOSTS[county]:
            errors.append(f"{sid}: source host is not on the official allowlist for {county}")
        if source.get("statewide") is not False:
            errors.append(f"{sid}: local source must explicitly be non-statewide")
        if stype in {"clerk_filing_procedure", "sheriff_execution_practice", "informational_guidance"} and source.get("legal_authority") is not False:
            errors.append(f"{sid}: clerk/sheriff/informational guidance cannot be marked legal authority")
        if stype in LEGAL_LOCAL_TYPES and source.get("legal_authority") is not True:
            errors.append(f"{sid}: local rule/order/form source must be explicitly classified as local legal authority")
        if source.get("status") not in ALLOWED_STATUS:
            errors.append(f"{sid}: invalid source status")
        if not source.get("supports"):
            errors.append(f"{sid}: missing supported local proposition")
        try:
            datetime.strptime(source.get("last_verified", ""), "%Y-%m-%d")
        except ValueError:
            errors.append(f"{sid}: malformed verification date")

    counties = data.get("counties", {})
    if set(x.get("county") for x in counties.values()) != ALLOWED_COUNTIES:
        errors.append("pilot must contain explicit Hillsborough, Orange, and Duval county records")
    if len(counties) != 3:
        errors.append("pilot must contain exactly three county records")

    statewide_clock_phrases = ("statewide deadline", "statewide legal deadline")
    for key, county_data in counties.items():
        county = county_data.get("county")
        if county not in ALLOWED_COUNTIES:
            errors.append(f"{key}: county record lacks explicit pilot county")
            continue
        for section in ("eviction", "foreclosure", "writ_execution"):
            item = county_data.get(section)
            if not isinstance(item, dict):
                errors.append(f"{key}: missing {section} local procedure section")
                continue
            for sid in item.get("source_ids", []):
                if sid not in by_id:
                    errors.append(f"{key}:{section}: unknown local source {sid}")
                elif by_id[sid].get("county") != county:
                    errors.append(f"{key}:{section}: source {sid} belongs to another county")
            if item.get("statewide_deadline_override") is True:
                errors.append(f"{key}:{section}: local practice cannot override statewide deadline")
            timing = item.get("operational_timing")
            if timing is not None:
                if not isinstance(timing, dict):
                    errors.append(f"{key}:{section}: operational timing must be object or null")
                else:
                    if timing.get("legal_deadline") is not False:
                        errors.append(f"{key}:{section}: local operational timing must be marked non-legal")
                    if county.lower() not in (timing.get("scope") or "").lower():
                        errors.append(f"{key}:{section}: local operational timing must name its county scope")
                    sid = timing.get("source_id")
                    if sid not in by_id or by_id.get(sid, {}).get("county") != county:
                        errors.append(f"{key}:{section}: operational timing source must resolve within county")

        combined = json.dumps(county_data).lower()
        if "fl-83-62" in combined or "§83.62" in combined:
            # Local eviction source descriptions may discuss §83.62, but the foreclosure/writ sections
            # may never use it as a foreclosure bridge.
            foreclosure_text = json.dumps(county_data.get("foreclosure", {})).lower()
            writ_text = json.dumps(county_data.get("writ_execution", {})).lower()
            if "fl-83-62" in foreclosure_text or "§83.62" in foreclosure_text:
                errors.append(f"{key}: foreclosure local overlay improperly imports §83.62")
            if "fl-83-62" in writ_text or "§83.62" in writ_text:
                errors.append(f"{key}: foreclosure writ local overlay improperly imports §83.62")

    router = data.get("router", {})
    for field in ("county", "court", "sheriff"):
        if router.get(field) is not None:
            errors.append(f"router {field} must remain null until user/case selects locality")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registered = {x.get("id") for x in registry.get("datasets", [])}
    for dep in data.get("dataset_dependencies", []):
        if dep not in registered:
            errors.append(f"unresolved dataset dependency: {dep}")

    foreclosure = json.loads(FORECLOSURE.read_text(encoding="utf-8"))
    housing = json.loads(HOUSING.read_text(encoding="utf-8"))
    valid_resources = set(foreclosure.get("resources", {})) | set(housing.get("resources", {}))
    foreclosure_route_ids = set(foreclosure.get("routes", {}))
    housing_route_ids = set(housing.get("document_routes", {}))
    federal_ids = {x.get("id") for x in json.loads((ROOT / "data" / "housing-federal.json").read_text(encoding="utf-8")).get("overlays", [])}

    cross_ids = []
    for link in data.get("cross_layer_routes", []):
        lid = link.get("id", "<missing-link>")
        cross_ids.append(lid)
        route_id = link.get("foreclosure_route")
        if route_id not in foreclosure_route_ids:
            errors.append(f"{lid}: foreclosure route does not resolve: {route_id}")
        for route_id in link.get("housing_routes", []):
            if route_id not in housing_route_ids:
                errors.append(f"{lid}: housing route does not resolve: {route_id}")
        for overlay in link.get("federal_overlays", []):
            if overlay not in federal_ids:
                errors.append(f"{lid}: federal overlay does not resolve: {overlay}")
        if link.get("local_section") not in {"eviction", "foreclosure", "writ_execution"}:
            errors.append(f"{lid}: invalid local section")
        if link.get("provider_routing") is not True:
            errors.append(f"{lid}: post-sale cross-layer route must preserve provider routing")
        classification = link.get("occupant_classification")
        if classification == "former_owner" and "ptfa" in link.get("federal_overlays", []):
            errors.append(f"{lid}: former owner cannot automatically receive PTFA")
        if classification == "unknown" and link.get("housing_routes"):
            errors.append(f"{lid}: unknown occupant cannot be assigned housing rights before classification")

    if len(set(cross_ids)) != len(cross_ids) or any(not x for x in cross_ids):
        errors.append("cross-layer route IDs must be present and unique")

    for key, county_data in counties.items():
        for rid in county_data.get("providers", []):
            if rid not in valid_resources:
                errors.append(f"{key}: unknown provider routing ID {rid}")

        for provider in county_data.get("local_providers", []):
            pid = provider.get("id", "<missing-provider>")
            if provider.get("official") is not True or provider.get("verified") is not True:
                errors.append(f"{key}:{pid}: local provider must be official and verified")
            purl = provider.get("url")
            if not https(purl):
                errors.append(f"{key}:{pid}: local provider URL must be HTTPS")
            elif urlparse(purl).netloc.lower() not in HOSTS[county]:
                errors.append(f"{key}:{pid}: local provider must use an official county/city host")
            if county.lower() not in (provider.get("coverage") or "").lower():
                errors.append(f"{key}:{pid}: local provider coverage must explicitly name the county")
            try:
                datetime.strptime(provider.get("last_verified", ""), "%Y-%m-%d")
            except ValueError:
                errors.append(f"{key}:{pid}: malformed provider verification date")
            note = (provider.get("note") or "").lower()
            if "guarantee" not in note and "not foreclosure representation" not in note:
                errors.append(f"{key}:{pid}: provider note must avoid implying guaranteed legal/housing assistance")

    return errors


def main() -> int:
    errors = validate(json.loads(DATA.read_text(encoding="utf-8")))
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Florida local procedure semantic validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
