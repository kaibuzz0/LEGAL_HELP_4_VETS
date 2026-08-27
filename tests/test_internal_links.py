"""Regression checks for local HTML links and fragments."""
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

WORK_DIR = Path(__file__).parent.parent
HTML_FILES = sorted(WORK_DIR.glob("*.html"))


class TestInternalLinks(unittest.TestCase):
    def test_internal_html_links_exist(self):
        for source in HTML_FILES:
            text = source.read_text(encoding="utf-8")
            for href in re.findall(r'href=["\']([^"\']+)["\']', text, re.IGNORECASE):
                if not href or href.startswith(("#", "http://", "https://", "mailto:", "tel:", "javascript:")):
                    continue
                parsed = urlsplit(href)
                path = parsed.path
                if not path or not path.lower().endswith(".html"):
                    continue
                target = (source.parent / path).resolve()
                self.assertTrue(target.exists(), f"{source.name}: missing target {href}")
                self.assertEqual(target.parent, WORK_DIR.resolve(), f"{source.name}: HTML link escapes repo root: {href}")

                if parsed.fragment:
                    target_text = target.read_text(encoding="utf-8")
                    ids = set(re.findall(r'id=["\']([^"\']+)["\']', target_text, re.IGNORECASE))
                    self.assertIn(parsed.fragment, ids, f"{source.name}: missing fragment {href}")


if __name__ == "__main__":
    unittest.main()
