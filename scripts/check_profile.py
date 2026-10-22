"""Check the complete, explicitly supported public profile entry set."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ('README.md', 'README.en.md', 'README.ru.md')


def check_profile(root=ROOT):
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
        banner = re.search(r'!\[[^\]]*\]\((assets/portfolio-banner[^)]*\.svg)\)', text)
        if not banner or not (root / banner.group(1)).is_file():
            raise ValueError(f'Missing referenced banner in {name}')
    for name in ('portfolio', 'history', 'downloads', 'data/claims.json'):
        path = root / name
        if path.is_file() or (path.is_dir() and any(path.rglob('*'))):
            raise ValueError(f'Retired public material: {name}')


if __name__ == '__main__':
    check_profile()
    print('Three profile entries checked; technical links and referenced banners present.')
