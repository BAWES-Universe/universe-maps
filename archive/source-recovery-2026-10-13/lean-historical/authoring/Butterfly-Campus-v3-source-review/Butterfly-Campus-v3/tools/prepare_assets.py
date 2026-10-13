from PIL import Image
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
# Hand-inspected object boxes; padding is independent of artwork scale.
furniture=[('meeting_table',(16,108,373,332),(128,76)),('desk',(386,128,676,330),(64,44)),('teacher',(692,136,907,333),(56,48)),('reception',(912,96,1247,340),(144,104)),('chair_s',(104,388,273,632),(26,38)),('chair_n',(420,407,607,622),(28,34)),('chair_e',(775,383,930,632),(24,38)),('chair_w',(1022,383,1175,632),(24,38)),('couch_s',(12,661,406,890),(96,56)),('couch_n',(413,694,756,874),(96,50)),('couch_e',(792,651,968,890),(40,56)),('couch_w',(994,651,1170,890),(40,56)),('rug',(12,932,489,1200),(224,128)),('coffee',(530,945,764,1196),(48,48)),('lamp',(816,918,942,1195),(24,56)),('plant',(988,935,1245,1192),(48,48))]
architecture=[('bookshelf',(100,28,660,316),(192,96)),('window',(776,8,1157,335),(96,80)),('double_door',(132,330,636,630),(192,112)),('door',(824,341,1109,621),(128,128)),('workbench',(114,649,725,929),(160,72)),('podium',(893,638,1111,923),(40,56)),('planter',(159,973,676,1215),(96,48)),('streetlamp',(936,918,1050,1245),(32,96))]
manifest=[]
for sheet,specs in [('furniture',furniture),('architecture',architecture)]:
 im=Image.open(R/'art-source'/f'{sheet}-original.png').convert('RGBA')
 for name,box,size in specs:
  a=im.crop(box); b=a.getchannel('A').getbbox(); a=a.crop(b)
  a.thumbnail(size,Image.Resampling.LANCZOS)
  a.save(R/'assets'/f'{name}.png')
  manifest.append({'name':name,'source':f'art-source/{sheet}-original.png','sourceBox':box,'sourcePixels':list(a.size) if False else [b[2]-b[0],b[3]-b[1]],'worldPixels':list(a.size),'operation':'single downsample; no upscale'})
json.dump(manifest,open(R/'docs/asset-manifest.json','w'),indent=2)
