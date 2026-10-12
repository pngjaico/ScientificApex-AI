from __future__ import annotations

import json
from pathlib import Path

import pytest

from article_machine.services.skill_registry import audit_skill_provenance, resolve_plugin_binding, tree_hash


def test_registry_covers_every_installed_skill_and_tooluniverse_is_held() -> None:
    root = Path(__file__).resolve().parents[1]
    registry = json.loads((root / "skills" / "registry.json").read_text(encoding="utf-8"))
    installed = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}

    assert registry["schema_version"] == 1
    assert installed <= set(registry["skills"])
    assert {name for name, entry in registry["skills"].items() if entry.get("required_for_clone")} <= installed
    tooluniverse = {name: entry for name, entry in registry["skills"].items() if name.startswith("tooluniverse-")}
    assert len(tooluniverse) == 14
    assert all(entry["status"] == "hold" for entry in tooluniverse.values())
    source = json.loads((root / registry["skills"]["research-lookup"]["sync_manifest"]).read_text(encoding="utf-8"))
    assert registry["skills"]["research-lookup"]["pinned_revision"] == source["revision"]
    assert registry["skills"]["research-lookup"]["license"] == source["license"]


def test_registry_tree_hash_is_complete_and_strict_provenance_audits_cleanly() -> None:
    root = Path(__file__).resolve().parents[1]
    registry = json.loads((root / "skills" / "registry.json").read_text(encoding="utf-8"))
    entry = registry["skills"]["zotero-reference-manager"]
    assert entry["tree_hash"] == tree_hash(root / "skills" / "zotero-reference-manager")
    report = audit_skill_provenance(root / "skills", root=root, strict=True)
    assert report["status"] == "pass", report["issues"]
    assert report["checked_skill_count"] == len(list((root / "skills").glob("*/SKILL.md")))


def test_tree_hash_is_portable_and_excludes_nested_caches(tmp_path: Path) -> None:
    skill = tmp_path / "skill"
    skill.mkdir()
    text = skill / "SKILL.md"
    text.write_bytes(b"first\r\nsecond\r\n")
    original = tree_hash(skill)
    text.write_bytes(b"first\nsecond\n")
    cache = skill / "scripts" / "__pycache__"
    cache.mkdir(parents=True)
    (cache / "test.pyc").write_bytes(b"transient")
    assert tree_hash(skill) == original


def test_plugin_binding_requires_exactly_one_existing_root(tmp_path: Path) -> None:
    root = tmp_path
    (root / ".machine").mkdir()
    plugin_root = root / "plugins" / "zotero"
    plugin_root.mkdir(parents=True)
    (root / ".machine" / "plugin_bindings.json").write_text(
        json.dumps({"bindings": {"zotero": [{"version": "0.1.2", "root": str(plugin_root)}]}}), encoding="utf-8"
    )
    assert resolve_plugin_binding("zotero", root)["version"] == "0.1.2"
    (root / ".machine" / "plugin_bindings.json").write_text(json.dumps({"bindings": {"zotero": []}}), encoding="utf-8")
    with pytest.raises(ValueError, match="exactly one"):
        resolve_plugin_binding("zotero", root)
