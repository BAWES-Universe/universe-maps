from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json
R=Path(__file__).resolve().parents[1];D=json.loads((R/'fixture-plan.json').read_text())
master=Image.open(R/'art-source/single-station-master.png').convert('RGBA');asset=master.convert('RGBa').resize((96,128),Image.Resampling.LANCZOS).convert('RGBA')
# A geometry proof uses a neutral receiver; this is not a new finished interior.
base=Image.new('RGBA',(512,384),'#e4ddc7');backs=Image.new('RGBA',(512,384));greg=Image.open(R/'assets/greg-reference.png').convert('RGBA').crop((32,96,64,128))
# Trace source's actual full chair-back contour in native asset coordinates.
poly=[(35,83),(37,81),(58,81),(61,84),(62,96),(60,101),(57,103),(38,103),(34,100),(34,86)]
m=Image.new('L',(96,128));ImageDraw.Draw(m).polygon(poly,fill=255);fullback=asset.copy();fullback.putalpha(ImageChops.multiply(asset.getchannel('A'),m))
for s in D['workstations']:
 x=s['desk']['asset_canvas']['x']-16;y=s['desk']['asset_canvas']['y']-16;base.alpha_composite(asset,(x,y));backs.alpha_composite(fullback,(x,y))
base.save(R/'docs/native-empty.png')
for s in D['workstations']:
 x,y=s['occupant']['center'];base.alpha_composite(greg,(x-16,y-16))
base.alpha_composite(backs);base.save(R/'docs/native-occupied.png');base.resize((1024,768),Image.Resampling.NEAREST).save(R/'docs/native-occupied-2x.png');asset.save(R/'art-source/single-station-native.png');backs.save(R/'art-source/fixture-chair-backs-native.png')
print({'master':master.size,'native_asset':asset.size,'proof':base.size,'seats':D['occupied_proof']['centers'],'actual_back_top_local':81,'planned':79,'back_geometry_deviation_px':2,'scope':'Static native occupied registration proof, no runtime or owner acceptance'})
