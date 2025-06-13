"""Utility functions for simple M&A quantitative analysis."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ComplianceResult:
    section_count: int
    ambiguity_score: float
    missing_clauses: List[str]


def analyze_agreement_structure_and_compliance(
    agreement_text: str,
    deal_context: Dict[str, Any],
    evaluation_profile: Dict[str, Any],
) -> ComplianceResult:
    """Rudimentary analysis of section structure and clause presence."""
    # Count sections by detecting typical section headers like "1." or "Section 1"
    section_pattern = re.compile(r"^(?:\d+\.|section\s+\d+)", re.IGNORECASE | re.MULTILINE)
    sections = section_pattern.findall(agreement_text)
    section_count = len(sections)

    # Ambiguity score: ratio of ambiguous modal verbs to total sentences
    ambiguous_terms = re.findall(r"\b(?:may|might|could|should)\b", agreement_text, re.IGNORECASE)
    sentences = re.split(r"[.!?]+", agreement_text)
    ambiguity_score = len(ambiguous_terms) / max(len(sentences), 1)

    # Clause checklist compliance
    checklist = evaluation_profile.get("critical_clauses_checklist", [])
    missing = []
    for clause in checklist:
        pattern = re.compile(re.escape(clause), re.IGNORECASE)
        if not pattern.search(agreement_text):
            missing.append(clause)

    return ComplianceResult(
        section_count=section_count,
        ambiguity_score=round(ambiguity_score, 3),
        missing_clauses=missing,
    )


@dataclass
class RiskItem:
    category: str
    severity: int
    likelihood: int


def identify_and_quantify_deal_risks(
    agreement_text: str,
    deal_context: Dict[str, Any],
    risk_assessment_parameters: Dict[str, Any],
) -> List[RiskItem]:
    """Simple keyword based risk extraction."""
    categories = risk_assessment_parameters.get(
        "risk_categories_to_scan",
        [
            "Legal_Compliance",
            "Financial_Exposure",
            "Operational_Disruption",
        ],
    )
    severity_max = risk_assessment_parameters.get("severity_scale_max", 5)
    likelihood_max = risk_assessment_parameters.get("likelihood_scale_max", 5)

    results: List[RiskItem] = []
    for cat in categories:
        pattern = re.compile(cat.replace("_", " "), re.IGNORECASE)
        hits = len(pattern.findall(agreement_text))
        if hits:
            severity = min(severity_max, hits)
            likelihood = min(likelihood_max, 1 + hits // 2)
            results.append(RiskItem(cat, severity, likelihood))
    return results


def predict_deal_closure_probability(
    deal_financials_input: Dict[str, Any],
    deal_structure_input: Dict[str, Any],
    agreement_analysis_input: Dict[str, Any],
    market_context_input: Dict[str, Any],
    prediction_model_config: Dict[str, Any],
) -> float:
    """Naive scoring model returning probability 0-100."""
    base = 50.0
    base += deal_financials_input.get("deal_value_usd_M", 0) / 1000.0
    base += market_context_input.get("regulatory_hurdle_score_1_5", 3) * (-2)
    base -= len(agreement_analysis_input.get("missing_clauses", [])) * 3
    base = max(0.0, min(100.0, base))
    return round(base, 2)


