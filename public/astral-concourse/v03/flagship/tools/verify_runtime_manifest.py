"""Read-only verification of the frozen Flagship v03 runtime; Python stdlib only."""
from pathlib import Path
import hashlib
import json
import posixpath
import struct

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'map32'
manifest = json.loads((ROOT / 'RUNTIME-MANIFEST.json').read_text())
expected = {x['file']: x for x in manifest['runtimeFiles']}
assert len(expected) == 9
assert set(expected) == {p.name for p in RUNTIME.iterdir() if p.is_file()}
for name, record in expected.items():
    data = (RUNTIME / name).read_bytes()
    assert len(data) == record['bytes'], name
    assert hashlib.sha256(data).hexdigest() == record['sha256'], name
assert sum(x['bytes'] for x in expected.values()) == manifest['runtimeBytes'] == 7018619
m = json.loads((RUNTIME / 'grand-auditorium.tmj').read_text())
w = json.loads((RUNTIME / 'grand-auditorium.wam').read_text())
assert m['tilewidth'] == m['tileheight'] == 32
assert [m['width'], m['height']] == [80, 60]
assert m['orientation'] == 'orthogonal' and not m['infinite']
assert w['mapUrl'] == './grand-auditorium.tmj'
closure = {'grand-auditorium.tmj', 'grand-auditorium.wam'}
for tileset in m['tilesets']:
    name = tileset['image']
    assert name == posixpath.basename(name) and name in expected, name
    assert tileset['tilewidth'] == tileset['tileheight'] == 32
    data = (RUNTIME / name).read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', name
    dimensions = struct.unpack('>II', data[16:24])
    assert dimensions == (tileset['imagewidth'], tileset['imageheight']), name
    assert max(dimensions) <= 1024, name
    closure.add(name)
assert closure == set(expected)
print(json.dumps({'passed': True, 'runtimeFiles': len(expected), 'runtimeBytes': manifest['runtimeBytes'], 'nativeTileSize': 32, 'worldPixels': [2560, 1920], 'companionMapUrl': w['mapUrl'], 'browserVerified': False, 'liveMediaVerified': False}, indent=2))
