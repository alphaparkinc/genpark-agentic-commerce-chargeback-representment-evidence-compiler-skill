# Commerce Chargeback Representment & Evidence Compiler Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Automated merchant dispute response for Visa Compelling Evidence 3.0 / Mastercard dispute condition 4853, compiling digital footprint, AVS/CVV matching, and IP geolocation proof. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `compile_visa_ce30_rebuttal`: Synthesize a formal Visa CE 3.0 dispute rebuttal linking prior undisputed historical transactions with matching device and IP fingerprints.
- `audit_avs_cvv_delivery_proof`: Verify Address Verification Service (AVS) match, CVV match, and carrier signature on delivery to calculate merchant win probability.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_agentic_commerce_chargeback_representment_evidence_compiler_skill.server --test
```
