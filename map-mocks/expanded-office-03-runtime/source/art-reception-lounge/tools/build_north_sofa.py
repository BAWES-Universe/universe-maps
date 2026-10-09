from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFont
import json, hashlib
R=Path(__file__).resolve().parents[1]
# One final-art reduction, directly from the preserved accepted master.
source=R/'source/sofa-north-master.png';master=Image.open(source).convert('RGBA');crop=master.getchannel('A').point(lambda p:255 if p>=5 else 0).getbbox()
obj=master.crop(crop).convert('RGBa').resize((128,64),Image.Resampling.LANCZOS).convert('RGBA');obj.putalpha(obj.getchannel('A').point(lambda p:0 if p<=4 else p))
asset=Image.new('RGBA',(160,96));asset.alpha_composite(obj,(16,16));asset.save(R/'native/sofa-north.png');asset.getchannel('A').save(R/'native/sofa-north-object-alpha.png')
# The actual full outer-back contour is traced, not replaced by a blanket rectangle.
polygons={
 'back':[(22,35),(25,34),(29,33),(131,33),(136,34),(139,37),(140,42),(139,69),(137,73),(132,75),(27,75),(22,73),(20,69),(19,41)],
 'left-arm':[(22,16),(27,17),(30,21),(30,31),(26,33),(22,35),(19,39),(18,46),(16,48),(16,29),(17,21)],
 'right-arm':[(137,16),(132,17),(130,21),(130,31),(134,33),(138,35),(141,39),(142,46),(144,48),(144,29),(143,21)]}
parts={};union=Image.new('L',asset.size)
for name,p in polygons.items():
 mask=Image.new('L',asset.size);ImageDraw.Draw(mask).polygon(p,fill=255);union=ImageChops.lighter(union,mask)
 part=asset.copy();part.putalpha(ImageChops.multiply(asset.getchannel('A'),mask));part.save(R/f'native/sofa-north-{name}-occluder.png');part.getchannel('A').save(R/f'native/sofa-north-{name}-occluder-alpha.png');parts[name]=part
fore=asset.copy();fore.putalpha(ImageChops.multiply(asset.getchannel('A'),union));fore.save(R/'native/sofa-north-foreground.png');fore.getchannel('A').save(R/'native/sofa-north-foreground-alpha.png')
contact=Image.new('L',asset.size);cd=ImageDraw.Draw(contact)
for r in [(21,75,31,80),(129,75,139,80)]:cd.rectangle((r[0],r[1],r[2]-1,r[3]-1),fill=255)
ImageChops.multiply(asset.getchannel('A'),contact).save(R/'native/sofa-north-contact-alpha.png')
source_sprite=R/'source/greg-reference-unchanged.png';sheet=Image.open(source_sprite).convert('RGBA');gregN=sheet.crop((32,96,64,128));gregS=sheet.crop((32,0,64,32))
# Pairing diagnostic only. No office layout or other art is modified.
size=(448,400);north_origin=[112,240];south_origin=[112,48];table_origin=[144,160]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
base=Image.new('RGBA',size,'#e5deca');d=ImageDraw.Draw(base);d.text((16,15),'Opposing sofa assets | Native 1x | 32px Greg fixtures',font=font,fill='#254c52');d.text((16,371),'Static scale proof; no sit animation or live claims implied.',font=font,fill='#254c52')
base.alpha_composite(Image.open(R/'native/sofa.png').convert('RGBA'),tuple(south_origin));base.alpha_composite(Image.open(R/'native/coffee-table.png').convert('RGBA'),tuple(table_origin));base.alpha_composite(asset,tuple(north_origin));base.save(R/'proofs/sofa-north-pair-empty.png')
actors=[{'id':'north-left','local_center':[52,32],'world_center':[164,272],'facing':'north','frame_index':10},{'id':'north-right','local_center':[108,32],'world_center':[220,272],'facing':'north','frame_index':10},{'id':'south-left','local_center':[52,52],'world_center':[164,100],'facing':'south','frame_index':1},{'id':'south-right','local_center':[108,52],'world_center':[220,100],'facing':'south','frame_index':1}]
occupied=base.copy()
for a in actors:
 x,y=a['world_center'];occupied.alpha_composite(gregN if a['facing']=='north' else gregS,(x-16,y-16))
before=occupied.copy();occupied.alpha_composite(fore,tuple(north_origin));occupied.alpha_composite(Image.open(R/'native/sofa-foreground.png').convert('RGBA'),tuple(south_origin));occupied.save(R/'proofs/sofa-north-pair-occupied.png');occupied.resize((896,800),Image.Resampling.NEAREST).save(R/'proofs/sofa-north-pair-occupied-2x.png')
checks=[]
for a in actors[:2]:
 cx,cy=a['world_center'];counts={'head_opaque':0,'head_changed':0,'lower_opaque':0,'lower_changed':0}
 for sy in range(32):
  for sx in range(32):
   if gregN.getpixel((sx,sy))[3]:
    zone='head' if sy<14 else 'lower';counts[zone+'_opaque']+=1;p=(cx-16+sx,cy-16+sy);counts[zone+'_changed']+=int(before.getpixel(p)!=occupied.getpixel(p))
 checks.append({'id':a['id'],**counts})
# The backrest is elevated art. Its floor blocker begins at local y48, exactly below the seated body's y32..47.
local_blocks=[['back-floor',[16,48,128,32]],['left-arm-floor',[16,16,12,32]],['right-arm-floor',[132,16,12,32]]]
blocks=[(n,[r[0]+north_origin[0],r[1]+north_origin[1],r[2],r[3]]) for n,r in local_blocks]
blocks += [('coffee-table',[160,176,64,32]),('south-back',[128,64,128,18]),('south-left-arm',[128,82,12,40]),('south-right-arm',[244,82,12,40])]
routes=[{'id':'north-left-enter','points':[[96,224],[164,224],[164,272]],'occupied':['north-right','south-left','south-right']},{'id':'north-left-exit','points':[[164,272],[164,224],[96,224]],'occupied':['north-right','south-left','south-right']},{'id':'north-right-enter','points':[[288,224],[220,224],[220,272]],'occupied':['north-left','south-left','south-right']},{'id':'north-right-exit','points':[[220,272],[220,224],[288,224]],'occupied':['north-left','south-left','south-right']},{'id':'north-approach-cross-lane','points':[[96,224],[288,224]],'occupied':['north-left','north-right','south-left','south-right']},{'id':'west-pair-bypass','points':[[96,336],[96,48]],'occupied':['north-left','north-right','south-left','south-right']},{'id':'east-pair-bypass','points':[[288,336],[288,48]],'occupied':['north-left','north-right','south-left','south-right']}]
def overlaps(a,b):return a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]
for route in routes:
 obstacles=blocks+[(a['id'],[a['world_center'][0]-8,a['world_center'][1],16,16]) for a in actors if a['id'] in route['occupied']]
 points=[]
 for (x,y),(ex,ey) in zip(route['points'],route['points'][1:]):
  steps=max(abs(ex-x),abs(ey-y));points.extend([(x+(ex-x)*i/steps,y+(ey-y)*i/steps) for i in range(steps+1)])
 failures=[{'center':[x,y],'blocker':n} for x,y in points for n,b in obstacles if overlaps([x-8,y,16,16],b)];route.update({'result':'pass' if not failures else 'fail','sample_count':len(points),'collisions':failures[:5]})
diag=occupied.copy();dd=ImageDraw.Draw(diag)
for n,(x,y,w,h) in blocks:dd.rectangle((x,y,x+w-1,y+h-1),outline='#d45636')
for route in routes:dd.line([tuple(p) for p in route['points']],fill='#329760',width=1)
for a in actors:
 x,y=a['world_center'];dd.ellipse((x-2,y-2,x+2,y+2),fill='#ffcc42')
diag.save(R/'proofs/sofa-north-routes.png')
manifest={'status':'North-facing counterpart complete; static native-scale art, head occlusion, and route checks passed. Runtime verification remains required.','asset':'native/sofa-north.png','canvas':[160,96],'visible_bounds_xywh':[16,16,128,64],'measured_alpha_bounds_xyxy':{str(t):asset.getchannel('A').point(lambda p:255 if p>=t else 0).getbbox() for t in [1,5,64,128,240]},'orientation':'north; original newly generated outer rear upholstered back, not a rotation or reflection','source_master':'source/sofa-north-master.png','source_size':list(master.size),'source_crop_xyxy':list(crop),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'native_sha256':hashlib.sha256((R/'native/sofa-north.png').read_bytes()).hexdigest(),'generation_prompts':['source/sofa-north-prompt.txt','source/sofa-north-correction-prompt.txt'],'preserved_initial_attempt':'source/sofa-north-attempt-01-high-back.png','initial_attempt_issue':'Actual backrest edge normalized to local y29..30, too high for protected head zone; preserved and corrected with a targeted built-in image_gen edit.','reduction':'One premultiplied Lanczos reduction directly from source alpha>=5 bounds to128x64, placed at16,16 on160x96 canvas. Final alpha<=4 traces zeroed. Original source retained; no avatar or post-generation shape warping.','seat_anchors_local':[[52,32],[108,32]],'facing':'north','sprite':{'file':'source/greg-reference-unchanged.png','sheet':[96,128],'frame':[32,96,32,32],'frame_index':10,'scale':1,'resampled':False,'body_relative_to_center':[-8,0,16,16],'protected_head_rows':[0,14],'sha256':hashlib.sha256(source_sprite.read_bytes()).hexdigest()},'actual_backrest_top_local_y':33,'actual_backrest_height_approx':42,'foreground':'native/sofa-north-foreground.png','actual_back_mask':'native/sofa-north-back-occluder.png','arm_masks':['native/sofa-north-left-arm-occluder.png','native/sofa-north-right-arm-occluder.png'],'polygons':polygons,'foreground_bounds_xyxy':list(fore.getchannel('A').getbbox()),'contact_rects_xyxy':[[21,75,31,80],[129,75,139,80]],'collision_parts_local_xywh':local_blocks,'collision_rationale':'Elevated full rear back projects upward, while its physical floor blocker starts at localy48; each unchanged avatar body at centery32 spansy32..47 and touches the blocker at48. Arms block only sides. Do not use the full visible128x64 rectangle as blocker.','walkable_seat_area_local_xywh':[28,16,104,32],'approach':'Enter and leave from north through each seat column. Never approach through the rear back.','pairing_diagnostic':{'north_asset_origin':north_origin,'south_asset_origin':south_origin,'coffee_table_origin':table_origin,'north_visible':[128,256,128,64],'south_visible':[128,64,128,64],'table_visible':[160,176,64,32],'clear_floor_between_table_and_each_sofa':48,'side_bypasses':64,'production_layout_modified':False},'native_occupied_checks':checks,'routes':routes,'validation':{'head_pixels_changed':sum(c['head_changed'] for c in checks),'lower_body_pixels_occluded_each':[c['lower_changed'] for c in checks],'routes_passed':sum(r['result']=='pass' for r in routes),'routes_total':len(routes),'runtime_tested':False,'sit_or_claim_api_added':False},'integration_order':['Draw native/sofa-north.png below unchanged actors at the asset origin, scale1.','Draw each north-facing avatar centered at asset origin plus its exact local seat anchor.','Draw native/sofa-north-foreground.png above actors at the identical asset origin.','Apply listed floor collision rectangles and retain a north approach lane at least48px deep.']}
(R/'sofa-north-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest['validation'],indent=2));print(json.dumps(checks,indent=2))
assert manifest['validation']['head_pixels_changed']==0
assert all(r['result']=='pass' for r in routes)
assert all(c['lower_changed']>200 for c in checks)
