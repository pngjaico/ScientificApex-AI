from pathlib import Path
import tomllib


WORKSPACE = Path(__file__).resolve().parents[1]
CODEX_DIR = WORKSPACE / ".codex"


def _read_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def test_project_codex_config_uses_sol_medium_and_bounded_luna_delegation() -> None:
    config = _read_toml(CODEX_DIR / "config.toml")
    agents = config["agents"]

    assert agents["enabled"] is True
    assert agents["max_concurrent_threads_per_session"] == 3
    assert agents["default_subagent_model"] == "gpt-6-luna"
    assert agents["default_subagent_reasoning_effort"] == "medium"
    assert config["model"] == "gpt-6.1-sol"
    assert config["model_reasoning_effort"] == "medium"
    assert config["service_tier"] == "standard"
    assert config["mcp_servers"]["openaiDeveloperDocs"]["url"] == "https://developers.openai.com/mcp"


def test_custom_agents_are_narrow_read_only_roles() -> None:
    expected = {
        "workspace-explorer.toml": ("workspace_explorer", "gpt-6-luna", "low"),
        "scientific-reviewer.toml": ("scientific_reviewer", "gpt-6.1-sol", "high"),
        "verification-runner.toml": ("verification_runner", "gpt-6-luna", "medium"),
    }

    for filename, (name, model, effort) in expected.items():
        agent = _read_toml(CODEX_DIR / "agents" / filename)
        assert agent["name"] == name
        assert agent["model"] == model
        assert agent["model_reasoning_effort"] == effort
        assert agent["sandbox_mode"] == "read-only"
        assert agent["description"].strip()
        assert agent["developer_instructions"].strip()


def test_user_benchmark_profiles_are_read_only_and_explicit() -> None:
    expected = {
        "xhigh-baseline.config.toml": "xhigh",
        "ultra-benchmark.config.toml": "ultra",
    }

    for filename, effort in expected.items():
        profile = _read_toml(CODEX_DIR / "profiles" / filename)
        assert profile["model"] == "gpt-5.6-sol"
        assert profile["model_reasoning_effort"] == effort
        assert profile["sandbox_mode"] == "read-only"
