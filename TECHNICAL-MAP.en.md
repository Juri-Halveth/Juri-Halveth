[Deutsch](TECHNICAL-MAP.md) · [English](TECHNICAL-MAP.en.md) · [Русский](TECHNICAL-MAP.ru.md)

# Technical interfaces. Concrete work samples.

**I build and investigate the boundaries between systems.**

Choose a technical area and open its function, counterexample or build definition. These examples connect seven public repositories through inspectable engineering work.

Source review: 2026-10-20 · 7 / 14

- [Interfaces & local applications](#interfaces)
- [C++ & native game worlds](#native)
- [Decisions & state](#state)
- [Security logic & counterexamples](#security)
- [Sources & data integrity](#data)
- [Graphics & numerical models](#models)
- [Builds & delivery](#delivery)

<a id="cross-references"></a>
## Recurring engineering patterns

**Validate inputs before admission**

[Validate game progress before admission](#cpp-state) · [Separate an identifier from authorization](#reference-authority) · [Read the same source packets in Node and browser](#node-browser-packet)

**Preserve open outcomes visibly**

[Model decisions with open outcomes](#decision-model) · [Evaluate rule conflicts and replay results](#python-replay) · [Check security drafts for missing evidence edges](#security-report-model)

**Trace sources, build and output**

[Bind source revision and output files separately](#artifact-provenance) · [Check generated output before deployment](#pages-delivery) · [Package engine sources for Windows](#native-packaging)

**Represent time and observation limits**

[Bind animation to visibility and user preferences](#browser-motion) · [Measure image changes within a declared region](#pixel-comparison) · [Check a graphics model against a counterexample](#optics-counterexample)

<a id="interfaces"></a>
## Interfaces & local applications

<a id="browser-motion"></a>
### Bind animation to visibility and user preferences

**Rendering, animation time and browser events**

JavaScript · Canvas 2D · Browser lifecycle

The portfolio artwork pauses offscreen and respects reduced motion. Tests simulate visibility changes and long interruptions.

**Review scope:** Browser adapter with simulated canvas and events; motion calculations are separately inspectable.

**Source and counterexample**

- Implementation — [Juri-Halveth/Juri-Halveth.github.io/landing-motion.js:1](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/landing-motion.js#L1-L47) · `945eef0`
- Counterexample — [Juri-Halveth/Juri-Halveth.github.io/tests/landing-motion.test.cjs:23](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tests/landing-motion.test.cjs#L23-L35) · `945eef0`

<a id="desktop-backup"></a>
### From a desktop dialog to a local backup

**Web interface, Python API and filesystem**

Python · pywebview · Windows

Tresor exports the encrypted vault file to a selected location. The regression covers a rejected file filter, the fallback dialog and user cancellation.

**Review scope:** Native dialogs are mocked in the test. This sample covers the UI/Python boundary; cryptography has its own assessment scope.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-tresor/src/tresor/app.py:223](https://github.com/Juri-Halveth/halveth-tresor/blob/66da64abfc58cd8cce05f935197aa51e31e232f2/src/tresor/app.py#L223-L256) · `66da64a`
- Counterexample — [Juri-Halveth/halveth-tresor/tests/test_app_backup.py:61](https://github.com/Juri-Halveth/halveth-tresor/blob/66da64abfc58cd8cce05f935197aa51e31e232f2/tests/test_app_backup.py#L61-L80) · `66da64a`

<a id="native"></a>
## C++ & native game worlds

<a id="cpp-state"></a>
### Validate game progress before admission

**Portable C++ state core and Unreal components**

C++20 · Unreal Engine · State import/export

Portal Garden models inventory, learning and quest decisions in a C++ core. Counterexamples cover invalid imported states and state preservation after rejected actions.

**Review scope:** Portable state core with source tests; the Unreal runtime is an additional integration surface.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-unreal/Source/HALVETHRealms/Public/KnowledgeSystem.h:455](https://github.com/Juri-Halveth/halveth-unreal/blob/44ccf28ffb80829def79a4f44ae5c6bcf8646de6/Source/HALVETHRealms/Public/KnowledgeSystem.h#L455-L494) · `44ccf28`
- Counterexample — [Juri-Halveth/halveth-unreal/tests/knowledge_test.cpp:40](https://github.com/Juri-Halveth/halveth-unreal/blob/44ccf28ffb80829def79a4f44ae5c6bcf8646de6/tests/knowledge_test.cpp#L40-L46) · `44ccf28`
- Pipeline — [Juri-Halveth/halveth-unreal/.github/workflows/source.yml:33](https://github.com/Juri-Halveth/halveth-unreal/blob/44ccf28ffb80829def79a4f44ae5c6bcf8646de6/.github/workflows/source.yml#L33-L57) · `44ccf28`

<a id="native-packaging"></a>
### Package engine sources for Windows

**Source project, Unreal build and output package**

PowerShell · Unreal Automation Tool · Win64

The build script invokes BuildCookRun with build, cook and stage, requires a fresh output directory and then checks the launcher path.

**Review scope:** Build script reviewed; no fresh full engine build was performed for this map. The published preview has its own version.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-scarlet/native/ashbound-unreal/package.ps1:1](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/native/ashbound-unreal/package.ps1#L1-L27) · `b768ca0`
- Build documentation — [Juri-Halveth/halveth-scarlet/native/ashbound-unreal/README.md:1](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/native/ashbound-unreal/README.md#L1-L26) · `b768ca0`
- [Published Windows preview](https://github.com/Juri-Halveth/halveth-scarlet/releases/tag/ashbound-native-v0.4.2-portal-preview)

<a id="state"></a>
## Decisions & state

<a id="decision-model"></a>
### Model decisions with open outcomes

**Entered options, weights and result view**

JavaScript · Web Crypto · Deterministic ranking

The decision model compares fully specified options. Missing values remain open; equal votes produce a tie. Tests cover both cases.

**Review scope:** One shared local algorithm with declared profile weights.

**Source and counterexample**

- Implementation — [Juri-Halveth/fortuna/docs/collective.mjs:52](https://github.com/Juri-Halveth/fortuna/blob/438f6ba7557924aa011cc0d4f26d4acb4bc4d77d/docs/collective.mjs#L52-L71) · `438f6ba`
- Counterexample — [Juri-Halveth/fortuna/docs/collective.test.mjs:29](https://github.com/Juri-Halveth/fortuna/blob/438f6ba7557924aa011cc0d4f26d4acb4bc4d77d/docs/collective.test.mjs#L29-L39) · `438f6ba`

<a id="python-replay"></a>
### Evaluate rule conflicts and replay results

**Declared rules, evaluation and replay receipt**

Python · JSON · Three-valued logic

The rule model preserves unknown values and conflicting rules. A receipt binds input, model source and output; replay detects changed results.

**Review scope:** Deterministic offline model for declared inputs and priorities.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-forschungslabor/branches/normenwerk-rule-universe/normenkern.py:125](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/normenwerk-rule-universe/normenkern.py#L125-L168) · `c6008ab`
- Counterexample — [Juri-Halveth/halveth-forschungslabor/branches/normenwerk-rule-universe/test_normenkern.py:57](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/normenwerk-rule-universe/test_normenkern.py#L57-L62) · `c6008ab`

<a id="security"></a>
## Security logic & counterexamples

<a id="reference-authority"></a>
### Separate an identifier from authorization

**Request data and separately bound authentication context**

JavaScript · Canonical JSON · Authorization model

The local reference verifier checks the principal, registry digest and current reference state. A principal written into a request is insufficient. Failure responses share one limited status.

**Review scope:** Synthetic security contract. A trusted authentication adapter is an external prerequisite.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-forschungslabor/branches/document-issue-reference-verifier/src/reference-verifier.mjs:179](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/document-issue-reference-verifier/src/reference-verifier.mjs#L179-L206) · `c6008ab`
- Counterexample — [Juri-Halveth/halveth-forschungslabor/branches/document-issue-reference-verifier/test/reference-verifier.test.mjs:83](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/document-issue-reference-verifier/test/reference-verifier.test.mjs#L83-L89) · `c6008ab`

<a id="security-report-model"></a>
### Check security drafts for missing evidence edges

**Declared observation, impact and report structure**

JavaScript · Closed input schema · Negative controls

The teaching model flags placeholders, missing actor/product bindings and proposed severity above the declared evidence tier. Counterexamples cover these transitions.

**Review scope:** Structural checks on synthetic reports; real findings remain bound to their case evidence.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-forschungslabor/branches/security-impact-learning/submission-review.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/security-impact-learning/submission-review.mjs#L1-L17) · `c6008ab`
- Counterexample — [Juri-Halveth/halveth-forschungslabor/branches/security-impact-learning/submission-review.test.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/security-impact-learning/submission-review.test.mjs#L1-L11) · `c6008ab`

<a id="data"></a>
## Sources & data integrity

<a id="node-browser-packet"></a>
### Read the same source packets in Node and browser

**Source bytes, transport packet and two data consumers**

Node.js · Browser Web Crypto · SHA-256 · Base64

A packet binds source revision, byte count and SHA-256. A differential test covers matching Node/browser interpretation and rejection of changed boundaries and bytes.

**Review scope:** Data integrity and bound interpretation within the implemented packet format.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-forschungslabor/scripts/packet.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/scripts/packet.mjs#L1-L25) · `c6008ab`
- Counterexample — [Juri-Halveth/halveth-forschungslabor/scripts/source-packet-browser.test.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/scripts/source-packet-browser.test.mjs#L1-L20) · `c6008ab`

<a id="artifact-provenance"></a>
### Bind source revision and output files separately

**Git working tree, website build and artifact bytes**

Node.js · Git · SHA-256 · Filesystem

The build check digests sorted paths and exact output bytes. The test detects changed and additional output files and a dirty source tree.

**Review scope:** Integrity checks for a bound website artifact and its source revision.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-scarlet/tools/artifact_tree.mjs:1](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/tools/artifact_tree.mjs#L1-L33) · `b768ca0`
- Counterexample — [Juri-Halveth/halveth-scarlet/tests/source-state.test.mjs:11](https://github.com/Juri-Halveth/halveth-scarlet/blob/b768ca093d9bd68b1453a8ccc5b6d02ecaa1eb07/tests/source-state.test.mjs#L11-L55) · `b768ca0`

<a id="models"></a>
## Graphics & numerical models

<a id="optics-counterexample"></a>
### Check a graphics model against a counterexample

**Geometric model, numerical prediction and comparison**

JavaScript · Ray geometry · Numerical tests

The optics lab calculates refracted rays and focus. A separate test shows extrapolation helping straight motion but worsening the result after an unseen reversal.

**Review scope:** Geometric teaching model with synthetic rays and motion traces.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-forschungslabor/branches/eye-optics-and-prediction/model.mjs:1](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/eye-optics-and-prediction/model.mjs#L1-L33) · `c6008ab`
- Counterexample — [Juri-Halveth/halveth-forschungslabor/branches/eye-optics-and-prediction/model.test.mjs:24](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/eye-optics-and-prediction/model.test.mjs#L24-L31) · `c6008ab`

<a id="pixel-comparison"></a>
### Measure image changes within a declared region

**Supplied RGBA frames and bounded change detection**

JavaScript · RGBA arrays · Sampling

The comparator counts changed pixels within a region and threshold. It explicitly reports gaps between the supplied sample times.

**Review scope:** Pure offline comparison of synthetic arrays; acquisition and capture are separate interfaces.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-forschungslabor/branches/pixel-region-change-observer/src/observer.js:130](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/pixel-region-change-observer/src/observer.js#L130-L192) · `c6008ab`
- Counterexample — [Juri-Halveth/halveth-forschungslabor/branches/pixel-region-change-observer/test/observer.test.js:44](https://github.com/Juri-Halveth/halveth-forschungslabor/blob/c6008ab5f8847921dc140d973b9a526750a89933/branches/pixel-region-change-observer/test/observer.test.js#L44-L54) · `c6008ab`

<a id="delivery"></a>
## Builds & delivery

<a id="pages-delivery"></a>
### Check generated output before deployment

**Project catalog, static build, CI and Pages**

GitHub Actions · Node.js · GitHub Pages

The portfolio pipeline builds from the catalog, requires matching committed output, runs tests and publishes main through a separate deploy job.

**Review scope:** A specific static publication path; CI and deployment have separate outcomes.

**Source and counterexample**

- Pipeline — [Juri-Halveth/Juri-Halveth.github.io/.github/workflows/pages.yml:17](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/.github/workflows/pages.yml#L17-L54) · `945eef0`
- Implementation — [Juri-Halveth/Juri-Halveth.github.io/tools/build-portfolio.cjs:13](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tools/build-portfolio.cjs#L13-L33) · `945eef0`
- Counterexample — [Juri-Halveth/Juri-Halveth.github.io/tests/portfolio.test.cjs:9](https://github.com/Juri-Halveth/Juri-Halveth.github.io/blob/945eef06bf0a03822e7db589d31ef3dbb902cc69/tests/portfolio.test.cjs#L9-L24) · `945eef0`

<a id="gradle-windows"></a>
### Verify Windows tools in a Java build

**java-tron fork, Gradle metadata and compiler artifacts**

Java ecosystem · Gradle · Protobuf · gRPC

The contribution adds SHA-256 entries for Windows protoc and protoc-gen-grpc-java. The linked diff shows its exact scope.

**Review scope:** A build-metadata contribution within inherited java-tron sources. The blockchain implementation remains attributed to upstream.

**Source and counterexample**

- Implementation — [Juri-Halveth/halveth-tron-security-lab/gradle/verification-metadata.xml:856](https://github.com/Juri-Halveth/halveth-tron-security-lab/blob/d25e104e6b887bc4d782185a96ecf3c4eb782d8c/gradle/verification-metadata.xml#L856-L858) · `d25e104`
- Implementation — [Juri-Halveth/halveth-tron-security-lab/gradle/verification-metadata.xml:1253](https://github.com/Juri-Halveth/halveth-tron-security-lab/blob/d25e104e6b887bc4d782185a96ecf3c4eb782d8c/gradle/verification-metadata.xml#L1253-L1255) · `d25e104`
- [Contribution commit](https://github.com/Juri-Halveth/halveth-tron-security-lab/commit/0472a5b9551ac838a2feecee2de1b1fac3f3fba9)

---

This map indexes published work by interface and describes its visible implementation scope, not formal qualifications. Connections are engineering cross-references, not a claim of one shared product runtime.

Project lead and curation: Juri / HALVETH. AI-assisted development. Linked sources retain their attribution and licences. Each sample is bound to a specific revision.

[Project overview](https://juri-halveth.github.io/en/) · [JSON](data/technical-map.json)
