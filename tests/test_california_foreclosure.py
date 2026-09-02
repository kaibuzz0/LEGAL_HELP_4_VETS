import json
import pathlib
import unittest
from scripts.validate_california_foreclosure import validate

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "california-foreclosure.json"

class CaliforniaForeclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.routes = cls.data["routes"]
        cls.authorities = {a["id"]: a for a in cls.data["authorities"]}

    def test_foreclosure_layer_passes_semantic_validator(self):
        self.assertEqual(validate(self.data), [])

    def test_nod_is_not_sale_notice(self):
        self.assertIn("notice_of_default", self.routes)
        self.assertIn("notice_of_trustees_sale", self.routes)
        self.assertNotEqual(self.routes["notice_of_default"]["label"], self.routes["notice_of_trustees_sale"]["label"])

    def test_every_published_numeric_clock_has_trigger_and_verified_authority(self):
        for route in self.routes.values():
            clocks = ([route["clock"]] if route.get("clock") else []) + route.get("other_clocks", [])
            for clock in clocks:
                self.assertIsNotNone(clock.get("value"))
                self.assertTrue(clock.get("unit"))
                self.assertTrue(clock.get("trigger"))
                ref = clock.get("computation_authority")
                self.assertIn(ref, self.authorities)
                self.assertEqual(self.authorities[ref]["status"], "verified")
                self.assertIs(clock.get("verified"), True)
                self.assertTrue(clock.get("display"))

    def test_2924f_sale_notice_clock_is_public_posting_not_generic_notice(self):
        route = self.routes["notice_of_trustees_sale"]
        self.assertEqual(route["clock"]["value"], 20)
        self.assertEqual(route["clock"]["computation_authority"], "ca-civ-2924f")
        self.assertIn("public", route["clock"]["unit"])
        self.assertIn("mailing", " ".join(route["warnings"]).lower())
        self.assertIn("publication", " ".join(route["warnings"]).lower())

    def test_postponement_old_clock_is_not_published(self):
        route = self.routes["sale_postponed"]
        self.assertIsNone(route["clock"])
        text = " ".join(route["warnings"]).lower()
        self.assertIn("withheld", text)
        self.assertIn("public announcement", text)

    def test_hbor_is_qualified_and_not_regulation_x(self):
        text = " ".join(self.routes["hbor_complete_application"]["warnings"]).lower()
        self.assertIn("not universal", text)
        self.assertIn("regulation x", text)
        self.assertIn("separate", text)

    def test_hbor_denial_appeal_clock_has_coverage_warning(self):
        route = self.routes["hbor_denial_appeal"]
        self.assertEqual(route["clock"]["value"], 30)
        self.assertEqual(route["clock"]["trigger"], "written_denial_of_covered_first_lien_loan_modification_application")
        self.assertIn("coverage", " ".join(route["warnings"]).lower())

    def test_reinstatement_not_redemption_or_modification(self):
        text = " ".join(self.routes["reinstatement"]["warnings"]).lower()
        self.assertIn("not redemption", text)
        self.assertIn("not a guaranteed loan modification", text)

    def test_former_owner_and_bona_fide_tenant_are_separate(self):
        self.assertIn("post_sale_former_owner", self.routes)
        self.assertIn("post_sale_bona_fide_tenant", self.routes)
        self.assertIsNone(self.routes["post_sale_former_owner"]["clock"])
        self.assertEqual(self.routes["post_sale_bona_fide_tenant"]["clock"]["value"], 90)

    def test_sheriff_five_day_rule_traces_to_ccp_715_010(self):
        route = self.routes["sheriff_writ_execution"]
        self.assertEqual(route["clock"]["value"], 5)
        self.assertEqual(route["clock"]["computation_authority"], "ca-ccp-715-010")
        self.assertIn("service_of_writ_copy", route["clock"]["trigger"])
        self.assertNotIn("after receiving notice", route["clock"]["display"].lower())

    def test_hoa_and_tax_not_mortgage_foreclosure(self):
        for key in ("hoa_foreclosure", "tax_foreclosure"):
            self.assertEqual(self.routes[key]["status"], "unverified")
            self.assertIsNone(self.routes[key]["clock"])

    def test_va_guaranty_not_servicing_and_current_partial_claim(self):
        warnings = " ".join(self.routes["va_home_loan_default"]["warnings"]).lower()
        self.assertIn("guarantees rather than owns or services", warnings)
        self.assertIn("partial claim", warnings)

    def test_sale_not_immediate_eviction(self):
        warnings = " ".join(self.routes["trustee_sale_completed"]["warnings"]).lower()
        self.assertIn("does not itself equal immediate physical eviction", warnings)

if __name__ == "__main__":
    unittest.main()
