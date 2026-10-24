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
    scenes = json.loads(manifest.read_text(encoding='utf-8'))['scenes']
    if type(scenes) is not list or [s.get('id') for s in scenes] != ['astralis', 'scarlet', 'endeck']:
        raise ValueError('Missing scene set')
    expected = []
    for scene in scenes:
        name = scene['image'].lstrip('/')
        if not re.fullmatch(r'assets/scene-[a-z]+\.webp', name):
            raise ValueError('Invalid scene image')
        image = root / name
        if not image.resolve().is_relative_to(root.resolve()) or not image.is_file():
            raise ValueError('Missing scene image')
        payload = image.read_bytes()
        if len(payload) != scene['bytes'] or hashlib.sha256(payload).hexdigest() != scene['sha256']:
            raise ValueError('Scene image digest mismatch')
        expected.append(name)
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
        images = re.findall(r'!\[[^\]]*\]\((assets/scene-[a-z]+\.webp)\)', text)
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
