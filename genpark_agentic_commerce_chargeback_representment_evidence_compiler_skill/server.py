# -*- coding: utf-8 -*-
"""MCP Server for Commerce Chargeback Representment & Evidence Compiler Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import ChargebackRepresentmentEvidenceCompiler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "compile_visa_ce30_rebuttal",
        "description": "Synthesize a formal Visa CE 3.0 dispute rebuttal linking prior undisputed historical transactions with matching device and IP fingerprints.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "disputed_charge_id": {
                    "type": "string"
                },
                "disputed_amount_usd": {
                    "type": "number"
                },
                "reason_code": {
                    "type": "string",
                    "enum": [
                        "10.4_OTHER_FRAUD",
                        "4853_CARDHOLDER_DISPUTE",
                        "13.1_MERCHANDISE_NOT_RECEIVED"
                    ]
                },
                "prior_undisputed_tx_count": {
                    "type": "integer"
                },
                "matching_core_elements": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "disputed_charge_id",
                "disputed_amount_usd",
                "reason_code",
                "prior_undisputed_tx_count"
            ]
        }
    },
    {
        "name": "audit_avs_cvv_delivery_proof",
        "description": "Verify Address Verification Service (AVS) match, CVV match, and carrier signature on delivery to calculate merchant win probability.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "avs_response_code": {
                    "type": "string",
                    "enum": [
                        "Y",
                        "A",
                        "Z",
                        "N",
                        "U"
                    ]
                },
                "cvv_result_code": {
                    "type": "string",
                    "enum": [
                        "M",
                        "N",
                        "P",
                        "U"
                    ]
                },
                "has_carrier_signature": {
                    "type": "boolean"
                },
                "customer_download_logged": {
                    "type": "boolean"
                }
            },
            "required": [
                "avs_response_code",
                "cvv_result_code",
                "has_carrier_signature"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-chargeback-representment-evidence-compiler-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(ChargebackRepresentmentEvidenceCompiler, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-chargeback-representment-evidence-compiler-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-chargeback-representment-evidence-compiler-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
