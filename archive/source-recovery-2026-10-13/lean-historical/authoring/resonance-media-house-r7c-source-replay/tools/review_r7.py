from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';D=R/'deliverables';D.mkdir(exist_ok=True)
g=json.loads((P/'validation/geometry.json').read_text());n=json.loads((P/'validation/native-routes.json').read_text())
c=canvas.Canvas(str(D/'resonance-media-house-r7c-review.pdf'),pagesize=(1088,1060));c.setTitle('Resonance Media House r7c - Expanded garden court')
def page(num,sub,image):
 c.setFillColorRGB(.06,.11,.12);c.rect(0,0,1088,1060,fill=1,stroke=0);c.setFillColorRGB(.96,.89,.72);c.setFont('Helvetica-Bold',23);c.drawString(32,1023,'RESONANCE MEDIA HOUSE / r7c');c.setFont('Helvetica',12);c.drawString(32,1000,sub);c.drawImage(str(image),32,88,width=1024,height=896,mask='auto');c.setFillColorRGB(.77,.84,.81);c.setFont('Helvetica',10);c.drawString(32,64,'1024 x 896 world. Native32 avatars unchanged. Artwork shown at one source pixel per PDF point.');c.drawString(32,47,'Static source evidence only. Live gameplay, keyboard physics and service integrations remain untested.');c.drawRightString(1056,24,f'{num} / 5');c.showPage()
page(1,'Actual native click arrivals; facing follows the path. No automatic turn toward the station.',P/'review/native-arrival-occupied.png')
page(2,'Collision audit: tinted cells are blocked; clear outdoor routes connect around the building.',P/'review/collision-native.png')
c.setPageSize((1088,760));c.setFillColorRGB(.06,.11,.12);c.rect(0,0,1088,760,fill=1,stroke=0);c.setFillColorRGB(.96,.89,.72);c.setFont('Helvetica-Bold',23);c.drawString(32,720,'PRESERVATION + VALIDATION');c.setFillColorRGB(.78,.85,.82);c.setFont('Helvetica',13)
lines=['Canvas: r6 768 x 608 -> r7 1024 x 896; added 128px each side, 96px north and 192px south.','R7c opens 12 courtyard cells and 3 viewer gaps; four inherited seat assets now match native-fit-stable arrivals.','Rear wall is also exact. North exterior foliage and equipment were adjusted for a usable passage.','Interior is translated by (128,96), with six backrest and four native-arrival alignment corrections; quiet arrival retained.','Ten seat roles; six corrected backrests plus four arrival-aligned stools/listening chairs. Native32 frames and scale 1 remain.',f"Static geometry: {g['anchorCount']} reachable anchors; {g['walkableCells']} reachable floor cells; no body/head conflicts.",f"Native extracted-engine replay: {n['legs']} route legs, {n['samples']:,} movement samples, {n['failures']} failures.",'Click and touch routes, every admitted floor cell, ordered anchor pairs and endpoint edges checked.','Conservative Tiled and WAM spawn domains checked; quiet arrival remains isolated from social seats.','Runtime atlas roundtrip is pixel-exact. No avatar is baked into runtime textures.','No engine edits, publication, network service setup or paid integration.','Review Wokas are unchanged native standing frames: placement proof, not a seated animation.']
for i,line in enumerate(lines):c.drawString(32,678-i*28,line)
c.setFont('Helvetica-Bold',16);c.setFillColorRGB(.96,.89,.72);c.drawString(32,294,'Reproducible files')
c.setFont('Helvetica',12);c.setFillColorRGB(.78,.85,.82)
for i,line in enumerate(['Runtime ZIP: portable TMJ, WAM companion and generated native32 atlases.','Source replay ZIP: r6 preserved baseline, new exterior asset, deterministic build and native fixture.','Run: python3 tools/expand_r7.py; python3 tools/check_spawn_and_boundaries.py resonance-media-house','Then: node tools/native/route-audit.cjs resonance-media-house','Requires Python + Pillow/NumPy and Node.js. Native occupant composite is preserved in the source.']):c.drawString(32,261-i*25,line)
c.setFont('Helvetica',10);c.drawString(32,55,'Independent review status is recorded separately after the frozen package is inspected.');c.drawRightString(1056,24,'3 / 5');c.showPage()
c.setPageSize((1088,1060))
for num,fn,title,body in [(4,'actual-atlas-depth-probes.png','CORRECTED EXTERIOR PROBES','Current TMJ layers with genuine south/north native32 actors. Lamps removed; paths physically clear.'),(5,'inherited-chair-depth-probes.png','CORRECTED CHAIR DEPTH','Top: actual native arrivals. Bottom: intended north/south facing and admitted motion probes.')]:
 c.setFillColorRGB(.06,.11,.12);c.rect(0,0,1088,1060,fill=1,stroke=0);c.setFillColorRGB(.96,.89,.72);c.setFont('Helvetica-Bold',22);c.drawString(32,1016,title);c.setFont('Helvetica',11);c.drawString(32,988,body)
 from PIL import Image
 if num==5:
  c.drawImage(str(P/'review/actual-native-arrivals.png'),32,540,width=1024,height=409.6)
  c.drawImage(str(P/'review/chair-motion-extrema.png'),114,100,width=860,height=430)
 else:
  im=Image.open(P/'review'/fn);w,h=im.size;scale=min(1024/w,850/h);c.drawImage(str(P/'review'/fn),32,980-h*scale,width=w*scale,height=h*scale)
 c.setFont('Helvetica',10);c.drawString(32,62,'Art-boundary and independent acceptance remain separate from successful geometry and route tests.');c.drawRightString(1056,24,f'{num} / 5');c.showPage()
c.save()
