from pathlib import Path
from PIL import Image
import json,io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader as RawReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
r=Path(__file__).resolve().parents[1];m=r/'mission-control-center';out=Path('/workspace/scratch/41c8dbf833be/mission-r3-delivery');out.mkdir(exist_ok=True)
l=json.loads((m/'source/layout.json').read_text());proof=Image.open(r/'geometry-checks/mission-control-center/decoded-below.png').convert('RGBA');fg=Image.open(r/'geometry-checks/mission-control-center/decoded-above.png').convert('RGBA')
routes=json.loads((m/'NATIVE-ROUTES.json').read_text())['rows']
for i,s in enumerate(l['seats'][:6]):
 w=Image.open(r/'source-assets'/f'woka-proof-{i}.png').convert('RGBA');x,y=next(row['final'] for row in routes if row['name']==s['name']+' same-cell');x,y=round(x),round(y);proof.alpha_composite(w.crop((32,96,64,128)),(x-16,y-16))
proof.alpha_composite(fg);full=proof.crop((384,576,1152,864));full.resize((1536,576),Image.Resampling.NEAREST).save(out/'Mission-Control-r3-six-operators-2x.png')
contact=Image.new('RGBA',(400,264),'#101923')
for i,s in enumerate(l['seats'][:6]):
 x,y=s['anchor'];crop=proof.crop((x-64,y-96,x+64,y+32));contact.alpha_composite(crop,((i%3)*136,(i//3)*136))
contact.resize((1200,792),Image.Resampling.NEAREST).save(out/'Mission-Control-r3-six-console-details-3x.png')
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('DV-B','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
def ir(p):
 b=io.BytesIO();Image.open(p).convert('RGB').save(b,format='JPEG',quality=88,optimize=True);b.seek(0);return RawReader(b)
c=canvas.Canvas(str(out/'Mission-Control-r3-review.pdf'),pagesize=(900,1000))
def header(t,sub):
 c.setFillColorRGB(.06,.10,.14);c.rect(0,0,900,1000,fill=1,stroke=0);c.setFillColorRGB(.87,.73,.42);c.setFont('DV-B',23);c.drawString(32,955,t);c.setFillColorRGB(.86,.90,.94);c.setFont('DV',11);c.drawString(32,932,sub)
header('Mission Control | Console alignment','Only the six operator chairs change. Approved sky, setting and briefing area are preserved.')
c.drawImage(ir(m/'review/empty-native.png'),32,120,width=836,height=766.33);c.drawString(32,82,'Chairs are aligned with native tap arrivals and tucked into their consoles working positions.');c.drawString(32,62,'Static runtime-atlas review. Live multi-user and AV tests remain separate.');c.showPage()
header('Six consoles | Six actual Wokas','Actual tested tap-arrival positions, reconstructed with six different native Wokas.')
c.drawImage(ir(out/'Mission-Control-r3-six-console-details-3x.png'),32,325,width=836,height=551.76)
c.setFont('DV',12)
for y,t in [(270,'Existing standing idle sprites are shown. No new seated pose or animation is implied.'),(245,'All six tested native tap arrivals now match the chair centers.'),(220,'The two middle chairs sit within keyboard width at the native fitted position. No engine change.'),(180,'Runtime-atlas reconstruction of native route endpoints, not a live gameplay screenshot.')]:c.drawString(32,y,t)
c.save()
