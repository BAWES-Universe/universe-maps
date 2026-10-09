from PIL import Image, ImageDraw
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
# Exact native silhouettes; enlarged nearest-neighbor solely as generation guides.
im=Image.new('RGBA',(160,96));d=ImageDraw.Draw(im)
d.rectangle((16,16,143,63),fill='#d5b581');d.rectangle((16,64,143,75),fill='#aa916b');d.rectangle((20,76,27,79),fill='#7b6246');d.rectangle((132,76,139,79),fill='#7b6246')
im.resize((1600,960),Image.Resampling.NEAREST).save(R/'guides/reception-geometry.png')
im=Image.new('RGBA',(160,96));d=ImageDraw.Draw(im)
d.rounded_rectangle((16,16,143,73),radius=7,fill='#126475');d.rounded_rectangle((20,18,139,35),radius=5,fill='#1a7180');d.rounded_rectangle((28,34,79,63),radius=4,fill='#4b9098');d.rounded_rectangle((80,34,131,63),radius=4,fill='#4b9098');d.rounded_rectangle((16,27,27,69),radius=4,fill='#206a79');d.rounded_rectangle((132,27,143,69),radius=4,fill='#206a79');d.rounded_rectangle((28,64,131,75),radius=3,fill='#175566');d.rectangle((22,74,28,79),fill='#8d6c39');d.rectangle((131,74,137,79),fill='#8d6c39')
im.resize((1600,960),Image.Resampling.NEAREST).save(R/'guides/sofa-geometry.png')
im=Image.new('RGBA',(96,64));d=ImageDraw.Draw(im)
d.rounded_rectangle((16,16,79,39),radius=3,fill='#d5b581');d.rectangle((18,40,77,45),fill='#946a43');d.rectangle((20,44,25,47),fill='#7b6237');d.rectangle((70,44,75,47),fill='#7b6237')
im.resize((1152,768),Image.Resampling.NEAREST).save(R/'guides/coffee-table-geometry.png')
plan={'units':'native pixels; half-open rectangles','avatar':{'path':'../universe-painted-arrival/runtime-work/greg.png','frame_size':[32,32],'scale':1,'south_idle_frame_index':1,'north_idle_frame_index':10,'anchor':'sprite center; body [cx-8,cy,16,16]'},'reception':{'canvas':[160,96],'visible_bounds':[16,16,128,64],'top':[16,16,128,48],'front':[16,64,128,12],'contact_band':[16,76,128,4],'collision_local':[16,16,128,64],'staff_anchor_relative_to_visible_origin':[64,-16],'staff_direction':'south','north_staff_pocket':[0,-64,128,64],'side_bypasses_width':64,'visitor_anchor_relative_to_visible_origin':[64,80],'visitor_direction':'north'},'sofa':{'canvas':[160,96],'visible_bounds':[16,16,128,64],'rear_back':[20,18,120,18],'seat_surface':[28,34,104,30],'front':[28,64,104,12],'arms':[[16,27,12,43],[132,27,12,43]],'seat_anchors_asset':[[52,52],[108,52]],'seat_directions':['south','south'],'front_foreground_min_y':64,'no_sit_api':True,'collision_parts_asset':[[16,16,128,18],[16,34,12,40],[132,34,12,40]],'walkable_seat_allocation':[28,34,104,46],'approach':'south; independently enter each seat while the other is occupied'},'coffee_table':{'canvas':[96,64],'visible_bounds':[16,16,64,32],'top':[16,16,64,24],'front':[18,40,60,6],'contact_band':[20,44,56,4],'collision_local':[16,16,64,32]},'lounge_layout_relative_to_sofa_visible_origin':{'sofa':[0,0,128,64],'seat_anchors':[[36,36],[92,36]],'table':[32,112,64,32],'free_floor_after_sofa':48,'side_bypasses':64},'proof':'Static asset-scale proof only; no engine, claim, multiplayer, or sit implementation.'}
(R/'geometry-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
