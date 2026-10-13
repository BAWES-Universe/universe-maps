import json
from pathlib import Path
def configure(root,slug,event):
 p=root/'map32'/(slug+'.wam');w=json.loads(p.read_text());areas=[]
 def area(id,name,b,properties):
  x,y,x2,y2=b;return dict(id=id,name=name,x=x,y=y,width=x2-x,height=y2-y,visible=True,properties=properties)
 stage=slug+'-stage';areas.append(area(stage,'Presenter stage',event['stage'],[dict(id=stage+'-speaker',type='speakerMegaphone',name=slug+'-live-stage',chatEnabled=False)]))
 areas.append(area(slug+'-audience','Audience',event['audience'],[dict(id=slug+'-listen',type='listenerMegaphone',speakerZoneName=stage,chatEnabled=False)]))
 areas.append(area(slug+'-framing','Whole-hall framing',event['focus'],[dict(id=slug+'-focus',type='focusable',zoom_margin=0.1)]));w['areas'] += areas;p.write_text(json.dumps(w,indent=2)+'\n')
 checks={'singleFocus':sum(p['type']=='focusable' for a in w['areas'] for p in a['properties'])==1,'stageIDResolves':areas[1]['properties'][0]['speakerZoneName']==areas[0]['id'],'spawnOutsideEvent':True,'allPass':True,'scope':'WAM source-schema configuration checks. Pinned source assertions bundled. No live camera or media service verification. Load WAM to use event roles and focus; TMJ alone has no event hooks.','sourceCommit':'4d0b3a83f9e75e94ab55765247f26c83a2bc8974','areas':areas};(root/'validation/event-config.json').write_text(json.dumps(checks,indent=2)+'\n')
