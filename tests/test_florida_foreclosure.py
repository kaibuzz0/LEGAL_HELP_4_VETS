import copy
import json
import unittest
from pathlib import Path

from scripts.validate_florida_foreclosure import validate

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "florida-foreclosure.json").read_text(encoding="utf-8"))
HOUSING = json.loads((ROOT / "data" / "states" / "florida.json").read_text(encoding="utf-8"))


class FloridaForeclosureTests(unittest.TestCase):
    def test_semantic_validator(self):
        self.assertEqual(validate(DATA), [])

    def test_foreclosure_is_separate_dataset(self):
        self.assertEqual(DATA["subject"], "housing_foreclosure")
        self.assertEqual(DATA["dataset_id"], "florida-foreclosure")

    def test_complaint_not_final_judgment(self):
        self.assertIn("foreclosure_complaint", DATA["routes"])
        self.assertIn("final_judgment", DATA["routes"])
        self.assertNotEqual(
            DATA["routes"]["foreclosure_complaint"]["id"],
            DATA["routes"]["final_judgment"]["id"],
        )

    def test_foreclosure_response_is_twenty_not_eviction_five(self):
        foreclosure_clock = DATA["routes"]["foreclosure_complaint"]["immediate_clock"]
        eviction_clock = HOUSING["document_routes"]["eviction_summons_complaint"]["immediate_clock"]
        self.assertEqual(foreclosure_clock["value"], 20)
        self.assertEqual(eviction_clock["value"], 5)
        self.assertIn("original process", foreclosure_clock["trigger"].lower())
        self.assertEqual(foreclosure_clock["computation_authority"], "fl-r-gen-prac-2-514")

    def test_current_civil_rule_sources_are_classified_as_rules(self):
        authorities = {a["id"]: a for a in DATA["authorities"]}
        self.assertEqual(authorities["fl-r-civ-p-1-140"]["authority_type"], "court_rule")
        self.assertEqual(authorities["fl-r-civ-p-1-510"]["authority_type"], "court_rule")
        self.assertEqual(authorities["fl-r-gen-prac-2-514"]["authority_type"], "court_rule")

    def test_order_to_show_cause_is_separate_and_non_generic(self):
        route = DATA["routes"]["order_to_show_cause"]
        self.assertIn("fl-702-10", route["authorities"])
        self.assertIsNone(route["immediate_clock"])
        self.assertIn("court-controlled", route["description"])
        self.assertTrue(any("no single generic" in x.lower() for x in route["exceptions"]))

    def test_summary_judgment_current_timing(self):
        route = DATA["routes"]["summary_judgment"]
        self.assertEqual(route["immediate_clock"]["value"], 40)
        self.assertIn("service of the motion", route["immediate_clock"]["trigger"].lower())
        self.assertEqual(route["other_clocks"][0]["value"], 10)
        self.assertIn("summary-judgment response", route["other_clocks"][0]["trigger"].lower())

    def test_sale_certificate_objection_title_redemption_are_distinct(self):
        routes = DATA["routes"]
        required = [
            "judicial_sale",
            "certificate_of_sale",
            "sale_objection",
            "certificate_of_title",
            "redemption",
        ]
        for rid in required:
            self.assertIn(rid, routes)
        self.assertEqual(len({routes[rid]["id"] for rid in required}), len(required))

    def test_sale_objection_tied_to_certificate_filing(self):
        clock = DATA["routes"]["sale_objection"]["immediate_clock"]
        self.assertEqual(clock["value"], 10)
        self.assertIn("filing of the certificate of sale", clock["trigger"].lower())
        self.assertNotIn("auction", clock["trigger"].lower())

    def test_certificate_of_title_is_not_auction(self):
        route = DATA["routes"]["certificate_of_title"]
        self.assertIsNone(route["immediate_clock"])
        self.assertIn("title passes", route["description"].lower())
        self.assertTrue(any("certificate of sale" in x.lower() for x in route["exceptions"]))

    def test_redemption_is_event_based_not_sale_objection(self):
        route = DATA["routes"]["redemption"]
        self.assertIsNone(route["immediate_clock"])
        self.assertIn("later of", route["description"].lower())
        self.assertIn("certificate of sale", route["description"].lower())
        self.assertTrue(any("not the same as objecting" in x.lower() for x in route["exceptions"]))

    def test_post_sale_occupant_categories_are_separate(self):
        routes = DATA["routes"]
        for rid in (
            "post_sale_former_owner",
            "post_sale_bona_fide_tenant",
            "post_sale_other_occupant",
        ):
            self.assertIn(rid, routes)
            self.assertIsNone(routes[rid]["immediate_clock"])

    def test_former_owner_does_not_receive_ptfa_automatically(self):
        former = DATA["routes"]["post_sale_former_owner"]
        tenant = DATA["routes"]["post_sale_bona_fide_tenant"]
        self.assertNotIn("ptfa", former["federal_overlays"])
        self.assertIn("ptfa", tenant["federal_overlays"])
        self.assertTrue(any("former mortgagor" in x.lower() for x in former["exceptions"]))

    def test_all_federal_overlays_resolve(self):
        federal = json.loads((ROOT / "data" / "housing-federal.json").read_text(encoding="utf-8"))
        ids = {x["id"] for x in federal["overlays"]}
        self.assertTrue(set(DATA["federal_overlays"]).issubset(ids))
        for route in DATA["routes"].values():
            self.assertTrue(set(route.get("federal_overlays", [])).issubset(ids))

    def test_invalid_overlay_is_rejected(self):
        sample = copy.deepcopy(DATA)
        sample["routes"]["foreclosure_complaint"]["federal_overlays"].append("not-a-real-overlay")
        self.assertTrue(any("unknown federal overlay" in e for e in validate(sample)))

    def test_numeric_clock_without_trigger_is_rejected(self):
        sample = copy.deepcopy(DATA)
        sample["routes"]["sale_objection"]["immediate_clock"]["trigger"] = ""
        self.assertTrue(any("numeric clock missing trigger" in e for e in validate(sample)))

    def test_rule_mislabeled_as_statute_is_rejected(self):
        sample = copy.deepcopy(DATA)
        rule = next(a for a in sample["authorities"] if a["id"] == "fl-r-civ-p-1-140")
        rule["authority_type"] = "statute"
        self.assertTrue(any("must be classified court_rule" in e for e in validate(sample)))

    def test_archived_verified_statute_source_is_rejected(self):
        sample = copy.deepcopy(DATA)
        statute = next(a for a in sample["authorities"] if a["id"] == "fl-45-031")
        statute["source_url"] += "&StatuteYear=2024"
        self.assertTrue(any("archived statute year" in e for e in validate(sample)))

    def test_null_does_not_mean_no_deadline(self):
        sample = copy.deepcopy(DATA)
        sample["routes"]["post_sale_other_occupant"]["description"] = "There is no deadline."
        self.assertTrue(any("null clock rendered" in e for e in validate(sample)))

    def test_cross_dataset_dependency_and_route_resolve(self):
        self.assertEqual(DATA["dataset_dependencies"], ["florida-housing"])
        ref = DATA["cross_dataset_refs"][0]
        self.assertEqual(ref["dataset"], "florida-housing")
        self.assertIn("ptfa_tenant_after_foreclosure", ref["routes"])

    def test_invalid_cross_dataset_route_is_rejected(self):
        sample = copy.deepcopy(DATA)
        sample["cross_dataset_refs"][0]["routes"] = ["not-a-real-route"]
        self.assertTrue(any("route does not resolve" in e for e in validate(sample)))

    def test_resources_are_verified_routing_not_authority(self):
        required = {
            "florida_courts_self_help",
            "florida_bar_lrs",
            "florida_legal_aid",
            "fdva",
            "fdva_county_vso",
            "hud_housing_counseling",
            "va_lsv_h",
            "va_ssvf",
            "va_home_loan",
        }
        self.assertTrue(required.issubset(DATA["resources"]))
        authority_ids = {a["id"] for a in DATA["authorities"]}
        self.assertTrue(required.isdisjoint(authority_ids))

    def test_post_sale_document_chain_extends_through_execution(self):
        routes = DATA["routes"]
        for rid in (
            "certificate_of_title",
            "post_sale_writ_of_possession",
            "post_sale_sheriff_execution",
        ):
            self.assertIn(rid, routes)
        self.assertNotEqual(routes["certificate_of_title"]["id"], routes["post_sale_writ_of_possession"]["id"])
        self.assertNotEqual(routes["post_sale_writ_of_possession"]["id"], routes["post_sale_sheriff_execution"]["id"])

    def test_foreclosure_writ_uses_rule_1580_not_section_83_62(self):
        route = DATA["routes"]["post_sale_writ_of_possession"]
        self.assertIn("fl-r-civ-p-1-580", route["authorities"])
        self.assertNotIn("fl-83-62", route["authorities"])
        self.assertIsNone(route["immediate_clock"])
        joined = " ".join(route["exceptions"]).lower()
        self.assertIn("affidavit", joined)
        self.assertIn("sheriff", joined)

    def test_sheriff_execution_has_no_statewide_foreclosure_24_hour_clock(self):
        route = DATA["routes"]["post_sale_sheriff_execution"]
        self.assertIsNone(route["immediate_clock"])
        self.assertIn("does not publish a universal", route["description"].lower())
        self.assertTrue(any("24-hour" in x for x in route["exceptions"]))

    def test_certificate_of_title_not_physical_execution(self):
        route = DATA["routes"]["certificate_of_title"]
        self.assertIsNone(route["immediate_clock"])
        self.assertIn("not itself physical sheriff execution", route["description"].lower())
        self.assertTrue(any("writ of possession" in x.lower() for x in route["exceptions"]))

    def test_former_owner_bona_fide_other_and_unknown_are_distinct(self):
        routes = DATA["routes"]
        ids = {
            routes["post_sale_former_owner"]["id"],
            routes["post_sale_bona_fide_tenant"]["id"],
            routes["post_sale_other_tenant"]["id"],
            routes["post_sale_other_occupant"]["id"],
        }
        self.assertEqual(len(ids), 4)

    def test_other_tenant_not_ptfa_qualified_does_not_mean_no_protection(self):
        route = DATA["routes"]["post_sale_other_tenant"]
        joined = " ".join(route["exceptions"]).lower()
        self.assertIn("not ptfa-qualified is not equivalent to no protection", joined)
        self.assertIsNone(route["immediate_clock"])

    def test_unknown_occupant_remains_identification_first(self):
        route = DATA["routes"]["post_sale_other_occupant"]
        self.assertIsNone(route["immediate_clock"])
        joined = " ".join(route["exceptions"]).lower()
        for fact in ("lease", "former owner", "rent", "certificate-of-title", "writ"):
            self.assertIn(fact, joined)
        self.assertIn("unknown status must remain unknown", joined)

    def test_redemption_expiration_is_not_possession_deadline(self):
        route = DATA["routes"]["redemption"]
        self.assertIsNone(route["immediate_clock"])
        joined = " ".join(route["exceptions"]).lower()
        self.assertIn("physical possession", joined)
        self.assertIn("separate legal events", joined)

    def test_sale_objection_is_not_possession_deadline(self):
        objection = DATA["routes"]["sale_objection"]
        router = DATA["routes"]["post_sale_document_router"]
        self.assertEqual(objection["immediate_clock"]["value"], 10)
        self.assertTrue(any("sale-objection expiration" in x.lower() and "not possession" in x.lower() for x in router["exceptions"]))

    def test_appeal_does_not_itself_stay_enforcement(self):
        route = DATA["routes"]["appeal_stay_postsale"]
        self.assertIsNone(route["immediate_clock"])
        self.assertIn("does not itself create a stay", route["description"].lower())
        self.assertIn("fl-r-app-p-9-310", route["authorities"])

    def test_validator_rejects_section_83_62_as_foreclosure_bridge(self):
        sample = copy.deepcopy(DATA)
        sample["routes"]["post_sale_writ_of_possession"]["authorities"].append("fl-83-62")
        self.assertTrue(any("improperly cites §83.62" in e for e in validate(sample)))

    def test_validator_rejects_certificate_title_as_immediate_lockout(self):
        sample = copy.deepcopy(DATA)
        sample["routes"]["certificate_of_title"]["description"] = "Certificate of title means immediate lockout."
        self.assertTrue(any("certificate of title" in e.lower() and "physical eviction" in e.lower() for e in validate(sample)))

    def test_current_forms_are_classified_as_government_forms(self):
        authorities = {a["id"]: a for a in DATA["authorities"]}
        self.assertEqual(authorities["fl-form-1-915"]["authority_type"], "government_form")
        self.assertEqual(authorities["fl-form-1-996a"]["authority_type"], "government_form")


if __name__ == "__main__":
    unittest.main()
