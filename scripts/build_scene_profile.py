from pathlib import Path
from check_profile import validate_scene_catalog
import json, argparse
parser=argparse.ArgumentParser(description="Build three localized profile entries from two function-first scenes")
parser.add_argument("--check",action="store_true")
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/scene-stage.json').read_text(encoding='utf-8'))
validate_scene_catalog(data)
copy={
'de':dict(intro='Ich bin **Juri**. Ich baue lokale Software, nachvollziehbare Forschungswerkzeuge und interaktive Lernangebote.',tag='Idee öffnen. Etwas verändern. Ergebnis ansehen. Dahinter liegt der Code.',scarlet='Mit Zuständen, Zeit und Varianten arbeiten',endeck='Bild und Raum unterscheiden',tryit='Selbst ausprobieren',map='Was ich praktisch einbringe',maptext='Browseroberflächen, lokale Python-Werkzeuge, Gegenproben und reproduzierbare Builds. Die Schnittstellenkarte führt von diesen Fähigkeiten direkt zu Funktionen, Tests und Quellrevisionen.',maplink='Technik im Zusammenhang',work='Ausgewählte Projekte',collab='Zusammenarbeit',offer='Ich entwickle interaktive Prototypen, technische Erklärungen und lokale Werkzeuge. Für eine Zusammenarbeit vereinbaren wir ein konkretes Ziel, den Umfang und nachvollziehbare Abnahmekriterien.',credit='Projektleitung, Richtung und Auswahl: Juri / HALVETH. Entwicklung mit KI-Unterstützung. Die Aufnahmen zeigen tatsächliche Browserzustände.',sources='Herkunft und Verarbeitung der Aufnahmen',portfolio='Portfolio öffnen',evidence='Zwei überprüfte Fallstudien'),
'en':dict(intro='I’m **Juri**. I build local software, traceable research tools and interactive learning applications.',tag='Open an idea. Change something. See the result. The code is behind it.',scarlet='Work with states, time and variants',endeck='Distinguish image and space',tryit='Try it yourself',map='What I contribute in practice',maptext='Browser interfaces, local Python tools, counterexamples and reproducible builds. The interface map connects those skills directly to functions, tests and source revisions.',maplink='Connected engineering examples',work='Selected projects',collab='Collaborate',offer='I develop interactive prototypes, technical explanations and local tools. A collaboration starts with a specific goal, an agreed scope and inspectable acceptance criteria.',credit='Project lead, direction and curation: Juri / HALVETH. AI-assisted development. Captures show actual browser states.',sources='Capture provenance and processing',portfolio='Open the portfolio',evidence='Two verified case studies'),
'ru':dict(intro='Я **Juri**. Я создаю локальные программы, проверяемые исследовательские инструменты и интерактивные учебные приложения.',tag='Откройте идею. Измените что-нибудь. Посмотрите результат. За ним стоит код.',scarlet='Работа с состояниями, временем и вариантами',endeck='Различать изображение и пространство',tryit='Попробовать самому',map='Мой практический вклад',maptext='Браузерные интерфейсы, локальные инструменты Python, контрпримеры и воспроизводимые сборки. Карта интерфейсов ведёт от этих навыков к функциям, тестам и версиям кода.',maplink='Технические примеры во взаимосвязи',work='Избранные проекты',collab='Сотрудничество',offer='Я создаю интерактивные прототипы, технические объяснения и локальные инструменты. Для совместной работы согласуем конкретную цель, объём и проверяемые критерии приёмки.',credit='Руководство, направление и подбор: Juri / HALVETH. Разработка с помощью ИИ. Снимки показывают реальные состояния браузера.',sources='Происхождение и обработка снимков',portfolio='Открыть портфолио',evidence='Два проверенных примера')}
gateway_copy={
    'de': {
        'alt': 'Geometrisches HALVETH-Sternnetz mit sechs Themenräumen.',
        'cta': 'Starship Lab interaktiv öffnen',
        'heading': 'Sechs Themenräume · 18 öffentliche Einstiege',
        'lead': 'Im Starship Lab sind 18 ausgewählte öffentliche Projekt- und Quelleneinstiege verbunden. Ein Projekt kann mehrere Themen berühren; jede Projektkarte erscheint nur einmal.',
        'columns': ('Themenraum', 'Was dort erkundet wird'),
        'source': 'Katalogstand und Quellzuordnung',
        'rooms': [
            ('Software & Werkzeuge', 'Lokale Anwendungen, Entwicklungswerkzeuge und Arbeitsabläufe.'),
            ('Sicherheit & Belege', 'Prüfbare Quellen, Gegenproben und Sicherheitsmodelle.'),
            ('Modelle & Visualisierung', 'Perspektiven, Zustände, Zeit und Unterschiede.'),
            ('Welten & Interaktion', 'Interaktive Szenen und regelgebundene Welten.'),
            ('Lernen & Wissen', 'Digitale Grundlagen, Übungen und Lernpfade.'),
            ('Gesellschaft & Quellen', 'Öffentliche Recherche und getrennte Reformvorschläge.'),
        ],
    },
    'en': {
        'alt': 'Geometric HALVETH star network with six topic areas.',
        'cta': 'Explore the interactive Starship Lab',
        'heading': 'Six topic areas · 18 public entries',
        'lead': 'The Starship Lab connects 18 selected public project and source entries. A project can belong to several topics; each project card appears only once.',
        'columns': ('Topic area', 'What you can explore'),
        'source': 'Catalog snapshot and source mapping',
        'rooms': [
            ('Software & tools', 'Local applications, development tools and workflows.'),
            ('Security & evidence', 'Inspectable sources, counterchecks and security models.'),
            ('Models & visualization', 'Perspectives, states, time and differences.'),
            ('Worlds & interaction', 'Interactive scenes and rule-bound worlds.'),
            ('Learning & knowledge', 'Digital foundations, exercises and learning paths.'),
            ('Society & sources', 'Public research and separately identified reform proposals.'),
        ],
    },
    'ru': {
        'alt': 'Геометрическая звёздная сеть HALVETH с шестью тематическими разделами.',
        'cta': 'Открыть интерактивную лабораторию Starship Lab',
        'heading': 'Шесть разделов · 18 открытых входов',
        'lead': 'Starship Lab объединяет 18 отобранных открытых входов к проектам и источникам. Проект может относиться к нескольким темам; каждая карточка появляется только один раз.',
        'columns': ('Раздел', 'Что можно исследовать'),
        'source': 'Снимок каталога и привязка к источникам',
        'rooms': [
            ('Программы и инструменты', 'Локальные приложения, инструменты разработки и рабочие процессы.'),
            ('Безопасность и доказательства', 'Доступные для проверки источники, контрпроверки и модели безопасности.'),
            ('Модели и визуализация', 'Перспективы, состояния, время и различия.'),
            ('Миры и взаимодействие', 'Интерактивные сцены и миры с явными правилами.'),
            ('Обучение и знания', 'Цифровые основы, упражнения и учебные маршруты.'),
            ('Общество и источники', 'Открытое исследование и отдельно обозначенные предложения реформ.'),
        ],
    },
}
for lang,t in copy.items():
    prefix='' if lang=='de' else lang+'/'
    mapname={'de':'TECHNICAL-MAP.md','en':'TECHNICAL-MAP.en.md','ru':'TECHNICAL-MAP.ru.md'}[lang]
    gateway=gateway_copy[lang]
    lines=['[Deutsch](README.md) · [English](README.en.md) · [Русский](README.ru.md)',
           '',f"![{gateway['alt']}](assets/starship-gateway.svg)",'',
           '# Juri · HALVETH','',t['intro'],'','**'+t['tag']+'**','',
           f"[**{gateway['cta']} ↗**](https://juri-halveth.github.io/universum/) · [{t['portfolio']}](https://juri-halveth.github.io/{prefix}) · [{t['evidence']}](https://juri-halveth.github.io/{prefix}belege/)",
           '',f"## {gateway['heading']}",'',gateway['lead'],'',
           f"| {gateway['columns'][0]} | {gateway['columns'][1]} |",'| --- | --- |']
    lines.extend(f'| **{name}** | {description} |' for name,description in gateway['rooms'])
    lines.extend(['',f"[{gateway['source']} · 01.11.2026](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/b7589d82ed4a50fb0507055840376a27c2cc6145/universum/data/catalog.js)",''])
    flagship_copy = {
        'de': ('Vier Projekte zum Einstieg', 'Python · JavaScript · Windows · lokale Verarbeitung · reproduzierbare Prüfungen', [
            ('NOVA', 'Frühere Notizen und Code wiederfinden, Korrekturen erhalten und nachvollziehbar weiterarbeiten.', 'lucinet-seedspace', 'Anleitung & Offline-Demo'),
            ('Tresor', 'Zugangsdaten lokal unter Windows verwalten. Quellcode, Release und Sicherheitsmodell gehören zusammen.', 'halveth-tresor', 'Desktopprojekt ansehen'),
            ('Mein Lernportal', 'Digitale Grundlagen und Programmierung ohne Pflichtkonto lernen.', 'mein-lernportal', 'Lernen starten'),
            ('Field Difference Lab', 'Gleiche Ausgangslage, andere Modellregel: Bewegungen direkt vergleichen.', 'halveth-field-difference-lab', 'Modell ausprobieren')]),
        'en': ('Four projects to start with', 'Python · JavaScript · Windows · local processing · reproducible checks', [
            ('NOVA', 'Recover notes and code, preserve corrections and resume traceable work.', 'lucinet-seedspace', 'Guide & offline demo'),
            ('Tresor', 'Manage credentials locally on Windows, with source, releases and a security model.', 'halveth-tresor', 'View desktop project'),
            ('Mein Lernportal', 'Learn digital skills and programming without a required account.', 'mein-lernportal', 'Start learning'),
            ('Field Difference Lab', 'Compare movement from the same initial state under different model rules.', 'halveth-field-difference-lab', 'Try the model')]),
        'ru': ('Четыре проекта для знакомства', 'Python · JavaScript · Windows · локальная обработка · воспроизводимые проверки', [
            ('NOVA', 'Находите заметки и код, сохраняйте исправления и продолжайте проверяемую работу.', 'lucinet-seedspace', 'Руководство и офлайн-демо'),
            ('Tresor', 'Локальное хранение учётных данных Windows: исходники, выпуски и модель безопасности.', 'halveth-tresor', 'Настольный проект'),
            ('Mein Lernportal', 'Цифровые навыки и программирование без обязательного аккаунта.', 'mein-lernportal', 'Начать обучение'),
            ('Field Difference Lab', 'Сравните движение при одинаковом начальном состоянии и разных правилах.', 'halveth-field-difference-lab', 'Открыть модель')])}
    heading, skills, flagship_rows = flagship_copy[lang]
    lines.extend([skills, '', '## '+heading, ''])
    for title, purpose, repo, action in flagship_rows:
        route = ('https://github.com/Juri-Halveth/'+repo if repo in ('lucinet-seedspace', 'halveth-tresor')
                 else 'https://juri-halveth.github.io/'+repo+'/')
        lines.extend(['### '+title, '', purpose, '', f'[{action} ↗]({route})', ''])
    by_id={s['id']:s for s in data['scenes']}
    for scene_id in data['presentationOrder']:
        s=by_id[scene_id]
        href=s['href']+('?lang='+lang if scene_id=='scarlet' and lang!='de' else '')
        heading={'scarlet':t['scarlet'],'endeck':t['endeck']}[scene_id]
        lines.extend(['## '+heading,'',f"[![{s['alt'][lang]}]({s['image'].lstrip('/')})]({href})",'', '**'+s['title'][lang]+'**','',s['purpose'][lang]+' '+s['use'][lang],'',f"[{t['tryit']} ↗]({href})",''])
        lines.extend([s['scope'][lang],''])
    lines.extend(['## '+t['map'],'',t['maptext'],'',f"[**{t['maplink']}**]({mapname}) · [{t['work']}](https://juri-halveth.github.io/{prefix}arbeiten/#repositories)",'','## '+t['collab'],'',t['offer'],'','**[juri@halveth.de](mailto:juri@halveth.de)** · Security: [security@halveth.de](mailto:security@halveth.de)','','---','',t['credit'],'',f"[{t['sources']}](ASSET-NOTICES.md) · [HALVETH](https://juri-halveth.github.io/{prefix})",''])
    target=ROOT/('README.md' if lang=='de' else f'README.{lang}.md')
    expected='\n'.join(lines).encode('utf-8')
    if args.check:
        if not target.is_file() or target.read_bytes()!=expected: raise SystemExit('Stale scene profile: '+target.name)
    else: target.write_bytes(expected)
print('Three function-first profile entries checked.' if args.check else 'Three function-first profile entries generated.')
