# -*- coding: utf-8 -*-
"""Commerce Chargeback Representment & Evidence Compiler for GenPark Agentic Commerce."""
import json
import time
from typing import Dict, Any, List

class ChargebackRepresentmentEvidenceCompiler:
    """Card brand chargeback representment and Visa CE 3.0 evidence compilation engine."""

    @staticmethod
    def compile_visa_ce30_rebuttal(disputed_charge_id: str, disputed_amount_usd: float, reason_code: str, prior_undisputed_tx_count: int, matching_core_elements: List[str] = None) -> Dict[str, Any]:
        """Compile Visa Compelling Evidence 3.0 (CE 3.0) rebuttal docket requiring 2 prior qualifying transactions."""
        qualifies_for_ce30 = prior_undisputed_tx_count >= 2 and len(matching_core_elements or []) >= 2
        
        evidence_summary = (
            f"Under Visa Compelling Evidence 3.0 rules, merchant establishes non-fraudulent participation: "
            f"Cardholder engaged in {prior_undisputed_tx_count} prior undisputed transactions using identical "
            f"credentials ({', '.join(matching_core_elements or ['IP', 'Device'])}). Chargeback liability must shift to issuer."
        )

        return {
            "disputed_charge_id": disputed_charge_id,
            "disputed_amount_usd": disputed_amount_usd,
            "reason_code": reason_code,
            "qualifies_for_visa_ce30": qualifies_for_ce30,
            "liability_shift_verdict": "ISSUER_LIABILITY_REVERSAL" if qualifies_for_ce30 else "STANDARD_EVIDENCE_ARBITRATION",
            "formal_rebuttal_text": evidence_summary,
            "action_required": "Transmit CE3.0 tokenized package to acquiring processor immediately."
        }

    @staticmethod
    def audit_avs_cvv_delivery_proof(avs_response_code: str, cvv_result_code: str, has_carrier_signature: bool, customer_download_logged: bool = False) -> Dict[str, Any]:
        """Estimate dispute win probability based on technical cryptographic payment indicators."""
        win_score = 0.0
        # AVS match (Y = full address & 9-digit zip match)
        if avs_response_code == "Y":
            win_score += 0.35
        elif avs_response_code in ["A", "Z"]:
            win_score += 0.20
        # CVV Match (M = Match)
        if cvv_result_code == "M":
            win_score += 0.30
        # Physical Proof
        if has_carrier_signature:
            win_score += 0.35
        if customer_download_logged:
            win_score += 0.25

        win_prob_pct = min(98.0, round(win_score * 100.0, 1))

        return {
            "avs_status": "FULL_MATCH" if avs_response_code == "Y" else "PARTIAL_OR_FAILED",
            "cvv_status": "MATCH" if cvv_result_code == "M" else "NO_MATCH",
            "proof_of_delivery": "CARRIER_SIGNATURE_CONFIRMED" if has_carrier_signature else "STANDARD_GEO_DROP",
            "merchant_win_probability_pct": win_prob_pct,
            "recommendation": "DEFINITIVELY_CONTEST" if win_prob_pct >= 70.0 else "REVIEW_DISPUTE_COSTS_VS_MARGIN"
        }
