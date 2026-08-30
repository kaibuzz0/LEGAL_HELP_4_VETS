"""Phase 3 procedural-depth legal quality checks."""
import json
import re
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
        self.assertNotIn("30 days to present evidence", text)
        self.assertNotIn("60-day period to request a predetermination hearing", text)

    def test_rating_protections_are_not_conflated(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        self.assertRegex(text, r"5\+ years.*3\.344")
        self.assertRegex(text, r"20\+ years.*3\.951")
        self.assertRegex(text, r"10-year protection:.*3\.957")
        self.assertIn("service connection", text.lower())
        self.assertIn("except fraud", text.lower())
        self.assertNotIn("older than five years cannot be reduced", text.lower())

    def test_total_rating_and_tdiu_rules_are_separate(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        self.assertIn("Total rating / TDIU", text)
        self.assertIn("actual employability must be established by clear and convincing evidence", text)
        self.assertIn("3.343(c)", text)

    def test_severance_uses_government_cue_burden_not_hlr_cue(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        self.assertIn("VA bears the burden", text)
        self.assertIn("clearly and unmistakably erroneous", text)
        appeals = (ROOT / "appeals.html").read_text(encoding="utf-8").lower()
        self.assertIn("do not have to prove clear and unmistakable error", appeals)

    def test_incarceration_is_not_generic_loss_of_benefits(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        self.assertIn("beginning on the 61st day", text)
        self.assertIn("possible apportionment to dependents", text)
        self.assertIn("restoration after release", text)
        self.assertNotIn("incarcerated veterans lose benefits", text.lower())

    def test_incompetency_is_not_guardianship_or_criminal_competency(self):
        text = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        self.assertIn("capacity to manage affairs and benefit funds", text)
        self.assertIn("presumes competency", text)
        self.assertIn("court-based exceptions", text)

    def test_medical_review_routes_are_separate(self):
        text = (ROOT / "medical-rights.html").read_text(encoding="utf-8")
        for anchor in ["clinical-appeal", "health-benefit-review", "community-care", "travel", "caregiver", "1151", "ftca"]:
            self.assertIn(f'id="{anchor}"', text)
        self.assertIn("VISN", text)
        self.assertIn("different review systems", text)
        self.assertIn("§1151 benefits route", text)
        self.assertIn("FTCA is a separate tort claim", text)

    def test_beneficiary_travel_uses_regulatory_trigger_and_exceptions(self):
        text = (ROOT / "medical-rights.html").read_text(encoding="utf-8")
        self.assertIn("30 calendar days after completing the travel", text)
        self.assertIn("special mode of transportation", text)
        self.assertIn("eligibility arose", text)
        self.assertIn("38 CFR §70.20", text)
        self.assertNotIn("generally must be submitted within <strong>30 days of the appointment</strong>", text)

    def test_caregiver_pre_2019_route_is_board_or_clinical(self):
        text = (ROOT / "medical-rights.html").read_text(encoding="utf-8")
        self.assertIn("before February 19, 2019", text)
        self.assertIn("Board Appeal using the PCAFC Notice of Disagreement", text)
        self.assertIn("Clinical Appeal", text)

    def test_primary_authority_registry_has_phase3_rules(self):
        data = json.loads((ROOT / "data" / "primary-authorities.json").read_text(encoding="utf-8"))
        ids = {a["id"] for a in data["authorities"]}
        required = {"38-cfr-3-105", "38-cfr-3-343", "38-cfr-3-344", "38-cfr-3-951", "38-cfr-3-957", "38-cfr-3-665", "38-cfr-3-353"}
        self.assertTrue(required.issubset(ids), required - ids)

    def test_sources_page_exposes_primary_registry_with_graceful_failure(self):
        js = (ROOT / "assets" / "js" / "components.js").read_text(encoding="utf-8")
        self.assertIn("addPrimaryAuthoritiesRegistry", js)
        self.assertIn("data/primary-authorities.json", js)
        self.assertIn("primary-authorities-registry", js)
        self.assertRegex(js, r"\.catch\(function\(\) \{ \}\)")

    def test_unsafe_appeals_and_claims_advice_not_restored(self):
        appeals = (ROOT / "appeals.html").read_text(encoding="utf-8").lower()
        claims = (ROOT / "claims.html").read_text(encoding="utf-8").lower()
        for bad in ['a short signed letter saying', 'goal: decision within 365', 'goal: decision within 550']:
            self.assertNotIn(bad, appeals)
        self.assertNotIn("describe your worst days, not your best", claims)
        self.assertNotIn("locks an earlier effective date", claims)

    def test_cod_is_not_described_as_discharge_upgrade(self):
        text = (ROOT / "discharge-upgrade.html").read_text(encoding="utf-8").lower()
        self.assertIn("does not change the military discharge itself", text)
        self.assertNotIn("cod determination upgrades", text)

if __name__ == '__main__':
    unittest.main()
