from pathlib import Path
import json
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from check_profile import check_profile, ENTRIES, ROOT, SCENE_IMAGES, PUBLIC_LABELS


@contextmanager
def presentation_fixture():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        shutil.copytree(ROOT / 'assets', root / 'assets')
        shutil.copytree(ROOT / 'data', root / 'data')
        for path in ROOT.glob('*.md'):
            shutil.copyfile(path, root / path.name)
        yield root


class ProfileEntryTests(unittest.TestCase):
    def test_complete_set_and_missing_language(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'assets', root / 'assets')
            shutil.copytree(ROOT / 'data', root / 'data')
            for name in ENTRIES:
                shutil.copyfile(ROOT / name, root / name)
            check_profile(root)
            for name in ENTRIES:
                original = (root / name).read_bytes()
                (root / name).unlink()
                with self.assertRaisesRegex(ValueError, 'Missing profile entry'):
                    check_profile(root)
                (root / name).write_bytes(original)

    def test_empty_profile_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'Missing'):
                check_profile(Path(directory))

    def test_changed_capture_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'assets', root / 'assets')
            shutil.copytree(ROOT / 'data', root / 'data')
            for name in ENTRIES:
                shutil.copyfile(ROOT / name, root / name)
            (root / 'assets/scene-endeck.webp').write_bytes(b'SYNTHETIC_CHANGED_CAPTURE')
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                check_profile(root)

    def test_missing_duplicate_or_unknown_presentation_identity_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'assets', root / 'assets')
            shutil.copytree(ROOT / 'data', root / 'data')
            for name in ENTRIES:
                shutil.copyfile(ROOT / name, root / name)
            manifest = root / 'data/scene-stage.json'
            catalog = json.loads(manifest.read_text(encoding='utf-8'))
            for order in (None, [], ['scarlet'], ['scarlet', 'scarlet'], ['scarlet', 'unknown'], ['scarlet', 'endeck', 'unknown']):
                catalog['presentationOrder'] = order
                manifest.write_text(json.dumps(catalog), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'presentation order'):
                    check_profile(root)

    def test_project_alias_is_rejected_in_public_copy_but_source_identifiers_remain(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'assets', root / 'assets')
            shutil.copytree(ROOT / 'data', root / 'data')
            for name in ENTRIES:
                shutil.copyfile(ROOT / name, root / name)
            check_profile(root)
            entry = root / 'README.md'
            with entry.open('a', encoding='utf-8') as output:
                output.write('\n## SCARLET\n')
            with self.assertRaisesRegex(ValueError, 'Functional public labels'):
                check_profile(root)

    def test_exact_two_capture_set_and_localized_evidence_labels(self):
        catalog = json.loads((ROOT / 'data/scene-stage.json').read_text(encoding='utf-8'))
        self.assertEqual([scene['id'] for scene in catalog['scenes']], ['scarlet', 'endeck'])
        self.assertEqual(catalog['presentationOrder'], ['scarlet', 'endeck'])
        self.assertEqual(len(catalog['scenes']), 2)
        self.assertEqual({p.name for p in (ROOT / 'assets').glob('scene-*.webp')},
                         {Path(name).name for name in SCENE_IMAGES.values()})
        for name in ENTRIES:
            text = (ROOT / name).read_text(encoding='utf-8')
            for label in PUBLIC_LABELS[name]:
                self.assertIn(label, text)
            self.assertEqual(text.count('[!['), 2)

    def test_missing_scene_cannot_pass_by_lowering_all_counts(self):
        with presentation_fixture() as root:
            manifest = root / 'data/scene-stage.json'
            catalog = json.loads(manifest.read_text(encoding='utf-8'))
            catalog['scenes'].pop()
            catalog['presentationOrder'].pop()
            manifest.write_text(json.dumps(catalog), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Missing scene set'):
                check_profile(root)

    def test_unlisted_capture_is_rejected_even_if_not_referenced(self):
        with presentation_fixture() as root:
            (root / 'assets/scene-unlisted.webp').write_bytes(b'SYNTHETIC_CAPTURE')
            with self.assertRaisesRegex(ValueError, 'Unlisted scene capture'):
                check_profile(root)

    def test_retired_presentation_is_rejected_across_copy_data_and_notices(self):
        targets = ('README.md', 'README.en.md', 'README.ru.md', 'TECHNICAL-MAP.md',
                   'TECHNICAL-MAP.en.md', 'TECHNICAL-MAP.ru.md', 'ASSET-NOTICES.md',
                   'data/scene-stage.json', 'data/technical-map.json')
        for target in targets:
            for retired in ('Unreal', 'ASHBOUND', 'Morrowind', 'HALVETHRealms'):
                with self.subTest(target=target, retired=retired), presentation_fixture() as root:
                    path = root / target
                    if path.suffix == '.json':
                        data = json.loads(path.read_text(encoding='utf-8'))
                        data['synthetic_retired_reference'] = retired
                        path.write_text(json.dumps(data), encoding='utf-8')
                    else:
                        with path.open('a', encoding='utf-8') as output:
                            output.write('\n[Synthetic fixture](https://example.invalid/' + retired + ')\n')
                    with self.assertRaisesRegex(ValueError, 'Retired game presentation'):
                        check_profile(root)

    def test_stale_case_count_or_all_projects_wording_is_rejected(self):
        for name in ENTRIES:
            for label in PUBLIC_LABELS[name]:
                with self.subTest(name=name, label=label), presentation_fixture() as root:
                    path = root / name
                    path.write_text(path.read_text(encoding='utf-8').replace(label, 'STALE_LABEL'), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'Missing'):
                        check_profile(root)
