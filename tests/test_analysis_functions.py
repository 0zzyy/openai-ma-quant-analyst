import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mna_quant.analysis_functions import (
    analyze_agreement_structure_and_compliance,
    identify_and_quantify_deal_risks,
    predict_deal_closure_probability,
    ComplianceResult,
)


def test_analyze_agreement_structure_and_compliance():
    text = "Section 1\nThis Agreement shall...\nSection 2\nThe Buyer may..."
    profile = {"critical_clauses_checklist": ["MAC", "Non_Compete"]}
    result = analyze_agreement_structure_and_compliance(text, {}, profile)
    assert isinstance(result, ComplianceResult)
    assert result.section_count == 2
    assert result.ambiguity_score >= 0
    assert "MAC" in result.missing_clauses


def test_identify_and_quantify_deal_risks():
    text = "Legal compliance is essential. Financial exposure may occur."
    params = {
        "risk_categories_to_scan": ["Legal_Compliance", "Financial_Exposure"],
        "severity_scale_max": 5,
        "likelihood_scale_max": 5,
    }
    risks = identify_and_quantify_deal_risks(text, {}, params)
    assert len(risks) == 2
    categories = {r.category for r in risks}
    assert categories == {"Legal_Compliance", "Financial_Exposure"}


def test_predict_deal_closure_probability():
    prob = predict_deal_closure_probability(
        deal_financials_input={"deal_value_usd_M": 500},
        deal_structure_input={},
        agreement_analysis_input={"missing_clauses": ["MAC"]},
        market_context_input={"regulatory_hurdle_score_1_5": 4},
        prediction_model_config={},
    )
    assert 0 <= prob <= 100
