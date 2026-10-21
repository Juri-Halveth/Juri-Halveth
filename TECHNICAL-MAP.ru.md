[Deutsch](TECHNICAL-MAP.md) · [English](TECHNICAL-MAP.en.md) · [Русский](TECHNICAL-MAP.ru.md)

# Технические интерфейсы. Конкретные примеры работы.

**Я разрабатываю и исследую интерфейсы между системами.**

Выберите техническую область и откройте функцию, контрпример или определение сборки. Примеры связывают семь публичных репозиториев через конкретную инженерную работу.

Изучение исходников: 2026-10-20 · 7 / 14

- [Интерфейсы и локальные приложения](#interfaces)
- [C++ и нативные игровые миры](#native)
- [Решения и состояния](#state)
- [Логика безопасности и контрпримеры](#security)
- [Источники и целостность данных](#data)
- [Графика и численные модели](#models)
- [Сборка и публикация](#delivery)

<a id="cross-references"></a>
## Повторяющиеся инженерные приёмы

**Проверять ввод до принятия**

[Проверять игровой прогресс перед принятием](#cpp-state) · [Отделять идентификатор от полномочий](#reference-authority) · [Читать одинаковые пакеты источников в Node и браузере](#node-browser-packet)

**Явно сохранять открытые результаты**

[Моделировать решения с открытым результатом](#decision-model) · [Вычислять конфликты правил и повторять результаты](#python-replay) · [Проверять недостающие основания в черновиках отчётов](#security-report-model)

**Прослеживать исходники, сборку и результат**

[Раздельно связывать версию исходников и выходные файлы](#artifact-provenance) · [Проверять сгенерированное состояние перед публикацией](#pages-delivery) · [Собрать Windows-пакет из исходников движка](#native-packaging)

**Учитывать время и границы наблюдения**

[Связать анимацию с видимостью и настройками](#browser-motion) · [Измерять изменения изображения в заданной области](#pixel-comparison) · [Проверять графическую модель на контрпримере](#optics-counterexample)

<a id="interfaces"></a>
## Интерфейсы и локальные приложения

<a id="browser-motion"></a>
### Связать анимацию с видимостью и настройками

**Отрисовка, время анимации и события браузера**

JavaScript · Canvas 2D · Browser lifecycle

Графика портфолио приостанавливается вне экрана и учитывает уменьшение движения. Тесты моделируют смену видимости и долгие паузы.

**Охват проверки:** Браузерный адаптер с имитацией Canvas и событий; расчёты движения проверяются отдельно.

**Код и контрпример**

- Реализация — [Juri-Halveth/Juri-Halveth.github.io/landing-motion.js:1](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/landing-motion.js#L1-L47) · `945eef0`
- Контрпример — [Juri-Halveth/Juri-Halveth.github.io/tests/landing-motion.test.cjs:23](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tests/landing-motion.test.cjs#L23-L35) · `945eef0`

<a id="desktop-backup"></a>
### От диалога приложения к локальной резервной копии

**Веб-интерфейс, API Python и файловая система**

Python · pywebview · Windows

Tresor экспортирует зашифрованный файл в выбранное место. Регрессия проверяет отклонённый фильтр, запасной диалог и отмену пользователем.

**Охват проверки:** В тесте нативные диалоги заменены. Пример охватывает границу UI/Python; криптография требует отдельной проверки.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-tresor/src/tresor/app.py:223](https://github.com/Juri-Halveth/halveth-tresor/blob/66da64abfc58cd8cce05f935197aa51e31e232f2/src/tresor/app.py#L223-L256) · `66da64a`
- Контрпример — [Juri-Halveth/halveth-tresor/tests/test_app_backup.py:61](https://github.com/Juri-Halveth/halveth-tresor/blob/66da64abfc58cd8cce05f935197aa51e31e232f2/tests/test_app_backup.py#L61-L80) · `66da64a`

<a id="native"></a>
## C++ и нативные игровые миры

<a id="cpp-state"></a>
### Проверять игровой прогресс перед принятием

**Переносимое ядро состояний C++ и компоненты Unreal**

C++20 · Unreal Engine · State import/export

Portal Garden моделирует инвентарь, обучение и решения квестов в ядре C++. Контрпримеры проверяют неверные состояния импорта и сохранение состояния при отказе.

**Охват проверки:** Переносимое ядро с тестами исходников; среда Unreal представляет отдельный уровень интеграции.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-unreal/Source/HALVETHRealms/Public/KnowledgeSystem.h:455](https://github.com/Juri-Halveth/halveth-unreal/blob/44ccf28ffb80829def79a4f44ae5c6bcf8646de6/Source/HALVETHRealms/Public/KnowledgeSystem.h#L455-L494) · `44ccf28`
- Контрпример — [Juri-Halveth/halveth-unreal/tests/knowledge_test.cpp:40](https://github.com/Juri-Halveth/halveth-unreal/blob/44ccf28ffb80829def79a4f44ae5c6bcf8646de6/tests/knowledge_test.cpp#L40-L46) · `44ccf28`
- Конвейер — [Juri-Halveth/halveth-unreal/.github/workflows/source.yml:33](https://github.com/Juri-Halveth/halveth-unreal/blob/44ccf28ffb80829def79a4f44ae5c6bcf8646de6/.github/workflows/source.yml#L33-L57) · `44ccf28`

<a id="native-packaging"></a>
### Собрать Windows-пакет из исходников движка

**Исходный проект, сборка Unreal и выходной пакет**

PowerShell · Unreal Automation Tool · Win64

ASHBOUND вызывает BuildCookRun с build, cook и stage, требует новую папку вывода и проверяет путь запуска.

**Охват проверки:** Скрипт сборки изучен; новая полная сборка движка для карты не выполнялась. Опубликованная версия имеет собственный номер.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-scarlet/native/ashbound-unreal/package.ps1:1](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/native/ashbound-unreal/package.ps1#L1-L27) · `b768ca0`
- Документация сборки — [Juri-Halveth/halveth-scarlet/native/ashbound-unreal/README.md:1](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/native/ashbound-unreal/README.md#L1-L26) · `b768ca0`
- [Опубликованная версия для Windows](https://github.com/Juri-Halveth/halveth-scarlet/releases/tag/ashbound-native-v0.4.2-portal-preview)

<a id="state"></a>
## Решения и состояния

<a id="decision-model"></a>
### Моделировать решения с открытым результатом

**Введённые варианты, веса и отображение результата**

JavaScript · Web Crypto · Deterministic ranking

Fortuna сравнивает полностью заданные варианты. Пропущенные значения остаются открытыми; равные голоса дают ничью. Оба случая проверяются.

**Охват проверки:** Один общий локальный алгоритм с объявленными весами профилей.

**Код и контрпример**

- Реализация — [Juri-Halveth/fortuna/docs/collective.mjs:52](https://github.com/Juri-Halveth/fortuna/blob/438f6ba7557924aa011cc0d4f26d4acb4bc4d77d/docs/collective.mjs#L52-L71) · `438f6ba`
- Контрпример — [Juri-Halveth/fortuna/docs/collective.test.mjs:29](https://github.com/Juri-Halveth/fortuna/blob/438f6ba7557924aa011cc0d4f26d4acb4bc4d77d/docs/collective.test.mjs#L29-L39) · `438f6ba`

<a id="python-replay"></a>
### Вычислять конфликты правил и повторять результаты

**Объявленные правила, вычисление и запись воспроизведения**

Python · JSON · Three-valued logic

Модель сохраняет неизвестные значения и противоречивые правила. Запись связывает ввод, исходник модели и результат; повтор выявляет изменения.

**Охват проверки:** Детерминированная офлайн-модель объявленных данных и приоритетов.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-forschungslabor/branches/normenwerk-rule-universe/normenkern.py:125](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/normenwerk-rule-universe/normenkern.py#L125-L168) · `c6008ab`
- Контрпример — [Juri-Halveth/halveth-forschungslabor/branches/normenwerk-rule-universe/test_normenkern.py:57](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/normenwerk-rule-universe/test_normenkern.py#L57-L62) · `c6008ab`

<a id="security"></a>
## Логика безопасности и контрпримеры

<a id="reference-authority"></a>
### Отделять идентификатор от полномочий

**Данные запроса и отдельно привязанный контекст аутентификации**

JavaScript · Canonical JSON · Authorization model

Локальный проверяющий модуль сверяет principal, дайджест реестра и актуальную ссылку. Principal из запроса недостаточен. Ошибки возвращают единый ограниченный статус.

**Охват проверки:** Синтетический контракт безопасности. Доверенный адаптер аутентификации задаётся извне.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-forschungslabor/branches/document-issue-reference-verifier/src/reference-verifier.mjs:179](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/document-issue-reference-verifier/src/reference-verifier.mjs#L179-L206) · `c6008ab`
- Контрпример — [Juri-Halveth/halveth-forschungslabor/branches/document-issue-reference-verifier/test/reference-verifier.test.mjs:83](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/document-issue-reference-verifier/test/reference-verifier.test.mjs#L83-L89) · `c6008ab`

<a id="security-report-model"></a>
### Проверять недостающие основания в черновиках отчётов

**Объявленное наблюдение, влияние и структура отчёта**

JavaScript · Closed input schema · Negative controls

Учебная модель выявляет заполнители, отсутствие привязки субъекта/продукта и серьёзность выше объявленных оснований. Переходы проверяются контрпримерами.

**Охват проверки:** Структурная проверка синтетических отчётов; реальные находки связаны с основаниями своего случая.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-forschungslabor/branches/security-impact-learning/submission-review.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/security-impact-learning/submission-review.mjs#L1-L17) · `c6008ab`
- Контрпример — [Juri-Halveth/halveth-forschungslabor/branches/security-impact-learning/submission-review.test.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/security-impact-learning/submission-review.test.mjs#L1-L11) · `c6008ab`

<a id="data"></a>
## Источники и целостность данных

<a id="node-browser-packet"></a>
### Читать одинаковые пакеты источников в Node и браузере

**Исходные байты, пакет передачи и два потребителя данных**

Node.js · Browser Web Crypto · SHA-256 · Base64

Пакет связывает версию источника, число байтов и SHA-256. Сравнительный тест проверяет одинаковое чтение в Node/браузере и отказ при изменении границ и байтов.

**Охват проверки:** Целостность данных и привязанная интерпретация в реализованном формате пакета.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-forschungslabor/scripts/packet.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/scripts/packet.mjs#L1-L25) · `c6008ab`
- Контрпример — [Juri-Halveth/halveth-forschungslabor/scripts/source-packet-browser.test.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/scripts/source-packet-browser.test.mjs#L1-L20) · `c6008ab`

<a id="artifact-provenance"></a>
### Раздельно связывать версию исходников и выходные файлы

**Рабочее дерево Git, сборка сайта и байты артефакта**

Node.js · Git · SHA-256 · Filesystem

SCARLET вычисляет дайджест упорядоченных путей и точных байтов сборки. Тест выявляет изменения, лишние файлы вывода и изменённое дерево исходников.

**Охват проверки:** Проверка целостности заданного артефакта сайта и его версии исходников.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-scarlet/tools/artifact_tree.mjs:1](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/tools/artifact_tree.mjs#L1-L33) · `b768ca0`
- Контрпример — [Juri-Halveth/halveth-scarlet/tests/source-state.test.mjs:11](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/tests/source-state.test.mjs#L11-L55) · `b768ca0`

<a id="models"></a>
## Графика и численные модели

<a id="optics-counterexample"></a>
### Проверять графическую модель на контрпримере

**Геометрическая модель, численное предсказание и сравнение**

JavaScript · Ray geometry · Numerical tests

Оптическая лаборатория вычисляет преломлённые лучи и фокус. Отдельный тест показывает пользу экстраполяции при прямом движении и ухудшение после ненаблюдаемого разворота.

**Охват проверки:** Геометрическая учебная модель с синтетическими лучами и траекториями.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-forschungslabor/branches/eye-optics-and-prediction/model.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/eye-optics-and-prediction/model.mjs#L1-L33) · `c6008ab`
- Контрпример — [Juri-Halveth/halveth-forschungslabor/branches/eye-optics-and-prediction/model.test.mjs:24](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/eye-optics-and-prediction/model.test.mjs#L24-L31) · `c6008ab`

<a id="pixel-comparison"></a>
### Измерять изменения изображения в заданной области

**Переданные RGBA-кадры и ограниченное обнаружение изменений**

JavaScript · RGBA arrays · Sampling

Модуль считает изменённые пиксели в области по заданному порогу и явно выводит промежутки между переданными моментами.

**Охват проверки:** Чистое офлайн-сравнение синтетических массивов; получение и запись кадров представляют отдельные интерфейсы.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-forschungslabor/branches/pixel-region-change-observer/src/observer.js:130](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/pixel-region-change-observer/src/observer.js#L130-L192) · `c6008ab`
- Контрпример — [Juri-Halveth/halveth-forschungslabor/branches/pixel-region-change-observer/test/observer.test.js:44](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/pixel-region-change-observer/test/observer.test.js#L44-L54) · `c6008ab`

<a id="delivery"></a>
## Сборка и публикация

<a id="pages-delivery"></a>
### Проверять сгенерированное состояние перед публикацией

**Каталог проектов, статическая сборка, CI и Pages**

GitHub Actions · Node.js · GitHub Pages

Конвейер портфолио собирает сайт из каталога, требует совпадения сохранённого вывода, запускает тесты и публикует main отдельным заданием.

**Охват проверки:** Конкретный путь статической публикации; CI и развёртывание имеют отдельные результаты.

**Код и контрпример**

- Конвейер — [Juri-Halveth/Juri-Halveth.github.io/.github/workflows/pages.yml:17](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/.github/workflows/pages.yml#L17-L54) · `945eef0`
- Реализация — [Juri-Halveth/Juri-Halveth.github.io/tools/build-portfolio.cjs:13](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tools/build-portfolio.cjs#L13-L33) · `945eef0`
- Контрпример — [Juri-Halveth/Juri-Halveth.github.io/tests/portfolio.test.cjs:9](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tests/portfolio.test.cjs#L9-L24) · `945eef0`

<a id="gradle-windows"></a>
### Проверять инструменты Windows в Java-сборке

**Форк java-tron, метаданные Gradle и артефакты компилятора**

Java ecosystem · Gradle · Protobuf · gRPC

Изменение добавляет SHA-256 для Windows-версий protoc и protoc-gen-grpc-java. Ссылка на diff показывает точный объём.

**Охват проверки:** Собственное изменение метаданных сборки в унаследованных исходниках java-tron. Реализация блокчейна относится к upstream.

**Код и контрпример**

- Реализация — [Juri-Halveth/halveth-tron-security-lab/gradle/verification-metadata.xml:856](https://github.com/Juri-Halveth/halveth-tron-security-lab/blob/d25e104e6b887bc4d782185a96ecf3c4eb782d8c/gradle/verification-metadata.xml#L856-L858) · `d25e104`
- Реализация — [Juri-Halveth/halveth-tron-security-lab/gradle/verification-metadata.xml:1253](https://github.com/Juri-Halveth/halveth-tron-security-lab/blob/d25e104e6b887bc4d782185a96ecf3c4eb782d8c/gradle/verification-metadata.xml#L1253-L1255) · `d25e104`
- [Коммит собственного изменения](https://github.com/Juri-Halveth/halveth-tron-security-lab/commit/0472a5b9551ac838a2feecee2de1b1fac3f3fba9)

---

Карта группирует опубликованные примеры по интерфейсам и описывает видимый объём реализации, а не формальную квалификацию. Связи являются техническими перекрёстными ссылками, а не общей средой выполнения.

Руководство и подбор: Юри Хальвет / HALVETH. Разработка с помощью ИИ. Источники сохраняют атрибуцию и лицензии. Каждый пример привязан к определённой версии.

[Обзор проектов](https://juri-halveth.github.io/ru/) · [JSON](data/technical-map.json)
