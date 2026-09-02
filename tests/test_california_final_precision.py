"""Final California cross-layer release invariants."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = json.loads((ROOT / "data" / "states" / "california.json").read_text(encoding="utf-8"))
FORECLOSURE = json.loads((ROOT / "data" / "california-foreclosure.json").read_text(encoding="utf-8"))
FEDERAL = json.loads((ROOT / "data" / "housing-federal.json").read_text(encoding="utf-8"))


class CaliforniaFinalPrecisionTests(unittest.TestCase):
    def test_noncurable_1161_route_is_quarantined(self):
        route = STATE["document_routes"]["notice_quit_breach_nuisance"]
        self.assertEqual(route["status"], "partially_verified")
        self.assertIsNone(route["immediate_clock"])

    def test_state_sheriff_route_uses_ccp_715_010(self):
        route = STATE["document_routes"]["sheriff_notice_to_vacate"]
        self.assertIn("ca-ccp-715-010", route["authorities"])
        self.assertEqual(route["immediate_clock"]["computation_authority"], "ca-ccp-715-010")
        self.assertIn("service_of_writ_copy", route["immediate_clock"]["trigger"])

    def test_project_based_section8_is_distinct_overlay(self):
        overlays = {item["id"]: item for item in FEDERAL["overlays"]}
        self.assertIn("project-based-section8", overlays)
        project = overlays["project-based-section8"]
        self.assertEqual(project["status"], "partially_verified")
        self.assertIn("separate", project["rule"].lower())
        route = STATE["document_routes"]["subsidized_housing_termination"]
        for key in ("public-housing", "hcv", "project-based-section8", "hud-vash"):
            self.assertIn(key, route["federal_overlays"])
        self.assertIsNone(route["immediate_clock"])

    def test_statewide_provider_core_is_present_without_representation_promises(self):
        resources = STATE["resources"]
        for key in (
            "california_courts_self_help",
            "california_state_bar_lrs",
            "california_free_legal_help",
            "california_veterans_legal_resources",
            "hud_housing_counselor",
            "va_lsvh",
            "va_ssvf",
            "va_home_loan_help",
        ):
            self.assertIn(key, resources)
            self.assertTrue(resources[key]["url"].startswith("https://"))
            self.assertEqual(resources[key]["last_verified"], "2026-09-02")
        combined = " ".join(str(v.get("eligibility_notes", "")) for v in resources.values()).lower()
        self.assertIn("not guaranteed", combined)

    def test_former_owner_route_uses_1161a_and_title_perfection_case(self):
        route = FORECLOSURE["routes"]["post_sale_former_owner"]
        self.assertIn("ca-ccp-1161a", route["authorities"])
        self.assertIn("ca-supreme-dr-leevil", route["authorities"])
        self.assertIsNone(route["clock"])
        text = " ".join(route["warnings"]).lower()
        self.assertIn("duly perfected", text)
        self.assertIn("before", text)
        self.assertIn("notice to quit", text)

    def test_foreclosure_references_to_state_routes_resolve(self):
        state_routes = STATE["document_routes"]
        for route in FORECLOSURE["routes"].values():
            for ref in route.get("reuse_state_routes", []):
                self.assertIn(ref, state_routes)

    def test_hbor_and_regulation_x_remain_distinct(self):
        route = FORECLOSURE["routes"]["hbor_coverage"]
        self.assertIn("ca-civ-2923-6", route["authorities"])
        self.assertIn("regulation x", " ".join(route["warnings"]).lower())
        self.assertIn("separate", " ".join(route["warnings"]).lower())


if __name__ == "__main__":
    unittest.main()
