from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1]
A={n:Image.open(R/f'native/{n}.png').convert('RGBA') for n in ['reception','sofa','coffee-table']}
# These polygons trace actual generated pixels after measured one-time reduction.
polys={
 'reception-front':[(16,59),(144,59),(144,75),(139,80),(132,80),(130,76),(28,76),(28,80),(20,80),(17,76)],
 'sofa-front':[(29,65),(131,65),(132,67),(132,75),(130,76),(30,76),(28,74),(28,67)],
 'sofa-left-arm':[(23,27),(27,28),(29,32),(29,73),(27,74),(21,74),(18,71),(16,66),(16,34),(18,29)],
 'sofa-right-arm':[(136,27),(132,29),(131,33),(131,72),(133,74),(139,74),(142,70),(144,64),(144,34),(142,29)],
 'coffee-table-front':[(18,41),(78,41),(78,46),(76,48),(70,48),(69,46),(27,46),(26,48),(20,48),(18,45)]}
M={}
for n,p in polys.items():
 name='sofa' if n.startswith('sofa') else 'reception' if n.startswith('reception') else 'coffee-table'
 m=Image.new('L',A[name].size);ImageDraw.Draw(m).polygon(p,fill=255)
 part=A[name].copy();part.putalpha(ImageChops.multiply(part.getchannel('A'),m));part.save(R/f'native/{n}-occluder.png');part.getchannel('A').save(R/f'native/{n}-occluder-alpha.png');M[n]=part
sofa_fore=Image.new('RGBA',A['sofa'].size)
for n in ['sofa-front','sofa-left-arm','sofa-right-arm']:sofa_fore.alpha_composite(M[n])
sofa_fore.save(R/'native/sofa-foreground.png');sofa_fore.getchannel('A').save(R/'native/sofa-foreground-alpha.png')
# Floor-contact pixels are subsets of the real object alpha, never painted additions.
contacts={'reception':[(20,75,29,80),(131,75,140,80)],'sofa':[(21,74,30,80),(130,74,139,80)],'coffee-table':[(20,44,27,48),(69,44,77,48)]}
for n,rects in contacts.items():
 m=Image.new('L',A[n].size);d=ImageDraw.Draw(m)
 for x,y,x2,y2 in rects:d.rectangle((x,y,x2-1,y2-1),fill=255)
 ImageChops.multiply(A[n].getchannel('A'),m).save(R/f'native/{n}-contact-alpha.png')
spritepath=R/'source/greg-reference-unchanged.png';sheet=Image.open(spritepath).convert('RGBA')
frames={'south':sheet.crop((32,0,64,32)),'north':sheet.crop((32,96,64,128))}
# Explicit asset placements; local coords refer to padded asset canvases.
places={'reception':[112,112],'sofa':[464,80],'coffee-table':[496,192]}
actors=[{'id':'reception-staff-scale-fixture','center':[192,112],'facing':'south','frame_index':1}, {'id':'reception-visitor-scale-fixture','center':[192,208],'facing':'north','frame_index':10},{'id':'sofa-left-scale-fixture','center':[516,132],'facing':'south','frame_index':1},{'id':'sofa-right-scale-fixture','center':[572,132],'facing':'south','frame_index':1}]
base=Image.new('RGBA',(768,352),'#e5deca');draw=ImageDraw.Draw(base)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
draw.text((24,18),'Reception + lounge | Native 1x | Unchanged 32px Greg scale fixtures',font=font,fill='#254c52')
draw.text((120,286),'128x64 reception',font=font,fill='#254c52');draw.text((464,286),'128x64 sofa / 64x32 table',font=font,fill='#254c52');draw.text((24,322),'Static asset proof, neutral receiver. No live occupants, claim state, or sit animation implied.',font=font,fill='#254c52')
for n,xy in places.items():base.alpha_composite(A[n],tuple(xy))
base.save(R/'proofs/native-empty.png')
occupied=base.copy()
for actor in actors:
 x,y=actor['center'];occupied.alpha_composite(frames[actor['facing']],(x-16,y-16))
before=occupied.copy();occupied.alpha_composite(sofa_fore,tuple(places['sofa']));occupied.save(R/'proofs/native-occupied.png');occupied.resize((1536,704),Image.Resampling.NEAREST).save(R/'proofs/native-occupied-2x.png')
# Actual occlusion changes to opaque avatar pixels, measured by native pixel, not rectangle overlap.
checks=[]
for actor in actors:
 cx,cy=actor['center'];frame=frames[actor['facing']];headchanged=0;lowerchanged=0;lower_visible=0
 for sy in range(32):
  for sx in range(32):
   if frame.getpixel((sx,sy))[3]>0:
    p=(cx-16+sx,cy-16+sy);changed=before.getpixel(p)!=occupied.getpixel(p)
    if sy<14:headchanged+=int(changed)
    else:lower_visible+=1;lowerchanged+=int(changed)
 checks.append({'id':actor['id'],'protected_head_changed_pixels':headchanged,'lower_body_changed_pixels':lowerchanged,'lower_body_source_opaque_pixels':lower_visible})
# Collision geometry: footprint rectangles are half-open native coordinates.
obstacles=[('reception',[128,128,128,64]),('sofa-back',[480,96,128,18]),('sofa-left-arm',[480,114,12,40]),('sofa-right-arm',[596,114,12,40]),('coffee-table',[512,208,64,32])]
routes=[
 {'id':'staff-enter-from-west','points':[[96,256],[96,96],[192,96],[192,112]],'occupied':['reception-visitor-scale-fixture']},
 {'id':'staff-exit-west','points':[[192,112],[192,96],[96,96],[96,256]],'occupied':['reception-visitor-scale-fixture']},
 {'id':'visitor-approach','points':[[192,256],[192,208]],'occupied':['reception-staff-scale-fixture']},
 {'id':'reception-west-bypass','points':[[96,256],[96,80]],'occupied':['reception-staff-scale-fixture','reception-visitor-scale-fixture']},
 {'id':'reception-east-bypass','points':[[288,256],[288,80]],'occupied':['reception-staff-scale-fixture','reception-visitor-scale-fixture']},
 {'id':'reception-north-bypass','points':[[96,80],[288,80]],'occupied':['reception-staff-scale-fixture','reception-visitor-scale-fixture']},
 {'id':'sofa-left-enter','points':[[448,256],[448,176],[516,176],[516,132]],'occupied':['sofa-right-scale-fixture']},
 {'id':'sofa-left-exit','points':[[516,132],[516,176],[448,176],[448,256]],'occupied':['sofa-right-scale-fixture']},
 {'id':'sofa-right-enter','points':[[640,256],[640,176],[572,176],[572,132]],'occupied':['sofa-left-scale-fixture']},
 {'id':'sofa-right-exit','points':[[572,132],[572,176],[640,176],[640,256]],'occupied':['sofa-left-scale-fixture']},
 {'id':'walk-between-sofa-and-table','points':[[448,176],[640,176]],'occupied':['sofa-left-scale-fixture','sofa-right-scale-fixture']},
 {'id':'lounge-west-bypass','points':[[448,256],[448,64]],'occupied':['sofa-left-scale-fixture','sofa-right-scale-fixture']},
 {'id':'lounge-east-bypass','points':[[640,256],[640,64]],'occupied':['sofa-left-scale-fixture','sofa-right-scale-fixture']}]
def overlaps(a,b):return a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]
for rt in routes:
 samples=[]
 for start,end in zip(rt['points'],rt['points'][1:]):
  dx,dy=end[0]-start[0],end[1]-start[1];num=max(abs(dx),abs(dy));samples.extend([(start[0]+dx*i/num,start[1]+dy*i/num) for i in range(num+1)])
 blockers=obstacles+[(a['id'],[a['center'][0]-8,a['center'][1],16,16]) for a in actors if a['id'] in rt['occupied']]
 failures=[{'center':[x,y],'blocker':name} for x,y in samples for name,r in blockers if overlaps([x-8,y,16,16],r)]
 rt['sample_count']=len(samples);rt['result']='pass' if not failures else 'fail';rt['collisions']=failures[:5]
routeim=occupied.copy();rd=ImageDraw.Draw(routeim)
for name,r in obstacles:
 x,y,w,h=r;rd.rectangle((x,y,x+w-1,y+h-1),outline='#d45636',width=1)
for rt in routes:rd.line([tuple(p) for p in rt['points']],fill='#42a571',width=1)
for a in actors:
 x,y=a['center'];rd.ellipse((x-2,y-2,x+2,y+2),fill='#efc942')
rd.text((24,42),'Green: sampled 16x16 body routes | Red: collision footprints | Gold: exact sprite centers',font=font,fill='#254c52');routeim.save(R/'proofs/native-route-diagnostic.png')
manifest={'status':'Original generated assets; static native proof passed. Runtime integration and owner review remain parent scope.','coordinates':'Native world pixels, half-open rectangles; avatar center anchor; 16x16 tested body at [cx-8,cy].','generator':'Built-in image_gen; one original generation per asset. No failed-generation image was discarded.','art_originality':'Original prompt-driven painted objects; no third-party art sources.','reduction_manifest':'reduction-manifest.json','geometry_plan':'geometry-plan.json','actual_geometry_deviation':{'reception':'Original source framing widened relative to guide; cropped meaningful source then reduced to 128x64. Actual tabletop reaches approximately native y59, about43px deep; actual shallow facade begins y60. This differs from planned48px top /12px apron. No staff/head/collision adjustment was made.','sofa':'Source framing normalized to128x64. Actual front rail starts y65, 1px lower than plan; exact planned anchors retained.','coffee_table':'Source framing normalized to64x32. Actual tabletop ends approximately y41,25px deep; plan24px. Source alpha<=4 haze is discarded during reduction.'},'native_assets':{'reception':{'origin':places['reception'],'canvas':[160,96],'visible_world':[128,128,128,64],'collider':[128,128,128,64],'contact_pixel_rects_local':contacts['reception'],'staff_pocket_world':[128,64,128,64],'side_bypasses_world':[[64,64,64,192],[256,64,64,192]],'staff_anchor':[192,112],'staff_facing':'south','visitor_anchor':[192,208],'visitor_facing':'north','occluders':['native/reception-front-occluder.png']},'sofa':{'origin':places['sofa'],'canvas':[160,96],'visible_world':[480,96,128,64],'collision_parts': [r for n,r in obstacles if n.startswith('sofa')],'seat_centers':[[516,132],[572,132]],'facing':'south','seat_local_centers':[[52,52],[108,52]],'contact_pixel_rects_local':contacts['sofa'],'front_mask':'native/sofa-front-occluder.png','arm_masks':['native/sofa-left-arm-occluder.png','native/sofa-right-arm-occluder.png'],'combined_mask':'native/sofa-foreground.png','free_floor_before_coffee_table':[480,160,128,48],'walkable_seat_surface':'Seat area is walkable; never use a solid 128x64 sofa rectangle as blocker.'},'coffee_table':{'origin':places['coffee-table'],'canvas':[96,64],'visible_world':[512,208,64,32],'collider':[512,208,64,32],'contact_pixel_rects_local':contacts['coffee-table'],'foreground':'native/coffee-table-front-occluder.png'}},'occluder_trace_polygons_native':polys,'occluder_bounds_native':{n:list(im.getchannel('A').getbbox()) for n,im in M.items()},'source_sprite':{'path':str(spritepath),'sha256':hashlib.sha256(spritepath.read_bytes()).hexdigest(),'size':list(sheet.size),'frames':actors,'unchanged':True},'head_and_body_occlusion_checks':checks,'routes':routes,'validation_summary':{'protected_head_changes':sum(x['protected_head_changed_pixels'] for x in checks),'passing_routes':sum(x['result']=='pass' for x in routes),'total_routes':len(routes),'minimum_sofa_table_clear_floor':48,'claim_or_sit_api_created':False,'runtime_verified':False},'consumer_instructions':['Draw full furniture at its native padded canvas origin and scale1. Draw actors unchanged at exact listed center anchor. Redraw sofa-foreground above actors when they occupy its seats.','Use actual object alpha for occlusion pieces; full sprite rectangle is never an occluder.','Reception/front and coffee-table/front masks are available for appropriate dynamic depth integration; no protected-head overlap is present at the supplied reception anchors.','No sit animation exists here: south cardinal idle frames are unchanged spatial occupancy proofs. Existing claim contract must be used by runtime owner if desired.','64px reception side bypass and north staff pocket, and48px clear sofa/table floor, are layout obligations.']}
(R/'asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest['validation_summary'],indent=2));print(json.dumps(checks,indent=2));print('Route failures:',[r['id'] for r in routes if r['result']!='pass'])
