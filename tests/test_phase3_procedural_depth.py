"""Phase 3 procedural-depth legal quality checks."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent

class TestPhase3ProceduralDepth(unittest.TestCase):
    def test_benefit_change_routes_exist(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        for anchor in ["rating", "severance", "dependency", "pension", "incarceration", "debt", "incompetency", "other"]:
            self.assertIn(f'id="{anchor}"', text)

    def test_reduction_deadlines_are_distinguished(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        self.assertIn("60 days to present evidence", text)
        self.assertIn("30-day period to request a predetermination hearing", text)
        self.assertIn("Do not generalize this", text)

    def test_rating_protections_present(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        for citation in ["3.344", "3.343", "3.951", "3.957", "3.665", "3.353"]:
            self.assertIn(citation, text)

    def test_medical_review_routes_are_separate(self):
        text = (ROOT / "medical-rights.html").read_text(encoding="utf-8")
        for anchor in ["clinical-appeal", "health-benefit-review", "community-care", "travel", "caregiver", "1151", "ftca"]:
            self.assertIn(f'id="{anchor}"', text)
        self.assertIn("VISN", text)

    def test_primary_authority_registry_has_phase3_rules(self):
        data = json.loads((ROOT / "data" / "primary-authorities.json").read_text(encoding="utf-8"))
        ids = {a["id"] for a in data["authorities"]}
        required = {"38-cfr-3-105", "38-cfr-3-343", "38-cfr-3-344", "38-cfr-3-951", "38-cfr-3-957", "38-cfr-3-665", "38-cfr-3-353"}
        self.assertTrue(required.issubset(ids), required - ids)

    def test_sources_page_exposes_primary_registry(self):
        js = (ROOT / "assets" / "js" / "components.js").read_text(encoding="utf-8")
        self.assertIn("addPrimaryAuthoritiesRegistry", js)
        self.assertIn("data/primary-authorities.json", js)
        self.assertIn("primary-authorities-registry", js)

    def test_unsafe_appeals_advice_not_restored(self):
        text = (ROOT / "appeals.html").read_text(encoding="utf-8").lower()
        self.assertNotIn('a short signed letter saying', text)
        self.assertNotIn('goal: decision within 365', text)
        self.assertNotIn('goal: decision within 550', text)

if __name__ == '__main__':
    unittest.main()
