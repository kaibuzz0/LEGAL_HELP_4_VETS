"""California Phase 5 housing invariants."""
import json
import unittest
from pathlib import Path

from scripts.validate_state_data import validate_state

ROOT = Path(__file__).parent.parent
CA = json.loads((ROOT / "data" / "states" / "california.json").read_text(encoding="utf-8"))


class TestCaliforniaHousing(unittest.TestCase):
    def test_california_uses_schema_1_2(self):
        self.assertEqual(CA["schema_version"], "1.2")
        self.assertEqual(CA["status"], "partially_verified")

    def test_california_passes_semantic_validator(self):
        self.assertEqual(validate_state(CA, "california.json"), [])

    def test_notice_types_remain_separate(self):
        routes = CA["document_routes"]
        for route_id in (
            "notice_pay_rent_or_quit",
            "notice_perform_covenant_or_quit",
            "notice_quit_breach_nuisance",
            "termination_30_day",
            "termination_60_day",
            "just_cause_termination",
        ):
            self.assertIn(route_id, routes)
        self.assertNotEqual(routes["notice_pay_rent_or_quit"]["immediate_clock"]["unit"], routes["termination_30_day"]["immediate_clock"]["unit"])

    def test_curable_three_day_notices_use_judicial_day_exclusions(self):
        for route_id in ("notice_pay_rent_or_quit", "notice_perform_covenant_or_quit"):
            clock = CA["document_routes"][route_id]["immediate_clock"]
            self.assertEqual(clock["value"], 3)
            self.assertIn("judicial_holidays", clock["unit"])
            self.assertEqual(clock["computation_authority"], "ca-ccp-1161")

    def test_termination_notices_use_calendar_day_model(self):
        self.assertEqual(CA["document_routes"]["termination_30_day"]["immediate_clock"]["unit"], "calendar_days_before_proposed_termination")
        self.assertEqual(CA["document_routes"]["termination_60_day"]["immediate_clock"]["unit"], "calendar_days_before_proposed_termination")

    def test_tenant_protection_act_is_not_universal(self):
        route = CA["document_routes"]["just_cause_termination"]
        text = (route["description"] + " " + " ".join(route["exceptions"])).lower()
        self.assertIn("covered", text)
        self.assertIn("exemption", text)
        self.assertIn("local", text)
        self.assertIsNone(route["immediate_clock"])

    def test_no_fault_relocation_clock_is_separate(self):
        clocks = CA["document_routes"]["just_cause_termination"]["other_clocks"]
        self.assertEqual(len(clocks), 1)
        self.assertEqual(clocks[0]["value"], 15)
        self.assertEqual(clocks[0]["trigger"], "service_of_covered_no_fault_just_cause_termination_notice_where_owner_elects_direct_payment")

    def test_unlawful_detainer_response_uses_service_specific_clock(self):
        route = CA["document_routes"]["summons_unlawful_detainer"]
        personal = route["immediate_clock"]
        substituted = route["other_clocks"][0]
        self.assertEqual(personal["value"], 10)
        self.assertIn("court_days", personal["unit"])
        self.assertIn("personal", personal["trigger"])
        self.assertEqual(substituted["value"], 20)
        self.assertIn("mixed", substituted["unit"])
        self.assertNotEqual(personal["trigger"], substituted["trigger"])

    def test_current_ud_answer_form_is_traced(self):
        route = CA["document_routes"]["summons_unlawful_detainer"]
        self.assertIn("UD-105", route["required_filing"])
        self.assertIn("ca-courts-forms", route["authorities"])

    def test_default_is_separate_from_response_deadline(self):
        route = CA["document_routes"]["default_requested_or_entered"]
        self.assertIsNone(route["immediate_clock"])
        self.assertIn("default", route["description"].lower())
        self.assertIn("ca-courts-default", route["authorities"])

    def test_appeal_is_not_automatic_stay(self):
        route = CA["document_routes"]["judgment_post_trial"]
        combined = (route["description"] + " " + " ".join(route["possession_consequences"])).lower()
        self.assertIn("does not", combined)
        self.assertIn("stop", combined)
        self.assertIn("sheriff", combined)

    def test_sheriff_execution_uses_posted_notice(self):
        route = CA["document_routes"]["sheriff_notice_to_vacate"]
        clock = route["immediate_clock"]
        self.assertEqual(clock["value"], 5)
        self.assertIn("posted notice", clock["display"].lower())
        self.assertIn("sheriff", clock["trigger"])

    def test_lockout_and_utility_are_separate(self):
        routes = CA["document_routes"]
        self.assertIn("self_help_lockout", routes)
        self.assertIn("utility_shutoff", routes)
        self.assertEqual(routes["self_help_lockout"]["authorities"], ["ca-civ-789-3"])
        self.assertEqual(routes["utility_shutoff"]["authorities"], ["ca-civ-789-3"])

    def test_state_and_federal_fair_housing_are_distinct(self):
        state = CA["document_routes"]["state_fair_housing"]
        federal = CA["document_routes"]["federal_fair_housing_overlay"]
        self.assertIn("ca-gov-12955", state["authorities"])
        self.assertEqual(federal["authorities"], [])
        self.assertEqual(federal["federal_overlays"], ["fha-disability-accommodation"])

    def test_local_law_is_not_collapsed_into_statewide_rule(self):
        local = CA["local_variation"]
        self.assertTrue(local["local_rules_possible"])
        self.assertIsNone(local["county"])
        self.assertIsNone(local["court"])
        self.assertIn("local", local["statewide_rule"].lower())

    def test_subsidized_housing_has_no_invented_deadline(self):
        route = CA["document_routes"]["subsidized_housing_termination"]
        self.assertEqual(route["status"], "partially_verified")
        self.assertIsNone(route["immediate_clock"])
        self.assertEqual(route["other_clocks"], [])
        self.assertIn("public-housing", route["federal_overlays"])
        self.assertIn("hcv", route["federal_overlays"])
        self.assertIn("hud-vash", route["federal_overlays"])

    def test_foreclosure_not_smuggled_into_eviction_core(self):
        self.assertFalse(any("foreclosure" in key for key in CA["document_routes"]))


if __name__ == "__main__":
    unittest.main()
