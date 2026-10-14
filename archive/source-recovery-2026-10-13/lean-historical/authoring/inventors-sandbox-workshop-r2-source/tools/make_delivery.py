from pathlib import Path
from PIL import Image
import io,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];M=R/'inventors-sandbox-workshop';O=Path('/workspace/scratch/41c8dbf833be/workshop-r2-delivery');O.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('DV',str(R/'source-assets/DejaVuSans.ttf')));pdfmetrics.registerFont(TTFont('DVB',str(R/'source-assets/DejaVuSans-Bold.ttf')))
def ir(p):
 b=io.BytesIO();Image.open(p).convert('RGB').save(b,format='JPEG',quality=90,optimize=True);b.seek(0);return ImageReader(b)
c=canvas.Canvas(str(O/'Inventors-Workshop-r2-review.pdf'),pagesize=(900,1000))
def head(title,sub):
 c.setFillColorRGB(.10,.15,.12);c.rect(0,0,900,1000,fill=1,stroke=0);c.setFillColorRGB(.91,.75,.44);c.setFont('DVB',23);c.drawString(32,955,title);c.setFillColorRGB(.93,.92,.84);c.setFont('DV',11);c.drawString(32,931,sub)
def line(y,t):c.setFont('DV',11);c.drawString(32,y,t)
head('Inventor’s Workshop | Native-scale revision','Brick, brass, green and oak, with a usable south courtyard and connected garden destinations.')
c.drawImage(ir(M/'review/empty-native.png'),32,260,width=836,height=627)
for y,t in [(220,'Six indoor workbench places, four collaboration places and two outdoor workbench places.'),(198,'Three creation pads remain open. North, west and south doorways are visibly walkable.'),(176,'The new northern garden landing provides usable headroom beyond the workshop wall.'),(132,'Native32 runtime map. No baked text, service activation, new audio or engine modification.'),(110,'Tools, boards and testing pads are decorative/editor-ready destinations.')]:line(y,t)
c.showPage()
head('All 12 places | Actual native tap arrivals','Runtime-atlas reconstruction with varied existing Wokas at tested movement endpoints.')
c.drawImage(ir(M/'review/actual-tap-all-12-native.png'),32,260,width=836,height=627)
for y,t in [(218,'Every authored tap lands exactly on its stool/body anchor.'),(196,'Native32 standing idle sprites show scale and occupancy. No new sitting animation is implied.'),(152,'All main indoor/outdoor destinations have native route coverage; substantial table art is solid.'),(130,'These are static reconstructions, not live browser or multi-user AV screenshots.')]:line(y,t)
c.showPage()
head('Furniture details | Empty and occupied','Empty view on the left; actual native tap-arrival occupancy on the right.')
for title,name,y,w in [('Indoor bench','indoor-bench',610,748),('Collaboration nook','collaboration',310,700),('Courtyard bench','courtyard-bench',40,560)]:
 p=M/'review'/(name+'-empty-occupied-3x.png');im=Image.open(p);h=w*im.height/im.width;c.setFont('DVB',13);c.drawString(32,y+h+12,title);c.drawImage(ir(p),32,y,width=w,height=h)
c.showPage();c.save()
for src,dest in [('actual-tap-all-12-native.png','Inventors-Workshop-r2-all-12-occupied.png'),('indoor-bench-empty-occupied-3x.png','Inventors-Workshop-r2-bench-detail.png'),('collaboration-empty-occupied-3x.png','Inventors-Workshop-r2-collaboration-detail.png'),('courtyard-bench-empty-occupied-3x.png','Inventors-Workshop-r2-courtyard-detail.png')]:shutil.copy2(M/'review'/src,O/dest)
for kind in ['runtime','source']:shutil.copy2(R/f'inventors-sandbox-workshop-r2-{kind}.zip',O/f'inventors-sandbox-workshop-r2-{kind}.zip')
print(O, (O/'Inventors-Workshop-r2-review.pdf').stat().st_size)
