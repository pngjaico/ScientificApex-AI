from __future__ import annotations

from copy import deepcopy


_STANDARD_MATRIX: dict[str, dict] = {
    "machine-governance": {
        "lane": "machine-governance",
        "guidelines": [],
        "risk_of_bias_tools": [],
        "policy_labels": ["machine-governance", "reproducibility", "fail-closed"],
        "deliverables": ["inventory", "upgrade record", "verification report", "benchmark", "release audit"],
    },
    "systematic-review": {
        "lane": "evidence-writing",
        "guidelines": ["PRISMA", "GRADE", "ROBIS", "AMSTAR 2"],
        "risk_of_bias_tools": ["RoB 2", "ROBINS-I"],
        "policy_labels": ["evidence-synthesis", "high-rigor"],
        "deliverables": ["protocol", "screening log", "claim map", "manuscript", "review report"],
        "registration_policy": {
            "required": True,
            "timing": "before-data-extraction",
            "accepted_registries": ["PROSPERO", "OSF"],
            "rationale": "Systematic reviews must be registered prospectively before extraction to strengthen rigor and editorial credibility.",
        },
    },
    "network-meta-analysis": {
        "lane": "evidence-writing",
        "guidelines": ["PRISMA-NMA", "GRADE"],
        "risk_of_bias_tools": ["RoB 2", "ROBINS-I"],
        "policy_labels": ["evidence-synthesis", "comparative-effectiveness"],
        "deliverables": ["protocol", "network tables", "claim map", "manuscript", "review report"],
        "registration_policy": {
            "required": True,
            "timing": "before-data-extraction",
            "accepted_registries": ["PROSPERO", "OSF"],
            "rationale": "Evidence syntheses and meta-analyses must be registered prospectively before extraction to strengthen rigor and editorial credibility.",
        },
    },
    "diagnostic-study": {
        "lane": "evidence-writing",
        "guidelines": ["STARD 2015", "QUADAS-3"],
        "risk_of_bias_tools": ["QUADAS-3"],
        "policy_labels": ["diagnostic-accuracy"],
        "deliverables": ["protocol", "analysis", "claim map", "manuscript", "review report"],
    },
    "observational-study": {
        "lane": "evidence-writing",
        "guidelines": ["STROBE"],
        "risk_of_bias_tools": ["ROBINS-I"],
        "policy_labels": ["observational"],
        "deliverables": ["protocol", "analysis", "claim map", "manuscript", "review report"],
    },
    "clinical-trial": {
        "lane": "evidence-writing",
        "guidelines": ["CONSORT 2025", "SPIRIT 2025"],
        "risk_of_bias_tools": ["RoB 2"],
        "policy_labels": ["interventional"],
        "deliverables": ["protocol", "analysis", "claim map", "manuscript", "review report"],
    },
    "animal-study": {
        "lane": "evidence-writing",
        "guidelines": ["ARRIVE"],
        "risk_of_bias_tools": ["SYRCLE"],
        "policy_labels": ["preclinical"],
        "deliverables": ["protocol", "analysis", "claim map", "manuscript", "review report"],
    },
    "prediction-model": {
        "lane": "evidence-writing",
        "guidelines": ["TRIPOD+AI"],
        "risk_of_bias_tools": ["PROBAST+AI"],
        "policy_labels": ["prediction"],
        "deliverables": ["protocol", "analysis", "claim map", "manuscript", "review report"],
    },
    "health-economics": {
        "lane": "evidence-writing",
        "guidelines": ["CHEERS"],
        "risk_of_bias_tools": [],
        "policy_labels": ["economic-evaluation"],
        "deliverables": ["protocol", "analysis", "claim map", "manuscript", "review report"],
    },
    "drug-discovery": {
        "lane": "computational-discovery",
        "guidelines": [],
        "risk_of_bias_tools": [],
        "policy_labels": ["hypothesis-generating", "non-clinical", "computational-discovery"],
        "deliverables": ["discovery plan", "benchmark", "analysis", "report", "manuscript"],
    },
    "intestinal-digital-twin": {
        "lane": "computational-discovery",
        "guidelines": [],
        "risk_of_bias_tools": [],
        "policy_labels": ["hypothesis-generating", "non-clinical", "digital-twin"],
        "deliverables": ["model spec", "sensitivity analysis", "analysis", "report", "manuscript"],
    },
    "thesis-chapter": {
        "lane": "evidence-writing",
        "guidelines": [],
        "risk_of_bias_tools": [],
        "policy_labels": ["thesis"],
        "deliverables": ["chapter brief", "claim map", "chapter draft", "review report"],
    },
}

_DEFAULT_STANDARD = {
    "lane": "evidence-writing",
    "guidelines": [],
    "risk_of_bias_tools": [],
    "policy_labels": [],
    "deliverables": ["analysis", "manuscript", "review report"],
    "registration_policy": {
        "required": False,
        "timing": "",
        "accepted_registries": [],
        "rationale": "",
    },
}


def route_standards(project_type: str) -> dict:
    key = (project_type or "").strip().lower()
    routed = deepcopy(_STANDARD_MATRIX.get(key, _DEFAULT_STANDARD))
    routed["contract_version"] = 2
    routed["project_type"] = key
    if key != "machine-governance":
        routed["registration_policy"] = {
            "required": True,
            "timing": "before-scientific-work",
            "accepted_registries": ["PROSPERO", "OSF"],
            "verification_required": True,
            "rationale": "User policy: verified protocol registration before scientific execution; preparing the protocol is permitted.",
        }
    checklist = {}
    for guideline in routed["guidelines"]:
        checklist[guideline] = {"status": "pending", "items": []}
    for tool in routed["risk_of_bias_tools"]:
        checklist[tool] = {"status": "pending", "items": []}
    routed["checklist_status"] = checklist
    return routed
