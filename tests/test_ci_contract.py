from pathlib import Path
import re


WORKFLOW = Path(__file__).parents[1] / ".github" / "workflows" / "quality-gate.yml"


def test_quality_gate_covers_clean_checkout_contract() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    required_fragments = (
        "runs-on: windows-2025",
        'python-version: "3.13"',
        'version: "0.11.31"',
        "uv sync --locked --all-extras --dev --python 3.13",
        "validate_operational_graph",
        "uv run --no-sync python -m pytest",
        "machine audit --workspace-root . --strict",
        "if: ${{ !cancelled() }}",
        "git diff --check",
        "git diff --exit-code",
    )
    for fragment in required_fragments:
        assert fragment in text

    assert "continue-on-error" not in text
    assert "pull_request_target" not in text
    assert "secrets." not in text

    pytest_position = text.index("uv run --no-sync python -m pytest")
    strict_position = text.index("machine audit --workspace-root . --strict")
    drift_position = text.index("git diff --check")
    assert pytest_position < strict_position < drift_position


def test_quality_gate_pins_third_party_actions_to_full_commit_shas() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    action_refs = re.findall(r"^\s*uses:\s*[^\s@]+@([^\s#]+)", text, flags=re.MULTILINE)

    assert len(action_refs) == 3
    assert all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in action_refs)
