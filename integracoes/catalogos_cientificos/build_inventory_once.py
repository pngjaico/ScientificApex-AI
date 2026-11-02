import json,re,subprocess,pathlib,configparser
root=pathlib.Path.cwd(); base=root/'integracoes/catalogos_cientificos'
meta={
'kdense':('K-Dense-AI','scientific-agent-skills','a25cf9ec00e2745d03f8704acf6f6919694ccd9a','2026-11-02T09:23:26Z','MIT repo LICENSE.md; each skill metadata/embedded assets can override','LICENSE.md'),
'denden':('DenDen047','claude-scientific-skills','190b4f0a5fdf2d3a7feae8e99505fcb92cb5faf1','2026-04-02T09:15:42+09:00','MIT repo LICENSE.md; individual skills and four Anthropic document terms require per-skill review','LICENSE.md'),
'orchestra':('Orchestra-Research','AI-research-SKILLs','773a52944ba4747a18bd4ae9ade53fff041adcbc','2026-06-15T21:36:40-04:00','MIT repo LICENSE','LICENSE'),
'imbad':('Imbad0202','academic-research-skills','2e02041a3b821a160d98c9398f173c484ac759a8','2026-11-02T15:27:50+08:00','CC BY-NC 4.0; non-commercial condition limits reuse','LICENSE'),
'internscience':('InternScience','Awesome-Scientific-Skills','e67760e2081508773a59398f72bf808f3ac3217c','2026-08-13T17:28:38+08:00','MIT applies to curated list; linked projects keep their own licenses','LICENSE')}
canonical={p.parent.name.casefold() for p in (root/'skills').glob('*/SKILL.md')}
def cmd(r,*a): return subprocess.run(['git','-C',str(r),*a],capture_output=True,text=True,encoding='utf8',errors='replace',check=True).stdout
manifest={'snapshot_utc':'2026-11-02','scope':'Tree-level inventory of all five requested repositories; selected-content spot audit is documented in source_audit.md. No upstream scripts, hooks, installers, lifecycle commands, or npx executed.','method':'git ls-remote HEAD/default-branch and depth-1 partial clones; tree paths, commit SHAs, dates and submodule gitlinks recorded. Unselected SKILL.md bodies are not claimed reviewed.','local_canonical_skill_count':len(canonical),'sources':[]}
inventory={'snapshot_utc':'2026-11-02','local_canonical_skill_count':len(canonical),'sources':[]}
for rid,(owner,repo,sha,date,license_note,license_path) in meta.items():
 path=base/rid
 # use kdense shallow partial clone; redundant no-checkout ref clone preserved as evidence of pinned commit
 if rid=='kdense' and not (path/'.git').exists(): path=base/'kdense_reference'
 tree=cmd(path,'ls-tree','-r','--full-tree','HEAD')
 files=[]; gitlinks=[]
 for line in tree.splitlines():
  mat=re.match(r'^(\d+) (\w+) ([0-9a-f]+)\t(.*)$',line)
  if not mat:continue
  mode,typ,oid,f=mat.groups();files.append(f)
  if typ=='commit':gitlinks.append({'path':f,'commit':oid})
 skillpaths=[f for f in files if pathlib.PurePosixPath(f).name.casefold()=='skill.md']
 names=[{'name':pathlib.PurePosixPath(f).parent.name,'path':f,'metadata_status':'tree_only'} for f in skillpaths]
 overlap=sorted({pathlib.PurePosixPath(f).parent.name for f in skillpaths if pathlib.PurePosixPath(f).parent.name.casefold() in canonical},key=str.casefold)
 licenses=sorted(f for f in files if pathlib.PurePosixPath(f).name.casefold().startswith(('license','licence')))
 headsubject=cmd(path,'log','-1','--format=%s','HEAD').strip()
 selected={
 'kdense':['skills/statistical-analysis/SKILL.md','skills/clinical-reports/SKILL.md','skills/scientific-writing/SKILL.md','skills/pytorch-lightning/SKILL.md','skills/uncertainty-and-units/SKILL.md','skills/analytical-method-validation/SKILL.md','skills/pkpd-modeling/SKILL.md'],
 'denden':['scientific-skills/statistical-analysis/SKILL.md'],
 'orchestra':['0-autoresearch-skill/SKILL.md','20-ml-paper-writing/ml-paper-writing/SKILL.md','22-agent-native-research-artifact/rigor-reviewer/SKILL.md'],
 'imbad':['academic-paper-reviewer/SKILL.md','academic-paper/SKILL.md','academic-pipeline/SKILL.md'],
 'internscience':[]}[rid]
 for item in names:
  if item['path'] in selected:item['metadata_status']='frontmatter_read_selected_spot_audit'
 source={'id':rid,'repository':f'{owner}/{repo}','official_url':f'https://github.com/{owner}/{repo}','default_branch_observed':'main','head_sha':sha,'observed_commit_date':date,'observed_head_subject':headsubject,'tree_path_count':len(files),'actual_skill_md_entrypoints':len(skillpaths),'local_exact_slug_overlap_count':len(overlap),'local_exact_slug_overlap':overlap,'license_assessment':license_note,'license_paths':licenses,'skill_entries_with_frontmatter_spot_checked':len(selected),'remaining_skill_bodies_unreviewed':len(skillpaths)-len(selected),'tree_only_names_and_paths':names,'gitlink_count':len(gitlinks),'gitlinks':gitlinks}
 if rid=='internscience':
  gm=cmd(path,'show','HEAD:.gitmodules'); c=configparser.ConfigParser();c.read_string(gm)
  url_by={c[s].get('path'):c[s].get('url') for s in c.sections()}
  for g in gitlinks:g['upstream_url']=url_by.get(g['path'])
 manifest['sources'].append(source)
 inventory['sources'].append({'source_id':rid,'repository':source['repository'],'pinned_sha':sha,'entrypoint_count':len(skillpaths),'entries':names,'pinned_submodules':gitlinks if rid=='internscience' else []})
(base/'manifesto_das_fontes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(base/'inventario_de_habilidades.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for s in manifest['sources']:
 print(f"{s['id']}: entrypoints={s['actual_skill_md_entrypoints']} paths={s['tree_path_count']} exact-overlap={s['local_exact_slug_overlap_count']} gitlinks={s['gitlink_count']}")
