"""Rebuild the hash-pinned r2 baseline and prove the r3 change is mat-only.

No native engine is executed here. Existing native arrivals are reapplied only
after exact map, layout, WAM and spawn-input equality has been established.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation

R = Path(__file__).resolve().parents[1]
SLUG = 'timber-mixed-six-mat-instructor-facing-r3'
OLD = 'timber-mixed-six-mat-instructor-facing-r2'
O = R / SLUG
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pixels = lambda p: np.asarray(Image.open(p).convert('RGBA'))
expected = load(R / 'evidence/r2-accepted/EXPECTED-OUTPUTS.json')
pin = {x['path'].replace(OLD + '/', ''): x['sha256'] for x in expected['files']}
report = {'scope': 'Fresh reproducible r3 art-only correction and exact transfer checks. Native engine routes are inherited r2 evidence, not a new engine execution.'}

with tempfile.TemporaryDirectory(prefix='yoga-r3-baseline-') as td:
    B = Path(td)
    (B / 'tools').mkdir()
    shutil.copytree(R / 'source-assets', B / 'source-assets')
    shutil.copy2(R / 'GUIDE.md', B / 'GUIDE.md')
    for name in ['reorient_source_mats.py', 'repair_runtime_doorways.py', 'build_native32.py']:
        shutil.copy2(R / 'tools' / name, B / 'tools' / name)
        cmd = [sys.executable, str(B / 'tools' / name)]
        if name == 'reorient_source_mats.py':
            cmd += ['--orientation', 'r2']
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    BO = B / SLUG
    baseline_files = [
        'map32/architecture-and-furniture.png', 'map32/foreground.png',
        'map32/logic.png', 'map32/map.tmj', 'map32/map.wam',
        'assets/base.png', 'assets/above.png', 'source/layout.json',
        'source/SOURCE-PRESERVATION.json', 'source/RUNTIME-DOORWAY-PATCH.json',
        'source/WOKA-PROOF.json', 'source/native-head-union.json',
        'review/empty-native.png', 'review/occupied-native.png',
        'review/classroom-occupied-native.png', 'review/nooks-occupied-native.png',
        'review/entry-occupied-native.png', 'VALIDATION.json',
    ]
    for name in baseline_files:
        assert sha(BO / name) == pin[name], ('r2 baseline does not match accepted output', name)
    report['r2BaselineRebuild'] = {'pinnedFilesChecked': len(baseline_files), 'allExact': True,
        'acceptedEmptyNativeSha256': pin['review/empty-native.png']}

    immutable = ['map32/map.tmj', 'map32/map.wam', 'map32/foreground.png',
        'map32/logic.png', 'assets/above.png', 'source/layout.json',
        'source/WOKA-PROOF.json', 'source/native-head-union.json',
        'review/nooks-occupied-native.png', 'review/entry-occupied-native.png']
    for name in immutable:
        assert (BO / name).read_bytes() == (O / name).read_bytes(), ('immutable file changed', name)
    report['unchangedFiles'] = {name: sha(O / name) for name in immutable}
    report['entireTmjWamLayoutAndForegroundByteExactToR2'] = True

    before = pixels(B / 'previews/instructor-facing-concept.png')
    after = pixels(R / 'previews/instructor-facing-concept.png')
    support = (np.asarray(Image.open(B / 'previews/mat-surface-shadow-mask.png')) > 0) | (np.asarray(Image.open(R / 'previews/mat-surface-shadow-mask.png')) > 0)
    changed = np.any(before != after, axis=2)
    assert not (changed & ~support).any(), 'Concept change escaped old/new mat surface-shadow alpha support'
    Image.fromarray(changed.astype('uint8') * 255).save(O / 'review/r3-mat-difference-mask-source.png')
    Image.fromarray(support.astype('uint8') * 255).save(O / 'review/r3-permitted-mat-support-source.png')
    native_support = binary_dilation(support.reshape(512, 2, 768, 2).any(axis=(1, 3)), structure=np.ones((7, 7), bool))
    native_before = pixels(BO / 'review/empty-native.png')
    native_after = pixels(O / 'review/empty-native.png')
    native_changed = np.any(native_before != native_after, axis=2)
    assert not (native_changed & ~native_support).any(), 'Native change escaped mat-only resampling support'
    Image.fromarray(native_changed.astype('uint8') * 255).save(O / 'review/r3-mat-difference-mask-native.png')
    Image.fromarray(native_support.astype('uint8') * 255).save(O / 'review/r3-permitted-mat-support-native.png')
    # Six explicit separate native bounds, rather than one broad classroom band.
    boxes = [[142, 159, 189, 229], [194, 159, 242, 229], [247, 159, 295, 229],
             [475, 159, 523, 229], [527, 159, 576, 229], [580, 159, 627, 229]]
    bounded = np.zeros_like(native_changed)
    for x0, y0, x1, y1 in boxes:
        bounded[y0:y1, x0:x1] = True
    assert not (native_changed & ~bounded).any(), 'Native change escaped six mat neighborhoods'
    report['pixelPreservation'] = {
        'sourceChangedPixels': int(changed.sum()), 'sourceChangedOutsideMatSurfaceShadowSupport': 0,
        'nativeChangedPixels': int(native_changed.sum()), 'nativeChangedOutsideMatResamplingSupport': 0,
        'nativeSixMatBoundsExclusive': boxes, 'nativeChangedOutsideSixMatBounds': 0,
        'nativeAllOtherPixelsExact': True,
        'nativeMedallionExact': bool(np.array_equal(native_before[141:268, 304:464], native_after[141:268, 304:464])),
        'nativeNookDoorwaysAndRoomArtExact': bool(np.array_equal(native_before[229:], native_after[229:])),
        'nativeBeforeSha256': sha(BO / 'review/empty-native.png'),
        'nativeAfterSha256': sha(O / 'review/empty-native.png'),
        'supportMethod': 'Union of each r2/r3 transformed mat surface and contact-shadow nonzero alpha. Native support uses exact 2x2 reduction plus 3 pixels for the existing Lanczos filter.'}
    assert report['pixelPreservation']['nativeMedallionExact']
    assert report['pixelPreservation']['nativeNookDoorwaysAndRoomArtExact']

    oldproof = load(BO / 'source/SOURCE-PRESERVATION.json')
    newproof = load(O / 'source/SOURCE-PRESERVATION.json')
    props = []
    edges = []
    for oldmat, mat in zip(oldproof['records'], newproof['records']):
        assert oldmat['id'] == mat['id'] and oldmat['props'] == mat['props']
        q = mat['destinationQuad']
        oldq = oldmat['destinationQuad']
        assert q[0][0] == q[1][0] and q[2][0] == q[3][0]
        assert q[0][1] == q[3][1] and q[1][1] == q[2][1]
        assert np.array_equal(np.mean(q, axis=0), np.mean(oldq, axis=0))
        assert q[2][0] - q[1][0] == 58 and q[1][1] - q[0][1] == 110
        edges.append({'mat': mat['id'], 'sourceQuad': q,
            'nativeBounds': [q[0][0] / 2, q[0][1] / 2, q[2][0] / 2, q[2][1] / 2],
            'centerUnchanged': True, 'verticalParallelLongEdges': True, 'fanDegrees': 0, 'taperPixels': 0})
        for p in mat['props']:
            fn = f"{mat['id']}-{p['kind']}-upright.png"
            assert (R / 'source-assets' / fn).read_bytes() == (B / 'source-assets' / fn).read_bytes()
            sprite = pixels(R / 'source-assets' / fn)
            opaque = sprite[:, :, 3] == 255
            x, y = p['destination']; h, w = opaque.shape
            assert np.array_equal(before[y:y+h, x:x+w][opaque], after[y:y+h, x:x+w][opaque])
            props.append({'mat': mat['id'], 'kind': p['kind'], 'destinationUnchanged': p['destination'],
                'sourceSpriteSha256': sha(R / 'source-assets' / fn), 'sourceSpriteByteExact': True,
                'opaqueRenderedSourcePixelsExact': int(opaque.sum())})
    report['sixMatEdges'] = edges
    report['twelveProps'] = props

    native = load(R / 'evidence/r2-accepted/NATIVE-ROUTES.json')
    for name, digest in native['inputHashes'].items():
        assert sha(O / name) == digest, ('inherited native evidence inputs changed', name)
    assert native['allRoutesPass'] and native['bodyCollisionSamples'] == 0
    layout = load(O / 'source/layout.json')
    collision = np.asarray(layout['collision'])
    starts = {tuple(x['position']) for x in native['spawnChecks']}
    arrival_checks = []
    mat_anchors = [x for x in layout['anchors'] if x['kind'] == 'mat']
    for anchor, edge in zip(mat_anchors, edges):
        matches = [x for x in native['rows'] if x['name'].startswith(anchor['name'] + ' spawn ')
            and x['click'] == anchor['floorClick'] and x['final'] == anchor['anchor'] and x['pass']]
        assert {tuple(x['start']) for x in matches} == starts, ('missing actual native arrival', anchor)
        x, y = anchor['anchor']; x0, y0, x1, y1 = edge['nativeBounds']
        assert x - 8 >= x0 and x + 8 <= x1 and y >= y0 and y + 16 <= y1
        cells = {(xx // 32, yy // 32) for yy in range(y, y + 16) for xx in range(x - 8, x + 8)}
        assert all(not collision[cy, cx] for cx, cy in cells)
        arrival_checks.append({'mat': anchor['name'], 'click': anchor['floorClick'],
            'nativeFinal': anchor['anchor'], 'nativeBodyBoxExclusive': [x-8, y, x+8, y+16],
            'bodyFullyOnStraightMat': True, 'bodyCollisionFree': True,
            'verifiedPriorNativeStarts': sorted([list(x) for x in starts]),
            'matchingInheritedNativeRecords': len(matches), 'freshEngineExecution': False})
    report['sixActualArrivalRechecks'] = arrival_checks
    report['inheritedNativeReplay'] = {
        'sourceEvidenceSha256': sha(R / 'evidence/r2-accepted/NATIVE-ROUTES.json'),
        'exactOriginalInputHashesRetained': native['inputHashes'],
        'allRoutesPass': native['allRoutesPass'], 'routes': native['routes'],
        'bodySamples': native['bodySamples'], 'bodyCollisionSamples': native['bodyCollisionSamples'],
        'engineCommit': native['engineCommit'], 'freshEngineExecution': False}

report['allChecksPass'] = True
(O / 'R3-MAT-CORRECTION.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'allChecksPass': True, 'nativeChangedPixels': report['pixelPreservation']['nativeChangedPixels'],
    'outsideSixMats': 0, 'straightParallelMats': len(edges), 'unchangedProps': len(props),
    'actualNativeArrivalsRechecked': len(arrival_checks), 'movementInputsByteExact': True}, indent=2))
