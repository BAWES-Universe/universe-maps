from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, hashlib, shutil

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/'art-source/landscape-original.png'
EDIT=ROOT/'art-source/landscape-alpha-extraction.png'
src=Image.open(EDIT).convert('RGBA')
entries=[
 ('olive',(0,0,545,518),(160,160)),
 ('fountain',(545,0,1016,501),(192,192)),
 ('garden',(1016,0,1536,503),(128,96)),
 ('booth-navy',(0,518,520,1024),(128,128)),
 ('booth-teal',(520,518,1016,1024),(128,128)),
 ('willow',(1016,503,1536,1024),(128,160)),
]
manifest={
 'generator':'OpenAI built-in image_gen; no paid external providers or third-party sprite sources',
 'source_dimensions':[1536,1024],
 'source_files':['art-source/landscape-original.png','art-source/landscape-alpha-extraction.png'],
 'edit_prompt':'Use case: background-extraction. Asset type: original game prop sprite atlas with genuine PNG RGBA transparency. Edit the supplied image ONLY to remove the entire colored gradient backdrop and all floor/background shadows. Retain the exact six objects and their original detail, shapes, colors, warm limestone/teal/navy/brass fantasy courtyard style and spacing. Object order remains olive tree, fountain, flower garden above navy market booth, teal market booth, willow tree. All empty areas between and around objects, between leaves and branches and under canopies must have alpha zero. Preserve natural edge alpha and only actual fountain water. Do not paint white, black, checkerboard or colored background. Output ACTUAL TRANSPARENT PNG alpha channel. Do not add labels, frames, extra scenery or any new objects.',
 'transparency_notes':'Source and extraction PNGs contain genuine generated RGBA alpha. The dark RGB background in alpha-zero pixels is hidden data, not an opaque backdrop. No matte, color key, threshold mask, rectangular erasure or hand-authored alpha was applied.',
 'processing':'Per-object rectangular crop; alpha-visible bounding box determines trim with 2 source-pixel padding; size-normalized to the requested production content dimensions with 2 output-pixel margins; premultiplied-alpha LANCZOS downsample; centered horizontally and bottom-aligned. Source generated alpha is preserved.',
 'assets':[]
}
for name,region,size in entries:
 crop=src.crop(region)
 a=np.asarray(crop.getchannel('A'))
 ys,xs=np.where(a>10)
 bbox=(max(0,int(xs.min())-2),max(0,int(ys.min())-2),min(crop.width,int(xs.max())+3),min(crop.height,int(ys.max())+3))
 crop=crop.crop(bbox)
 crop.save(ROOT/f'art-source/landscape-crop-{name}.png')
 fitted=(size[0]-4,size[1]-4)
 resized=crop.convert('RGBa').resize(fitted,Image.Resampling.LANCZOS).convert('RGBA')
 out=Image.new('RGBA',size,(0,0,0,0))
 pos=((size[0]-fitted[0])//2,size[1]-fitted[1]-2)
 out.paste(resized,pos)
 path=ROOT/f'assets/outdoor-{name}.png';out.save(path)
 alpha=np.asarray(out.getchannel('A')); yy,xx=np.where(alpha>10)
 bb=[int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1]
 asset={
  'name':name,'file':f'assets/outdoor-{name}.png','canvas_size':list(size),
  'visible_alpha_over_10_bbox':bb,'visible_size':[bb[2]-bb[0],bb[3]-bb[1]],
  'anchor_bottom_center':[size[0]//2,bb[3]],
  'source_region':list(region),'source_trim_bbox':list(bbox),'source_crop_size':[crop.width,crop.height],
  'alpha_range':[int(alpha.min()),int(alpha.max())],
  'fully_transparent_pixel_count':int((alpha==0).sum()),
  'fully_transparent_fraction':float((alpha==0).mean()),
  'edge_alpha_max':int(max(alpha[0].max(),alpha[-1].max(),alpha[:,0].max(),alpha[:,-1].max())),
  'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 }
 manifest['assets'].append(asset)
(ROOT/'assets/outdoor-provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Composites below are QA inspection only; they are not delivered as transparent sprites.
w,h=1152,660
qa=Image.new('RGB',(w,h),'#1a252d');d=ImageDraw.Draw(qa)
try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
except OSError: font=ImageFont.load_default()
backgrounds=[('WARM LIMESTONE','#d2c4a3'),('TEAL GRASS','#426e59'),('DARK FLOOR','#172933')]
for r,(label,color) in enumerate(backgrounds):
 d.rectangle((0,r*220,w,(r+1)*220),fill=color)
 d.text((10,r*220+7),label,fill='#ffffff' if r else '#28332e',font=font)
 for c,(name,region,size) in enumerate(entries):
  im=Image.open(ROOT/f'assets/outdoor-{name}.png').convert('RGBA')
  x=c*192+(192-im.width)//2;y=r*220+220-im.height-22
  qa.paste(im,(x,y),im)
  d.text((c*192+9,r*220+199),name,fill='#ffffff' if r else '#28332e',font=font)
qa.save(ROOT/'art-source/landscape-native-size-qa.png')
print(json.dumps(manifest['assets'],indent=2))
