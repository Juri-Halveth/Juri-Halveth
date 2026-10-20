from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
for p in root.glob('README*.md'):
 text=p.read_text(encoding='utf-8')
 assert not re.search(r'CLAIMED|CISSP|ISTQB|OSCE|open-research-branches|xai-40m',text,re.I),p
 assert 'halveth-forschungslabor' in text,p
 assert (root/'assets/portfolio-banner.svg').is_file()
 assert 'security@halveth.de' in text,p
for path in ['portfolio','history','downloads','data/claims.json']:
 p=root/path
 assert not p.is_file() and not (p.is_dir() and any(p.rglob('*'))),path
print('Three profile entries checked; technical links and banner present.')
