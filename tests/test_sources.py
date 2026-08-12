"""
Regression tests for LEGAL HELP 4 VETS source registry.
Run with: python tests/test_sources.py
"""
import unittest
import json
import re
from pathlib import Path

WORK_DIR = Path(__file__).parent.parent
PAGES = [
    "index.html", "help-now.html", "claims.html", "appeals.html", "discharge-upgrade.html",
    "housing.html", "employment-money.html", "family-immigration.html", "legal-library.html",
    "toolkit.html", "about.html", "sources.html", "substance-use.html", "widows.html",
    "state-resources.html", "faith-encouragement.html", "va-debt.html"
]

class TestSources(unittest.TestCase):
    def test_no_unresolved_markers(self):
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding='utf-8')
            self.assertNotIn('>[?]<', text, f"{page} has unresolved [?] citation")

    def test_all_cited_sources_exist(self):
        sources = json.loads((WORK_DIR / "data" / "sources.json").read_text(encoding='utf-8'))
        registered = {s['id'] for s in sources['sources']}
        for page in PAGES:
            text = (WORK_DIR / page).read_text(encoding='utf-8')
            for m in re.finditer(r'href="sources\.html#source-([^"]+)"', text):
                sid = m.group(1)
                self.assertIn(sid, registered, f"{page} cites unknown source {sid}")

    def test_source_ids_unique(self):
        sources = json.loads((WORK_DIR / "data" / "sources.json").read_text(encoding='utf-8'))
        ids = [s['id'] for s in sources['sources']]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate source IDs found")

    def test_lifecycle_fields_present(self):
        sources = json.loads((WORK_DIR / "data" / "sources.json").read_text(encoding='utf-8'))
        for s in sources['sources']:
            self.assertIn('status', s, f"Source {s.get('id')} missing status")
            self.assertIn('verified_date', s, f"Source {s.get('id')} missing verified_date")
            self.assertIn('next_review', s, f"Source {s.get('id')} missing next_review")

    def test_source_registry_loads(self):
        sources = json.loads((WORK_DIR / "data" / "sources.json").read_text(encoding='utf-8'))
        self.assertGreater(len(sources['sources']), 0, "Source registry is empty")

if __name__ == '__main__':
    unittest.main()
