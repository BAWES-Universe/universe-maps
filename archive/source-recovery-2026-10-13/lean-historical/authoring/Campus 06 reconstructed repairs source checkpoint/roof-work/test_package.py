"""Directory packaging regressions; all writes remain in this roof-work directory."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from apply_roof_patch import apply_roof_patch, RESTORED_INPUT

HERE = Path(__file__).resolve().parent
BASE = Path(os.environ.get('ROOF_BASE_MAP', str(RESTORED_INPUT / 'magical-campus.tmj')))
BASE_BYTES = BASE.read_bytes()
BASE_MAP = json.loads(BASE_BYTES)


class PackagingTest(unittest.TestCase):
    def copy_fixture(self, map_dir):
        map_dir.mkdir(parents=True, exist_ok=True)
        (map_dir / 'scripts').mkdir(exist_ok=True)
        (map_dir / 'magical-campus.tmj').write_bytes(BASE_BYTES)
        (map_dir / 'scripts/adaptive-roofs.js').write_text('// copied old script\n')

    def test_directory_shapes_determinism_and_idempotence(self):
        outputs = []
        with tempfile.TemporaryDirectory(dir=HERE) as temp:
            for i, suffix in enumerate(['', 'map16', 'public/butterfly-town/v6/map16']):
                root = Path(temp) / str(i)
                directory = root / suffix
                self.copy_fixture(directory)
                manifest = apply_roof_patch(root)
                self.assertEqual(manifest, apply_roof_patch(root))
                outputs.append((directory / 'magical-campus.tmj').read_bytes())
                self.assertEqual((directory / 'scripts/adaptive-roofs.js').read_bytes(), (HERE / 'adaptive-roofs.js').read_bytes())
                self.assertEqual(len(manifest['files']), 2)
            self.assertTrue(all(output == outputs[0] for output in outputs))

    def test_preexisting_geometry_edits_survive_composition(self):
        with tempfile.TemporaryDirectory(dir=HERE) as temp:
            root = Path(temp)
            self.copy_fixture(root)
            changed = json.loads(BASE_BYTES)
            collision = next(l for l in changed['layers'] if l['name'] == 'collision-permanent')
            collision['data'][0] = 12345  # Deliberate marker for an independent geometry patch.
            (root / 'magical-campus.tmj').write_text(json.dumps(changed))
            apply_roof_patch(root)
            result = json.loads((root / 'magical-campus.tmj').read_text())
            self.assertEqual(next(l for l in result['layers'] if l['name'] == 'collision-permanent'), collision)
            self.assertEqual(result['tilesets'], changed['tilesets'])

    def test_source_and_incomplete_tree_are_rejected_without_mutation(self):
        with self.assertRaisesRegex(ValueError, 'Refusing to mutate'):
            apply_roof_patch(RESTORED_INPUT)
        with tempfile.TemporaryDirectory(dir=HERE) as temp:
            root = Path(temp)
            (root / 'magical-campus.tmj').write_bytes(BASE_BYTES)
            with self.assertRaisesRegex(ValueError, 'existing scripts'):
                apply_roof_patch(root)
            self.assertEqual((root / 'magical-campus.tmj').read_bytes(), BASE_BYTES)
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(), hashlib.sha256(BASE_BYTES).hexdigest())

    def test_ambiguous_tree_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=HERE) as temp:
            root = Path(temp)
            self.copy_fixture(root)
            self.copy_fixture(root / 'map16')
            with self.assertRaisesRegex(ValueError, 'exactly one'):
                apply_roof_patch(root)


if __name__ == '__main__':
    unittest.main(verbosity=2)
