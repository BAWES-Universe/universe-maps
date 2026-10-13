from pathlib import Path
import json,hashlib,zipfile,shutil,subprocess
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_text());write=lambda p,o:p.write_text(json.dumps(o,indent=2)+'\n')
files=[]
for p in sorted((P/'map32').iterdir()):files.append(dict(path=str(p.relative_to(P)),sha256=H(p),bytes=p.stat().st_size))
repo=Path('/workspace/shared/native32-replan-baseline/play/public/resources/characters/pipoya');names=sorted(set(a['sheet'] for a in J(P/'review/occupants.json')))
write(P/'validation/woka-provenance.json',dict(repoCommit='90a148c03e03401e26d236eaac9bea4123b42c57',sourcePath='play/public/resources/characters/pipoya',files=[dict(name=n,sha256=H(repo/n),frameDimensions=[32,32]) for n in names],runtimeContainsAvatars=False,standaloneSheetsRedistributed=False,pose='Actual unchanged native standing animation frame 1 in appropriate cardinal row; not invented seated art',foregroundPixels=0,headTest='No above-player pixels exist; all displayed native upper-head pixels are clear of foreground. Architectural tangency evidence separately supplied.'))
(P/'README.md').write_text('''# Resonance Media House r4 — human-scale derivative

Original r03 remains immutable. Runtime is an actual768×608 world (24×19 native32 tiles), containing the approved768×512 interior plus96px natural north context, rather than1536×1024. WokaScale stays1 and every review frame is an unchanged32×32 repository frame. Desks, architecture and room spacing are genuinely smaller. No camera trick or enlarged people.

10 seats:3 editor task chairs,3 charcoal screen chairs,2 musician stools,2 opposed wood/steel listening chairs. A compact wood table serves the listening pair. Microphone and front joinery are refit to the smaller tile-aligned clearances. Occupied previews use standing frames at seating anchors, not a claimed seated animation or live screenshot.

## Verify/rebuild
From source root: python tools/rebuild.py; python tools/check_spawn_and_boundaries.py resonance-media-house; node tools/native/route-audit.cjs resonance-media-house.
Python requires Pillow and NumPy; Node uses bundled extracted native fixture/EasyStar. Set WOKA_REPO to the local authorized WorkAdventure source checkout for native review occupants. Raw Pipoya sheets are not redistributed; source lookup/hash/license metadata is included. Runtime rebuild and review rendering are deterministic with the documented local dependencies.

## Scope
Static source-derived geometry, compiled atlas, spawn domains and native-route fixture checks only. No live browser room, keyboard/physics/device/network testing or publication. Imagine, recording, music and screen integration placeholders remain unconfigured; no new service, credentials or paid API. No engine edits. WAM companion is not automatically imported by Custom TMJ; use a new test room and configure deliberately.
''')
(P/'PROVENANCE.md').write_text('''# Source provenance

Architecture: derivative of original project-generated Media House r03 clean-seats master, resized in actual world coordinates. Source master and exact deterministic authored re-fit operations are bundled. Editor task chair and compact wood table are existing project-generated assets. Charcoal screen chair, wood/steel listening chair and musician stool were generated with built-in image generation for this task on2026-10-11; the immutable generated asset sheet and extracted native assets are supplied. No external paid service was introduced.

Review-only Wokas: actual unchanged Pipoya repository sheets,32×32 frames, source checkout90a148c03e03401e26d236eaac9bea4123b42c57, catalog/hash record in validation/woka-provenance.json. Pipoya standalone sheets are excluded from both ZIPs. Read source about.txt for applicable terms. Repo assets are external local inputs for regenerating previews; rendered occupied map evidence is supplied. No Woka is baked into the runtime atlases.

Native movement validation reuses the source-extracted engine methods pinned60e7afdc and EasyStar0.4.4 from the original package. It does not modify the engine and does not constitute live gameplay.
''')
shutil.copy2(repo/'about.txt',P/'validation/PIPOYA-LICENSE.txt')
geo=J(P/'validation/geometry.json');routes=J(P/'validation/native-routes.json');spawn=J(P/'validation/spawn-domains.json');assert geo['allPass'] and routes['allPass'] and spawn['allPass']
write(P/'MANIFEST.json',dict(title='Resonance Media House',revision='r06-fixture-footprint-pass',world=[768,608],interiorWorld=[768,512],northContextHeight=96,originalWorld=[1536,1024],nativeTileSize=32,wokaScale=1,visualSeats=10,anchors=17,runtime=files,geometry={k:v for k,v in geo.items() if k!='anchors'},nativeRoutes={k:v for k,v in routes.items() if k!='rows'},spawnDomains=spawn,preview='review/occupied-native.png',status=dict(compiled=True,staticValidated=True,nativeRouteReplay=True,livePlaytest=False,published=False,externalServicesConfigured=False,independentReview='pending')))
# Keep both images at1 source pixel per output pixel, explicitly unlike fitting to equal frame sizes.
old=Image.open('/workspace/shared/overnight-social-media/resonance-media-house/review/occupied-native.png').convert('RGB');new=Image.open(P/'review/occupied-native.png').convert('RGB')
comparison=Image.new('RGB',(1568,1744),'#172626');comparison.paste(old,(16,40));comparison.paste(new,(16,1110));d=ImageDraw.Draw(comparison);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
d.text((16,12),'BEFORE:1536×1024 actual world; unchanged32px avatar frames',font=font,fill='white');d.text((16,1080),'AFTER:768×608 actual world including96px added north context; unchanged32px repository Woka frames — both images1:1',font=font,fill='white');comparison.save(P/'review/before-after-native100.png')
with zipfile.ZipFile(P/'resonance-media-house-runtime.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((P/'map32').iterdir()):z.write(p,p.name)
with zipfile.ZipFile(P/'resonance-media-house-source-replay.zip','w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['tools','source','resonance-media-house']:
  for p in sorted((R/folder).rglob('*')):
   if not p.is_file() or p.suffix=='.zip' or p.name=='FREEZE.json' or '__pycache__' in p.parts:continue
   if p.name.startswith('Female ') or p.name.startswith('Male '):continue
   z.write(p,p.relative_to(R))
write(P/'FREEZE.json',dict(revision='r06-fixture-footprint-pass',manifestSHA256=H(P/'MANIFEST.json'),runtimeZipSHA256=H(P/'resonance-media-house-runtime.zip'),sourceZipSHA256=H(P/'resonance-media-house-source-replay.zip'),immutableUntilExplicitRevision=True))
print((P/'FREEZE.json').read_text())
