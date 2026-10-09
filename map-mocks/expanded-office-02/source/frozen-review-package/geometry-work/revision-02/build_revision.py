#!/usr/bin/env python3
"""Compact workbench revision. The parent directory is read-only input."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
ART = Path('../universe-expanded-office/art-workbench')

def rect(x, y, w, h):
    return dict(x=x, y=y, width=w, height=h)

def pt(x, y):
    return dict(x=x, y=y)

def load(path):
    return json.loads(path.read_text())

def write(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

frozen = load(ROOT / 'frozen-baseline-sha256.json')
assert all(digest(BASE / name) == value for name, value in frozen.items()), 'Frozen baseline changed'
g = copy.deepcopy(load(BASE / 'source-coordinate-geometry.json'))
source = load(ART / 'geometry-plan.json')
assert source['table']['collisionRectangle'] == [0, 0, 128, 96]
g.update(format='studenthub-source-geometry-v2', revision='02-compact-shared-workbenches',
         status='offline compact workbench geometry; receiver cabinet masks pending integration')
g['coordinateSystem'].update(gridSize=16, artAndAvatarNativeScale=32,
                             gridPurpose='16px TMJ cells preserve exact workbench/body collision; native32px art and Wokas are unchanged')
g['packaging'] = dict(tmjTileWidth=16, tmjTileHeight=16, widthTiles=152, heightTiles=84,
                     mapPixelWidth=2432, mapPixelHeight=1344, avatarFrameSize=32, avatarScale=1,
                     requirement='Use real TMJ/engine 16px collision cells or equivalent supported exact object collision. Do not round to32px or substitute preview-only static colliders.')
g['capacity'].update(sharedWorkbenches=7, provisionalSeatsPerWorkbench=4,
                     statement='Seven fixed shared workbenches with four provisional seat/work-edge places each. Initial map capacity only; no headcounts or assignments.')
g['claims'].update(entitiesInstantiated=False, fixedBenchesMovable=False,
                   claimedScope='one seat and work-edge quadrant only; shared fixed bench remains unowned')
g['workbenches'] = []
g['stations'] = []
g['claimPlots'] = []
g['furnitureCollisionRectangles'] = []
routes = []
entrance, cross = pt(992, 1312), pt(992, 576)
for pod in g['pods']:
    if pod['kind'] == 'growth-reservation':
        continue
    slug = pod['id'].removeprefix('studenthub-pod-')
    L, T = pod['x'] + 112, pod['y'] + 144
    bench_id = f'studenthub-{slug}-workbench'
    table = rect(L, T, 128, 96)
    bench = dict(id=bench_id, podId=pod['id'], name=f'{pod["name"]} shared workbench',
                 table=table, collision=table, tableAssetCanvas=rect(L-16,T-16,160,128),
                 tableAsset=str(ART/'assets/workbench-native.png'),
                 tableTightAsset=str(ART/'assets/workbench-visible-native.png'),
                 compositeAssetCanvas=rect(L-64,T-80,256,256),
                 compositeBaseAsset=str(ART/'assets/workbench-four-empty-native.png'),
                 compositeForegroundAsset=str(ART/'assets/workbench-four-foreground-native.png'),
                 visibleFurnitureBounds=rect(L,T-40,128,164),
                 scale=1, collisionType='fixed full table rectangle',
                 furnishingType='fixed baked TMJ fixture', ownerId=None,
                 movableWamEntity=False, wholeTableClaim=False, seatIds=[])
    g['workbenches'].append(bench)
    g['furnitureCollisionRectangles'].append(dict(id=bench_id, kind='fixed-shared-workbench', **table))
    for s in source['seats']:
        seat_id = f'{bench_id}-{s["id"]}'
        sx, sy = L+s['centerRelativeToTable'][0], T+s['centerRelativeToTable'][1]
        north = s['id'].startswith('north')
        west = s['id'].endswith('1')
        cx, cy = L+s['chairOriginRelativeToTable'][0], T+s['chairOriginRelativeToTable'][1]
        claim = dict(id=f'{seat_id}-plot', name=f'{pod["name"]} unassigned {s["id"]} place',
                     **rect(L+(0 if west else 64), T+(-64 if north else 48), 64, 112),
                     podId=pod['id'], stationId=seat_id, workbenchId=bench_id,
                     ownerId=None, propertyId=f'{seat_id}-personal-area',
                     scope='seat plus nearest half-table work edge; fixed shared bench is not an editable entity')
        g['claimPlots'].append(claim)
        # Each north seat enters laterally from its nearest side. This avoids
        # relying on a route behind the north chair through the back-cabinet band.
        approach = pt(L-16 if west else L+144, sy) if north else pt(sx,T+160)
        station = dict(id=seat_id, name=f'{pod["name"]} provisional {s["id"]} seat',
                       podId=pod['id'], sharedWorkbenchId=bench_id, ownerId=None,
                       headcountEvidence=None, claimPlotId=claim['id'],
                       seat=dict(x=sx,y=sy,facing=s['facing'],frameIndex=s['frameIndex'],
                                 spriteBounds=rect(sx-16,sy-16,32,32), bodyBounds=rect(sx-8,sy,16,16),
                                 sittingAnimationImplemented=False),
                       approach=approach, chairAssetCanvas=rect(cx,cy,48,64),
                       chairAsset=str(ART/s['chairAsset']), chairForegroundAsset=str(ART/s['foregroundAsset']),
                       assetScale=1, assetResampling=False,
                       chairCollision='none; walkable seat allocation',
                       movableWamEntity=False)
        g['stations'].append(station)
        bench['seatIds'].append(seat_id)
        # Openings remain centered on the pod. Turn toward the table only after
        # clearing the two front-edge low dividers.
        near_y = T+160 if pod['y'] < 448 else T-80
        pts = [entrance,cross,pt(pod['x']+176,576),pt(pod['x']+176,near_y)]
        if north:
            side_x = L-16 if west else L+144
            pts += [pt(side_x,near_y),pt(side_x,sy),pt(sx,sy)]
        elif pod['y'] < 448:
            pts += [pt(sx,T+160),pt(sx,sy)]
        else:
            side_x = L-16 if west else L+144
            pts += [pt(side_x,near_y),pt(side_x,T+160),pt(sx,T+160),pt(sx,sy)]
        compact = []
        for p in pts:
            if not compact or p != compact[-1]:
                compact.append(p)
        routes.append(dict(id=f'entrance-to-{seat_id}', targetStationId=seat_id,
                           purpose='through bay opening to own seat with the other three bench seats occupied',
                           points=compact, alsoTestReverse=True, avoidOtherClaimPlots=True,
                           alsoTestOtherSeatsOccupied=True, receiverObstacleMasksIncluded=False))
    # Separate all-four-occupied circulation proof, outside all personal plots.
    # North row touches the future back-cabinet band; its validity remains pending
    # final receiver masks and is explicitly not reported as assembled-room proof.
    near_y = T+160 if pod['y'] < 448 else T-80
    left, right, top, bottom = L-16,L+144,T-80,T+160
    loop = [pt(pod['x']+176,576),pt(pod['x']+176,near_y),pt(left,near_y),
            pt(left,top),pt(right,top),pt(right,bottom),pt(left,bottom),
            pt(left,near_y),pt(pod['x']+176,near_y),pt(pod['x']+176,576)]
    compact = []
    for p in loop:
        if not compact or p != compact[-1]:
            compact.append(p)
    routes.append(dict(id=f'{bench_id}-all-seats-occupied-circulation',
                       purpose='through bay opening and around bench while all four seat bodies are occupied',
                       points=compact, alsoTestReverse=True, avoidOtherClaimPlots=True,
                       alsoTestOtherSeatsOccupied=True, receiverObstacleMasksIncluded=False))

base_routes = load(BASE/'route-manifest.json')['routes']
routes += [r for r in base_routes if 'targetStationId' not in r]
for r in routes:
    r['receiverObstacleMasksIncluded'] = False

g['floor']['policy'] = 'Within shell floor envelopes minus permanentWalls, lowDividers, and furnitureCollisionRectangles. No receiver cabinet masks yet.'
g['limitations'] = [
    'Revised painted receiver/cabinet obstacles are excluded until pixel-aligned masks are assembled. This is not final furnished-bay route acceptance.',
    'Reported reference cabinet bands around y144..176 and x96..144 / x400..448 to y352 are art observations, not final collision rectangles.',
    'Use16px TMJ cells for exact table collisions;32px rounding falsely blocks north contact seats. Art and Wokas remain native32px and unscaled.',
    'The 64×112 claims touch at edges and cover separate seat/work-edge quadrants. The fixed shared bench deliberately crosses four plots and remains baked, unowned, and non-movable.',
    'Reception, lounge, and meeting furniture footprints remain the baseline reservations pending separate final integration.',
    'Geometry checks do not establish live engine behavior, claimability, multiplayer collision policy, privacy, or seated animation.',
]
g['pendingObstacleMasks'] = dict(status='required after assembled-art registration',
                                sources='revised receiver back and side cabinets; planter/trim masks as applicable',
                                referenceObservationsOnly=dict(backCabinetY=[144,176],westCabinetX=[96,144],eastCabinetX=[400,448],sideCabinetBottomY=352),
                                authoritativeCollisionRectangles=None,
                                requiredNextStep='Extract exact registered obstacle masks from assembled source art, include them in real TMJ collision, and rerun all routes.')
g['provenance'] += [dict(path=str(p),sha256=digest(p)) for p in [ART/'geometry-plan.json',ART/'asset-manifest.json',ART/'proofs/checks.json',ROOT/'frozen-baseline-sha256.json']]
write('source-coordinate-geometry.json',g)
write('furniture-collision-rectangles.json',dict(status='compact benches only; art-obstacle masks pending',
                                               units='native world pixels; half-open',
                                               tmjCollisionCellSize=16, avatarBody=rect(-8,0,16,16),
                                               fixedWorkbenches=g['furnitureCollisionRectangles'],
                                               retainedLowDividers=g['lowDividers'],
                                               chairsAreWalkable=True,
                                               pendingObstacleMasks=g['pendingObstacleMasks']))
write('route-manifest.json',dict(format='studenthub-route-manifest-v2',coordinateSystem=g['coordinateSystem'],
                                status='offline draft; excludes revised receiver art-obstacle masks',routes=routes))
areas = [dict(id=p['id'],name=p['name'],**{k:p[k] for k in ['x','y','width','height']},visible=True,
              properties=[dict(id=p['propertyId'],type='personalAreaPropertyData',accessClaimMode='dynamic',allowedTags=[],ownerId=None)]) for p in g['claimPlots']]
wam = dict(version='2.0.0',mapUrl='./studenthub-expanded-workbench-candidate.tmj',entities={},entityCollections=[],areas=areas,
           metadata=dict(name='StudentHub compact workbenches — OFFLINE DRAFT',
                         description='28 unassigned seat/work-edge quadrants around seven shared fixed benches. Provisional capacity, no headcounts or assignments. No live claim or permission configuration.'),
           vendor=dict(studenthubDraft=dict(offlineOnly=True,revision='02',fixedBakedBenches=True,
                                            sharedBenchesAreNotMovableEntities=True,
                                            allowedTagsMeaning='Empty draft placeholder; the claim prompt accepts any logged-in user. Not an approved audience policy.',
                                            activation='Sibling WAM adjacency activates nothing. Room routing and effective claimant permissions need separate verification.',
                                            receiverMasksPending=True)))
write('personal-areas.offline-draft.wam',wam)
write('claim-manifest.json',dict(status='offline draft only',scope='seat and work-edge quadrants; fixed baked benches remain shared and unowned',
                                dimensions=dict(width=64,height=112), touchingEdgesAllowed=True, overlapsAllowed=False,
                                noStaffAssignments=True,noLiveClaims=True,noMovableEntities=True,areas=areas))
print(json.dumps(dict(workbenches=len(g['workbenches']),seats=len(g['stations']),claims=len(areas),routes=len(routes),baselineUnchanged=True)))
