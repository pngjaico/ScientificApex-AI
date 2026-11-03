"""Read-only checks of existing manuscript artifacts; writes only this audit bundle."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

datasets = {}
for name in ['primary_psg_dataset.csv', 'sensitivity_all_pico_dataset.csv', 'corrected_extraction.csv']:
    path = ROOT / 'analysis' / name
    with path.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    datasets[name] = {
        'rows': len(rows), 'unique_dois': len({r['DOI'] for r in rows}),
        'participants': sum(int(r['Total N Arm']) for r in rows),
        'events': sum(int(r['Events (OSA)']) for r in rows),
        'dois': sorted({r['DOI'] for r in rows}), 'sha256': digest(path),
    }

documents = []
folder = ROOT / 'publicacoes/journal-of-craniofacial-surgery/v01/09_submissao'
for path in sorted(folder.rglob('*.docx')):
    with ZipFile(path) as archive:
        tree = ET.fromstring(archive.read('word/document.xml'))
        paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', NS))
                      for p in tree.findall('.//w:p', NS)]
        text = '\n'.join(paragraphs)
        probes = ['6 to 12', '6 a 12', '1.5', '09-082', '09-178', 'Claude Opus 5.5',
                  '4- to 8-fold', '4 to 8', '10 studies (20 surgical arms',
                  'ausência', 'apenas 10', 'Colombia', 'Colômbia', 'single center']
        documents.append({
            'path': str(path.relative_to(ROOT)), 'sha256': digest(path),
            'paragraphs': len(paragraphs), 'tables': len(tree.findall('.//w:tbl', NS)),
            'embedded_images': len([n for n in archive.namelist() if n.startswith('word/media/')]),
            'replacement_characters': text.count('\ufffd'),
            'probe_locations': {s: [i for i, t in enumerate(paragraphs, 1) if s in t] for s in probes},
        })

inputs = ['drafts/ingles/manuscrito_completo.md', 'reviews/red_team_hostile_review_jcs.md',
          'scripts/gerar_analises_e_figuras_publicacao.R', 'scripts/build_submission_docx_jcs.py',
          'analysis/r_metaprop_summary.txt', 'analysis/table3_grade_sof_certainty_en.csv',
          'evidence/claim_map.jsonl', 'drafts/references.bib', 'protocol.yaml',
          'publicacoes/journal-of-craniofacial-surgery/v01/07_manuscrito/ingles/manuscript_journal_of_craniofacial_surgery_en.md',
          'publicacoes/journal-of-craniofacial-surgery/v01/07_manuscrito/ingles/manuscript_jcs_gdocs_en.md',
          'publicacoes/journal-of-craniofacial-surgery/v01/07_manuscrito/portugues/pacote_orientador_gdocs_pt.md']
report = {'review_date': '2026-11-03', 'scope': 'Internal author-requested artifact integrity review',
          'datasets': datasets, 'docx': documents,
          'input_sha256': {name: digest(ROOT / name) for name in inputs},
          'limits': ['No source-data re-extraction or meta-analysis rerun',
                     'DOCX XML inspection, not rendered layout QA',
                     'Google Docs live content not inspected',
                     'DOI counts identify reports, not proven independent cohorts']}
(OUT / 'verificacao_local.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({'datasets': datasets, 'docx_count': len(documents), 'output': str(OUT / 'verificacao_local.json')}, ensure_ascii=False))
