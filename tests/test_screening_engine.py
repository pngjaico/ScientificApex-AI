"""Tests for the Canonical Triple-Reviewer Screening Engine and PRISMA Checklists."""

import json
from pathlib import Path

import pytest

from article_machine.cli import main
from article_machine.services.screening_engine import (
    TripleReviewerScreeningEngine,
    run_triple_screening_command,
)


@pytest.fixture
def mock_screening_project(tmp_path: Path) -> Path:
    """Create a minimal project structure with a deduplicated screening queue."""
    project_dir = tmp_path / "test-screening-project"
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Minimal protocol.yaml
    protocol_content = {
        "contract_version": 2,
        "research_question": "Comparative efficacy of liver machine perfusion vs static cold storage.",
        "pico": {
            "population": "Adult human liver transplant recipients",
            "interventions": [{"code": "HOPE", "name": "Hypothermic Oxygenated Perfusion"}],
            "comparator": {"code": "SCS", "name": "Static Cold Storage"}
        }
    }
    (project_dir / "protocol.yaml").write_text(json.dumps(protocol_content), encoding="utf-8")
    
    # Create screening directory and queue
    screening_dir = project_dir / "screening"
    screening_dir.mkdir(parents=True, exist_ok=True)
    
    queue_records = [
        {
            "record_id": "STUDY-TEST-001",
            "title": "A multicenter randomized controlled trial of hypothermic oxygenated machine perfusion in liver transplantation",
            "abstract": "We randomized 150 human adult liver transplant recipients to HOPE versus static cold storage. Early allograft dysfunction occurred in 15% vs 35% (P < 0.01).",
            "authors": ["van Rijn, R.", "Schlegel, A."],
            "journal": "N Engl J Med",
            "year": "2021",
            "doi": "10.1056/nejm.test.001",
            "pmid": "12345671"
        },
        {
            "record_id": "STUDY-TEST-002",
            "title": "Evaluation of mitochondrial respiration in a rat liver perfusion model",
            "abstract": "Male Wistar rats were sacrificed and livers perfused ex-vivo with cold solution to assess ATP depletion in hepatocytes.",
            "authors": ["Muller, X."],
            "journal": "J Surg Res",
            "year": "2020",
            "doi": "10.1016/j.jss.test.002",
            "pmid": "12345672"
        },
        {
            "record_id": "STUDY-TEST-003",
            "title": "Machine perfusion in liver transplantation: a comprehensive narrative review of the literature",
            "abstract": "In this review, we summarize the molecular biology and historical evolution of liver preservation.",
            "authors": ["Dutkowski, P."],
            "journal": "Transplantation",
            "year": "2022",
            "doi": "10.1097/tpa.test.003",
            "pmid": "12345673"
        },
        {
            "record_id": "STUDY-TEST-004",
            "title": "Preliminary experience with normothermic machine perfusion: a single-center case series of 5 patients",
            "abstract": "We report our first 5 clinical cases using normothermic machine perfusion without a control group.",
            "authors": ["Watson, C."],
            "journal": "Clin Transplant",
            "year": "2019",
            "doi": "10.1111/ctr.test.004",
            "pmid": "12345674"
        },
        {
            "record_id": "STUDY-TEST-005",
            "title": "Study protocol for a randomized controlled trial comparing HOPE vs SCS in liver transplantation",
            "abstract": "This article outlines the design, inclusion criteria and primary endpoints for our upcoming trial.",
            "authors": ["Czigany, Z."],
            "journal": "Trials",
            "year": "2023",
            "doi": "10.1186/trials.test.005",
            "pmid": "12345675"
        }
    ]
    
    queue_path = screening_dir / "title_abstract_queue.jsonl"
    queue_path.write_text("".join(json.dumps(r) + "\n" for r in queue_records), encoding="utf-8")
    
    return project_dir


def test_triple_reviewer_screening_engine(mock_screening_project: Path):
    """Test that TripleReviewerScreeningEngine enforces dual-blind + senior arbiter consensus and Rayyan output."""
    engine = TripleReviewerScreeningEngine(mock_screening_project)
    result = engine.run_screening()
    
    assert result["status"] == "pass"
    assert result["total_records_screened"] == 5
    assert result["included"] == 1  # Only STUDY-TEST-001 (RCT)
    assert result["excluded"] == 4  # Rat (animal), review, single-arm, protocol
    
    # 1. Verify Rayyan CSV
    rayyan_path = mock_screening_project / "screening" / "rayyan_screening_export.csv"
    assert rayyan_path.is_file()
    rayyan_content = rayyan_path.read_text(encoding="utf-8-sig")
    assert "RAYYAN-INCLUSION:" in rayyan_content
    assert "RAYYAN-EXCLUSION-REASONS:" in rayyan_content
    assert "Tier-1_RCT" in rayyan_content
    assert "STUDY-TEST-001" in rayyan_content
    
    # 2. Verify Multi-Agent Ledger
    ledger_path = mock_screening_project / "screening" / "multi_agent_screening_ledger.jsonl"
    assert ledger_path.is_file()
    ledger_records = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line]
    assert len(ledger_records) == 5
    
    # Verify evaluations for STUDY-TEST-001
    rct_eval = next(r for r in ledger_records if r["record_id"] == "STUDY-TEST-001")
    assert rct_eval["final_decision"] == "include"
    assert rct_eval["study_design_tier"] == "Tier-1_RCT"
    assert rct_eval["evaluations"]["reviewer_1_clinical"]["decision"] == "include"
    assert rct_eval["evaluations"]["reviewer_2_methodologist"]["decision"] == "include"
    assert rct_eval["evaluations"]["reviewer_3_senior_arbiter"]["final_decision"] == "include"
    
    # Verify evaluations for STUDY-TEST-002 (Animal)
    animal_eval = next(r for r in ledger_records if r["record_id"] == "STUDY-TEST-002")
    assert animal_eval["final_decision"] == "exclude"
    assert animal_eval["exclusion_reason"] == "EXCL_ANIMAL_PRECLINICAL"
    
    # 3. Verify Consensus Matrix
    matrix_path = mock_screening_project / "screening" / "screening_consensus_matrix.json"
    assert matrix_path.is_file()
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    assert matrix["total_records"] == 5
    assert matrix["unanimous_include"] == 1
    
    # 4. Verify PRISMA Checklists
    prisma_2020_path = mock_screening_project / "evidence" / "prisma" / "tabela_checklist_prisma_2020.md"
    prisma_nma_path = mock_screening_project / "evidence" / "prisma" / "tabela_checklist_prisma_nma.md"
    assert prisma_2020_path.is_file()
    assert prisma_nma_path.is_file()
    assert "PRISMA 2020" in prisma_2020_path.read_text(encoding="utf-8")
    assert "PRISMA-NMA" in prisma_nma_path.read_text(encoding="utf-8")


def test_cli_corpus_screen_and_checklist(mock_screening_project: Path):
    """Test the CLI commands article-machine corpus screen and article-machine methodology prisma-checklist."""
    # 1. Run corpus screen
    screen_code = main(["corpus", "screen", str(mock_screening_project)])
    assert screen_code == 0
    
    # 2. Run prisma checklist
    checklist_code = main(["methodology", "prisma-checklist", str(mock_screening_project)])
    assert checklist_code == 0
