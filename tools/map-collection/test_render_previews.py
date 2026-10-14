#!/usr/bin/env python3
"""Independent synthetic checks for the source-only scene renderer."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
from PIL import Image
s=importlib.util.spec_from_file_location('renderer',Path(__file__).with_name('render_previews.py'))
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)

class SceneTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  # Distinct RGBA corner pixels in a 2x2 tile, plus a white animation target.
  im=Image.new('RGBA',(4,2));im.putdata([(255,0,0,255),(0,255,0,255),(255,255,255,255),(255,255,255,255),(0,0,255,255),(255,255,0,255),(255,255,255,255),(255,255,255,255)]);im.save(self.root/'atlas.png')
  self.m={'orientation':'orthogonal','width':4,'height':4,'tilewidth':2,'tileheight':2,'renderorder':'right-down','tilesets':[{'firstgid':1,'image':'atlas.png','imagewidth':4,'imageheight':2,'tilewidth':2,'tileheight':2,'columns':2,'tilecount':2}],'layers':[]}
 def tearDown(self): self.tmp.cleanup()
 def renderer(self):
  p=self.root/'map.tmj';p.write_text(json.dumps(self.m));return r.Renderer(p,self.root)
 def layer(self,gid=1,**kw): return {'type':'tilelayer','name':'scene','width':1,'height':1,'data':[gid],**kw}
 def test_gid_flips_all_eight(self):
  obj=self.renderer();src=obj.tile(1)[0]
  for h in (0,1):
   for v in (0,1):
    for diagonal in (0,1):
     raw=1|(h<<31)|(v<<30)|(diagonal<<29);im=obj.tile(raw)[0]
     # Forward pixel coordinate transform, checked independently from Pillow transpose.
     for y in range(2):
      for x in range(2):
       dx,dy=(y,x) if diagonal else (x,y)
       if h:dx=1-dx
       if v:dy=1-dy
       self.assertEqual(im.getpixel((dx,dy)),src.getpixel((x,y)))
 def test_bit29_is_cleared(self): self.assertEqual(self.renderer().tile(1)[0].tobytes(),self.renderer().tile(1|0x10000000)[0].tobytes())
 def test_nested_offsets_and_opacity(self):
  self.m['layers']=[{'type':'group','name':'g','offsetx':1,'offsety':1,'opacity':0.5,'layers':[self.layer(x=1,y=1,offsetx=1)]}]
  im=self.renderer().render();self.assertEqual(im.getpixel((4,3)),(255,0,0,128));self.assertEqual(im.getpixel((0,0)),(0,0,0,0))
 def test_layer_order_and_visibility(self):
  self.m['layers']=[self.layer(),self.layer(2,visible=False),self.layer(2,opacity=0)]
  im=self.renderer().render();self.assertEqual(im.getpixel((0,0)),(255,0,0,255))
  self.m['layers'].append(self.layer(2));im=self.renderer().render();self.assertEqual(im.getpixel((0,0)),(255,255,255,255))
 def test_animation_first_frame(self):
  self.m['tilesets'][0]['tiles']=[{'id':0,'animation':[{'tileid':1,'duration':10},{'tileid':0,'duration':10}]}];self.m['layers']=[self.layer()]
  obj=self.renderer();im=obj.render();self.assertEqual(im.getpixel((0,0)),(255,255,255,255));self.assertEqual(obj.stats['animated_tile_instances'],1)
 def test_invalid_gid_fails(self):
  self.m['layers']=[self.layer(3)]
  with self.assertRaisesRegex(ValueError,'outside tileset'):self.renderer().render()
 def test_visual_object_fails_instead_of_omission(self):
  self.m['layers']=[self.layer(),{'type':'objectgroup','name':'art','objects':[{'gid':1}]}]
  with self.assertRaisesRegex(ValueError,'Visual object'):self.renderer().render()
 def test_all_invisible_fails(self):
  self.m['layers']=[self.layer(visible=False)]
  with self.assertRaisesRegex(ValueError,'No visible'):self.renderer().render()
 def test_spacing_margin(self):
  im=Image.new('RGBA',(7,4));im.paste((255,0,0,255),(1,1,3,3));im.paste((0,255,0,255),(4,1,6,3));im.save(self.root/'atlas.png')
  self.m['tilesets'][0].update(imagewidth=7,imageheight=4,margin=1,spacing=1);self.m['layers']=[self.layer(2)]
  self.assertEqual(self.renderer().render().getpixel((0,0)),(0,255,0,255))
if __name__=='__main__':unittest.main()
