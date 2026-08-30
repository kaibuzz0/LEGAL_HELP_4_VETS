"""Phase 4 Texas housing legal-data regression tests."""
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

    def test_status_vocabulary_and_route_level_status(self):
        allowed = set(self.texas["status_values"])
        self.assertTrue({"verified", "partially_verified", "unverified", "needs_refresh"}.issubset(allowed))
        for key, route in self.texas["document_routes"].items():
            self.assertIn(route["status"], allowed, key)

    def test_published_state_law_routes_have_traceable_authorities(self):
        known = {item["id"] for item in self.texas["primary_authorities"]}
        for key, route in self.texas["document_routes"].items():
            if route["status"] in {"verified", "partially_verified"} and key != "va_home_loan_default":
                self.assertTrue(route.get("authorities"), key)
                self.assertTrue(set(route["authorities"]).issubset(known), key)

    def test_va_route_has_traceable_federal_guidance(self):
        overlays = {x["id"] for x in self.federal["overlays"]}
        self.assertIn("va-home-loan", overlays)
        route = self.texas["document_routes"]["va_home_loan_default"]
        self.assertEqual(route["status"], "verified")
        self.assertIn("private lender/servicer", " ".join(route["do_now"]).lower())

    def test_unverified_route_does_not_publish_clock(self):
        tax = self.texas["document_routes"]["tax_foreclosure_paper"]
        self.assertEqual(tax["status"], "unverified")
        self.assertIsNone(tax["immediate_clock"])
        self.assertFalse(tax["authorities"])

    def test_null_is_not_rendered_as_no_deadline(self):
        self.assertIn("Deadline not yet verified", self.js)
        self.assertNotIn("No deadline", self.js)

    def test_eviction_appeal_clock_attaches_to_signed_judgment(self):
        clock = self.texas["document_routes"]["judgment"]["immediate_clock"]
        self.assertEqual(clock["deadline_value"], 5)
        self.assertEqual(clock["deadline_trigger"], "judgment_signed")
        self.assertEqual(clock["time_computation_authority"], "tx-trcp-510")
        self.assertIn("judgment is signed", clock["display"].lower())
        self.assertNotIn("received", clock["display"].lower())

    def test_notice_trial_appeal_and_writ_clocks_are_distinct(self):
        routes = self.texas["document_routes"]
        self.assertEqual(routes["court_citation"]["immediate_clock"]["deadline_trigger"], "trial_date_in_citation")
        self.assertEqual(routes["judgment"]["immediate_clock"]["deadline_trigger"], "judgment_signed")
        self.assertEqual(routes["writ_of_possession"]["immediate_clock"]["deadline_trigger"], "judgment_and_appeal_status")
        self.assertNotEqual(routes["notice_to_vacate"]["immediate_clock"]["deadline_trigger"], routes["judgment"]["immediate_clock"]["deadline_trigger"])

    def test_mortgage_cure_and_sale_notice_are_separate_clocks(self):
        routes = self.texas["document_routes"]
        cure = routes["foreclosure_default_notice"]["immediate_clock"]
        sale = routes["foreclosure_sale_notice"]["immediate_clock"]
        self.assertEqual(cure["deadline_value"], 20)
        self.assertEqual(cure["deadline_trigger"], "default_notice_given_by_certified_mail")
        self.assertEqual(sale["deadline_value"], 21)
        self.assertEqual(sale["deadline_trigger"], "foreclosure_sale_date")
        self.assertEqual(cure["time_computation_authority"], "tx-prop-51-002")
        self.assertEqual(sale["time_computation_authority"], "tx-prop-51-002")

    def test_foreclosure_categories_are_not_collapsed(self):
        categories = self.texas["foreclosure_categories"]
        self.assertEqual(categories["ordinary_deed_of_trust"], "verified_core")
        self.assertEqual(categories["home_equity"], "partially_verified")
        self.assertEqual(categories["tax"], "unverified")
        self.assertIn("hoa_poa_foreclosure_notice", self.texas["document_routes"])
        self.assertIn("va_home_loan_default", self.texas["document_routes"])

    def test_lockout_and_utility_remedies_are_not_conflated(self):
        lockout = self.texas["document_routes"]["locked_out"]
        utility = self.texas["document_routes"]["utility_shutoff"]
        self.assertIn("tx-prop-92-009", lockout["authorities"])
        self.assertIn("tx-prop-92-0091", utility["authorities"])
        self.assertIn("writ of reentry", lockout["remedy"].lower())
        self.assertIn("writ of restoration", utility["remedy"].lower())

    def test_local_rule_model_has_official_locator(self):
        local = self.texas["local_variation"]
        self.assertTrue(local["local_rule_possible"])
        self.assertTrue(local["local_rule_locator"].startswith("https://topics.txcourts.gov/"))
        self.assertIsNone(local["county"])
        self.assertIsNone(local["court"])

    def test_scra_eviction_and_foreclosure_are_status_specific(self):
        overlays = {x["id"]: x for x in self.federal["overlays"]}
        for key in ["scra-eviction", "scra-mortgage"]:
            warning = overlays[key]["warning"].lower()
            self.assertIn("veteran status", warning)
        self.assertIn("originated before", overlays["scra-mortgage"]["rule"].lower())

    def test_federal_programs_are_not_substituted_for_legal_rights(self):
        overlays = {x["id"]: x for x in self.federal["overlays"]}
        self.assertIn("not itself an eviction defense", overlays["hud-vash"]["warning"].lower())
        self.assertIn("not a statutory entitlement", overlays["ssvf"]["warning"].lower())
        self.assertIn("does not guarantee representation", overlays["lsv-h"]["warning"].lower())
        self.assertIn("not a state deadline", self.page.lower())

    def test_regulation_x_does_not_guarantee_modification(self):
        overlays = {x["id"]: x for x in self.federal["overlays"]}
        self.assertIn("does not require a servicer to offer any particular", overlays["reg-x-loss-mitigation"]["rule"].lower())

    def test_accommodation_workflow_limits_medical_disclosure(self):
        workflow = self.federal["reasonable_accommodation_workflow"]
        combined = " ".join(workflow["steps"] + workflow["limits"]).lower()
        self.assertIn("full medical records", combined)
        self.assertIn("nexus", combined)
        self.assertIn("hud", workflow["hud_complaint"]["url"])

    def test_page_is_document_first_and_has_manual_date_map(self):
        self.assertIn("START WITH THE PAPER IN YOUR HAND", self.page)
        for label in ["NOTICE TO VACATE", "COURT CITATION", "JUDGMENT", "WRIT OF POSSESSION", "DEFAULT / INTENT TO ACCELERATE", "FORECLOSURE SALE NOTICE", "VA HOME LOAN DEFAULT"]:
            self.assertIn(label, self.page)
        self.assertIn('id="my-dates"', self.page)
        self.assertIn("does <strong>not</strong> calculate legal deadlines", self.page)

    def test_renderer_escapes_data_and_fails_safe(self):
        self.assertIn("escapeHtml", self.js)
        self.assertIn("State procedure could not load", self.js)
        self.assertIn("find-legal-help.html#homelessness", self.js)
        self.assertIn("route.status === 'verified' || route.status === 'partially_verified'", self.js)


if __name__ == "__main__":
    unittest.main()
