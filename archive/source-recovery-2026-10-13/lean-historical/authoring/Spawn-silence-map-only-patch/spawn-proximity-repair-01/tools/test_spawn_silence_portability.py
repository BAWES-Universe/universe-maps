"""Run with python -m unittest discover -s tools -p 'test_spawn_silence*.py'."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from spawn_silence import apply, audit


def sample_map():
    """Return a minimal finite native32 map with one deterministic start."""
    return {
        'orientation': 'orthogonal', 'infinite': False,
        'width': 12, 'height': 12, 'tilewidth': 32, 'tileheight': 32,
        'nextobjectid': 2,
        'layers': [{
            'id': 1, 'name': 'areas', 'type': 'objectgroup',
            'objects': [{
                'id': 1, 'name': 'start', 'class': 'area', 'type': 'area',
                'x': 96, 'y': 96, 'width': 32, 'height': 32,
            }],
        }],
        'tilesets': [],
    }


class SpawnSilencePortabilityTests(unittest.TestCase):
    def test_destination_layer_offsets_are_applied_once(self):
        """Generated area coordinates must be local to their destination layer."""
        original = sample_map()
        original['layers'][0].update(offsetx=64, offsety=32)
        changed = apply(original)
        result = audit(changed)
        self.assertTrue(result['allSpawnsProtected'])
        self.assertEqual(result['silentAreas'][0]['rect'], [128, 128, 96, 64])
        quiet = changed['layers'][0]['objects'][-1]
        self.assertEqual([quiet['x'], quiet['y']], [64, 96])
        self.assertEqual(changed['layers'][0]['objects'][0], original['layers'][0]['objects'][0])

    def test_cli_preserves_unicode_under_ascii_locale(self):
        """A non-UTF-8 process locale must not corrupt Tiled text properties."""
        original = sample_map()
        original['properties'] = [{'name': 'label', 'type': 'string', 'value': 'Café 你好'}]
        env = dict(os.environ, LC_ALL='C', LANG='C', PYTHONUTF8='0', PYTHONCOERCECLOCALE='0')
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source, output, report = (directory / name for name in ('input.tmj', 'output.tmj', 'report.json'))
            source.write_text(json.dumps(original, ensure_ascii=False), encoding='utf-8')
            run = subprocess.run(
                [sys.executable, str(Path(__file__).with_name('spawn_silence.py')), str(source),
                 '--output', str(output), '--report', str(report)],
                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(run.returncode, 0, run.stderr.decode('utf-8', errors='replace'))
            changed = json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual(changed['properties'], original['properties'])
            self.assertTrue(json.loads(report.read_text(encoding='utf-8'))['after']['allSpawnsProtected'])


if __name__ == '__main__':
    unittest.main()
