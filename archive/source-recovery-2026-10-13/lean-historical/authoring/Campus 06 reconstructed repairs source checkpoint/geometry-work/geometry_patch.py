"""NEW reconstruction of two revision06 playtest corrections from restored pixels.

This is not the unavailable lost patch. The two-cell fountain diagonal is justified
from native source art; the old three-cell list is unknown. No baseline is edited.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

OPEN_FOUNTAIN_CELLS = ((101, 114), (100, 115))
# Only the duplicated pavement/fascia-bottom row can overlap a legal 32px Woka
# at the unchanged y=3040 collision frontage. Adjacent foliage stays foreground.
BELOW_PLAYER_FASCIA_CELLS = tuple((x, 189) for x in (*range(173, 182), *range(186, 195)))
CONTACT_ROUTES = (
    {"id": "books", "centerX": [2784, 2896], "bodyTopY": [3040, 3120]},
    {"id": "curios", "centerX": [2992, 3104], "bodyTopY": [3040, 3120]},
)
EVIDENCE = Path(__file__).with_name('geometry-source-evidence.json')

def map_path(root):
    root = Path(root)
    if root.is_file(): return root
    candidates = [root/'magical-campus.tmj', root/'map16/magical-campus.tmj', root/'public/butterfly-town/v6/map16/magical-campus.tmj']
    found = [p for p in candidates if p.is_file()]
    if len(found) != 1: raise ValueError(f'Expected one native map under {root}, found {found}')
    return found[0]

def apply_to_map(source):
    """Return a patched deep copy; all unrelated content is preserved verbatim.

    Expected GID checks allow independent roof metadata changes before/after this
    patch, while refusing source drift in either affected native geometry layer.
    Applying the patch twice is harmless.
    """
    result = copy.deepcopy(source)
    assert (result['width'], result['height'], result['tilewidth'], result['tileheight']) == (240, 216, 16, 16)
    by_name = {layer['name']: layer for layer in result['layers']}
    manifest = json.loads(EVIDENCE.read_text())
    for edit in manifest['edits']:
        data = by_name[edit['layer']]['data']
        index = edit['y'] * result['width'] + edit['x']
        if data[index] not in (edit['beforeGid'], 0):
            raise ValueError(f"Native source drift at {edit['layer']} ({edit['x']},{edit['y']})")
        data[index] = 0
    return result

def apply_geometry_patch(target):
    """Patch a caller-owned copy of the baseline. Never accepts restored baseline."""
    path = map_path(target).resolve()
    if 'recovered-campus06' in path.parts:
        raise ValueError('Refusing to mutate the restored baseline; pass a copied runtime.')
    source = json.loads(path.read_text())
    result = apply_to_map(source)
    path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    return {"status": "NEW reconstruction", "map": str(path), "fountainOpened": [list(c) for c in OPEN_FOUNTAIN_CELLS], "foregroundCleared": len(BELOW_PLAYER_FASCIA_CELLS), "mapSha256": hashlib.sha256(path.read_bytes()).hexdigest()}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', help='Copied native-runtime, map16 directory, or TMJ')
    print(json.dumps(apply_geometry_patch(parser.parse_args().target), indent=2))
