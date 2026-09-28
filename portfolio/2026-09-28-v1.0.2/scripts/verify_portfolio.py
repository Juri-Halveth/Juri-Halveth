"""Read-only structure, evidence, local-link and byte-manifest verifier for this portfolio."""
from pathlib import Path, PurePosixPath
import hashlib
import importlib.util
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    errors=[]
    ev=[json.loads(x) for x in (ROOT/'machine/evidence.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    rel=[json.loads(x) for x in (ROOT/'machine/relations.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    benchmarks=load('machine/credential-benchmarks.json')
    definition=load('machine/claim-definition.json')
    if definition.get('authority_effect')!='NONE':errors.append('Definition grants authority')
    eids={e['id']:e for e in ev}; bids={b['id']:b for b in benchmarks}
    if len(eids)!=len(ev) or len(bids)!=len(benchmarks):errors.append('Duplicate evidence/benchmark IDs')
    for e in ev:
        value={k:v for k,v in e.items() if k!='record_digest'}
        if e['record_digest']!='sha256:'+sha(canonical(value)):errors.append('Evidence digest '+e['id'])
        if not e['claim'] or not e['evidence_state'] or not e['origin']:errors.append('Missing evidence binding '+e['id'])
        if e['authority_effect']!='NONE':errors.append('Unexpected authority '+e['id'])
        if not set(e['benchmark_refs'])<=bids.keys():errors.append('Unknown benchmark '+e['id'])
    expected={(e['id'],b) for e in ev for b in e['benchmark_refs']}
    actual=set()
    for r in rel:
        l=r['left'];rt=r['right'];actual.add((l['id'],rt['id']))
        if l['id'] not in eids or rt['id'] not in bids:errors.append('Unknown relation endpoint');continue
        if l['digest']!=eids[l['id']]['record_digest']:errors.append('Left digest '+r['id'])
        if rt['digest']!='sha256:'+sha(canonical(bids[rt['id']])):errors.append('Right digest '+r['id'])
        if r['authority_effect']!='NONE':errors.append('Relation authority '+r['id'])
    if actual!=expected or len(actual)!=len(rel):errors.append('Relation closure mismatch')
    for b in benchmarks:
        pc=b.get('portfolio_claim',{})
        if pc.get('status')!='CLAIMED' or pc.get('filing_status')!='ZDA':errors.append('Portfolio claim missing '+b['id'])
        if pc.get('definition_id')!=definition['definition_id'] or pc.get('definition_digest')!='sha256:'+sha(canonical(definition)):errors.append('Claim definition mismatch '+b['id'])
        if pc.get('claim_type')!='PORTFOLIO_BENCHMARK_CLAIM' or pc.get('authority_effect')!='NONE':errors.append('Claim type or authority mismatch '+b['id'])
        if not set(b['evidence_refs'])<=eids.keys():errors.append('Unknown evidence '+b['id'])
        if b['credential_status']!='ISSUER_AWARD_NOT_VERIFIED_IN_REVIEWED_MATERIAL':errors.append('Unexpected credential state '+b['id'])
        if set(b['evidence_refs'])!={e['id'] for e in ev if b['id'] in e['benchmark_refs']}:errors.append('Mapping mismatch '+b['id'])
    snapshots=load('machine/repository-snapshots.json')
    if any(r['visibility']!='PUBLIC' for r in snapshots['repositories']):errors.append('Nonpublic repository')
    if snapshots['private_entries_exported']!=0:errors.append('Private entries exported')
    links=0
    for f in ROOT.rglob('*.md'):
        text=f.read_text(encoding='utf-8')
        for url in re.findall(r'\]\(([^\n]+?)\)',text):
            url=url.strip('<>');parts=urlsplit(url)
            if parts.scheme or not parts.path:continue
            target=(f.parent/unquote(parts.path)).resolve()
            if not target.is_relative_to(ROOT):errors.append('Link leaves package '+str(f.relative_to(ROOT)))
            elif not target.exists():errors.append('Missing link '+str(f.relative_to(ROOT))+': '+url)
            links+=1
    for f in ROOT.rglob('*'):
        if f.is_file() and f.suffix.lower() in {'.md','.json','.jsonl','.svg','.txt'}:
            t=f.read_text(encoding='utf-8')
            # Obvious local-source leakage; this is not a substitute for editorial review.
            if re.search(r'C:[\\/]Users[\\/]|AppData[\\/]|\.myshopify\.com|ghp_[A-Za-z0-9]{20,}',t,re.I):errors.append('Private locator/token pattern '+str(f.relative_to(ROOT)))
    spec=importlib.util.spec_from_file_location('finite_model',ROOT/'examples/branch_models.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    example=module.self_check()
    manifest=ROOT/'SHA256SUMS.txt';checked=0
    if not manifest.exists():errors.append('Manifest missing')
    else:
        seen=set()
        for line in manifest.read_text(encoding='utf-8').splitlines():
            h,p=line.split('  ',1);pp=PurePosixPath(p)
            if pp.is_absolute() or '..' in pp.parts or p in seen:errors.append('Invalid manifest path');continue
            seen.add(p);fp=ROOT.joinpath(*pp.parts)
            if not fp.is_file() or sha(fp.read_bytes())!=h:errors.append('Manifest mismatch '+p)
            checked+=1
        files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt' and p.relative_to(ROOT).as_posix() not in {'machine/validation.json','machine/publication-receipt.json'}}
        if files!=seen:errors.append('Manifest coverage mismatch')
    result={'schema':'halveth.portfolio.validation.v1','valid':not errors,'evidence_records':len(ev),'benchmark_records':len(benchmarks),
            'relation_records':len(rel),'public_repositories':len(snapshots['repositories']),'local_links_checked':links,
            'manifest_files_checked':checked,'example_checks':example,'errors':errors,
            'claim_ceiling':'File structure, linked records and manifest bytes only; not factual or issuer validation'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not errors else 1

if __name__=='__main__':
    sys.dont_write_bytecode=True
    raise SystemExit(main())
