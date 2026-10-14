"""Check the current TMJ's actual relative runtime closure and finite boundary."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
MAP_ROOT = ROOT / 'map32'
MAP_PATH = MAP_ROOT / 'magical-campus.tmj'
data = json.loads(MAP_PATH.read_text())
layers = data['layers']
tile_layers = [layer for layer in layers if layer['type'] == 'tilelayer']
tilesets = data['tilesets']
checks = {}
assets = {MAP_PATH}

def resolve_asset(relative):
    assert not relative.startswith(('http:', 'https:', '/'))
    path = (MAP_ROOT / relative).resolve()
    assert path.is_relative_to(MAP_ROOT.resolve()) and path.is_file()
    assets.add(path)
    return path

gids = set()
animated = set()
for tileset in tilesets:
    resolve_asset(tileset['image'])
    assert tileset['tilewidth'] == data['tilewidth'] == 32
    assert tileset['tileheight'] == data['tileheight'] == 32
    assert 0 < tileset['imagewidth'] <= 2048
    assert 0 < tileset['imageheight'] <= 2048
    first = tileset['firstgid']
    count = tileset['tilecount']
    new_gids = set(range(first, first + count))
    assert not gids.intersection(new_gids)
    gids.update(new_gids)
    for tile in tileset.get('tiles', []):
        if 'animation' in tile:
            animated.add(first + tile['id'])
            assert all(0 <= frame['tileid'] < count and frame['duration'] > 0
                       for frame in tile['animation'])

count = data['width'] * data['height']
checks['finiteNative32Grid'] = data.get('infinite', False) is False
checks['completeTileArrays'] = all(len(layer['data']) == count for layer in tile_layers)
checks['allGidsResolve'] = all(gid == 0 or gid in gids for layer in tile_layers for gid in layer['data'])
checks['fourTileLayers'] = len(tile_layers) == 4
checks['nativeArtAndWokaScale'] = all(next(p['value'] for p in data['properties'] if p['name'] == key) == 1
                                    for key in ['artScale', 'wokaScale'])
checks['playerBetweenCollisionAndAbove'] = [layer['name'] for layer in layers].index('collision-permanent') < [layer['name'] for layer in layers].index('floorLayer') < [layer['name'] for layer in layers].index('campus-above')
checks['noVisibilityMutationScript'] = not any(prop['name'] == 'script' for prop in data.get('properties', []))
collision = next(layer for layer in layers if layer['name'] == 'collision-permanent')
checks['fixedCollisionLayerActive'] = collision['visible'] is True and collision['opacity'] == 0
width, height = data['width'], data['height']
blocked = {index for index, gid in enumerate(collision['data']) if gid}
outer = set(range(width)) | set(range((height - 1) * width, height * width))
outer |= {row * width for row in range(height)} | {row * width + width - 1 for row in range(height)}
checks['finiteOuterBoundarySolid'] = outer.issubset(blocked)

objects = [obj for layer in layers for obj in layer.get('objects', [])]
start = next(obj for obj in objects if obj['name'] == 'start')
checks['classifiedDefaultSpawn'] = start.get('class') == 'area' and start['width'] == start['height'] == 32
spawn_x, spawn_y = start['x'] + 16, start['y'] + 16
spawn_cells = {int(y // 32) * width + int(x // 32)
               for x in [spawn_x - 8, spawn_x + 7.999]
               for y in [spawn_y, spawn_y + 15.999]}
checks['entireDefaultSpawnBodyClear'] = not spawn_cells.intersection(blocked)
audio_urls = set()
for obj in objects:
    for prop in obj.get('properties', []):
        if prop['name'] == 'playAudio':
            assert obj.get('class') == 'area'
            resolve_asset(prop['value'])
            audio_urls.add(prop['value'])
checks['twoNativeAmbientAssets'] = len(audio_urls) == 2
checks['noConversationSilence'] = not any(prop['name'] == 'silent' for obj in objects for prop in obj.get('properties', []))
effects = next(layer for layer in layers if layer['name'] == 'campus-native-effects')
checks['animatedEffectsPlaced'] = all(gid in animated for gid in effects['data'] if gid)

rows = [{'path':str(path.relative_to(MAP_ROOT)), 'bytes':path.stat().st_size,
         'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(assets)]
report = {
    'pass':all(checks.values()),
    'scope':'Runtime file closure, source layer semantics and finite collision boundary. No live room, physical device or audio playback claim.',
    'mapSha256':hashlib.sha256(MAP_PATH.read_bytes()).hexdigest(),
    'worldPixels':[width * 32, height * 32],
    'tileLayers':len(tile_layers), 'tileObjects':count * len(tile_layers),
    'tiledObjects':len(objects), 'atlasPages':len(tilesets),
    'gpuRgbaBytes':sum(ts['imagewidth'] * ts['imageheight'] * 4 for ts in tilesets),
    'uniqueDefinedTiles':sum(ts['tilecount'] for ts in tilesets),
    'nonemptyCells':{layer['name']:sum(bool(gid) for gid in layer['data']) for layer in tile_layers},
    'spawn':[spawn_x,spawn_y], 'runtimeBytes':sum(row['bytes'] for row in rows),
    'checks':checks, 'files':rows,
}
(ROOT / 'docs/runtime09-closure-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key:report[key] for key in ['pass','tileObjects','tiledObjects','atlasPages','gpuRgbaBytes','runtimeBytes','checks']}, indent=2))
assert report['pass']
