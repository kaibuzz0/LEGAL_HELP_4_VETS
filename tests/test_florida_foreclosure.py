import json
import unittest
from pathlib import Path
from scripts.validate_florida_foreclosure import validate

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "florida-foreclosure.json").read_text(encoding="utf-8"))

class FloridaForeclosureTests(unittest.TestCase):
    def test_semantic_validator(self):
        self.assertEqual(validate(DATA), [])

    def test_foreclosure_is_separate_dataset(self):
        self.assertEqual(DATA["subject"], "housing_foreclosure")
        self.assertEqual(DATA["dataset_id"], "florida-foreclosure")

    def test_complaint_not_final_judgment(self):
        self.assertIn("foreclosure_complaint", DATA["routes"])
        self.assertIn("final_judgment", DATA["routes"])
        self.assertNotEqual(DATA["routes"]["foreclosure_complaint"]["id"], DATA["routes"]["final_judgment"]["id"])

    def test_judgment_sale_title_possession_separate(self):
        routes = DATA["routes"]
        for rid in ("final_judgment", "judicial_sale", "post_sale", "post_sale_possession"):
            self.assertIn(rid, routes)

    def test_unverified_court_clocks_are_null(self):
        for rid in ("foreclosure_complaint", "summary_judgment", "judicial_sale", "post_sale", "post_sale_possession"):
            self.assertIsNone(DATA["routes"][rid]["immediate_clock"])

    def test_order_to_show_cause_separate(self):
        self.assertIn("order_to_show_cause", DATA["routes"])
        self.assertIn("fl-702-10", DATA["routes"]["order_to_show_cause"]["authorities"])

    def test_federal_overlays_not_state_authorities(self):
        state_authority_ids = {a["id"] for a in DATA["authorities"]}
        for overlay in DATA["federal_overlays"]:
            self.assertNotIn(overlay, state_authority_ids)

    def test_cross_dataset_dependency(self):
        self.assertEqual(DATA["dataset_dependencies"], ["florida-housing"])

if __name__ == "__main__":
    unittest.main()
