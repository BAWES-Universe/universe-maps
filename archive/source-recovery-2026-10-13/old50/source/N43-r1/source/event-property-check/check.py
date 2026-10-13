#!/usr/bin/env python3
"""Source-method fixture; not an engine, schema-library, browser or live-media test."""
import json, pathlib, hashlib
root=pathlib.Path(__file__).resolve().parent
s={p.name:p.read_text() for p in (root/'source').glob('*.ts')}
checks=[]
def check(name, ok):
    checks.append({'check':name,'passed':bool(ok)})
    assert ok, name
check('WAM speaker schema', 'type: z.literal("speakerMegaphone")' in s['types.ts'] and 'name: z.string()' in s['types.ts'])
check('WAM listener schema', 'type: z.literal("listenerMegaphone")' in s['types.ts'] and 'speakerZoneName: z.string()' in s['types.ts'])
check('WAM area id resolves to speaker name', 'area.id === areaId' in s['Utils.ts'] and 'return speakerMegaphoneProperty.data.name' in s['Utils.ts'])
check('WAM streaming starts on speaker entry', 'space.startStreaming();' in s['AreasPropertiesListener.ts'])
check('focus margin defaults zero', 'margin = 0,' in s['CameraManager.ts'])
check('focus margin multiplies target dimensions', '1 + margin' in s['CameraManager.ts'] and 'width * multiplier' in s['CameraManager.ts'] and 'height * multiplier' in s['CameraManager.ts'])
check('focus fits both dimensions', 'Math.min(realSize.width / viewportWidth, realSize.height / viewportHeight)' in s['WaScaleManager.ts'])
check('WAM load is explicit', 'else if (_room.wamUrl)' in s['GameScene.ts'] and 'if (this.wamUrlFile)' in s['GameScene.ts'])
fixture={'version':'2.0.0','mapUrl':'./map.tmj','entities':{},'entityCollections':[],'areas':[
 {'id':'hall-focus','name':'Whole event hall','x':320,'y':160,'width':640,'height':672,'visible':True,'properties':[{'id':'hall-focus-property','type':'focusable','zoom_margin':0.1}]},
 {'id':'stage-area','name':'Stage','x':320,'y':160,'width':640,'height':256,'visible':True,'properties':[{'id':'stage-speaker','type':'speakerMegaphone','name':'Main Stage','chatEnabled':False}]},
 {'id':'audience-area','name':'Audience','x':320,'y':448,'width':640,'height':384,'visible':True,'properties':[{'id':'audience-listener','type':'listenerMegaphone','speakerZoneName':'stage-area','chatEnabled':False}]}]}
areas=fixture['areas']; lookup={a['id']:a for a in areas}
check('unique area and property IDs',len(lookup)==len(areas) and len({p['id'] for a in areas for p in a['properties']})==sum(len(a['properties']) for a in areas))
listener=areas[2]['properties'][0]; speaker=lookup[listener['speakerZoneName']]['properties'][0]
check('listener target exists and is speaker',speaker['type']=='speakerMegaphone')
check('speaker and audience have no overlap',areas[1]['y']+areas[1]['height']<=areas[2]['y'])
check('focus contains both role rectangles', all(a['x']>=areas[0]['x'] and a['y']>=areas[0]['y'] and a['x']+a['width']<=areas[0]['x']+areas[0]['width'] and a['y']+a['height']<=areas[0]['y']+areas[0]['height'] for a in areas[1:]))
check('no silent zones',not any(p['type']=='silent' for a in areas for p in a['properties']))
(root/'example.wam').write_text(json.dumps(fixture,indent=2)+'\n')
report={'commit':'4d0b3a83f9e75e94ab55765247f26c83a2bc8974','method':'Read-only pinned source assertions plus independent illustrative fixture geometry and ID checks. Not Zod execution, engine execution, import, browser, or live-media verification.','checks':checks,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'source').glob('*.ts')}}
(root/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'report':str(root/'report.json')}))
