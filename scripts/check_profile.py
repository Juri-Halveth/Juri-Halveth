"""Check all localized public profile entries and their actual capture bytes."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ('README.md', 'README.en.md', 'README.ru.md')

def check_profile(root=ROOT):
    root = Path(root)
    manifest = root / 'data/scene-stage.json'
    if not manifest.is_file():
        raise ValueError('Missing scene provenance')
    catalog = json.loads(manifest.read_text(encoding='utf-8'))
    if catalog.get('schema') != 'halveth.scene-stage.v2' or catalog.get('person') != 'Juri' or catalog.get('project') != 'HALVETH':
        raise ValueError('Invalid scene catalog identity or version')
    scenes = catalog['scenes']
    if type(scenes) is not list or [s.get('id') for s in scenes] != ['astralis', 'scarlet', 'endeck']:
        raise ValueError('Missing scene set')
    order = catalog.get('presentationOrder')
    if type(order) is not list or len(order) != 3 or any(type(item) is not str for item in order) or set(order) != {'astralis', 'scarlet', 'endeck'}:
        raise ValueError('Complete unique presentation order required')
    expected = [next(scene['image'].lstrip('/') for scene in scenes if scene['id'] == item) for item in order]
    for scene in scenes:
        name = scene['image'].lstrip('/')
        expected_image = {'astralis':'assets/scene-astralis.webp', 'scarlet':'assets/scene-scarlet-functions.webp', 'endeck':'assets/scene-endeck.webp'}[scene['id']]
        if name != expected_image:
            raise ValueError('Invalid scene image')
        image = root / name
        if not image.resolve().is_relative_to(root.resolve()) or not image.is_file():
            raise ValueError('Missing scene image')
        payload = image.read_bytes()
        if len(payload) != scene['bytes'] or hashlib.sha256(payload).hexdigest() != scene['sha256']:
            raise ValueError('Scene image digest mismatch')
    for name in ENTRIES:
        path = root / name
        if not path.is_file():
            raise ValueError(f'Missing profile entry: {name}')
        text = path.read_text(encoding='utf-8')
        if re.search(r'CLAIMED|CISSP|ISTQB|OSCE|open-research-branches|xai-40m', text, re.I):
            raise ValueError(f'Unsupported public claim in {name}')
        for required in ('halveth-forschungslabor', 'security@halveth.de', 'TECHNICAL-MAP'):
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
    print('Three profile entries checked; actual capture bytes and scene routes verified.')
