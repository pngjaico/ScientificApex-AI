"""Copy only this chat's new skill and planning inputs; preserve both workspaces."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

SOURCE = Path('C:/Users/Usuario-pc/Desktop/Doutorado')
TARGET = Path('D:/Usuario-pc/Projetos/Doutorado')
PROJECT = TARGET / 'projects/mandaqui-ifabp-programa-2026'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    pairs = []
    skill = SOURCE / 'skills/fapesp-cnpq-projects'
    destination = TARGET / 'skills/fapesp-cnpq-projects'
    for source in sorted(skill.rglob('*')):
        if source.is_file() and '__pycache__' not in source.parts and source.suffix not in {'.pyc', '.pyo'}:
            pairs.append((source, destination / source.relative_to(skill)))
    pairs.append((SOURCE / 'tests/test_fapesp_cnpq_skill.py', TARGET / 'tests/test_fapesp_cnpq_skill.py'))
    # Only hypotheses and planning scores, not abstracts, patients, claims, corpus or manuscript.
    pairs.append((SOURCE / 'projects/mandaqui-ifabp-research-line-2026/context/ideas/idea_candidates.json', PROJECT / 'context/ideas/idea_candidates.json'))
    entries = []
    for source, dest in pairs:
        assert dest.resolve().is_relative_to(TARGET.resolve())
        if dest.exists() and sha(dest) != sha(source):
            raise RuntimeError(f'Conflicting existing destination preserved: {dest}')
        entries.append({'source': str(source), 'destination': str(dest), 'sha256': sha(source), 'action': 'copy-new-or-verify-identical', 'rollback': 'Original in C remains unchanged; no deletion needed.'})
    record = PROJECT / 'context/migracao/manifesto_copia.json'
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps({'generated_at': datetime.now(timezone.utc).isoformat(), 'authorization': 'User explicitly directed current work to canonical D workspace', 'scope': 'new skill, software test, planning hypotheses only; no raw clinical data or formal scientific corpus', 'files': entries}, ensure_ascii=False, indent=2), encoding='utf-8')
    # Manifest precedes mutation; no existing differing file is overwritten.
    for source, dest in pairs:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.copy2(source, dest)
        assert sha(source) == sha(dest)
    controls = ['article_machine/agent_skills.py', 'scripts/generate_skill_registry.py', 'scripts/publish_workspace_skills.py', 'skills/registry.json', 'SKILL_INDEX.md', 'SKILLS_CANON.md', 'AGENT_MANIFEST.md', '.machine/handoff_sessao.json', 'docs/HANDOFF_ENTRE_AGENTES.md']
    backups = []
    for relative in controls:
        source = TARGET / relative
        if not source.is_file():
            continue
        dest = PROJECT / 'context/migracao/backup_controle' / relative
        if dest.exists():
            raise RuntimeError(f'Backup already exists; refusing to overwrite: {dest}')
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        backups.append({'path': relative, 'sha256_before': sha(source), 'backup': str(dest.relative_to(PROJECT))})
    (record.parent / 'manifesto_backups.json').write_text(json.dumps(backups, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': 'copied-and-hash-verified', 'new_files': len(entries), 'backups': len(backups)}))


if __name__ == '__main__':
    main()
