from pathlib import Path
import shutil
import tempfile
import unittest
from check_profile import check_profile, ENTRIES, ROOT


class ProfileEntryTests(unittest.TestCase):
    def test_complete_set_and_missing_language(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'assets', root / 'assets')
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
            with self.assertRaisesRegex(ValueError, 'Missing profile entry'):
                check_profile(Path(directory))
