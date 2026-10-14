from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];S=R/'source-assets';O=R/'working';O.mkdir(exist_ok=True)
src=Image.open(S/'original-approved-concept.png').convert('RGBA');base=src.copy();patches=[]
def patch(name,box):
 global base
 im=Image.open(S/name).convert('RGBA');mask=Image.new('L',src.size);d=ImageDraw.Draw(mask);d.rectangle(box,fill=255)
 # Feather strictly inside documented rectangle. No pixels outside it change.
 a=np.array(mask);blur=np.array(mask.filter(ImageFilter.GaussianBlur(2)));a=np.minimum(a,blur);mask=Image.fromarray(a)
 base=Image.composite(im,base,mask);patches.append({'source':name,'bounds':list(box)})
patch('generated-two-desk-repair.png',(118,262,336,462))
patch('generated-empty-rugs.png',(413,393,688,642))
patch('generated-empty-rugs.png',(847,391,1130,642))
patch('generated-nook-empty-floor.png',(1200,276,1416,450))
base=base.resize((768,512),Image.Resampling.LANCZOS)
# Extend the existing round rug under the native-grid conversation arrangement.
rug=Image.open(S/'generated-empty-rugs.png').convert('RGBA').crop((1240,285,1404,418))
rm=Image.new('L',rug.size);ImageDraw.Draw(rm).ellipse((0,0,163,132),fill=255);rug.putalpha(rm)
rug=rug.resize((120,68),Image.Resampling.LANCZOS);base.alpha_composite(rug,(596,171))
# Keep the original bookcase pixels above the newly centered rug at their overlap.
original_native=src.resize((768,512),Image.Resampling.LANCZOS)
base.paste(original_native.crop((626,225,662,243)),(626,225))
above=Image.new('RGBA',base.size)
polys={
'nw':[(478,416),(487,413),(514,415),(518,419),(527,420),(525,447),(530,461),(524,479),(518,486),(513,487),(512,480),(483,483),(481,489),(476,487),(473,469),(469,453),(470,423)],
'ne':[(582,420),(590,417),(595,413),(621,415),(632,421),(636,448),(632,465),(630,486),(624,487),(622,481),(592,483),(590,488),(585,486),(582,470),(578,458),(581,444)],
'sw':[(472,530),(478,533),(480,538),(486,537),(494,533),(500,538),(506,550),(523,557),(530,557),(534,564),(531,580),(527,588),(527,600),(521,602),(519,593),(481,595),(480,602),(474,601),(474,581),(469,557)],
'se':[(638,530),(632,532),(630,539),(624,538),(616,534),(609,539),(603,548),(586,558),(580,560),(576,566),(579,584),(583,590),(583,600),(589,602),(592,594),(629,594),(631,601),(638,600),(640,579),(643,555)],
'table':[(516,474),(579,474),(588,479),(591,489),(590,541),(586,549),(580,550),(579,541),(523,541),(522,550),(516,549),(511,537),(512,483)],
'nook-left':[(1271,294),(1279,295),(1285,309),(1296,314),(1301,318),(1305,340),(1298,348),(1297,359),(1294,361),(1294,347),(1273,344),(1270,359),(1267,358),(1269,339),(1264,320),(1263,308)],
'nook-right':[(1382,295),(1374,297),(1366,311),(1358,315),(1356,322),(1353,340),(1359,348),(1360,360),(1364,361),(1364,348),(1384,344),(1387,359),(1390,357),(1388,338),(1392,320),(1394,308),(1390,299)],
'round-table':[(1310,296),(1320,293),(1339,294),(1355,301),(1360,313),(1362,325),(1356,336),(1341,341),(1338,363),(1335,363),(1334,342),(1324,351),(1318,356),(1315,354),(1326,341),(1310,336),(1303,326),(1302,313)]}
def asset(n,size=None):
 p=polys[n];m=Image.new('L',src.size);ImageDraw.Draw(m).polygon(p,fill=255);box=m.getbbox();a=src.crop(box);a.putalpha(m.crop(box));size=size or (round(a.width/2),round(a.height/2));return a.resize(size,Image.Resampling.LANCZOS),box
records=[]
def place(n,xy,size=None,fg_y=None):
 a,b=asset(n,size);base.alpha_composite(a,xy)
 if fg_y is not None:
  mask=Image.new('L',a.size);ImageDraw.Draw(mask).rectangle((0,max(0,fg_y-xy[1]),a.width,a.height),fill=255);aa=a.copy();aa.putalpha(Image.fromarray(np.minimum(np.array(a.getchannel('A')),np.array(mask))));above.alpha_composite(aa,xy)
 records.append({'asset':n,'source_bounds':b,'destination':list(xy),'size':list(a.size),'foreground_min_y':fg_y})
for x in [-4,220]:
 place('nw',(234+x,206));place('ne',(290+x,206));place('sw',(233+x,264),fg_y=278);place('se',(288+x,264),fg_y=278)
place('table',(258,241),(28,29));place('table',(482,241),(28,29))
# Two opposing chairs at the southeast portion of original round-rug nook.
# Exact native proof anchors are calibrated separately; these are art positions.
place('nook-left',(598,187),(34,36),fg_y=206)
place('nook-right',(681,187),(34,36),fg_y=206)
place('round-table',(641,188),(29,35))
# Remove foreground pixels from base so recomposition is byte-exact.
a=np.array(base);hi=np.array(above);a[hi[:,:,3]>0]=0;lo=Image.fromarray(a)
# Fractional edge alpha layers require retaining original under-colour; cut only opaque above pixels.
a=np.array(base);a[hi[:,:,3]==255]=0;lo=Image.fromarray(a)
# Use original composited pixels for every masked foreground point to avoid double alpha.
full=np.array(base);fm=hi[:,:,3]>0;high=np.zeros_like(full);high[fm]=full[fm];low=full.copy();low[fm]=0;lo=Image.fromarray(low);above=Image.fromarray(high)
assert Image.alpha_composite(lo,above).tobytes()==base.tobytes()
base.save(O/'art-native.png');lo.save(O/'base.png');above.save(O/'above.png');(O/'ART-PLACEMENTS.json').write_text(json.dumps({'patches':patches,'furniture':records,'source_uniform_scale':.5,'original_sha256':hashlib.sha256((S/'original-approved-concept.png').read_bytes()).hexdigest()},indent=2))
