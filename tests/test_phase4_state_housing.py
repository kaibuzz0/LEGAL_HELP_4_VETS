"""Phase 4 state housing data and routing regression tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent


class TestPhase4StateHousing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texas = json.loads((ROOT / "data" / "states" / "texas.json").read_text(encoding="utf-8"))
        cls.federal = json.loads((ROOT / "data" / "housing-federal.json").read_text(encoding="utf-8"))
        cls.page = (ROOT / "state-housing.html").read_text(encoding="utf-8")
        cls.js = (ROOT / "assets" / "js" / "state-housing.js").read_text(encoding="utf-8")

    def test_texas_document_routes_exist(self):
        routes = self.texas["document_routes"]
        required = {
            "notice_to_vacate", "court_citation", "judgment", "writ_of_possession",
            "locked_out", "utility_shutoff", "foreclosure_notice"
        }
        self.assertTrue(required.issubset(routes), required - set(routes))

    def test_unverified_routes_do_not_publish_deadlines_or_authorities(self):
        for key, route in self.texas["document_routes"].items():
            if route.get("status") == "not_yet_verified":
                self.assertIsNone(route.get("deadline"), key)
                self.assertFalse(route.get("authorities"), key)

    def test_verified_routes_have_traceable_authorities(self):
        known = {item["id"] for item in self.texas["primary_authorities"]}
        for key, route in self.texas["document_routes"].items():
            if route.get("status") == "verified":
                self.assertTrue(route.get("authorities"), key)
                self.assertTrue(set(route["authorities"]).issubset(known), key)

    def test_texas_answer_rule_does_not_invent_deadline(self):
        answer = self.texas["document_routes"]["court_citation"]["answer_deadline"].lower()
        self.assertIn("written answer is not required", answer)
        self.assertIn("trial", answer)

    def test_texas_eviction_appeal_is_kept_distinct(self):
        appeal = self.texas["document_routes"]["judgment"]["appeal_deadline"].lower()
        self.assertIn("five days", appeal)
        self.assertIn("judgment is signed", appeal)
        self.assertIn("rule 510", appeal)

    def test_lockout_and_utility_remedies_are_not_conflated(self):
        lockout = self.texas["document_routes"]["locked_out"]
        utility = self.texas["document_routes"]["utility_shutoff"]
        self.assertIn("tx-prop-92-009", lockout["authorities"])
        self.assertIn("tx-prop-92-0091", utility["authorities"])
        self.assertNotEqual(lockout["authorities"], utility["authorities"])

    def test_scra_is_not_presented_as_veteran_status_protection(self):
        scra = next(x for x in self.federal["overlays"] if x["id"] == "scra-eviction")
        warning = scra["warning"].lower()
        self.assertIn("military-service", warning)
        self.assertIn("veteran status alone", warning)

    def test_federal_overlay_keeps_programs_and_rights_separate(self):
        ids = {x["id"] for x in self.federal["overlays"]}
        self.assertTrue({"scra-eviction", "fha-disability-accommodation", "hud-vash", "ssvf", "lsv-h"}.issubset(ids))

    def test_state_page_is_document_first_and_has_fallback(self):
        self.assertIn("START WITH THE PAPER IN YOUR HAND", self.page)
        for label in ["NOTICE TO VACATE", "COURT CITATION", "JUDGMENT", "WRIT OF POSSESSION", "LOCKED OUT", "UTILITY SHUTOFF", "FORECLOSURE NOTICE"]:
            self.assertIn(label, self.page)
        self.assertIn("State procedure could not load", self.js)
        self.assertIn("find-legal-help.html#homelessness", self.js)

    def test_renderer_hides_unverified_procedure(self):
        self.assertIn("procedure not yet verified for publication", self.js)
        self.assertIn("route.status === 'not_yet_verified'", self.js)


if __name__ == "__main__":
    unittest.main()
