---
name: protocol-registration-governor
description: Use when preregistration, PROSPERO, OSF registration, ClinicalTrials.gov registration, protocol freeze, amendments, or registry-to-manuscript consistency is needed.
---

# Protocol Registration Governor

Use this skill before corpus build, screening, trial analysis, or any claim that a protocol was prespecified.

## Gate
- Confirm whether the project type requires registration or public protocol posting.
- Compare `protocol.yaml` against registry records, protocol PDFs, amendments, and dated snapshots.
- Record registry URL, identifier, registered_at, amendment history, and unresolved deviations in `protocol.yaml`.
- Block "prospective", "registered", "prespecified", or "protocol-driven" wording unless the registry evidence supports it.

## Registry Routes
- Systematic review: PROSPERO when eligible; OSF or institutional registry when PROSPERO is unavailable or not applicable.
- Clinical trial: ClinicalTrials.gov, WHO ICTRP, ReBEC, or jurisdiction-specific registry as relevant.
- Observational or secondary-data study: OSF, institutional repository, or protocol manuscript.
- Animal/preclinical: registry or protocol archive when required by venue or funder.

## Required Outputs
- `context/protocol_registration_audit.md`
- registry metadata in `protocol.yaml`
- deviations table when methods changed after protocol freeze

## Red Flags
- Registering after extraction and calling the study prospective.
- Hiding amendments that affect outcomes, eligibility, or analysis plan.
- Citing a registry page without a dated snapshot or retrieval manifest.
