from pathlib import Path
import json
import shutil
import tempfile
import unittest
from check_profile import check_profile, ENTRIES, ROOT


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
            for order in (None, [], ['scarlet', 'endeck'], ['scarlet', 'scarlet', 'astralis'], ['scarlet', 'endeck', 'unknown']):
                catalog['presentationOrder'] = order
                manifest.write_text(json.dumps(catalog), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'presentation order'):
                    check_profile(root)
