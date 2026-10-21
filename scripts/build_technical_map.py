"""Render the source-bound interface map in three languages, without network access."""
from pathlib import Path
import argparse
import json
import re
import hashlib
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
LANGS = ('de', 'en', 'ru')
FILES = {'de': 'TECHNICAL-MAP.md', 'en': 'TECHNICAL-MAP.en.md', 'ru': 'TECHNICAL-MAP.ru.md'}
COPY = {
    'de': dict(scope='Prüfumfang', evidence='Quellcode und Gegenprobe', state='Quellprüfung', cross='Wiederkehrende Arbeitsweisen', close='Zum Projektüberblick', release='Veröffentlichte Windows-Vorschau', contribution='Eigener Commit', note='Projektleitung und Zusammenstellung: Juri Halveth / HALVETH. Entwicklung mit KI-Unterstützung. Verlinkte Quellen behalten ihre Attribution und Lizenzen. Der Stand jedes Beispiels ist an eine konkrete Revision gebunden.'),
    'en': dict(scope='Review scope', evidence='Source and counterexample', state='Source review', cross='Recurring engineering patterns', close='Project overview', release='Published Windows preview', contribution='Contribution commit', note='Project lead and curation: Juri Halveth / HALVETH. AI-assisted development. Linked sources retain their attribution and licences. Each sample is bound to a specific revision.'),
    'ru': dict(scope='Охват проверки', evidence='Код и контрпример', state='Изучение исходников', cross='Повторяющиеся инженерные приёмы', close='Обзор проектов', release='Опубликованная версия для Windows', contribution='Коммит собственного изменения', note='Руководство и подбор: Юри Хальвет / HALVETH. Разработка с помощью ИИ. Источники сохраняют атрибуцию и лицензии. Каждый пример привязан к определённой версии.'),
}
ROLES = {
    'de': dict(source='Implementierung', test='Gegenprobe', documentation='Builddokumentation', workflow='Pipeline'),
    'en': dict(source='Implementation', test='Counterexample', documentation='Build documentation', workflow='Pipeline'),
    'ru': dict(source='Реализация', test='Контрпример', documentation='Документация сборки', workflow='Конвейер'),
}

def translated(value):
    if type(value) is not dict or set(value) != set(LANGS):
        raise ValueError('All three language variants are required')
    if any(type(value[l]) is not str or not value[l].strip() for l in LANGS):
        raise ValueError('Language copy must be nonempty text')

def validate(data):
    if data['schema'] != 'halveth.technical-interface-map.v1':
        raise ValueError('Unsupported technical map')
    for key in ('title','positioning','introduction','scope'): translated(data[key])
    if data['development'] != 'AI_ASSISTED': raise ValueError('Development attribution is required')
    areas = data['areas']
    area_ids = [a['id'] for a in areas]
    ids = [i['id'] for i in data['items']]
    if not ids or len(ids) != len(set(ids)) or len(area_ids) != len(set(area_ids)):
        raise ValueError('Unique nonempty areas and samples required')
    for ident in ids + area_ids:
        if not re.fullmatch('[a-z][a-z0-9-]{0,63}',ident): raise ValueError('Invalid anchor ID')
    for a in areas:
        translated(a['title'])
        if not any(i['area']==a['id'] for i in data['items']): raise ValueError('Empty area')
    for i in data['items']:
        if i['area'] not in area_ids: raise ValueError('Unknown sample area')
        if i['review'] != 'STATIC_SOURCE_REVIEW': raise ValueError('Map must not imply fresh product runtime validation')
        for key in ('title','interface','summary','scope'): translated(i[key])
        if not i['technologies'] or any(type(t) is not str or not t.strip() for t in i['technologies']): raise ValueError('Technology names required')
        roles = set()
        for e in i['evidence']:
            roles.add(e['role'])
            if e['role'] not in {'source','test','documentation','workflow'}: raise ValueError('Invalid evidence role')
            if not re.fullmatch(r'Juri-Halveth/[A-Za-z0-9_.-]+',e['repository']): raise ValueError('Public repository binding required')
            if not re.fullmatch('[0-9a-f]{40}',e['revision']) or not re.fullmatch('[0-9a-f]{64}',e['sha256']): raise ValueError('Exact version and file digest required')
            if not e['path'] or any(p in ('','..','.') for p in e['path'].split('/')): raise ValueError('Invalid source path')
            if type(e['startLine']) is not int or type(e['endLine']) is not int or not 1 <= e['startLine'] <= e['endLine']: raise ValueError('Invalid line span')
            expected=f"https://github.com/{e['repository']}/blob/{e['revision']}/{quote(e['path'],safe='/')}#L{e['startLine']}-L{e['endLine']}"
            if e['url'] != expected: raise ValueError('Evidence URL must match bound file and span')
        if not ({'source','workflow'} & roles): raise ValueError('An implementation or workflow is required')
        if not ({'test','documentation'} & roles) and 'contribution' not in i: raise ValueError('Matching test, build documentation or contribution required')
        for kind in ('release','contribution'):
            if kind in i and not i[kind]['url'].startswith('https://github.com/Juri-Halveth/'): raise ValueError('Invalid supplemental link')
    for c in data['connections']:
        translated(c['title'])
        if len(set(c['items'])) < 2 or any(i not in ids for i in c['items']): raise ValueError('Cross-reference has unknown or repeated-only endpoints')

def render(data, lang):
    t=COPY[lang]
    lines=['[Deutsch](TECHNICAL-MAP.md) · [English](TECHNICAL-MAP.en.md) · [Русский](TECHNICAL-MAP.ru.md)', '', '# '+data['title'][lang], '', '**'+data['positioning'][lang]+'**', '', data['introduction'][lang], '', f"{t['state']}: {data['reviewedAt']} · {len(data['areas'])} / {len(data['items'])}", '']
    for a in data['areas']: lines.append(f"- [{a['title'][lang]}](#{a['id']})")
    lines += ['', '<a id="cross-references"></a>', '## '+t['cross'], '']
    by_id={i['id']:i for i in data['items']}
    for c in data['connections']:
        links=' · '.join(f"[{by_id[i]['title'][lang]}](#{i})" for i in c['items'])
        lines += ['**'+c['title'][lang]+'**', '', links, '']
    for a in data['areas']:
        lines += [f'<a id="{a["id"]}"></a>', '## '+a['title'][lang], '']
        for i in data['items']:
            if i['area'] != a['id']: continue
            lines += [f'<a id="{i["id"]}"></a>', '### '+i['title'][lang], '', '**'+i['interface'][lang]+'**', '', ' · '.join(i['technologies']), '', i['summary'][lang], '', f"**{t['scope']}:** {i['scope'][lang]}", '', '**'+t['evidence']+'**', '']
            for e in i['evidence']:
                lines.append(f"- {ROLES[lang][e['role']]} — [{e['repository']}/{e['path']}:{e['startLine']}]({e['url']}) · `{e['revision'][:7]}`")
            for kind in ('release','contribution'):
                if kind in i: lines.append(f"- [{t[kind]}]({i[kind]['url']})")
            lines += ['']
    prefix='' if lang=='de' else lang+'/'
    lines += ['---', '', data['scope'][lang], '', t['note'], '', f"[{t['close']}](https://juri-halveth.github.io/{prefix}) · [JSON](data/technical-map.json)", '']
    return '\n'.join(lines)

def fetch_source(e):
    url = f"https://raw.githubusercontent.com/{e['repository']}/{e['revision']}/{quote(e['path'], safe='/')}"
    with urlopen(Request(url, headers={'User-Agent': 'HALVETH-source-verification/1'}), timeout=30) as response:
        payload = response.read(2 * 1024 * 1024 + 1)
    if len(payload) > 2 * 1024 * 1024:
        raise ValueError('Evidence source exceeds the 2 MiB verification limit')
    return payload

def verify_sources(data, reader=fetch_source):
    """Compare declared hashes and line spans with actual version-pinned bytes."""
    validate(data)
    cache = {}
    for item in data['items']:
        for e in item['evidence']:
            key = (e['repository'], e['revision'], e['path'])
            if key not in cache:
                cache[key] = reader(e)
            payload = cache[key]
            if hashlib.sha256(payload).hexdigest() != e['sha256']:
                raise ValueError(f"Source digest mismatch: {key}")
            if len(payload.decode('utf-8').splitlines()) < e['endLine']:
                raise ValueError(f"Source span exceeds actual file: {key}")
    return len(cache)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--verify-sources', action='store_true', help='Read pinned public source bytes and verify all digests and spans')
    args=parser.parse_args()
    data=json.loads((ROOT/'data/technical-map.json').read_text(encoding='utf-8'))
    validate(data)
    if args.verify_sources:
        print(f'{verify_sources(data)} unique pinned source files verified against actual bytes.')
    for lang,name in FILES.items():
        expected=render(data,lang).encode('utf-8')
        file=ROOT/name
        if args.check:
            if not file.exists() or file.read_bytes() != expected: raise SystemExit(f'Stale generated map: {name}')
        else: file.write_bytes(expected)
    print('Three source-bound maps checked.' if args.check else 'Three source-bound maps generated.')

if __name__ == '__main__': main()
