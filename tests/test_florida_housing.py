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
        self.assertIn("nonpayment_notice", routes)
        self.assertIn("lease_violation_curable", routes)
        self.assertIn("lease_violation_serious_repeat", routes)

    def test_periodic_termination_is_not_eviction_judgment(self):
        self.assertIn("periodic_termination", DATA["document_routes"])
        self.assertIn("default_or_judgment", DATA["document_routes"])

    def test_unresolved_nonpayment_clock_is_null(self):
        self.assertIsNone(DATA["document_routes"]["nonpayment_notice"]["immediate_clock"])

    def test_rent_registry_not_universalized(self):
        route = DATA["document_routes"]["eviction_summons_complaint"]
        text = " ".join(route["exceptions"]).lower()
        self.assertIn("do not assume", text)
        self.assertIsNone(route["immediate_clock"])

    def test_writ_has_verified_24_hour_clock(self):
        clock = DATA["document_routes"]["writ_of_possession"]["immediate_clock"]
        self.assertEqual(clock["value"], 24)
        self.assertEqual(clock["unit"], "hours")
        self.assertTrue(clock["verified"])
        self.assertEqual(clock["computation_authority"], "fl-83-62")

    def test_writ_is_not_self_help(self):
        self.assertNotEqual(DATA["document_routes"]["writ_of_possession"]["id"], DATA["document_routes"]["self_help_lockout"]["id"])

    def test_florida_servicemember_right_separate_from_scra(self):
        route = DATA["document_routes"]["servicemember_lease_termination"]
        self.assertIn("fl-83-682", route["authorities"])
        self.assertIn("scra-eviction", route["federal_overlays"])
        self.assertIn("veteran status alone", " ".join(route["exceptions"]).lower())

    def test_ptfa_is_applicability_qualified(self):
        route = DATA["document_routes"]["ptfa_tenant_after_foreclosure"]
        self.assertTrue(route["exceptions"])
        self.assertEqual(route["immediate_clock"]["value"], 90)

if __name__ == "__main__":
    unittest.main()
