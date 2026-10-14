"""Apply the registered exterior source pack after native assembly, before compile.

Usage: python apply_exterior.py /path/to/project/layers [--out /other/layers]
This is an image-source importer, not a geometry or engine change. Re-run the
ordinary assembly before applying it again. Ordinary above layers are cleared
only where a source owner actually replaces the visible ground/art object.
"""
from pathlib import Path
from PIL import Image,ImageChops
import argparse,json,hashlib

def apply(layer_dir,out_dir=None):
 root=Path(__file__).resolve().parent
 manifest=json.loads((root/'exterior-manifest.json').read_text())
 layer_dir=Path(layer_dir);out=Path(out_dir or layer_dir);out.mkdir(parents=True,exist_ok=True)
 layers={n:Image.open(layer_dir/f'campus-{n}.png').convert('RGBA') for n in ['base','foreground','glass','shade']}
 assert all(im.size==tuple(manifest['world']) for im in layers.values())
 backing=Image.open(root/manifest['groundBacking']).convert('RGBA')
 backing.alpha_composite(layers['base']);layers['base']=backing
 keep=Image.new('L',tuple(manifest['world']),255)
 for owner in manifest['owners']:
  src=Image.open(root/owner['source']).convert('RGBA');mask=Image.open(root/owner['mask']).convert('L')
  if owner['mode']=='replace':layers['base']=Image.composite(src,layers['base'],mask)
  else:
   src.putalpha(ImageChops.multiply(src.getchannel('A'),mask));layers['base'].alpha_composite(src)
  if owner['clearAbove']:keep=ImageChops.multiply(keep,ImageChops.invert(mask))
 for n in ['foreground','glass','shade']:
  im=layers[n];im.putalpha(ImageChops.multiply(im.getchannel('A'),keep))
 above=Image.new('RGBA',tuple(manifest['world']))
 for n,im in layers.items():
  im.save(out/f'campus-{n}.png')
  if n!='base':above.alpha_composite(im)
 above.save(out/'campus-above.png')
 return {'world':manifest['world'],'owners':len(manifest['owners']),'collisionChanged':False,'output':str(out),'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.glob('campus-*.png')}}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('layers');p.add_argument('--out');args=p.parse_args();print(json.dumps(apply(args.layers,args.out),indent=2))
