import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "california-foreclosure.json"

class CaliforniaForeclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.routes = cls.data["routes"]

    def test_nod_is_not_sale_notice(self):
        self.assertIn("notice_of_default", self.routes)
        self.assertIn("notice_of_trustees_sale", self.routes)
        self.assertNotEqual(self.routes["notice_of_default"]["label"], self.routes["notice_of_trustees_sale"]["label"])

    def test_every_published_numeric_clock_has_trigger_and_authority(self):
        for route in self.routes.values():
            clocks = []
            if route.get("clock"):
                clocks.append(route["clock"])
            clocks.extend(route.get("other_clocks", []))
            for clock in clocks:
                self.assertIsNotNone(clock.get("value"))
                self.assertTrue(clock.get("unit"))
                self.assertTrue(clock.get("trigger"))
                self.assertTrue(clock.get("computation_authority"))
                self.assertIs(clock.get("verified"), True)
                self.assertTrue(clock.get("display"))

    def test_reinstatement_not_redemption_or_modification(self):
        text = " ".join(self.routes["reinstatement"]["warnings"]).lower()
        self.assertIn("not redemption", text)
        self.assertIn("not a guaranteed loan modification", text)

    def test_regulation_x_not_california_law(self):
        limits = " ".join(self.data["publication_limits"]).lower()
        self.assertIn("federal overlays", limits)
        self.assertIn("not california authority", limits)

    def test_scra_requires_qualifying_service(self):
        questions = " ".join(self.data["priority_questions"]).lower()
        self.assertIn("qualifying military service", questions)

    def test_va_guaranty_not_servicing(self):
        warnings = " ".join(self.routes["va_home_loan_default"]["warnings"]).lower()
        self.assertIn("guarantees rather than owns or services", warnings)

    def test_hoa_and_tax_not_mortgage_foreclosure(self):
        self.assertEqual(self.routes["hoa_foreclosure"]["status"], "unverified")
        self.assertEqual(self.routes["tax_foreclosure"]["status"], "unverified")
        self.assertIsNone(self.routes["hoa_foreclosure"]["clock"])
        self.assertIsNone(self.routes["tax_foreclosure"]["clock"])

    def test_sale_not_immediate_eviction(self):
        warnings = " ".join(self.routes["trustee_sale_completed"]["warnings"]).lower()
        self.assertIn("does not itself equal immediate physical eviction", warnings)
        self.assertIn("summons_unlawful_detainer", self.routes["post_sale_possession"]["reuse_state_routes"])

    def test_nod_three_month_clock_has_recording_trigger(self):
        clock = self.routes["notice_of_default"]["clock"]
        self.assertEqual(clock["value"], 3)
        self.assertEqual(clock["trigger"], "recording_of_notice_of_default")

    def test_postponement_clock_is_qualified(self):
        clock = self.routes["sale_postponed"]["clock"]
        self.assertEqual(clock["value"], 5)
        self.assertEqual(clock["trigger"], "postponement_of_sale_for_at_least_10_business_days")

if __name__ == "__main__":
    unittest.main()
