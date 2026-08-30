"""Formal state-schema and semantic invariant tests."""
import json
import unittest
from datetime import date
from pathlib import Path

from scripts.validate_state_data import validate_state, stale_authority_ids

ROOT = Path(__file__).parent.parent


class TestStateSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "data" / "states" / "schema.json").read_text(encoding="utf-8"))
        cls.texas = json.loads((ROOT / "data" / "states" / "texas.json").read_text(encoding="utf-8"))
        cls.template = json.loads((ROOT / "data" / "states" / "_template.json").read_text(encoding="utf-8"))

    def test_schema_is_json_schema_2020_12(self):
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("route", self.schema["$defs"])
        self.assertIn("clock", self.schema["$defs"])
        self.assertIn("authority", self.schema["$defs"])
        self.assertIn("resource", self.schema["$defs"])
        self.assertIn("localVariation", self.schema["$defs"])

    def test_texas_passes_semantic_validator(self):
        self.assertEqual(validate_state(self.texas, "texas.json"), [])

    def test_deadline_value_requires_trigger(self):
        sample = {
            "state": "Test", "status": "unverified", "primary_authorities": [], "resources": {},
            "document_routes": {"x": {"label": "X", "status": "unverified", "immediate_clock": {"deadline_value": 5, "time_computation_authority": "rule-x"}}}
        }
        errors = validate_state(sample)
        self.assertTrue(any("lacks triggering event" in e for e in errors))

    def test_deadline_value_requires_computation_authority(self):
        sample = {
            "state": "Test", "status": "unverified", "primary_authorities": [], "resources": {},
            "document_routes": {"x": {"label": "X", "status": "unverified", "immediate_clock": {"deadline_value": 5, "deadline_trigger": "judgment_signed"}}}
        }
        errors = validate_state(sample)
        self.assertTrue(any("lacks computation authority" in e for e in errors))

    def test_verified_route_requires_authority(self):
        sample = {"state": "Test", "status": "partially_verified", "primary_authorities": [], "resources": {}, "document_routes": {"x": {"label": "X", "status": "verified"}}}
        self.assertTrue(any("verified route lacks authority" in e for e in validate_state(sample)))

    def test_duplicate_authority_ids_fail(self):
        authority = {"id": "dup", "title": "A", "authority_type": "statute", "jurisdiction": "Test", "status": "verified", "url": "https://example.gov/a", "last_verified": "2026-08-30"}
        sample = {"state": "Test", "status": "unverified", "primary_authorities": [authority, dict(authority)], "resources": {}, "document_routes": {}}
        self.assertTrue(any("duplicate authority IDs" in e for e in validate_state(sample)))

    def test_authority_requires_verification_date_and_https_url(self):
        sample = {"state": "Test", "status": "unverified", "primary_authorities": [{"id": "a", "title": "A", "authority_type": "statute", "jurisdiction": "Test", "status": "verified", "url": "http://example.com"}], "resources": {}, "document_routes": {}}
        errors = validate_state(sample)
        self.assertTrue(any("verification date" in e for e in errors))
        self.assertTrue(any("HTTPS" in e for e in errors))

    def test_action_classification_is_enforced(self):
        sample = {"state": "Test", "status": "unverified", "primary_authorities": [], "resources": {}, "document_routes": {"x": {"label": "X", "status": "unverified", "required_actions": [{"text": "Save a copy"}]}}}
        self.assertTrue(any("action lacks classification" in e for e in validate_state(sample)))

    def test_null_clock_remains_unknown(self):
        sample = {"state": "Test", "status": "unverified", "primary_authorities": [], "resources": {}, "document_routes": {"x": {"label": "X", "status": "unverified", "immediate_clock": None}}}
        self.assertEqual(validate_state(sample), [])

    def test_staleness_flags_refresh_without_declaring_invalid(self):
        sample = {"primary_authorities": [{"id": "old", "status": "verified", "last_verified": "2024-01-01"}]}
        self.assertEqual(stale_authority_ids(sample, as_of=date(2026, 8, 30), max_age_days=365), ["old"])
        sample["primary_authorities"][0]["status"] = "needs_refresh"
        self.assertEqual(stale_authority_ids(sample, as_of=date(2026, 8, 30), max_age_days=365), [])

    def test_template_contains_no_real_state_law(self):
        self.assertEqual(self.template["state_code"], "XX")
        self.assertEqual(self.template["status"], "unverified")
        self.assertEqual(self.template["primary_authorities"], [])
        self.assertIsNone(self.template["document_routes"]["example_route"]["immediate_clock"])


if __name__ == "__main__":
    unittest.main()
