import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image
from pack_effects import pack_effect


class EffectPackingTests(unittest.TestCase):
    def test_identical_first_pixels_do_not_merge_different_animations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = Image.new('RGBA', (64, 32), 'red')
            second = first.copy()
            second.paste('blue', (0, 0, 32, 32))
            second.paste('green', (32, 0, 64, 32))
            first.save(root / '0.png'); second.save(root / '1.png')
            effect = {'name': 'two', 'frames': ['0.png', '1.png'], 'origin': [0, 0], 'duration': 120}
            pages, cells, end, audit = pack_effect(effect, root, root, 10, (64, 32), page_cells=8)
            self.assertEqual(audit['storedTiles'], 5)
            self.assertEqual(audit['uniqueAnimations'], 2)
            self.assertNotEqual(cells[0], cells[1])
            self.assertEqual(end, 15)
            animations = {entry['id']: entry['animation'] for entry in pages[0]['tiles']}
            self.assertNotEqual(animations[cells[0] - 10], animations[cells[1] - 10])

    def test_frame_groups_never_cross_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, colors in enumerate([('red', 'green'), ('blue', 'yellow')]):
                frame = Image.new('RGBA', (64, 32), colors[0])
                frame.paste(colors[1], (32, 0, 64, 32)); frame.save(root / f'{index}.png')
            effect = {'name': 'paged', 'frames': ['0.png', '1.png'], 'origin': [0, 0], 'durations': [100, 200]}
            pages, cells, end, audit = pack_effect(effect, root, root, 1, (64, 32), page_cells=3)
            self.assertEqual(len(pages), 2)
            self.assertEqual(end, 7)
            for page in pages:
                self.assertEqual(page['tilecount'], 3)
                for entry in page['tiles']:
                    self.assertTrue(all(frame['tileid'] < page['tilecount'] for frame in entry['animation']))
                    self.assertEqual([frame['duration'] for frame in entry['animation']], [100, 200])

    def test_static_pixels_do_not_get_animation_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            Image.new('RGBA', (32, 32), 'red').save(root / 'still.png')
            effect = {'name': 'still', 'frames': ['still.png'] * 8, 'origin': [0, 0], 'duration': 100}
            pages, _, end, audit = pack_effect(effect, root, root, 1, (32, 32))
            self.assertNotIn('tiles', pages[0])
            self.assertEqual(audit['staticCells'], 1)
            self.assertEqual(audit['storedTiles'], 1)
            self.assertEqual(end, 2)


if __name__ == '__main__':
    unittest.main()
