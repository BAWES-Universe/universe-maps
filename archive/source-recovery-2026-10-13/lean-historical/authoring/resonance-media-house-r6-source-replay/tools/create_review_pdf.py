from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';out=R/'output/pdf/resonance-media-house-r6-review.pdf'
C=canvas.Canvas(str(out),pagesize=(832,760));C.setTitle('Resonance Media House - native-scale review')
def header(n,sub):
 C.setFillColorRGB(.075,.14,.15);C.rect(0,0,832,760,fill=1,stroke=0);C.setFillColorRGB(.95,.89,.72);C.setFont('Helvetica-Bold',20);C.drawString(32,724,'RESONANCE MEDIA HOUSE');C.setFont('Helvetica',10);C.setFillColorRGB(.78,.84,.82);C.drawString(32,705,sub);C.setFont('Helvetica',8);C.drawRightString(800,18,f'{n} / 2 | Static source proof. Not a live room screenshot.')
header(1,'Human-scale studios | 10 occupied seats | 96px of natural north context | no baked labels')
C.drawImage(str(P/'review/occupied-native.png'),32,80,width=768,height=608,mask='auto');C.setFont('Helvetica',9);C.drawString(32,60,'768 x 608 world. Unchanged 32 x 32 repository Wokas. Image embedded at one source pixel per PDF point.')
C.drawString(32,44,'Standing frames show placement and facing; they do not claim a seated animation. Viewer fit-to-page may resize the page.')
C.showPage();header(2,'Before / after at the same native image scale: architecture changed, avatars did not')
old=Image.open('/workspace/shared/overnight-social-media/resonance-media-house/review/occupied-native.png').convert('RGB');new=Image.open(P/'review/occupied-native.png').convert('RGB')
C.setFillColorRGB(.95,.89,.72);C.setFont('Helvetica-Bold',11);C.drawString(32,676,'BEFORE: original editor bay crop, native 100%');C.drawImage(ImageReader(old.crop((96,16,800,240))),64,438,width=704,height=224)
C.drawString(32,416,'AFTER: revised editor bay and voice-room edge, native 100%');C.drawImage(ImageReader(new.crop((32,112,736,336))),64,178,width=704,height=224)
C.setFillColorRGB(.78,.84,.82);C.setFont('Helvetica',9.5)
for y,t in [(150,'Interior world: 1536 x 1024 -> 768 x 512. Added north context makes the final world 768 x 608.'),(135,'Distinct editor task chairs, charcoal viewing chairs, backless keyboard stools and opposed listening chairs.'),(120,'Native source checks: 666 route legs, audited movement samples, zero failures; all 17 anchors reachable.'),(105,'Boundary probe placements; conservative spawn-domain checks pass. Review assets use varied real Wokas.'),(90,'Source replay reproduces runtime files and occupied proof byte-for-byte. Original r03 hashes remain unchanged.'),(65,'Runtime TMJ/WAM and source ZIP supplied separately. Raw Pipoya sheets are excluded; local repo lookup is documented.'),(50,'Media services remain unconfigured. No engine changes, publication, live gameplay or new paid service is claimed.')]:C.drawString(32,y,t)
C.save();print(out)
