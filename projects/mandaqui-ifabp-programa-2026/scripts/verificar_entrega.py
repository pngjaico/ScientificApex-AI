"""Validate planning delivery and software metadata without clinical execution."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import yaml
from article_machine.agent_skills import audit_workspace_skills, route_workspace_skills


def main():
    pairs = []
    directory = PROJECT / 'context/planejamento'
    portuguese = {p.name for p in (directory / 'portugues').glob('*.md')}
    english = {p.name for p in (directory / 'ingles').glob('*.md')}
    assert portuguese == english, (portuguese, english)
    for name in sorted(portuguese):
        pt = (directory / 'portugues' / name).read_text(encoding='utf-8')
        en = (directory / 'ingles' / name).read_text(encoding='utf-8')
        pt_ids = re.findall(r'^\| (C\d{2}) \|', pt, re.M)
        en_ids = re.findall(r'^\| (C\d{2}) \|', en, re.M)
        assert pt_ids == en_ids, name
        if name == 'carteira_de_30_estudos.md':
            assert pt_ids == [f'C{i:02d}' for i in range(1, 31)]
        pairs.append({'name': name, 'portfolio_rows': len(pt_ids), 'pt_sha256': hashlib.sha256(pt.encode()).hexdigest(), 'en_sha256': hashlib.sha256(en.encode()).hexdigest()})
    project = yaml.safe_load((PROJECT / 'project.yaml').read_text(encoding='utf-8'))
    protocol = yaml.safe_load((PROJECT / 'protocol.yaml').read_text(encoding='utf-8'))
    assert project['state']['current_mode'] == 'bootstrap'
    assert protocol['status'] == 'draft'
    assert protocol['registration']['required'] is True
    assert protocol['registration']['status'] == 'pending'
    assert not protocol['registration']['registry_id']
    assert (PROJECT / 'evidence/claim_map.jsonl').stat().st_size == 0
    assert not (PROJECT / 'sources/registry.jsonl').exists()
    route = route_workspace_skills('FAPESP CNPq bolsa de mestrado doutorado')
    assert 'fapesp-cnpq-projects' in {entry['skill'] for entry in route['selected_skills']}
    audit = audit_workspace_skills(strict=True, provenance=True)
    assert audit['status'] == 'pass', audit['issues']
    link = ROOT / '.agents/skills/fapesp-cnpq-projects'
    assert link.resolve() == (ROOT / 'skills/fapesp-cnpq-projects').resolve()
    report = {'status': 'pass-local-planning-checks', 'generated_at': datetime.now(timezone.utc).isoformat(), 'canonical_workspace': str(ROOT), 'pairs': pairs, 'portfolio_candidates': 30, 'main_degrees': 2, 'sources_promoted_to_formal_corpus': 0, 'clinical_data_processed': False, 'claims_promoted': 0, 'registration': 'pending', 'scientific_execution': 'blocked-until-verified-registration', 'skills_audit': audit['status'], 'skill_count': audit['provenance']['checked_skill_count'], 'limitations': ['Structural checks and prior independent planning critique do not approve scientific merit, novelty, sample size, ethics or funding.', 'Bilingual numeric audit of the two main documents is separate; lexical equivalence is not semantic proof.']}
    output = PROJECT / 'reviews/verificacao_entrega.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'pairs'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
