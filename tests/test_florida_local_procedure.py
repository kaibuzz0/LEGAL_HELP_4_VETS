import copy
import json
import unittest
from pathlib import Path

from scripts.validate_florida_local_procedure import validate

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "florida-local-procedure.json").read_text(encoding="utf-8"))


class FloridaLocalProcedureTests(unittest.TestCase):
    def test_semantic_validator(self):
        self.assertEqual(validate(DATA), [])

    def test_pilot_counties_are_explicit(self):
        counties = {x["county"] for x in DATA["counties"].values()}
        self.assertEqual(counties, {"Hillsborough", "Orange", "Duval"})
        self.assertIsNone(DATA["default_county"])

    def test_router_is_null_safe(self):
        for field in ("county", "court", "sheriff"):
            self.assertIsNone(DATA["router"][field])
        self.assertIn("Never default", DATA["router"]["warning"])

    def test_all_sources_are_official_and_local(self):
        for source in DATA["sources"]:
            self.assertTrue(source["official"])
            self.assertFalse(source["statewide"])
            self.assertIn(source["county"], {"Hillsborough", "Orange", "Duval"})
            self.assertTrue(source["url"].startswith("https://"))

    def test_clerk_and_sheriff_guidance_is_not_legal_authority(self):
        for source in DATA["sources"]:
            if source["source_type"] in {"clerk_filing_procedure", "sheriff_execution_practice", "informational_guidance"}:
                self.assertFalse(source["legal_authority"])

    def test_local_operational_timing_is_not_legal_deadline(self):
        duval = DATA["counties"]["duval"]["writ_execution"]
        timing = duval["operational_timing"]
        self.assertEqual(timing["value"], 24)
        self.assertFalse(timing["legal_deadline"])
        self.assertIn("Duval", timing["scope"])
        self.assertIn("not a statewide", timing["display"].lower())

    def test_orange_eviction_24_hour_guidance_does_not_become_foreclosure_clock(self):
        orange = DATA["counties"]["orange"]
        self.assertIn("24-hour", orange["eviction"]["summary"])
        self.assertIsNone(orange["writ_execution"]["operational_timing"])
        self.assertIn("eviction guidance", orange["writ_execution"]["summary"].lower())

    def test_hillsborough_chapter83_sheriff_guidance_not_foreclosure_authority(self):
        hills = DATA["counties"]["hillsborough"]
        self.assertIn("Chapter 83", hills["eviction"]["summary"])
        self.assertNotIn("§83.62", hills["foreclosure"]["summary"])
        self.assertIsNone(hills["writ_execution"]["operational_timing"])

    def test_duval_clerk_24_hour_statement_stays_local(self):
        source = next(x for x in DATA["sources"] if x["id"] == "duval-clerk-foreclosure")
        self.assertFalse(source["legal_authority"])
        self.assertEqual(source["county"], "Duval")
        self.assertTrue(any("not encoded as a statewide" in x for x in source["supports"]))

    def test_local_source_cannot_be_marked_statewide(self):
        sample = copy.deepcopy(DATA)
        sample["sources"][0]["statewide"] = True
        self.assertTrue(any("non-statewide" in e for e in validate(sample)))

    def test_nonofficial_source_is_rejected(self):
        sample = copy.deepcopy(DATA)
        sample["sources"][0]["official"] = False
        self.assertTrue(any("must be official" in e for e in validate(sample)))

    def test_local_operational_timing_requires_explicit_county_scope(self):
        sample = copy.deepcopy(DATA)
        sample["counties"]["duval"]["writ_execution"]["operational_timing"]["scope"] = "Florida"
        self.assertTrue(any("must name its county scope" in e for e in validate(sample)))

    def test_local_guidance_cannot_override_statewide_deadline(self):
        sample = copy.deepcopy(DATA)
        sample["counties"]["orange"]["foreclosure"]["statewide_deadline_override"] = True
        self.assertTrue(any("cannot override statewide" in e for e in validate(sample)))

    def test_foreclosure_writ_section_cannot_import_83_62(self):
        sample = copy.deepcopy(DATA)
        sample["counties"]["duval"]["writ_execution"]["summary"] += " §83.62"
        self.assertTrue(any("improperly imports §83.62" in e for e in validate(sample)))

    def test_provider_routes_resolve(self):
        for county in DATA["counties"].values():
            self.assertTrue(county["providers"])

    def test_local_veteran_providers_have_explicit_county_coverage(self):
        for county in DATA["counties"].values():
            self.assertTrue(county["local_providers"])
            for provider in county["local_providers"]:
                self.assertTrue(provider["official"])
                self.assertTrue(provider["verified"])
                self.assertIn(county["county"].lower(), provider["coverage"].lower())
                self.assertTrue(provider["url"].startswith("https://"))
                self.assertIn("guarantee", provider["note"].lower())

    def test_local_provider_without_county_coverage_is_rejected(self):
        sample = copy.deepcopy(DATA)
        sample["counties"]["duval"]["local_providers"][0]["coverage"] = "Florida"
        self.assertTrue(any("coverage must explicitly name the county" in e for e in validate(sample)))


if __name__ == "__main__":
    unittest.main()
