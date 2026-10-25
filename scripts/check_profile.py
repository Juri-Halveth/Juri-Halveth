"""Check all localized public profile entries and their actual capture bytes."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ('README.md', 'README.en.md', 'README.ru.md')
SCENE_IMAGES = {'scarlet': 'assets/scene-state-space.webp', 'endeck': 'assets/scene-endeck.webp'}
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
        for required in ('halveth-forschungslabor', 'security@halveth.de', 'TECHNICAL-MAP', *PUBLIC_LABELS[name]):
            if required not in text:
                raise ValueError(f'Missing {required} in {name}')
        images = re.findall(r'!\[[^\]]*\]\((assets/scene-[a-z]+(?:-[a-z]+)?\.webp)\)', text)
        if images != expected:
            raise ValueError(f'Missing referenced scene in {name}')
        for scene in scenes:
            if scene['href'] not in text:
                raise ValueError(f'Missing scene route in {name}')
    for name in ('portfolio', 'history', 'downloads', 'data/claims.json'):
        path = root / name
        if path.is_file() or (path.is_dir() and any(path.rglob('*'))):
            raise ValueError(f'Retired public material: {name}')

if __name__ == '__main__':
    check_profile()
    print('Three profile entries checked; two original captures, scene routes and current presentation verified.')
