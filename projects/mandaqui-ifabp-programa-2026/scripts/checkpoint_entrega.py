"""Write a scoped handoff and commit only this delivery's explicit paths."""
from datetime import datetime
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def main():
    if git('diff', '--cached', '--name-only'):
        raise RuntimeError('An existing staged change was found; preserve it and stop the checkpoint.')
    state_path = ROOT / '.machine/handoff_sessao.json'
    history_path = ROOT / 'docs/HANDOFF_ENTRE_AGENTES.md'
    backup = PROJECT / 'context/migracao/backup_handoff_final'
    if backup.exists():
        raise RuntimeError('Final handoff backup already exists; refusing overwrite/repeated checkpoint.')
    backup.mkdir(parents=True)
    for path in [state_path, history_path]:
        (backup / path.name).write_bytes(path.read_bytes())
    stamp = datetime.now().astimezone().isoformat()
    state = json.loads(state_path.read_text(encoding='utf-8'))
    state.update(updated_at=stamp, active_project='projects/mandaqui-ifabp-programa-2026', current_mode='bootstrap')
    state['last_session'] = {'agent': 'Codex', 'timestamp': stamp, 'summary': 'Preparacao em D: de programa I-FABP Mandaqui: doutorado, mestrado e 30 candidatas P/C/I; pares PT/EN, critica independente, skill FAPESP/CNPq copiada e integrada com hashes/backups. Registro pendente; sem corpus formal, dados humanos ou submissao.', 'tests_status': '417 passed, 1 skipped', 'machine_audit': 'Skill provenance pass; final strict machine audit follows scoped checkpoint', 'scientific_readiness': 'Planning only; execution blocked pending frozen protocol and verified final registration', 'branch': git('branch', '--show-current'), 'git_commit': 'see scoped checkpoint commit'}
    state['next_recommended_actions'] = ['Obter fluxo agregado autorizado, eventos e compromissos locais.', 'Dimensionar os estimandos, concluir protocolo e registro final verificado.', 'Nao executar corpus/analise clinica nem prometer publicacoes antes dos gates.']
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    history = history_path.read_text(encoding='utf-8')
    history += '\n\n### [2026-11-03] Handoff: Codex -> proxima sessao\n- Projeto ativo: `projects/mandaqui-ifabp-programa-2026`, raiz canonica D:.\n- Modo: bootstrap, preparacao de protocolos; registro pending.\n- Entrega: programa de doutorado/mestrado e carteira C01-C30 classificada P/C/I, com pares PT/EN e revisao critica. Skill FAPESP/CNPq preservada e integrada em D:.\n- Verificacao: 417 passed, 1 skipped; auditoria de proveniencia das 269 skills PASS; auditar maquina apos checkpoint.\n- Limite: corpus-build BLOCK esperado; nenhum corpus formal/dado humano/resultado clinico/submissao.\n- Proximo passo: viabilidade local, laboratorio/custos, estimandos e registro final.\n- Arquivos externos ao escopo e originais de C: preservados; nao declarar worktree global limpo.\n'
    history_path.write_text(history, encoding='utf-8')
    root_files = ['article_machine/agent_skills.py', 'scripts/generate_skill_registry.py', 'scripts/publish_workspace_skills.py', 'skills/registry.json', 'SKILL_INDEX.md', 'SKILLS_CANON.md', 'AGENT_MANIFEST.md', 'graphify-out/GRAPH_REPORT.md', 'graphify-out/graph.json', 'graphify-out/graph.html', '.machine/handoff_sessao.json', 'docs/HANDOFF_ENTRE_AGENTES.md', 'tests/test_fapesp_cnpq_skill.py']
    paths = [ROOT / item for item in root_files]
    for folder in [ROOT / 'skills/fapesp-cnpq-projects', PROJECT]:
        for path in folder.rglob('*'):
            if not path.is_file() or path.suffix.lower() not in {'.md', '.json', '.jsonl', '.yaml', '.yml', '.py', '.csv', '.bib'}:
                continue
            relative = path.relative_to(folder)
            if '__pycache__' in relative.parts or any(part.startswith('backup_') for part in relative.parts):
                continue
            paths.append(path)
    paths = sorted(set(paths))
    for path in paths:
        assert path.resolve().is_relative_to(ROOT.resolve()), path
        assert path.name != '.env'
    manifest = PROJECT / 'context/migracao/manifesto_checkpoint.json'
    manifest.write_text(json.dumps({'generated_at': stamp, 'parent_commit': git('rev-parse', 'HEAD'), 'preservation': 'Only explicit task paths; no raw data, secrets, control backups or unrelated untracked files.', 'files': [{'path': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths]}, ensure_ascii=False, indent=2), encoding='utf-8')
    paths.append(manifest)
    subprocess.run(['git', 'add', '-f', '--', *[path.relative_to(ROOT).as_posix() for path in paths]], cwd=ROOT, check=True)
    staged = set(git('diff', '--cached', '--name-only').splitlines())
    allowed = {path.relative_to(ROOT).as_posix() for path in paths}
    assert staged <= allowed, staged - allowed
    subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', 'handoff(Codex): planejar programa IFABP Mandaqui e integrar skill FAPESP em D'], cwd=ROOT, check=True)
    print(json.dumps({'status': 'scoped-checkpoint-created', 'commit': git('rev-parse', 'HEAD'), 'staged_paths': len(staged)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
