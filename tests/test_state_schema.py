"""Formal state-schema and semantic invariant tests."""
import json
import unittest
from datetime import date
from pathlib import Path

from scripts.validate_state_data import validate_state, stale_authority_ids

ROOT = Path(__file__).parent.parent


def authority(aid="law", jurisdiction="Test", status="verified", kind="statute"):
    return {"id": aid, "title": "Test law", "authority_type": kind, "jurisdiction": jurisdiction,
            "status": status, "url": "https://example.gov/law", "last_verified": "2026-08-30",
            "supports": ["test proposition"]}


def sample_state(route=None, authorities=None, version="1.2"):
    return {"schema_version": version, "state": "Test", "status": "partially_verified",
            "primary_authorities": authorities or [], "resources": {},
            "document_routes": {"x": route} if route else {}}


class TestStateSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "data" / "states" / "schema.json").read_text(encoding="utf-8"))
        cls.texas = json.loads((ROOT / "data" / "states" / "texas.json").read_text(encoding="utf-8"))
        cls.template = json.loads((ROOT / "data" / "states" / "_template.json").read_text(encoding="utf-8"))

    def test_schema_is_json_schema_2020_12(self):
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        for key in ("route", "clock", "authority", "resource", "localVariation"):
            self.assertIn(key, self.schema["$defs"])

    def test_texas_11_passes_semantic_validator(self):
        self.assertEqual(validate_state(self.texas, "texas.json"), [])

    def test_verified_route_requires_authority_or_overlay(self):
        data = sample_state({"label": "X", "status": "verified"})
        self.assertTrue(any("lacks authority or verified overlay" in e for e in validate_state(data)))

    def test_missing_authority_reference_fails(self):
        data = sample_state({"label": "X", "status": "verified", "authorities": ["missing"]})
        self.assertTrue(any("unknown authority references" in e for e in validate_state(data)))

    def test_wrong_state_authority_fails(self):
        data = sample_state({"label": "X", "status": "verified", "authorities": ["law"]}, [authority(jurisdiction="Other")])
        self.assertTrue(any("wrong jurisdiction" in e for e in validate_state(data)))

    def test_nonverified_authority_cannot_support_verified_route(self):
        data = sample_state({"label": "X", "status": "verified", "authorities": ["law"]}, [authority(status="needs_refresh")])
        self.assertTrue(any("non-verified authority" in e for e in validate_state(data)))

    def test_program_cannot_satisfy_state_legal_authority(self):
        data = sample_state({"label": "X", "status": "verified", "authorities": ["program"]}, [authority("program", kind="government_program")])
        self.assertTrue(any("cannot support state-law proposition" in e for e in validate_state(data)))

    def test_12_authority_requires_supported_proposition(self):
        a = authority(); a.pop("supports")
        self.assertTrue(any("lacks supported proposition" in e for e in validate_state(sample_state(authorities=[a]))))

    def test_deadline_value_requires_trigger_unit_authority_verified_and_display(self):
        route = {"label": "X", "status": "partially_verified", "authorities": ["law"],
                 "immediate_clock": {"value": 5}}
        errors = validate_state(sample_state(route, [authority()]))
        for text in ("triggering event", "unit/computation description", "computation authority", "explicitly verified", "display text"):
            self.assertTrue(any(text in e for e in errors), text)

    def test_deadline_computation_authority_must_exist(self):
        clock = {"value": 5, "unit": "court_days", "trigger": "service", "computation_authority": "missing", "verified": True, "display": "5 court days after service"}
        data = sample_state({"label": "X", "status": "partially_verified", "immediate_clock": clock}, [authority()])
        self.assertTrue(any("does not exist" in e for e in validate_state(data)))

    def test_deadline_authority_must_be_verified(self):
        clock = {"value": 5, "unit": "court_days", "trigger": "service", "computation_authority": "law", "verified": True, "display": "5 court days after service"}
        data = sample_state({"label": "X", "status": "partially_verified", "immediate_clock": clock}, [authority(status="needs_refresh")])
        self.assertTrue(any("verified deadline uses non-verified authority" in e for e in validate_state(data)))

    def test_null_clock_remains_unknown(self):
        data = sample_state({"label": "X", "status": "unverified", "immediate_clock": None})
        self.assertEqual(validate_state(data), [])

    def test_legal_action_requires_valid_authority(self):
        route = {"label": "X", "status": "partially_verified", "required_actions": [{"type": "legal_requirement", "text": "File now", "authority": None}]}
        self.assertTrue(any("action lacks valid authority" in e for e in validate_state(sample_state(route))))

    def test_practical_action_does_not_require_authority(self):
        route = {"label": "X", "status": "unverified", "optional_actions": [{"type": "practical_action", "text": "Keep a copy", "authority": None}]}
        self.assertEqual(validate_state(sample_state(route)), [])

    def test_duplicate_authority_ids_fail(self):
        a = authority("dup")
        self.assertTrue(any("duplicate authority IDs" in e for e in validate_state(sample_state(authorities=[a, dict(a)]))))

    def test_authority_requires_verification_date_and_https_url(self):
        a = authority(); a.pop("last_verified"); a["url"] = "http://example.com"
        errors = validate_state(sample_state(authorities=[a]))
        self.assertTrue(any("verification date" in e for e in errors))
        self.assertTrue(any("HTTPS" in e for e in errors))

    def test_unknown_schema_version_fails(self):
        self.assertTrue(any("unsupported schema_version" in e for e in validate_state(sample_state(version="9.0"))))

    def test_staleness_is_warning_input_not_invalidity(self):
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
