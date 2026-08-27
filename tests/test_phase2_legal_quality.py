"""Phase 2 legal-content quality checks."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
PHASE2 = ["emergency.html", "medical-rights.html", "find-legal-help.html"]
REQUIRED_AUTHORITIES = {
    "38-cfr-3-155", "38-cfr-3-400", "38-cfr-3-2500", "38-cfr-3-2501",
    "10-usc-1552-b", "va-form-20-0995", "va-form-20-0996", "va-form-10182",
    "va-form-20-0998", "va-form-21-0966", "va-emergency-non-va", "38-cfr-17-4010",
    "38-usc-1151", "38-cfr-3-361", "28-usc-2401-b", "28-usc-2675",
    "va-ogc-ftca", "doj-sf95", "va-lsv-h", "va-accreditation-search"
}

class TestPhase2LegalQuality(unittest.TestCase):
    def test_verification_metadata(self):
        for page in PHASE2:
            text = (ROOT / page).read_text(encoding="utf-8")
            self.assertIn('name="legal-last-verified"', text, page)
            self.assertIn('Last legally verified:', text, page)

    def test_no_public_placeholders(self):
        bad = re.compile(r'pending verification|TODO|FIXME|example\.com', re.I)
        for page in PHASE2:
            text = (ROOT / page).read_text(encoding="utf-8")
            self.assertIsNone(bad.search(text), page)

    def test_required_primary_authorities_registered(self):
        data = json.loads((ROOT / "data" / "primary-authorities.json").read_text(encoding="utf-8"))
        ids = {a["id"] for a in data["authorities"]}
        self.assertTrue(REQUIRED_AUTHORITIES.issubset(ids), REQUIRED_AUTHORITIES - ids)

    def test_emergency_routes_exist(self):
        text = (ROOT / "emergency.html").read_text(encoding="utf-8")
        for anchor in ["homeless", "eviction", "medical-now", "medical-denied", "claim-denied",
                       "benefit-reduction", "debt", "job", "discharge", "court", "family", "home-loss"]:
            self.assertIn(f'id="{anchor}"', text)

    def test_ftca_and_1151_are_separate(self):
        text = (ROOT / "medical-rights.html").read_text(encoding="utf-8")
        self.assertIn('id="1151"', text)
        self.assertIn('id="ftca"', text)
        self.assertIn('§1151 vs FTCA', text)

if __name__ == '__main__':
    unittest.main()
