import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "states" / "florida.json").read_text(encoding="utf-8"))


class FloridaHousingTests(unittest.TestCase):
    def test_schema_and_status(self):
        self.assertEqual(DATA["schema_version"], "1.2")
        self.assertEqual(DATA["status"], "partially_verified")

    def test_notice_types_are_separate(self):
        routes = DATA["document_routes"]
        for rid in (
            "nonpayment_notice",
            "lease_violation_curable",
            "lease_violation_noncurable",
            "lease_violation_repeat",
        ):
            self.assertIn(rid, routes)
        self.assertNotEqual(routes["nonpayment_notice"]["id"], routes["lease_violation_curable"]["id"])

    def test_nonpayment_exact_three_day_computation(self):
        clock = DATA["document_routes"]["nonpayment_notice"]["immediate_clock"]
        self.assertEqual(clock["value"], 3)
        self.assertIn("delivery", clock["trigger"].lower())
        self.assertIn("written", clock["trigger"].lower())
        self.assertIn("saturday", clock["unit"])
        self.assertIn("sunday", clock["unit"])
        self.assertIn("court_observed_legal_holidays", clock["unit"])
        self.assertEqual(clock["computation_authority"], "fl-83-56")

    def test_nonpayment_computation_does_not_spread(self):
        nonpay = DATA["document_routes"]["nonpayment_notice"]["immediate_clock"]["unit"]
        curable = DATA["document_routes"]["lease_violation_curable"]["immediate_clock"]["unit"]
        noncurable = DATA["document_routes"]["lease_violation_noncurable"]["immediate_clock"]["unit"]
        self.assertNotEqual(nonpay, curable)
        self.assertNotEqual(nonpay, noncurable)

    def test_curable_noncompliance_has_separate_seven_day_rule(self):
        route = DATA["document_routes"]["lease_violation_curable"]
        self.assertEqual(route["immediate_clock"]["value"], 7)
        self.assertIn("curable", route["immediate_clock"]["trigger"])
        self.assertTrue(any("12 months" in x for x in route["exceptions"]))

    def test_noncurable_and_repeat_are_not_collapsed(self):
        noncurable = DATA["document_routes"]["lease_violation_noncurable"]
        repeat = DATA["document_routes"]["lease_violation_repeat"]
        self.assertEqual(noncurable["immediate_clock"]["value"], 7)
        self.assertIsNone(repeat["immediate_clock"])
        self.assertTrue(any("12-month" in x or "12 month" in x for x in repeat["exceptions"]))

    def test_notice_delivery_is_not_service_of_process(self):
        notice_trigger = DATA["document_routes"]["nonpayment_notice"]["immediate_clock"]["trigger"].lower()
        court_trigger = DATA["document_routes"]["eviction_summons_complaint"]["immediate_clock"]["trigger"].lower()
        self.assertIn("delivery", notice_trigger)
        self.assertNotIn("service of process", notice_trigger)
        self.assertIn("service of process", court_trigger)

    def test_eviction_response_is_five_day_summary_procedure(self):
        route = DATA["document_routes"]["eviction_summons_complaint"]
        clock = route["immediate_clock"]
        self.assertEqual(clock["value"], 5)
        self.assertEqual(clock["computation_authority"], "fl-r-gen-prac-2-514")
        self.assertIn("fl-51-011", route["authorities"])
        self.assertIn("fl-48-183", route["authorities"])
        self.assertTrue(any("later of posting or mailing" in x for x in route["exceptions"]))

    def test_rent_registry_is_conditional_and_five_days(self):
        route = DATA["document_routes"]["rent_registry"]
        clock = route["immediate_clock"]
        self.assertEqual(clock["value"], 5)
        self.assertIn("service of process", clock["trigger"].lower())
        self.assertIn("saturday", clock["unit"])
        joined = " ".join(route["exceptions"]).lower()
        self.assertIn("defense other than payment", joined)
        self.assertIn("public-housing", joined)
        self.assertIn("rent subsidies", joined)
        self.assertIn("does not mean every tenant must always", route["description"].lower())

    def test_payment_defense_is_preserved(self):
        joined = " ".join(DATA["document_routes"]["rent_registry"]["exceptions"]).lower()
        self.assertIn("payment defense", joined)
        self.assertIn("expressly distinct", joined)

    def test_registry_default_consequence_does_not_skip_court_stages(self):
        consequences = " ".join(DATA["document_routes"]["rent_registry"]["possession_consequences"]).lower()
        self.assertIn("default judgment", consequences)
        self.assertIn("writ", consequences)
        self.assertIn("sheriff execution", consequences)

    def test_periodic_termination_is_not_eviction_judgment(self):
        self.assertIn("periodic_termination", DATA["document_routes"])
        self.assertIn("default_or_judgment", DATA["document_routes"])

    def test_writ_has_verified_24_hour_clock(self):
        clock = DATA["document_routes"]["writ_of_possession"]["immediate_clock"]
        self.assertEqual(clock["value"], 24)
        self.assertEqual(clock["unit"], "hours")
        self.assertTrue(clock["verified"])
        self.assertEqual(clock["computation_authority"], "fl-83-62")

    def test_writ_is_not_self_help(self):
        self.assertNotEqual(
            DATA["document_routes"]["writ_of_possession"]["id"],
            DATA["document_routes"]["self_help_lockout"]["id"],
        )

    def test_florida_servicemember_right_separate_from_scra(self):
        route = DATA["document_routes"]["servicemember_lease_termination"]
        self.assertIn("fl-83-682", route["authorities"])
        self.assertIn("scra-eviction", route["federal_overlays"])
        self.assertIn("veteran status alone", " ".join(route["exceptions"]).lower())

    def test_ptfa_state_route_is_applicability_qualified(self):
        route = DATA["document_routes"]["ptfa_tenant_after_foreclosure"]
        self.assertTrue(route["exceptions"])
        self.assertEqual(route["immediate_clock"]["value"], 90)
        self.assertIn("ptfa", route["federal_overlays"])
        self.assertTrue(any("former mortgagor" in x.lower() for x in route["exceptions"]))

    def test_provider_routing_is_statewide_and_nonpromissory(self):
        required = {
            "florida_courts_self_help",
            "florida_bar_lrs",
            "florida_legal_aid",
            "fdva",
            "fdva_county_vso",
            "hud_housing_counseling",
            "va_lsv_h",
            "va_ssvf",
            "va_home_loan",
        }
        self.assertTrue(required.issubset(DATA["resources"]))
        combined = " ".join(
            (r.get("eligibility_notes") or "") + " " + (r.get("coverage") or "")
            for r in DATA["resources"].values()
        ).lower()
        self.assertIn("not guaranteed", combined)
        self.assertIn("does not override", combined)


if __name__ == "__main__":
    unittest.main()
