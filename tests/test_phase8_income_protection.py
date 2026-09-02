import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONEY = (ROOT / "employment-money.html").read_text(encoding="utf-8")
USERRA = (ROOT / "employment-rights.html").read_text(encoding="utf-8")
DEBT = (ROOT / "va-debt.html").read_text(encoding="utf-8")
SEARCH = (ROOT / "assets" / "js" / "app.js").read_text(encoding="utf-8")
SOURCES_HTML = (ROOT / "sources.html").read_text(encoding="utf-8")
SOURCES = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))["sources"]
SOURCE_BY_ID = {s["id"]: s for s in SOURCES}


class Phase8IncomeProtectionTests(unittest.TestCase):
    def test_userra_has_distinct_return_timing_categories(self):
        text = USERRA.lower()
        self.assertIn("less than 31 days", text)
        self.assertIn("31 through 180 days", text)
        self.assertIn("more than 180 days", text)
        self.assertIn("14 days", text)
        self.assertIn("90 days", text)
        self.assertIn("8 hours of rest", text)
        self.assertIn("not one universal deadline", text)

    def test_userra_missed_report_time_not_automatic_total_forfeiture(self):
        text = USERRA.lower()
        self.assertIn("does not automatically erase every userra right", text)
        self.assertIn("unexcused absences", text)

    def test_userra_five_year_rule_is_qualified(self):
        text = USERRA.lower()
        self.assertIn("five-year", text)
        self.assertIn("statutory exceptions", text)
        self.assertIn("do not calculate this by simply adding every day", text)

    def test_userra_escalator_does_not_guarantee_exact_old_job(self):
        text = USERRA.lower()
        self.assertIn("not “exact old job guaranteed”", text)
        self.assertIn("priority system", text)
        self.assertIn("qualification", text)

    def test_userra_discrimination_and_retaliation_are_distinct(self):
        text = USERRA.lower()
        self.assertIn("military discrimination and retaliation", text)
        self.assertIn("38 u.s.c. §4311", text)
        self.assertIn("not a rule that every bad action", text)

    def test_userra_enforcement_is_employer_specific(self):
        text = USERRA.lower()
        self.assertIn("private employer", text)
        self.assertIn("state or local government employer", text)
        self.assertIn("federal executive agency", text)
        self.assertIn("osc/mspb", text)
        self.assertIn("doj does not automatically take every complaint", text)

    def test_userra_enforcement_sol_and_reemployment_timing_are_separate(self):
        text = USERRA.lower()
        self.assertIn("no statute of limitations applies", text)
        self.assertIn("does not eliminate the separate §4312 report/application", text)

    def test_userra_benefits_have_specific_rules(self):
        text = USERRA.lower()
        self.assertIn("24 months", text)
        self.assertIn("102%", text)
        self.assertIn("three times the military-service period", text)
        self.assertIn("capped at five years", text)

    def test_userra_regulation_citation_is_current(self):
        self.assertIn("20 C.F.R. Part 1002", USERRA)
        source = SOURCE_BY_ID["userra-regulations-29-cfr-100"]
        self.assertIn("/title-20/", source["source_url"])
        self.assertIn("part-1002", source["source_url"])
        self.assertIn("20 C.F.R. Part 1002", source["claim"])

    def test_scra_six_percent_is_coverage_qualified(self):
        text = MONEY.lower()
        self.assertIn("before", text)
        self.assertIn("qualifying military service", text)
        self.assertIn("veteran status by itself is not enough", text)
        self.assertIn("180 days after termination or release", text)
        self.assertIn("forgiven rather than postponed", text)
        self.assertIn("one year afterward", text)

    def test_scra_no_stale_nonmortgage_six_month_rule(self):
        source = SOURCE_BY_ID["scra-50usc-3937"]["claim"].lower()
        self.assertNotIn("six months post-service", source)
        self.assertIn("nonmortgage", source)
        self.assertIn("during military service", source)

    def test_fdcpa_does_not_treat_every_creditor_as_debt_collector(self):
        text = MONEY.lower()
        self.assertIn("does not automatically apply to every creditor", text)
        self.assertIn("original creditor", text)
        self.assertIn("covered debt collector", text)

    def test_fdcpa_validation_trigger_and_pause_are_qualified(self):
        text = MONEY.lower()
        self.assertIn("receipt of the validation notice", text)
        self.assertIn("disputes the debt <strong>in writing within that period</strong>", MONEY.lower())
        self.assertIn("until it mails the verification", text)
        self.assertIn("lawful collection activity can continue", text)
        self.assertNotIn("within 30 days of first contact", text)

    def test_fdcpa_sample_does_not_claim_every_requested_document_is_required(self):
        text = MONEY.lower()
        self.assertIn("not represented here as documents the fdcpa necessarily requires", text)

    def test_tdiu_preserves_416b(self):
        text = MONEY.lower()
        self.assertIn("§4.16(b)", text)
        self.assertIn("extraschedular", text)
        self.assertIn("do not stop there", text)
        self.assertIn("marginal", text)

    def test_pension_service_rule_is_not_universalized(self):
        text = MONEY.lower()
        self.assertIn("before september 8, 1980", text)
        self.assertIn("after september 7, 1980", text)
        self.assertIn("24 months", text)
        self.assertNotIn("confirm you served at least 90 days", text)

    def test_gi_bill_debt_has_no_generic_thirty_day_deadline(self):
        text = MONEY.lower() + " " + DEBT.lower()
        self.assertIn("do not use a generic “30-day gi bill", text)
        self.assertNotIn("dispute the debt in writing within 30 days if you believe the debt is wrong", text)

    def test_va_debt_four_concepts_are_separate(self):
        text = DEBT.lower()
        self.assertIn("a. “i do not owe this debt.”", text)
        self.assertIn("b. “the va decision that caused the debt is wrong.”", text)
        self.assertIn("c. “the debt may be valid, but va should waive recovery.”", text)
        self.assertIn("d. “i owe it, but i cannot pay it this way.”", text)
        self.assertIn("separately or simultaneously", text)

    def test_va_debt_thirty_day_dispute_is_not_waiver_deadline(self):
        text = DEBT.lower()
        self.assertIn("30-day collection-protection window", text)
        self.assertIn("first debt letter", text)
        self.assertIn("not</strong> a universal waiver deadline", text)
        self.assertNotIn("request a waiver in writing within 30 days", text)

    def test_va_waiver_uses_current_one_year_rule(self):
        text = DEBT.lower()
        self.assertIn("one-year waiver window", text)
        self.assertIn("38 u.s.c. §5302", text)
        self.assertIn("38 c.f.r. §1.963", text)
        self.assertIn("one-year", SOURCE_BY_ID["38-usc-5302"]["claim"].lower())
        self.assertIn("one-year", SOURCE_BY_ID["38-cfr-1-963"]["claim"].lower())

    def test_va_waiver_and_hardship_not_same_thing(self):
        text = DEBT.lower()
        self.assertIn("equity and good conscience", text)
        self.assertIn("fraud", text)
        self.assertIn("bad-faith", text)
        self.assertIn("va form 5655", text)

    def test_va_underlying_decision_and_debt_are_cross_routed(self):
        self.assertIn('href="benefit-reductions.html"', DEBT)
        self.assertIn('href="appeals.html"', DEBT)
        reductions = (ROOT / "benefit-reductions.html").read_text(encoding="utf-8")
        self.assertIn('href="va-debt.html"', reductions)

    def test_va_collection_mechanisms_not_automatic(self):
        text = DEBT.lower()
        self.assertIn("different mechanisms", text)
        self.assertIn("do not all start automatically", text)
        self.assertIn("treasury offset program", text)

    def test_va_education_separates_student_and_school_debt(self):
        text = DEBT.lower()
        self.assertIn("student debt and school debt are different", text)
        self.assertIn("school certifying official", text)

    def test_search_index_routes_common_income_protection_phrases(self):
        for phrase in (
            "VA says I owe money",
            "VA overpayment",
            "Treasury offset",
            "military job rights",
            "fired for deployment",
            "employer won't rehire me",
            "6 percent interest",
            "debt collector",
            "GI Bill overpayment",
            "TDIU",
            "pension",
            "VA took my check",
        ):
            self.assertIn(phrase.lower(), SEARCH.lower(), phrase)

    def test_phase8_source_ids_resolve_in_both_registries(self):
        required = {
            "scra-50usc-3937",
            "doj-scra-6pct",
            "fdcpa-15usc",
            "38-cfr-4-16",
            "va-pension-eligibility",
            "38-usc-5302",
            "38-cfr-1-963",
            "38-cfr-1-911",
            "38-cfr-1-965",
            "va-options-debt-help",
            "va-form-5655",
            "va-education-debt",
            "38-usc-4312",
            "38-usc-4313",
            "38-usc-4316",
            "38-usc-4317",
            "38-usc-4318",
            "38-usc-4324",
            "38-usc-4327",
            "osc-userra",
            "doj-userra",
        }
        self.assertTrue(required.issubset(SOURCE_BY_ID))
        for sid in required:
            self.assertIn(f'id="source-{sid}"', SOURCES_HTML, sid)

    def test_target_pages_contain_they_said_no_pattern(self):
        for page in (MONEY, USERRA, DEBT):
            self.assertIn("THEY SAID NO", page)

    def test_no_stale_money_page_va_waiver_or_tdiu_language(self):
        lower = MONEY.lower()
        self.assertNotIn("you must have at least one service-connected disability rated 60%", lower)
        self.assertNotIn("request a waiver in writing within 30 days", lower)
        self.assertNotIn("within 30 days of first contact by a debt collector", lower)


if __name__ == "__main__":
    unittest.main()
