"""Check all localized public profile entries and their actual capture bytes."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ('README.md', 'README.en.md', 'README.ru.md')
SCENE_IMAGES = {'scarlet': 'assets/scene-state-space.webp', 'endeck': 'assets/scene-endeck.webp'}
GATEWAY_IMAGE = 'assets/starship-gateway.svg'
GATEWAY_SHA256 = '16b71c47e054f3776dfdc8509f867b1f1a1ac686170e47f14c193206b86b038c'
ENTITY_ROOM_BASE = 'https://juri-halveth.github.io/halveth-scarlet/entities/'
ENTITY_ROOM_SOURCE = 'https://github.com/Juri-Halveth/halveth-scarlet/blob/c36150b55fe9ed4207f185d7092b3184c353df93/README.md#L47-L66'
GATEWAY_LABELS = {
    'README.md': ('Software & Werkzeuge', 'Sicherheit & Belege', 'Modelle & Visualisierung', 'Welten & Interaktion', 'Lernen & Wissen', 'Gesellschaft & Quellen'),
    'README.en.md': ('Software & tools', 'Security & evidence', 'Models & visualization', 'Worlds & interaction', 'Learning & knowledge', 'Society & sources'),
    'README.ru.md': ('Программы и инструменты', 'Безопасность и доказательства', 'Модели и визуализация', 'Миры и взаимодействие', 'Обучение и знания', 'Общество и источники'),
}
PUBLIC_LABELS = {
    'README.md': ('Zwei überprüfte Fallstudien', 'Ausgewählte Projekte'),
    'README.en.md': ('Two verified case studies', 'Selected projects'),
    'README.ru.md': ('Два проверенных примера', 'Избранные проекты'),
}
RETIRED_PRESENTATION = re.compile(
    r'\b(?:unreal|ashbound|astralis|morrowind|realms|halvethrealms|games?|spiel\w*|игр\w*)\b',
    re.I,
)

def reject_retired_presentation(text, source):
    if RETIRED_PRESENTATION.search(text):
        raise ValueError(f'Retired game presentation in {source}')

def validate_scene_catalog(catalog):
    reject_retired_presentation(json.dumps(catalog, ensure_ascii=False), 'scene catalog')
    if catalog.get('schema') != 'halveth.scene-stage.v2' or catalog.get('person') != 'Juri' or catalog.get('project') != 'HALVETH':
        raise ValueError('Invalid scene catalog identity or version')
    scenes = catalog.get('scenes')
    if type(scenes) is not list or [s.get('id') for s in scenes] != list(SCENE_IMAGES):
        raise ValueError('Missing scene set')
    order = catalog.get('presentationOrder')
    if type(order) is not list or len(order) != len(SCENE_IMAGES) or any(type(item) is not str for item in order) or set(order) != set(SCENE_IMAGES):
        raise ValueError('Complete unique presentation order required')
    return scenes

def check_profile(root=ROOT):
    root = Path(root)
    manifest = root / 'data/scene-stage.json'
    if not manifest.is_file():
        raise ValueError('Missing scene provenance')
    catalog = json.loads(manifest.read_text(encoding='utf-8'))
    scenes = validate_scene_catalog(catalog)
    gateway = root / GATEWAY_IMAGE
    if not gateway.is_file() or hashlib.sha256(gateway.read_bytes()).hexdigest() != GATEWAY_SHA256:
        raise ValueError('Missing or changed Starship gateway image')
    order = catalog['presentationOrder']
    expected = [next(scene['image'].lstrip('/') for scene in scenes if scene['id'] == item) for item in order]
    for scene in scenes:
        name = scene['image'].lstrip('/')
        expected_image = SCENE_IMAGES[scene['id']]
        if name != expected_image:
            raise ValueError('Invalid scene image')
        image = root / name
        if not image.resolve().is_relative_to(root.resolve()) or not image.is_file():
            raise ValueError('Missing scene image')
        payload = image.read_bytes()
        if len(payload) != scene['bytes'] or hashlib.sha256(payload).hexdigest() != scene['sha256']:
            raise ValueError('Scene image digest mismatch')
    actual_captures = {p.relative_to(root).as_posix() for p in (root / 'assets').glob('scene-*.webp')}
    if actual_captures != set(SCENE_IMAGES.values()):
        raise ValueError('Unlisted scene capture in current presentation')
    for path in sorted({*root.glob('*.md'), *root.glob('data/*.json'), *root.glob('assets/*.svg')}):
        reject_retired_presentation(path.read_text(encoding='utf-8'), path.name)
    for name in ENTRIES:
        path = root / name
        if not path.is_file():
            raise ValueError(f'Missing profile entry: {name}')
        text = path.read_text(encoding='utf-8')
        visible_text = re.sub(r'\]\([^)]*\)', ']', text)
        if re.search(r'\b(?:SCARLET|ENDECK|FORTUNA|TRIAD)\b', visible_text, re.I):
            raise ValueError(f'Functional public labels required in {name}')
        if re.search(r'CLAIMED|CISSP|ISTQB|OSCE|open-research-branches|xai-40m', text, re.I):
            raise ValueError(f'Unsupported public claim in {name}')
        for required in ('halveth-forschungslabor', 'security@halveth.de', 'TECHNICAL-MAP',
                         'assets/starship-gateway.svg', 'https://juri-halveth.github.io/universum/',
                         '18', *GATEWAY_LABELS[name], *PUBLIC_LABELS[name]):
            if required not in text:
                raise ValueError(f'Missing {required} in {name}')
        if not re.search(r'\[!\[[^\]]+\]\(assets/starship-gateway\.svg\)\]\(https://juri-halveth\.github\.io/universum/\)', text):
            raise ValueError(f'Gateway image must open the interactive Starship Lab in {name}')
        images = re.findall(r'!\[[^\]]*\]\((assets/scene-[a-z]+(?:-[a-z]+)?\.webp)\)', text)
        if images != expected:
            raise ValueError(f'Missing referenced scene in {name}')
        for scene in scenes:
            if scene['href'] not in text:
                raise ValueError(f'Missing scene route in {name}')
        lang = {'README.md': 'de', 'README.en.md': 'en', 'README.ru.md': 'ru'}[name]
        entity_url = ENTITY_ROOM_BASE + ('?lang=en' if lang == 'en' else '')
        wave_url = ENTITY_ROOM_BASE + ('?view=chain&lang=en#scarlet' if lang == 'en' else '?view=chain#scarlet')
        if text.count(f']({entity_url})') != 1 or text.count(f']({wave_url})') != 1 or text.count(f']({ENTITY_ROOM_SOURCE})') != 1:
            raise ValueError(f'Missing or duplicated entity room binding in {name}')
        if not (text.index(f']({entity_url})') < text.index(f']({wave_url})') < text.index('halveth-forschungslabor/endeck/')):
            raise ValueError(f'Entity rooms must stay with their parent scene in {name}')
    for name in ('portfolio', 'history', 'downloads', 'data/claims.json'):
        path = root / name
        if path.is_file() or (path.is_dir() and any(path.rglob('*'))):
            raise ValueError(f'Retired public material: {name}')

if __name__ == '__main__':
    check_profile()
    print('Three profile entries checked; two original captures, scene routes and current presentation verified.')
