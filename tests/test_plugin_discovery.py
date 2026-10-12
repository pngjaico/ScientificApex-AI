from pathlib import Path

import pytest

from article_machine.services.plugins import discover_plugin_candidates, resolve_scientific_plugin


def test_discovery_handles_remote_cache_and_does_not_choose_ambiguous_versions(tmp_path: Path, monkeypatch) -> None:
    cache = tmp_path / "plugins" / "cache"
    package = cache / "openai-curated-remote" / "example" / "1.0"
    (package / "skills").mkdir(parents=True)
    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    assert discover_plugin_candidates("example") == [package]
    assert resolve_scientific_plugin("example", tmp_path) == package
    (package.parent / "2.0" / "skills").mkdir(parents=True)
    with pytest.raises(ValueError, match="explicit binding"):
        resolve_scientific_plugin("example", tmp_path)
