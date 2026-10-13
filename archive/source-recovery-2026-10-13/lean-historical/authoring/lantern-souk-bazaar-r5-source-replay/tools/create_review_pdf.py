from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
from reportlab.lib.utils import ImageReader
from PIL import Image
from io import BytesIO
def compact(path):
 b=BytesIO();Image.open(path).convert("RGB").save(b,format="JPEG",quality=88,optimize=True);b.seek(0);return ImageReader(b)
R=Path(__file__).resolve().parents[1];P=R/'lantern-souk-bazaar-r5';out=P/'Lantern-Souk-Bazaar-r5-review.pdf'
c=canvas.Canvas(str(out),pagesize=(960,700));c.setTitle('Lantern Souk Bazaar | Panorama and Seating Review')
def page(title,sub):
 c.setFillColor(HexColor('#112729'));c.rect(0,0,960,700,fill=1,stroke=0);c.setFillColor(HexColor('#f6dfab'));c.setFont('DVB',23);c.drawString(30,659,title);c.setFillColor(HexColor('#d0ddd9'));c.setFont('DV',10);c.drawString(30,639,sub)
page('Lantern Souk Bazaar','r5 | Unlabelled courtyard, wider city panorama, opposing seats')
c.drawImage(compact(P/'review/empty-native.png'),30,32,width=900,height=600,mask='auto');c.showPage()
page('Two seats, face to face','Two different repository Wokas, native 32px sprites. Both seats and entry/exit routes covered by replay.')
c.drawImage(compact(P/'review/opposed-seats-3x.png'),30,171,width=900,height=900*480/1008,mask='auto')
c.setFillColor(HexColor('#d0ddd9'));c.setFont('DV',12)
for i,t in enumerate(['Original carpet and courtyard preserved outside the three furniture placements.','Labels and preset demo areas removed; owners can label their own spaces.','1,318 native route legs passed; 2,158,184 movement samples, zero failures.','Native source replay and static visual QA only. Live room and multi-user tests remain separate.']):c.drawString(30,139-i*23,t)
c.setFont('DV',8);c.drawString(30,28,'Review sprites: Pipoya 32x32, from BAWES-Universe/workadventure-universe. No characters are baked into the runtime map.')
c.save();print(out)
