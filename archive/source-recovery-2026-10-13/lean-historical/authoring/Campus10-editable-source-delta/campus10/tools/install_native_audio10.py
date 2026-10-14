"""Native Tiled dynamic areas: automatic bounded ambience, original files preserved."""
from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];O=R/'map32';original=R/'audio/assets';out=O/'audio';out.mkdir(exist_ok=True)
for src,name in [('fountain.mp3','fountain-soft.mp3'),('fire-gentle-original.mp3','fire-soft.mp3')]:
 dest=out/name
 if not dest.exists():subprocess.run(['ffmpeg','-v','error','-i',str(original/src),'-af','volume=0.18','-map_metadata','-1','-c:a','libmp3lame','-b:a','96k',str(dest)],check=True)
cfg={'mode':'native-classified-area-properties','feetOffsetY':16,'sources':[{'id':'fountain','url':'audio/fountain-soft.mp3','bounds':[712,1231,448,384],'center':[936,1423]},{'id':'fire','url':'audio/fire-soft.mp3','bounds':[2108,1480,576,576],'center':[2396,1768]}],'quietZones':[[720,64,1536,960],[0,1136,640,1152]],'audioCeilingBakedGain':0.18,'gainBands':[0.35,0.7,1],'notes':['Normal native autoplay attempt with native browser retry only if blocked.','Existing native mute, pause and block-audio controls govern playback.','Native dynamic areas evaluate player y+16.','Three rectangular gain bands; not continuous radial or stereo spatialization.','Unsupported element-volume devices receive the same preattenuated ceiling throughout each sound area; native mute still applies.','No ambient area overlaps office, classroom, event or meeting floor.','Only the separately authored spawn area is silent; ambience properties do not silence proximity conversations.']}
p=O/'magical-campus.tmj';m=json.loads(p.read_text());m['properties']=[x for x in m.get('properties',[])if x['name']not in['script','campusAmbience','gateRoomUrl']]+[{'name':'gateRoomUrl','type':'string','value':''}]
layer=next(x for x in m['layers']if x['name']=='campus-areas');layer['objects']=[o for o in layer['objects']if not o['name'].startswith('ambient-')];nextid=max(o['id']for l in m['layers']if l['type']=='objectgroup'for o in l['objects'])+1
for s in cfg['sources']:
 x,y,w,h=s['bounds']
 for index,(inset,gain)in enumerate([(0,0.35),(48,0.7),(96,1)]):
  layer['objects'].append({'id':nextid,'name':f"ambient-{s['id']}-{index}",'class':'area','type':'area','visible':True,'x':x+inset,'y':y+inset,'width':w-2*inset,'height':h-2*inset,'properties':[{'name':'playAudio','type':'string','value':s['url']},{'name':'audioLoop','type':'bool','value':True},{'name':'audioVolume','type':'float','value':gain}]});nextid+=1
m['nextobjectid']=nextid;p.write_text(json.dumps(m,separators=(',',':'))+'\n');(O/'audio/configuration.json').write_text(json.dumps(cfg,indent=2)+'\n')
print('Installed6 classified native sound areas; no custom audio script/menu, no added tile layers.')
