from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
D=Path(__file__).parent
c=canvas.Canvas(str(D/'Reading-Conservatory-r1-review.pdf'),pagesize=(1120,840))
c.setTitle('Reading Conservatory | New map concept r1')
c.setAuthor('Universe')
c.setFillColor(HexColor('#F5F1E7'));c.rect(0,0,1120,840,fill=1,stroke=0)
c.setFillColor(HexColor('#24493D'));c.setFont('Sans-Bold',26);c.drawString(40,792,'Reading Conservatory')
c.setFont('Sans',12);c.drawString(40,768,'A new Knowledge + Social room direction: quiet study, mentorship and small reading groups')
c.setFillColor(HexColor('#867140'));c.setFont('Sans-Bold',10);c.drawRightString(1080,796,'VISUAL CONCEPT / R1')
c.drawImage(str(D/'Reading-Conservatory-r1-concept.png'),40,62,width=1040,height=693.333,mask='auto')
c.setFillColor(HexColor('#43564B'));c.setFont('Sans',9)
c.drawString(40,42,'Proposed Art Nouveau theme. New artwork, not a working map. No runtime, seating-depth or native32 occupied proof yet.')
c.drawRightString(1080,24,'11 October 2026 / 1')
c.showPage()
c.setFillColor(HexColor('#F5F1E7'));c.rect(0,0,1120,840,fill=1,stroke=0)
c.setFillColor(HexColor('#24493D'));c.setFont('Sans-Bold',26);c.drawString(40,792,'A room for slower conversations')
c.setFont('Sans',12);c.drawString(40,767,'Different from a classroom or presentation hall: small groups, quiet desks and an obvious open arrival.')
c.drawImage(str(D/'Reading-Conservatory-r1-concept.png'),40,270,width=735,height=490,mask='auto')
x=803;y=720
for title,lines in [
 ('Two reading circles',['Two groups of four matching armchairs.','Seats turn inward toward low tables.']),
 ('Quiet study corner',['Four individual desks in the northwest.','A separate two-person mentorship nook.']),
 ('Coherent material palette',['Pale limestone, jade ironwork, oak,','ochre upholstery and botanical mosaic.']),
 ('Complete setting',['Garden scenery above and at both sides.','A clear, wide southern entrance.'])]:
 c.setFillColor(HexColor('#24493D'));c.setFont('Sans-Bold',13);c.drawString(x,y,title);y-=23
 c.setFont('Sans',10);c.setFillColor(HexColor('#43564B'))
 for line in lines:c.drawString(x,y,line);y-=16
 y-=30
c.setFillColor(HexColor('#E7E7D9'));c.roundRect(40,74,1040,164,9,fill=1,stroke=0)
c.setFillColor(HexColor('#24493D'));c.setFont('Sans-Bold',14);c.drawString(60,212,'What this review establishes')
c.setFont('Sans',11)
for yy,line in [(188,'A proposed visual direction within the original Knowledge / Social template families. This exact theme is a new suggestion.'),(165,'The empty artwork is ready for style review. Native32 is the implementation target; authentic occupied scale is still unproven.'),(142,'A working map still needs furniture-footprint, entry/exit, collision, spawn, foreground-depth and native-route checks.'),(119,'No TMJ/WAM, automatic sitting, facing, media configuration, hosting or live browser/device testing is included.'),(96,'Earlier map versions are preserved. This concept has not been published to GitHub.')]:c.drawString(60,yy,line)
c.setFillColor(HexColor('#43564B'));c.setFont('Sans',9);c.drawString(40,42,'Artwork generated with built-in image generation. Original prompt retained with the concept source.')
c.drawRightString(1080,24,'11 October 2026 / 2')
c.save()
