from pathlib import Path
import pytest

from article_machine.projects import init_project, load_project
from article_machine.serialization import load_structured_file
from article_machine.standards import route_standards


EXPANDED_TYPES = [
    ("scoping-review", "evidence-writing", ["PRISMA-ScR"], []),
    ("diagnostic-meta-analysis", "evidence-writing", ["PRISMA-DTA", "GRADE-DTA"], ["QUADAS-2", "QUADAS-C"]),
    ("dose-response-meta-analysis", "evidence-writing", ["PRISMA 2020", "MOOSE"], ["ROBINS-I", "RoB 2"]),
    ("case-series", "evidence-writing", ["PROCESS 2023"], []),
    ("case-report", "evidence-writing", ["CARE 2017"], []),
    ("delphi-consensus", "evidence-writing", ["CREDES", "AGREE II"], []),
    ("grant-proposal", "evidence-writing", ["FAPESP", "CNPq"], []),
    ("omics-discovery", "computational-discovery", [], []),
]


@pytest.mark.parametrize("kind,expected_lane,expected_guidelines,expected_rob", EXPANDED_TYPES)
def test_route_standards_for_expanded_types(kind, expected_lane, expected_guidelines, expected_rob):
    routed = route_standards(kind)
    assert routed["lane"] == expected_lane
    assert routed["guidelines"] == expected_guidelines
    assert routed["risk_of_bias_tools"] == expected_rob
    assert routed["contract_version"] == 2
    for g in expected_guidelines:
        assert g in routed["checklist_status"]


@pytest.mark.parametrize("kind,expected_lane,expected_guidelines,expected_rob", EXPANDED_TYPES)
def test_init_project_creates_valid_structure_for_expanded_types(tmp_path: Path, kind, expected_lane, expected_guidelines, expected_rob):
    project_dir = init_project(tmp_path, f"Teste {kind}", kind)
    assert project_dir.is_dir()

    project = load_project(project_dir)
    assert project["project_type"] == kind
    assert project["lane"] == expected_lane
    assert project["state"]["current_mode"] == "bootstrap"

    standards = load_structured_file(project_dir / "standards.yaml")
    assert standards["guidelines"] == expected_guidelines
    assert standards["risk_of_bias_tools"] == expected_rob

    protocol = load_structured_file(project_dir / "protocol.yaml")
    assert protocol["project_type"] == kind

    # Check specialized artifacts per type
    if kind == "diagnostic-meta-analysis":
        assert (project_dir / "analysis" / "diagnostic_config.yaml").is_file()
        assert (project_dir / "evidence" / "diagnostic_2x2_data.csv").is_file()
    elif kind == "dose-response-meta-analysis":
        assert (project_dir / "analysis" / "dose_response_config.yaml").is_file()
        assert (project_dir / "evidence" / "dose_response_data.csv").is_file()
    elif kind == "case-report":
        assert (project_dir / "context" / "case_report_care_template.md").is_file()
    elif kind == "case-series":
        assert (project_dir / "context" / "case_series_process_template.md").is_file()
    elif kind == "delphi-consensus":
        assert (project_dir / "context" / "delphi_protocol.yaml").is_file()
    elif kind == "grant-proposal":
        assert (project_dir / "context" / "grant_proposal_template.md").is_file()
    elif kind == "omics-discovery":
        assert (project_dir / "context" / "omics_discovery_plan.yaml").is_file()
