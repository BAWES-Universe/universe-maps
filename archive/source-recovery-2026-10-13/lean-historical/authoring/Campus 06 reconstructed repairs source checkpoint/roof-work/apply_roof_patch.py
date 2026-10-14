#!/usr/bin/env python3
"""Apply the NEW bounded roof reconstruction to a copied native-runtime/map16 tree."""
import argparse
import hashlib
import json
import os
from pathlib import Path

from patch_roof_map import patch_roof_map

RESTORED_INPUT = Path(os.environ.get(
    'ROOF_BASE_MAP',
    '/workspace/shared/recovered-campus06/public/butterfly-town/v6/map16/magical-campus.tmj',
)).resolve().parent


def apply_roof_patch(directory):
    """Patch only magical-campus.tmj and scripts/adaptive-roofs.js in a copied tree.

    Accept map16 itself, its containing runtime directory, or a repository root.
    Collision/artwork changes already applied by another patch are preserved.
    Return deterministic relative output paths and SHA-256 hashes.
    """
    root = Path(directory).resolve()
    candidates = [root, root / 'map16', root / 'public/butterfly-town/v6/map16']
    found = [p for p in candidates if (p / 'magical-campus.tmj').is_file()]
    if len(found) != 1:
        raise ValueError('Expected exactly one map16 tree in the selected directory')
    map_dir = found[0].resolve()
    if map_dir == RESTORED_INPUT:
        raise ValueError('Refusing to mutate the exact restored06 input; patch a copied tree')
    target_map = map_dir / 'magical-campus.tmj'
    target_script = map_dir / 'scripts/adaptive-roofs.js'
    if not target_script.is_file():
        raise ValueError('Expected the existing scripts/adaptive-roofs.js in the copied tree')
    if target_map.is_symlink() or target_script.is_symlink() or map_dir not in target_script.resolve().parents:
        raise ValueError('Expected regular copied files, not links to the source')
    replacement = Path(__file__).with_name('adaptive-roofs.js').read_bytes()
    patched = patch_roof_map(json.loads(target_map.read_text()))
    map_bytes = (json.dumps(patched, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    target_map.write_bytes(map_bytes)
    target_script.write_bytes(replacement)
    return {
        'reconstruction': 'NEW restored06 binary roof reconstruction; not lost07repair recovery',
        'files': {str(p.relative_to(root)): hashlib.sha256(data).hexdigest()
                  for p, data in [(target_map, map_bytes), (target_script, replacement)]},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(apply_roof_patch(args.directory), indent=2))
