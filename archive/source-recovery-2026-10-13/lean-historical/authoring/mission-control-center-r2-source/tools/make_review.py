from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader as RawImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from pathlib import Path
import io
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
def image(p):
 b=io.BytesIO();Image.open(p).convert('RGB').save(b,format='JPEG',quality=88,optimize=True);b.seek(0);return RawImageReader(b)
r=Path('/workspace/shared/mission-control-sky-seats-r2/mission-control-center/review');dest='/workspace/scratch/41c8dbf833be/mission-control-delivery/Mission-Control-r2-review.pdf';c=canvas.Canvas(dest,pagesize=(900,1000))
def header(title,sub):
 c.setFillColorRGB(.06,.10,.14);c.rect(0,0,900,1000,fill=1,stroke=0);c.setFillColorRGB(.87,.73,.42);c.setFont('DejaVu-Bold',23);c.drawString(32,955,title);c.setFillColorRGB(.85,.9,.95);c.setFont('DejaVu',11);c.drawString(32,932,sub)
header('Mission Control | View and seating','Completed upper wall and night view; context-matched chair orientation.')
c.drawImage(image(r/'empty-native.png'),32,120,width=836,height=766.33);c.setFont('DejaVu',11);c.drawString(32,82,'Original interior preserved at1:1 scale except the eight chair footprints. No new audio added.');c.drawString(32,62,'Static compiled-map render. Live room, AV and multi-user checks remain separate.');c.showPage()
header('Occupied chair checks','Eight varied repository Wokas, original native32 idle frames, no invented sitting poses.')
c.setFillColorRGB(.87,.73,.42);c.setFont('DejaVu-Bold',16);c.drawString(32,892,'Operators face their consoles');c.drawImage(image(r/'operators-occupied-native.png'),32,555,width=836,height=313.5)
c.drawString(32,518,'Briefing seats face each other');c.drawImage(image(r/'briefing-occupied-native.png'),32,178,width=672,height=313.6)
c.setFillColorRGB(.85,.9,.95);c.setFont('DejaVu',11);c.drawString(32,128,'All chairs retain full silhouettes and caster bases. Operator anchors are14px closer to the desks.');c.drawString(32,108,'480 native route legs; zero body collisions. All reachable head positions tested against nine sprite sheets.');c.drawString(32,88,'Native walk-to visual seating remains unchanged; furniture direction is authored, not a new player action.');c.save();print(dest)
