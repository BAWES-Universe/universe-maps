from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';D=R/'deliverables';D.mkdir(exist_ok=True)
J=lambda p:json.loads(p.read_text());W=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
geo=J(P/'validation/geometry.json');routes=J(P/'validation/native-routes.json');spawn=J(P/'validation/spawn-domains.json');pres=J(P/'validation/r6-preservation.json')
assert all(x['allPass'] for x in [geo,routes,spawn]);assert pres['byteExactOutsideChairCorrections']
(P/'README.md').write_text('''# Resonance Media House r7c - expanded garden court

New unpublished r7c derivative. Relative to r7b: twelve clear courtyard cells and three viewer carpet gaps opened; three upper backs are slimmer and four inherited seat assets/anchors translated to native-fit-stable arrival positions. Mixed wall/parapet cells remain solid. Viewer upper backs and their complete rails are slimmer together; original legs/feet remain exact. World: 1024 x 896 pixels, 32 x 28 native32 tiles. Approved r6 768 x 512 interior is byte-exact except ten explicit seat-depth/arrival corrections at offset (128,192); its rear wall band remains exact. The r6 map offset is (128,96). This adds 128 pixels to each side, 96 north and 192 south. Architecture and native32 avatar scale are unchanged. Three editor low-lumbar chairs and three viewer chair backs have narrowly corrected depth/anchors with protected rear feet. Ten seat roles remain; six backrest roles are corrected and four backless/side-facing assets retain their shape and move +10px/+7px to match native arrival. New courtyard and garden paths are authored as conservatively reachable floor; surrounding foliage and fixtures are solid scenery.

## Replay
From the source root: python3 tools/expand_r7.py; python3 tools/check_chair_depth.py; python3 tools/check_spawn_and_boundaries.py resonance-media-house; node tools/native/route-audit.cjs resonance-media-house; node tools/native/arrival-audit.cjs resonance-media-house; python3 tools/render_actual_seat_facings.py; python3 tools/render_native_arrivals.py. Requires Pillow, NumPy and Node.js. The r6-preserved snapshot and generated exterior are bundled. Rebuild restores the original map layers, applies only six localized backrest repairs and four exact seat translations, then compiles TMJ/atlases. Independently restores old r6 below/above layers (the old above layer is transparent).

Occupied proof decodes current TMJ below/above layers and inserts unchanged native32 standing frames extracted from a provenance-tracked existing proof overlay. No prior occupied screenshot is pasted. Primary native-arrival proof uses actual final direction from source-extracted movement. Intended configuration-facing illustrations are separate; station-facing is not automatic. It is a scale/placement illustration, not a live room screenshot or a claim of seated animation. Boundary evidence uses the original supplied Greg reference frame. No new avatar artwork is created or baked into runtime.

## Scope
Atlas roundtrip, body/head clearance, connectivity, exhaustive conservative spawn domains and bundled source-extracted native click/touch movement replay. Live browser gameplay, keyboard physics, devices, networking and service integrations remain untested. Media integrations remain unconfigured. No engine changes or publication. Import TMJ into a new test room and deliberately configure its WAM companion if needed.
''')
(P/'PROVENANCE.md').write_text('''# r7 provenance

Approved r6 map and occupant proof come from resonance-media-house-r6-source-replay.zip. The approved interior plus rear wall (r6 rectangle [0,80,768,608]) is exact outside ten documented seat neighborhoods; see validation/r6-preservation.json. Original generated architecture and furniture assets remain in source. The exterior expansion was created using built-in image generation on 2026-10-11, guided by a locked-size padded source. The r7b correction removes south-crosspath lamps and moves foliage off admitted floor. Compact planting beds physically terminate the north side stubs. The generated north scenery band was registered from 176px to 160px high so planter ground ends fit the tile boundary; approved interior is untouched. The old clear central entrance strip is retained. It introduces only exterior garden and courtyard scenery.

The occupied renderer uses unchanged repository native32 frames extracted from the included provenance-tracked proof overlay. Both under- and above-player layers are decoded from the current TMJ. Boundary sweeps use the supplied Greg reference. Raw Pipoya sprite sheets are not added. Existing license and provenance records are retained from r6; no fresh live repository verification is implied.

Native replay uses the unchanged bundled extracted engine methods pinned at 60e7afdc and EasyStar 0.4.4. Only map geometry and adapter inputs change. No engine edits, new integration, paid service or publication.
''')
W(P/'validation/scale.json',dict(originalInterior=[768,512],r6World=[768,608],world=[1024,896],offset=[128,96],pixelExactInteriorOutsideChairCorrections=True,wokaScale=1,nativeSpriteFrame=[32,32],architectureRescaled=False,liveScreenshot=False))
files=[dict(path=str(p.relative_to(P)),sha256=H(p),bytes=p.stat().st_size) for p in sorted((P/'map32').iterdir())]
W(P/'MANIFEST.json',dict(title='Resonance Media House',revision='r07c-ground-clearance-delta',world=[1024,896],interiorWorld=[768,512],nativeTileSize=32,wokaScale=1,visualSeats=10,anchors=len(J(P/'source/layout.json')['anchors']),runtime=files,preservation=pres,geometry={k:v for k,v in geo.items() if k!='anchors'},nativeRoutes={k:v for k,v in routes.items() if k!='rows'},spawnDomains=spawn,preview='review/native-arrival-occupied.png',delta=J(P/'validation/r7c-delta.json'),nativeArrivalProof=J(P/'validation/native-arrival-proof.json'),chairDepth=J(P/'validation/chair-depth-check.json'),decodedProof=J(P/'validation/decoded-runtime-proof.json'),status=dict(compiled=True,staticValidated=True,nativeRouteReplay=True,livePlaytest=False,published=False,externalServicesConfigured=False,independentReview='pending')))
# Remove superseded comparison and stale revision freeze; r6 remains separately preserved.
for name in ['review/before-after-native100.png','FREEZE.json']:
 p=P/name
 if p.exists():p.unlink()
with zipfile.ZipFile(D/'resonance-media-house-r7c-runtime.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((P/'map32').iterdir()):z.write(p,p.name)
with zipfile.ZipFile(D/'resonance-media-house-r7c-source-replay.zip','w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['tools','source','resonance-media-house','r6-preserved']:
  for p in sorted((R/folder).rglob('*')):
   if not p.is_file() or p.suffix=='.zip' or '__pycache__' in p.parts:continue
   rel=str(p.relative_to(R))
   if folder=='r6-preserved' and rel not in ['r6-preserved/source/layout.json','r6-preserved/source/runtime-base.png','r6-preserved/source/runtime-above.png','r6-preserved/review/empty-native.png']:continue
   if folder=='source' and not (p.name in ['media-environment-clean-seats-master.png','greg-reference.png','industrial-chair40-native.png','congress-low-table.png','screen-chair.png','listening-chair-east.png','keyboard-stool.png','r7-exterior-generated.png','r7b-path-repair-master.png','r7b-preserved-south-entry-strip.png','r7-generation-prompts.json','r7b-generation-spec.json'] or p.name.startswith('chair-lowback-') or 'proof-inputs' in p.parts):continue
   z.write(p,p.relative_to(R))
shutil.copy2(P/'review/native-arrival-occupied.png',D/'resonance-media-house-r7c-native-arrival-occupied.png')
shutil.copy2(P/'review/actual-native-arrivals.png',D/'resonance-media-house-r7c-actual-native-arrivals.png')
shutil.copy2(P/'review/intended-config-occupied.png',D/'resonance-media-house-r7c-intended-config-facing.png')
W(D/'resonance-media-house-r7c-checks.json',dict(geometry=geo['allPass'],nativeRoutes=routes['allPass'],routeLegs=routes['legs'],movementSamples=routes['samples'],spawn=spawn['allPass'],preservation=pres,files=[dict(name=p.name,sha256=H(p),bytes=p.stat().st_size) for p in sorted(D.iterdir()) if p.is_file() and not p.name.endswith('-checks.json')]))
print(json.dumps(dict(deliverables=str(D),routeLegs=routes['legs'],samples=routes['samples'],anchors=len(geo['anchors']),floorCells=geo['walkableCells']),indent=2))
