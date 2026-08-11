"""
Regression tests for LEGAL HELP 4 VETS HTML structure.
Run with: python tests/test_html.py
"""
import unittest
import re
from pathlib import Path

WORK_DIR = Path(__file__).parent.parent
PAGES = [
    "index.html", "help-now.html", "claims.html", "appeals.html", "discharge-upgrade.html",
    "housing.html", "employment-money.html", "family-immigration.html", "legal-library.html",
    "toolkit.html", "about.html", "sources.html", "substance-use.html", "widows.html",
    "state-resources.html", "faith-encouragement.html", "404.html"
]

class TestHTML(unittest.TestCase):
    def test_all_pages_exist(self):
        for page in PAGES:
            self.assertTrue((WORK_DIR / page).exists(), f"Missing {page}")

    def test_single_h1(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            opens = text.lower().count("<h1")
            closes = text.lower().count("</h1>")
            self.assertEqual(opens, 1, f"{page} has {opens} opening H1 tags")
            self.assertEqual(closes, 1, f"{page} has {closes} closing H1 tags")

    def test_title_present(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            self.assertIn("<title>", text.lower())
            self.assertIn("</title>", text.lower())

    def test_meta_description(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            self.assertIn('name="description"', text, f"{page} missing meta description")

    def test_no_broken_internal_anchors(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            ids = set(re.findall(r'id="([^"]+)"', text))
            for m in re.finditer(r'href="#([^"]+)"', text):
                target = m.group(1)
                self.assertIn(target, ids, f"{page} broken anchor #{target}")

    def test_print_button(self):
        for page in PAGES:
            if page == '404.html':
                continue
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            self.assertIn('print-btn', text, f"{page} missing print button")

    def test_disclaimer(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            self.assertIn('Legal Information, Not Legal Advice', text, f"{page} missing disclaimer")

    def test_crisis_line(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            self.assertIn('tel:988', text, f"{page} missing 988 crisis line link")

    def test_last_updated(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding="utf-8")
            self.assertIn('Last updated', text, f"{page} missing last-updated date")

if __name__ == '__main__':
    unittest.main()
