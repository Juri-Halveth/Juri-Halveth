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
direct_copy = {
    'de': {
        'title': 'Juri · Entwickler',
        'intro': 'Ich entwickle lokale Werkzeuge, Webanwendungen und interaktive Modelle. **HALVETH** verbindet diese Arbeiten mit ihren Quellständen und Prüfungen. Python · JavaScript · Windows · browserlokale Anwendungen.',
        'quick': '**Direkt zu Ergebnissen:** [Mein Lernportal](https://juri-halveth.github.io/mein-lernportal/) · [Field Difference Lab](https://juri-halveth.github.io/halveth-field-difference-lab/) · [Ausgewählte Projekte](https://juri-halveth.github.io/arbeiten/) · [Zusammenarbeit](#zusammenarbeit)',
        'heading': 'Vier ausgewählte Arbeiten',
        'lead': 'Vier Einstiege aus 18 öffentlichen Projekt- und Quelleneinträgen. Die ersten beiden laufen im Browser; NOVA und Tresor sind lokale Projekte mit Anleitung beziehungsweise Release.',
        'projects': [
            ('Mein Lernportal', 'Digitale Grundlagen und Programmierung ohne Pflichtkonto lernen.', 'Lektion direkt öffnen', 'https://juri-halveth.github.io/mein-lernportal/'),
            ('Field Difference Lab', 'Bewegungen aus derselben Ausgangslage unter zwei Modellregeln vergleichen.', 'Modell direkt öffnen', 'https://juri-halveth.github.io/halveth-field-difference-lab/'),
            ('NOVA', 'Frühere Notizen und Code wiederfinden und Korrekturen nachvollziehbar fortsetzen.', 'Anleitung und Offline-Demo', 'https://github.com/Juri-Halveth/lucinet-seedspace'),
            ('Tresor', 'Zugangsdaten lokal unter Windows verwalten.', 'Release und Startanleitung', 'https://github.com/Juri-Halveth/halveth-tresor'),
        ],
        'evidence': '[Zwei überprüfte Fallstudien](https://juri-halveth.github.io/belege/) zeigen Eingabe, Ergebnis und Gegenprobe.',
        'optional': 'Optional: Starship Lab',
        'lab': 'Das [Starship Lab](https://juri-halveth.github.io/universum/) verbindet 18 öffentliche Projekt- und Quelleneinstiege als interaktives Labor. Jeder Projektlink lässt sich auch ohne Flugmodus über die Projektliste öffnen. Ein Projekt kann mehrere Themen berühren; jede Karte erscheint einmal.',
    },
    'en': {
        'title': 'Juri · Developer',
        'intro': 'I build local tools, web applications and interactive models. **HALVETH** connects this work to its source revisions and checks. Python · JavaScript · Windows · browser-local applications.',
        'quick': '**Go straight to results:** [Mein Lernportal](https://juri-halveth.github.io/mein-lernportal/) · [Field Difference Lab](https://juri-halveth.github.io/halveth-field-difference-lab/) · [Selected projects](https://juri-halveth.github.io/en/arbeiten/) · [Collaborate](#collaborate)',
        'heading': 'Four selected projects',
        'lead': 'Four entry points from 18 public project and source entries. The first two run in the browser; NOVA and Tresor are local projects with a guide or release.',
        'projects': [
            ('Mein Lernportal', 'Learn digital skills and programming without a required account.', 'Open a lesson directly', 'https://juri-halveth.github.io/mein-lernportal/'),
            ('Field Difference Lab', 'Compare movement from the same initial state under two model rules.', 'Open the model directly', 'https://juri-halveth.github.io/halveth-field-difference-lab/'),
            ('NOVA', 'Recover notes and code and resume traceable work with preserved corrections.', 'Guide and offline demo', 'https://github.com/Juri-Halveth/lucinet-seedspace'),
            ('Tresor', 'Manage credentials locally on Windows.', 'Release and setup guide', 'https://github.com/Juri-Halveth/halveth-tresor'),
        ],
        'evidence': '[Two verified case studies](https://juri-halveth.github.io/en/belege/) show inputs, results and counterchecks.',
        'optional': 'Optional: Starship Lab',
        'lab': 'The [Starship Lab](https://juri-halveth.github.io/universum/) connects 18 public project and source entries as an interactive laboratory. Every project link is also available through a plain list without flight controls. A project can belong to several topics; each card appears once.',
    },
    'ru': {
        'title': 'Juri · Разработчик',
        'intro': 'Я создаю локальные инструменты, веб-приложения и интерактивные модели. **HALVETH** связывает эти работы с версиями кода и проверками. Python · JavaScript · Windows · приложения, работающие локально в браузере.',
        'quick': '**Сразу к результатам:** [Mein Lernportal](https://juri-halveth.github.io/mein-lernportal/) · [Field Difference Lab](https://juri-halveth.github.io/halveth-field-difference-lab/) · [Избранные проекты](https://juri-halveth.github.io/ru/arbeiten/) · [Сотрудничество](#сотрудничество)',
        'heading': 'Четыре избранные работы',
        'lead': 'Четыре входа из 18 открытых записей о проектах и источниках. Первые два работают в браузере; NOVA и Tresor — локальные проекты с руководством или выпуском.',
        'projects': [
            ('Mein Lernportal', 'Цифровые навыки и программирование без обязательного аккаунта.', 'Открыть урок напрямую', 'https://juri-halveth.github.io/mein-lernportal/'),
            ('Field Difference Lab', 'Сравнить движения при одинаковом начальном состоянии и двух правилах модели.', 'Открыть модель напрямую', 'https://juri-halveth.github.io/halveth-field-difference-lab/'),
            ('NOVA', 'Находить заметки и код, сохранять исправления и продолжать работу.', 'Руководство и офлайн-демо', 'https://github.com/Juri-Halveth/lucinet-seedspace'),
            ('Tresor', 'Локально управлять учётными данными Windows.', 'Выпуск и инструкция', 'https://github.com/Juri-Halveth/halveth-tresor'),
        ],
        'evidence': '[Два проверенных примера](https://juri-halveth.github.io/ru/belege/) показывают исходные данные, результат и контрпроверку.',
        'optional': 'Дополнительно: Starship Lab',
        'lab': '[Starship Lab](https://juri-halveth.github.io/universum/) объединяет 18 открытых проектов и источников в интерактивной лаборатории. Ссылки на проекты доступны также в обычном списке без режима полёта. Проект может относиться к нескольким темам; каждая карточка появляется один раз.',
    },
}
entity_room_base = 'https://juri-halveth.github.io/halveth-scarlet/entities/'
entity_room_source = 'https://github.com/Juri-Halveth/halveth-scarlet/blob/c36150b55fe9ed4207f185d7092b3184c353df93/README.md#L47-L66'
entity_room_copy = {
    'de': ('Weitere Räume dieser Browseranwendung:', '1001 / Konstellation · 68 Entitäten', 'Welle · 68 Formen', 'Projektquelle · c36150b'),
    'en': ('More spaces in this browser application:', '1001 / Constellation · 68 entities', 'Wave · 68 forms', 'Project source · c36150b'),
    'ru': ('Другие пространства этого браузерного приложения:', '1001 / Созвездие · 68 сущностей', 'Волна · 68 форм', 'Источник проекта · c36150b'),
}
for lang,t in copy.items():
    prefix='' if lang=='de' else lang+'/'
    mapname={'de':'TECHNICAL-MAP.md','en':'TECHNICAL-MAP.en.md','ru':'TECHNICAL-MAP.ru.md'}[lang]
    gateway=gateway_copy[lang]
    direct=direct_copy[lang]
    lines=['[Deutsch](README.md) · [English](README.en.md) · [Русский](README.ru.md)',
           '',f"# {direct['title']}",'',direct['intro'],'',direct['quick'],'',
           f"## {direct['heading']}",'',direct['lead'],'']
    lines.extend(f'- **{name}:** {purpose} [{action} ↗]({url})' for name,purpose,action,url in direct['projects'])
    lines.extend(['',direct['evidence'],'',f"## {direct['optional']}",'',
           f"[![{gateway['alt']}](assets/starship-gateway.svg)](https://juri-halveth.github.io/universum/)",'',
           direct['lab'],'',
           f"| {gateway['columns'][0]} | {gateway['columns'][1]} |",'| --- | --- |'])
    lines.extend(f'| **{name}** | {description} |' for name,description in gateway['rooms'])
    lines.extend(['',f"[{gateway['source']} · 01.11.2026](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/b7589d82ed4a50fb0507055840376a27c2cc6145/universum/data/catalog.js)",''])
    by_id={s['id']:s for s in data['scenes']}
    for scene_id in data['presentationOrder']:
        s=by_id[scene_id]
        href=s['href']+('?lang='+lang if scene_id=='scarlet' and lang!='de' else '')
        heading={'scarlet':t['scarlet'],'endeck':t['endeck']}[scene_id]
        lines.extend(['## '+heading,'',f"[![{s['alt'][lang]}]({s['image'].lstrip('/')})]({href})",'', '**'+s['title'][lang]+'**','',s['purpose'][lang]+' '+s['use'][lang],'',f"[{t['tryit']} ↗]({href})",''])
        lines.extend([s['scope'][lang],''])
        if scene_id=='scarlet':
            intro,entity_label,wave_label,source_label=entity_room_copy[lang]
            language_query='?lang=en' if lang=='en' else ''
            wave_query='?view=chain&lang=en#scarlet' if lang=='en' else '?view=chain#scarlet'
            lines.extend([f'{intro} [{entity_label}]({entity_room_base}{language_query}) · '
                          f'[{wave_label}]({entity_room_base}{wave_query}). '
                          f'[{source_label}]({entity_room_source}).',''])
    lines.extend(['## '+t['map'],'',t['maptext'],'',f"[**{t['maplink']}**]({mapname}) · [{t['work']}](https://juri-halveth.github.io/{prefix}arbeiten/#repositories)",'','## '+t['collab'],'',t['offer'],'','**[juri@halveth.de](mailto:juri@halveth.de)** · Security: [security@halveth.de](mailto:security@halveth.de)','','---','',t['credit'],'',f"[{t['sources']}](ASSET-NOTICES.md) · [HALVETH](https://juri-halveth.github.io/{prefix})",''])
    target=ROOT/('README.md' if lang=='de' else f'README.{lang}.md')
    expected='\n'.join(lines).encode('utf-8')
    if args.check:
        if not target.is_file() or target.read_bytes()!=expected: raise SystemExit('Stale scene profile: '+target.name)
    else: target.write_bytes(expected)
print('Three function-first profile entries checked.' if args.check else 'Three function-first profile entries generated.')
