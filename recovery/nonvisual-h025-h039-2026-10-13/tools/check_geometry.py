#!/usr/bin/env python3
"""Fresh nonvisual checks of retained declared geometry, never image acceptance."""
from pathlib import Path
from collections import deque
import json
import math
import sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / 'generated'


def main(mapid):
    root = OUT / mapid
    design = json.loads((root / 'source/design.json').read_text())
    layout = json.loads((root / 'source/layout.json').read_text())
    grid = np.array(layout['collision'], dtype=np.uint8)
    height, width = grid.shape

    def clear(x, y):
        if not (x >= 8 and x + 8 <= width * 32 and y >= 0 and y + 16 <= height * 32):
            return False
        return not grid[math.floor(y / 32):math.floor((y + 16 - 1e-8) / 32) + 1,
                        math.floor((x - 8) / 32):math.floor((x + 8 - 1e-8) / 32) + 1].any()

    targets = [{'name': s['name'], 'origin': s['anchor'], 'bodyClear': clear(*s['anchor'])}
               for s in layout['seats'] + layout['anchors']]
    if mapid == 'H025':
        floor = json.loads((root / 'source/visible-floor.json').read_text())
        paths = [dict(p, room=room) for room, data in floor['rooms'].items() for p in data['visiblePaths']]
    else:
        paths = design['visiblePaths']
    path_rows = []
    for p in paths:
        count, failed = 0, []
        for a, b in zip(p['origins'], p['origins'][1:]):
            steps = max(1, math.ceil(math.dist(a, b) / .5))
            for k in range(steps + 1):
                x, y = [a[i] + (b[i] - a[i]) * k / steps for i in range(2)]
                count += 1
                if not clear(x, y):
                    failed.append([x, y])
        path_rows.append({'name': p['name'], 'samples': count, 'pass': not failed,
                          'failureCount': len(failed), 'firstFailure': failed[:1]})

    footprints = []
    if mapid == 'H025':
        for room in design['rooms']:
            ox, oy = room['offset']
            for i, polygon in enumerate(room['fullFixturePolygons']):
                mask = Image.new('1', (1248, 1248))
                ImageDraw.Draw(mask).polygon([tuple(p) for p in polygon], fill=1)
                ys, xs = np.where(np.asarray(mask))
                admitted = int((grid[(ys + oy) // 32, (xs + ox) // 32] == 0).sum())
                footprints.append({'room': room['id'], 'index': i, 'pixels': len(xs),
                                   'admittedPixels': admitted, 'pass': admitted == 0})
    else:
        for contour in design['fixtureContours']:
            x0, y0, x1, y1 = contour['bounds']
            ys, xs = np.indices((y1 - y0, x1 - x0))
            admitted = int((grid[(ys + y0) // 32, (xs + x0) // 32] == 0).sum())
            footprints.append({'name': contour['name'], 'pixels': (y1-y0)*(x1-x0),
                               'admittedPixels': admitted, 'pass': admitted == 0})

    # Room flood fill verifies component reachability only, not native click fit.
    components = []
    for room in layout['rooms']:
        spawn = room['spawn']
        start = (spawn[0] // 32, spawn[1] // 32)
        seen, todo = {start}, deque([start])
        while todo:
            x, y = todo.popleft()
            for qx, qy in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= qx < width and 0 <= qy < height and not grid[qy, qx] and (qx, qy) not in seen:
                    seen.add((qx, qy)); todo.append((qx, qy))
        expected = [s for s in layout['anchors'] + layout['seats'] if s['room'] == room['id']]
        unreachable = [s['name'] for s in expected if (s['anchor'][0] // 32, s['anchor'][1] // 32) not in seen]
        components.append({'room': room['id'], 'spawnBodyClear': clear(*spawn),
                           'reachableCells': len(seen), 'unreachableTargets': unreachable,
                           'pass': clear(*spawn) and not unreachable})
    bands = []
    if mapid == 'H039':
        for band in design['fullWidthBands']:
            x0, y0, x1, y1 = band['bounds']
            failures = 0
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    failures += not clear(x, y)
            bands.append({'name': band['name'], 'samples': (x1-x0+1)*(y1-y0+1),
                          'failureCount': failures, 'pass': failures == 0})
    report = {'scope': 'New nonvisual checks of retained declared geometry. No TMJ, rendered-pixel, actual-engine, browser, device or live acceptance.',
              'map': mapid, 'openCells': int((grid == 0).sum()), 'body': [16, 16],
              'sampleSpacingMaximum': .5, 'targets': targets, 'paths': path_rows,
              'footprints': footprints, 'components': components, 'fullWidthBands': bands,
              'allPass': all(x['bodyClear'] for x in targets) and all(x['pass'] for x in path_rows + footprints + components + bands)}
    (root / 'validation/nonvisual-geometry.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'map': mapid, 'openCells': report['openCells'], 'targets': len(targets),
                      'paths': len(path_rows), 'pathSamples': sum(p['samples'] for p in path_rows),
                      'wholeFootprints': len(footprints), 'fullWidthBandSamples': sum(b['samples'] for b in bands),
                      'allPass': report['allPass']}))
    assert report['allPass'], mapid + ' nonvisual geometry failed; inspect report'


for mapid in ['H025', 'H039']:
    main(mapid)
