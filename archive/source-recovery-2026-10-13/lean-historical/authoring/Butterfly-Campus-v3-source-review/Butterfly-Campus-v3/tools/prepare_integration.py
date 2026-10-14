from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];m=json.load(open(R/'map/butterfly-campus.tmj'));areas={a['name']:a for l in m['layers'] for a in l.get('objects',[]) if a.get('class')=='area'}
labels={'hq-cedar-meeting':'Cedar Meeting Room','hq-olive-meeting':'Olive Meeting Room','hq-willow-meeting':'Willow Meeting Room','learning-inside':'Learning Hall','creative-design-review':'Design Review','events-stage':'Lantern Stage','events-audience':'Lantern Stage Audience'}
def native(name,kind):
 a=areas[name];o={k:a[k] for k in ['name','x','y','width','height']};o.update(id=name,name=labels.get(name,name),visible=True)
 if kind=='meeting':p={'id':name+'-native-call','type':'livekitRoomProperty','roomName':labels.get(name,name.replace('-',' ').title()),'livekitRoomConfig':{'startWithAudioMuted':True,'startWithVideoMuted':True,'disableChat':False}}
 elif kind=='speaker':p={'id':'events-stage-native-call','type':'speakerMegaphone','name':'The Lantern Stage','chatEnabled':True}
 else:p={'id':'events-audience-native-call','type':'listenerMegaphone','speakerZoneName':'events-stage','chatEnabled':True}
 o['properties']=[p];return o
native_areas=[native(n,'meeting') for n in ['hq-cedar-meeting','hq-olive-meeting','hq-willow-meeting','learning-inside','creative-design-review']]+[native('events-stage','speaker'),native('events-audience','audience')]
proposal={'version':'2.0.0','mapUrl':'./butterfly-campus.tmj','entities':{},'entityCollections':[],'areas':native_areas}
json.dump(proposal,open(R/'integration/native-areas-proposal.wam','w'),indent=2)
hooks=[]
for name,cap in [('gate-onboarding-guide','Onboarding guide'),('campus-guide-stop','Campus guide'),('hq-reception','StudentHub reception'),('creative-imagine-images','Imagine image workflow'),('creative-music','ImagineMusic / ACE-Step workflow'),('creative-design-review','Designer collaboration'),('research-lab','Research assistant workflow'),('operations-command','Linear and operations tools'),('sales-research','Attio and sales research')]+[(f'market-booth-{i}','Student commerce or showcase') for i in range(1,5)]:
 a=areas[name];hooks.append({'id':name,'areaName':name,'bounds':{k:a[k] for k in ['x','y','width','height']},'intendedCapability':cap,'enabled':False,'status':'Prepared activity zone; live binding and permissions need deployment-specific setup'})
json.dump({'version':1,'map':'butterfly-campus.tmj','hooks':hooks},open(R/'integration/interaction-hooks.json','w'),indent=2)
policy=R/'map/audio/runtime-policy.json'
if policy.is_file():
 (R/'integration/audio-policy.json').write_text(policy.read_text())
else:
 json.dump({'enabled':False,'integrationStatus':'Native water modules disabled until compatible deployed engine is verified.'},open(R/'integration/audio-policy.json','w'),indent=2)

layout=json.load(open(R/'layout.json'))
json.dump({'activeInternalPortals':[{'area':'gate-threshold','behavior':'same-map teleport','destination':layout['campus']['spawn']},{'area':'campus-return','behavior':'same-map teleport','destination':layout['gate']['spawn']}],'externalDestinations':[],'extensionStatus':'Private/focus rooms, additional Universe places and student-created spaces require verified room URLs, access rules and return spawns. No broken or placeholder exit URLs are installed.'},open(R/'integration/portal-extension-plan.json','w'),indent=2)
