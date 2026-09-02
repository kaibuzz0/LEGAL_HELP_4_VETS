"""Repository-level guards for the reusable state replication contract."""
import copy
import json
import unittest
from pathlib import Path

from scripts.validate_dataset_registry import load_registry, validate_registry

ROOT = Path(__file__).resolve().parents[1]


class StateReplicationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_registry()
        cls.subject_template = json.loads((ROOT / "data" / "_subject_layer_template.json").read_text(encoding="utf-8"))
        cls.state_template = json.loads((ROOT / "data" / "states" / "_template.json").read_text(encoding="utf-8"))
        cls.contract = (ROOT / "docs" / "STATE_IMPLEMENTATION_CONTRACT.md").read_text(encoding="utf-8").lower()

    def test_current_registry_passes(self):
        self.assertEqual(validate_registry(self.registry), [])

    def test_unregistered_production_dataset_fails(self):
        sample = copy.deepcopy(self.registry)
        sample["datasets"] = [e for e in sample["datasets"] if e["id"] != "california-foreclosure"]
        errors = validate_registry(sample)
        self.assertTrue(any("not registered" in e for e in errors))

    def test_unknown_cross_dataset_dependency_fails(self):
        sample = copy.deepcopy(self.registry)
        sample["datasets"][0]["cross_dataset_dependencies"] = ["does-not-exist"]
        self.assertTrue(any("unknown dataset dependency" in e for e in validate_registry(sample)))

    def test_missing_validator_fails(self):
        sample = copy.deepcopy(self.registry)
        sample["datasets"][1]["validator"] = "scripts/not-real.py"
        self.assertTrue(any("validator does not exist" in e for e in validate_registry(sample)))

    def test_texas_is_only_state_11_registry_exception(self):
        sample = copy.deepcopy(self.registry)
        california = next(e for e in sample["datasets"] if e["id"] == "california-housing")
        california["schema_version"] = "1.1"
        self.assertTrue(any("Texas is the only 1.1 legacy exception" in e for e in validate_registry(sample)))

    def test_new_state_template_uses_current_schema(self):
        self.assertEqual(self.state_template["schema_version"], "1.2")
        self.assertEqual(self.state_template["state_code"], "XX")
        self.assertEqual(self.state_template["status"], "unverified")

    def test_subject_template_contains_no_california_law(self):
        self.assertEqual(self.subject_template["state_code"], "XX")
        self.assertEqual(self.subject_template["authorities"], [])
        self.assertEqual(self.subject_template["routes"], {})
        self.assertEqual(self.subject_template["cross_dataset_refs"], [])

    def test_contract_declares_null_safety(self):
        self.assertIn("null is a legal-safety state", self.contract)
        self.assertIn("never render as “no deadline,”", self.contract)

    def test_contract_separates_verification_and_applicability(self):
        self.assertIn("verification is not applicability", self.contract)
        self.assertIn("must never convert `verified` into “you have this right.”", self.contract)

    def test_contract_rejects_hybrid_state_federal_rule(self):
        self.assertIn("do not invent a hybrid deadline or hybrid right", self.contract)


if __name__ == "__main__":
    unittest.main()
