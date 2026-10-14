from PIL import Image
from pathlib import Path
import json,hashlib
D=Path(__file__).parent; S=D/'source/source/source-assets'
base=Image.open(D.parent/'Reading-Conservatory-r1-concept.png').convert('RGBA').resize((768,512),Image.Resampling.LANCZOS)
overlay=Image.open(S/'occupied-proof-overlay.png').convert('RGBA');proof=json.load(open(S/'WOKA-PROOF.json'));out=base.copy();rows=[]
positions=[(8,384,474,'south arrival'),(0,384,395,'entrance landing'),(7,384,293,'central aisle'),(2,190,183,'quiet study approach'),(3,174,275,'west browsing aisle'),(4,563,285,'east browsing aisle'),(5,301,322,'west reading approach'),(6,467,322,'east reading approach')]
for i,x,y,label in positions:
 a=proof['actors'][i];ox,oy=a['position'];fr=overlay.crop((ox-16,oy-16,ox+16,oy+16));out.alpha_composite(fr,(x-16,y-16));rows.append(dict(source_actor=a,frame_crop=[ox-16,oy-16,ox+16,oy+16],frame_rgba_sha256=hashlib.sha256(fr.tobytes()).hexdigest(),new_center=[x,y],label=label))
out.save(D/'Reading-Conservatory-native32-scale-study.png')
(D/'SCALE-STUDY.json').write_text(json.dumps(dict(status='Static scale / composition study only. No runtime, route, collision or seat-depth proof.',world_size=[768,512],native_sprite_canvas=[32,32],background_scale=.5,avatar_scaling='none',avatar_source='Retained compiled review overlay from local timber-mixed-six-mat-instructor-facing-r2-source.zip; preserved source provenance identifies native repository frames. No raw sprite sheets are included.',repoCommit=proof['repoCommit'],standing_idle_only=True,actors=rows),indent=2))
