#!/usr/bin/env python3
"""Additive, original-pixel crops for sparse authored world canvases.

Does not alter any existing full previews or their manifest. Each crop is cut
from the complete t=0 source rendering before any scaling. No new artwork.
"""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('renderer',Path(__file__).with_name('render_previews.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
SPECS={
 'lighthouse-keepers-return-r2-runtime':[
  ('keeper-island','Island exterior',(0,0,1536,1024),'ground-and-objects layer bounds; foreground and authored inlays retained'),
  ('keeper-house','Keeper house (separate room)',(2304,256,2944,768),'keeper-house layer bounds; authored inlays retained'),
  ('keeper-workshop','Workshop (separate room)',(2304,1792,2944,2304),'lighthouse-workshop layer bounds; authored inlays retained'),
  ('keeper-lantern-room','Lantern room (separate room)',(256,2304,896,2816),'lantern-room layer bounds; authored inlays retained')],
 'butterfly-town-v2':[
  ('butterfly-town','Town area (cropped original view)',(2304,512,3840,1536),'town-ground and town-steady layer bounds; authored roof/foreground visibility retained'),
  ('butterfly-gate','Gate area (cropped original view)',(448,320,1600,1984),'gate-steady layer bounds expanded by 64 source pixels on each side')]
}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--full-manifest',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 full=json.loads(args.full_manifest.read_text());records={a['runtime_id']:a for a in full['maps']};crops=[]
 for mid,specs in SPECS.items():
  rec=records[mid]; tmj=args.root/Path(rec['source_tmj']['path']).relative_to(r.BASE)
  renderer=r.Renderer(tmj,args.root); im=renderer.render()
  assert hashlib.sha256(im.tobytes()).hexdigest()==rec['full_render_rgba_sha256'],mid
  for name,label,bounds,basis in specs:
   crop=im.crop(bounds);pixels=hashlib.sha256(crop.tobytes()).hexdigest();original_size=list(crop.size);crop.thumbnail((480,480),Image.Resampling.LANCZOS)
   if crop.getchannel('A').getextrema()[0]!=255: raise ValueError('Selected crop requires PNG transparency: '+name)
   p=args.output/(name+'.jpg');crop.convert('RGB').save(p,quality=88,subsampling=0,optimize=True)
   entry={'id':name,'runtime_id':mid,'label':label,'disclosure':'Cropped original view. Static source rendering with initial authored visibility; separate authored spaces are not relocated in the source. No generated/replacement artwork.','crop_bounds_pixels_xyxy':list(bounds),'bounds_semantics':'left/top inclusive, right/bottom exclusive; pixels in the full authored TMJ canvas','bounds_basis':basis,'source_crop_dimensions':original_size,'source_crop_rgba_sha256':pixels,'source_tmj':rec['source_tmj'],'source_assets':renderer.assets,'full_scene_rgba_sha256':rec['full_render_rgba_sha256'],'output':{'path':f'docs/map-collection/previews/crops/{p.name}','filename':p.name,'sha256':r.sha(p),'dimensions':list(crop.size),'bytes':p.stat().st_size,'format':'JPEG','quality':88,'resampling':'Lanczos; aspect ratio retained; no color adjustment'}}
   crops.append(entry);print(p,flush=True)
 # Explicitly separated and labeled room contact sheet, not a replacement map.
 sheet=Image.new('RGB',(1000,990),(242,245,244));d=ImageDraw.Draw(sheet)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16);bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20);title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
 d.text((20,14),"Keeper's Return | Cropped original views",font=title,fill=(20,39,43))
 d.text((20,52),'Separate authored spaces, shown side by side for review. Full source layout is preserved.',font=font,fill=(50,61,65))
 for i,entry in enumerate(crops[:4]):
  x=10+(i%2)*500;y=90+(i//2)*426;thumb=Image.open(args.output/entry['output']['filename']);thumb.thumbnail((480,360),Image.Resampling.LANCZOS)
  sheet.paste(thumb,(x+(480-thumb.width)//2,y+(360-thumb.height)//2))
  d.text((x+5,y+368),entry['label'],font=bold,fill=(20,39,43))
  d.text((x+5,y+398),'Source crop: '+', '.join(map(str,entry['crop_bounds_pixels_xyxy'])),font=font,fill=(50,61,65))
 d.text((20,961),'Initial authored visibility | Static preview | No live acceptance established',font=font,fill=(50,61,65))
 sp=args.output/'keeper-detail-sheet.jpg';sheet.save(sp,quality=85,subsampling=0,optimize=True)
 manifest={'schema_version':1,'purpose':'Additive source-pixel focus views for sparse world overviews; original full previews preserved.','method':'Reconstruct complete scene using the verified original-pixel renderer, confirm full RGBA hash against the full preview manifest, crop at recorded integer pixel bounds, then resize to at most 480 pixels. Contact sheet labels separate authored spaces.','full_preview_manifest_sha256':r.sha(args.full_manifest),'renderer_sha256':r.sha(Path(__file__).with_name('render_previews.py')),'crop_script_sha256':r.sha(__file__),'crops':crops,'detail_sheet':{'path':'docs/map-collection/previews/crops/keeper-detail-sheet.jpg','sha256':r.sha(sp),'dimensions':list(sheet.size),'bytes':sp.stat().st_size,'label':'Cropped original views; separate authored spaces shown side by side for review'},'limitations':['TMJ initial visibility only; no runtime script or WAM state applied.','No game acceptance, interactions, sound or transitions verified.','Detail sheet is a labeled review layout, not the spatial arrangement of the map.']}
 (args.output.parent.parent/'crop-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('CROP_MANIFEST',args.output.parent.parent/'crop-manifest.json')
if __name__=='__main__':main()
