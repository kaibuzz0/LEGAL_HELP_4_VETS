import copy
import json
import pathlib
import unittest
from scripts.validate_california_foreclosure import validate

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "california-foreclosure.json"
STATE_DATA = ROOT / "data" / "states" / "california.json"

class CaliforniaForeclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.state_data = json.loads(STATE_DATA.read_text(encoding="utf-8"))
        cls.routes = cls.data["routes"]
        cls.authorities = {a["id"]: a for a in cls.data["authorities"]}

    def mutated(self):
        return copy.deepcopy(self.data)

    def assert_invalid(self, data, needle):
        errors = validate(data)
        self.assertTrue(any(needle in e for e in errors), errors)

    def test_foreclosure_layer_passes_semantic_validator(self):
        self.assertEqual(validate(self.data), [])

    def test_validator_rejects_unknown_authority_reference(self):
        data = self.mutated()
        data["routes"]["notice_of_default"]["authorities"] = ["does-not-exist"]
        self.assert_invalid(data, "unknown authority")

    def test_validator_rejects_wrong_jurisdiction_for_verified_california_route(self):
        data = self.mutated()
        data["routes"]["notice_of_default"]["authorities"] = ["federal-ptfa"]
        self.assert_invalid(data, "cannot rely on federal authority")

    def test_validator_rejects_http_source(self):
        data = self.mutated()
        data["authorities"][0]["source_url"] = "http://example.com/statute"
        self.assert_invalid(data, "source must be HTTPS")

    def test_validator_rejects_missing_verification_date(self):
        data = self.mutated()
        data["authorities"][0]["last_verified"] = ""
        self.assert_invalid(data, "missing/malformed verification date")

    def test_validator_rejects_missing_supported_proposition(self):
        data = self.mutated()
        data["authorities"][0]["supports"] = []
        self.assert_invalid(data, "missing supported proposition")

    def test_validator_rejects_numeric_clock_without_trigger(self):
        data = self.mutated()
        data["routes"]["notice_of_default"]["clock"]["trigger"] = ""
        self.assert_invalid(data, "numeric clock missing trigger")

    def test_validator_rejects_numeric_clock_without_authority(self):
        data = self.mutated()
        data["routes"]["notice_of_default"]["clock"]["computation_authority"] = ""
        self.assert_invalid(data, "clock authority does not resolve")

    def test_validator_rejects_numeric_clock_with_unverified_authority(self):
        data = self.mutated()
        data["authorities"][0]["status"] = "partially_verified"
        data["routes"]["default_servicing_problem"]["clock"]["computation_authority"] = data["authorities"][0]["id"]
        self.assert_invalid(data, "verified clock uses nonverified authority")

    def test_null_clock_is_safe_unknown_not_no_deadline(self):
        data = self.mutated()
        data["routes"]["sale_postponed"]["warnings"] = ["There is no deadline."]
        self.assert_invalid(data, "null clock must not be interpreted as no deadline")

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

    def test_2924g_postponement_uses_current_model_and_null_clock(self):
        route = self.routes["sale_postponed"]
        self.assertEqual(route["status"], "verified")
        self.assertIsNone(route["clock"])
        text = " ".join(route["warnings"]).lower()
        self.assertIn("public declaration", text)
        self.assertIn("365", text)
        self.assertIn("withdrawn", text)
        self.assertNotIn("automatically invalid", text)

    def test_hbor_coverage_precedes_rights(self):
        route = self.routes["hbor_coverage"]
        text = " ".join(route["warnings"]).lower()
        self.assertEqual(route["status"], "verified")
        self.assertIsNone(route["clock"])
        self.assertIn("not universal", text)
        self.assertIn("2924.15", text)
        self.assertIn("small-servicer", text)
        self.assertIn("regulation x", text)

    def test_hbor_complete_application_is_not_regulation_x(self):
        text = " ".join(self.routes["hbor_complete_application"]["warnings"]).lower()
        self.assertIn("not universal", text)
        self.assertIn("regulation x", text)
        self.assertIn("separate", text)

    def test_hbor_denial_appeal_clock_has_coverage_warning(self):
        route = self.routes["hbor_denial_appeal"]
        self.assertEqual(route["clock"]["value"], 30)
        self.assertEqual(route["clock"]["trigger"], "written_denial_of_covered_first_lien_loan_modification_application")
        self.assertIn("coverage", " ".join(route["warnings"]).lower())
        self.assertIn("separately", " ".join(route["warnings"]).lower())

    def test_hbor_remedies_do_not_claim_sale_automatically_void(self):
        route = self.routes["hbor_remedies"]
        text = " ".join(route["warnings"]).lower()
        self.assertEqual(route["status"], "verified")
        self.assertIsNone(route["clock"])
        self.assertIn("injunctive", text)
        self.assertIn("actual-economic-damages", text)
        self.assertIn("corrected", text)
        self.assertIn("do not state", text)
        self.assertIn("bona fide purchaser", text)

    def test_reinstatement_not_redemption_or_modification(self):
        text = " ".join(self.routes["reinstatement"]["warnings"]).lower()
        self.assertIn("not redemption", text)
        self.assertIn("not a guaranteed loan modification", text)

    def test_former_owner_and_bona_fide_tenant_are_separate(self):
        self.assertIn("post_sale_former_owner", self.routes)
        self.assertIn("post_sale_bona_fide_tenant", self.routes)
        self.assertIsNone(self.routes["post_sale_former_owner"]["clock"])
        self.assertEqual(self.routes["post_sale_bona_fide_tenant"]["clock"]["value"], 90)
        self.assertIn("do not say all tenants", " ".join(self.routes["post_sale_bona_fide_tenant"]["warnings"]).lower())

    def test_cross_dataset_reuse_state_routes_resolve(self):
        state_routes = self.state_data["document_routes"]
        for route in self.routes.values():
            for ref in route.get("reuse_state_routes", []):
                self.assertIn(ref, state_routes, ref)

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
