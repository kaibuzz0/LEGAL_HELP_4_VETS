"""
Regression tests for LEGAL HELP 4 VETS high-risk legal language.
Run with: python tests/test_legal_language.py

These tests FLAG newly introduced high-risk words for review; they do not fail merely because the word appears.
The output is a report of occurrences that should be manually reviewed.
"""
import re
from pathlib import Path

WORK_DIR = Path(__file__).parent.parent
PAGES = [
    "index.html", "help-now.html", "claims.html", "appeals.html", "discharge-upgrade.html",
    "housing.html", "employment-money.html", "family-immigration.html", "legal-library.html",
    "toolkit.html", "about.html", "sources.html", "substance-use.html", "widows.html",
    "state-resources.html", "faith-encouragement.html"
]

RISK_WORDS = ['must', 'always', 'guaranteed', 'automatically', 'entitled', 'required', 'qualifies', 'eligible', 'illegal', 'unlawful', 'prohibited', 'cannot', 'deadline']

def test_high_risk_language():
    findings = []
    for page in PAGES:
        text = (WORK_DIR / page).read_text(encoding='utf-8')
        for word in RISK_WORDS:
            for m in re.finditer(rf'\b{word}\b', text, re.IGNORECASE):
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                context = text[start:end].replace('\n', ' ')
                findings.append({
                    "page": page,
                    "word": word,
                    "context": context
                })
    return findings

if __name__ == '__main__':
    findings = test_high_risk_language()
    print(f"High-risk language occurrences: {len(findings)}")
    for f in findings[:20]:
        print(f"\n  {f['page']} | {f['word']}: ...{f['context']}...")
    if len(findings) > 20:
        print(f"\n  ... and {len(findings) - 20} more")
