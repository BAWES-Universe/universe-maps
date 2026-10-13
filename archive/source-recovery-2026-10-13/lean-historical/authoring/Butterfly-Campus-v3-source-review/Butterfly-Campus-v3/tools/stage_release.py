from pathlib import Path
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];D=R/'repo-addition/public/butterfly-town/v3';D.mkdir(parents=True,exist_ok=True)
m=json.load(open(R/'map/butterfly-campus.tmj'))
refs=['butterfly-campus.tmj']+[ts['image'] for ts in m['tilesets']]+[str(p.relative_to(R/'map')) for folder in ['scripts','audio'] for p in sorted((R/'map'/folder).rglob('*')) if p.is_file()]
for f in refs:
 target=D/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/'map'/f,target)
shutil.copyfile(R/'evidence/campus-overview-exterior.png',D/'preview.png')
shutil.copyfile(R/'docs/ART-PROVENANCE.md',D/'ART-PROVENANCE.md')
if (R/'docs/AUDIO-ACTIVATION.md').is_file():shutil.copyfile(R/'docs/AUDIO-ACTIVATION.md',D/'AUDIO-ACTIVATION.md')
(D/'README.md').write_text('''# Butterfly Campus v3 · candidate\n\nImport entry: `butterfly-campus.tmj`. Keep `tilesets/` and `scripts/` beside it.\n\nA fuller StudentHub workplace and public student campus, with a quiet gate, fountain, commons, three meeting rooms, classroom, stage/audience, creative/media, research, operations/sales and market.\n\nThis folder is self-contained and separate from earlier versions. It has not been published. The map script handles only local scene/roof behavior. Bounded fountain/cascade audio is packaged but stays off until compatible native playback is deployed and accepted. Named areas are prepared for later approved native media and bot setup. A pasted TMJ does not activate WAM meeting or stage properties, create bots, or grant private-room permissions.\n\nArtwork uses native32px world tiles and deliberately scaled individual props. It does not add high-DPI renderer support or sitting animation. Objects are static TMJ layers; individually movable/Y-sorted objects require the native WAM entity route.\n''')
manifest=[]
for p in sorted(D.rglob('*')):
 if p.is_file() and p.name not in ['SHA256SUMS.txt','RELEASE.json']:manifest.append({'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
release={'family':'butterfly-town','version':'v3-candidate','status':'local-review-unpublished','entry':'butterfly-campus.tmj','baseRepository':'BAWES-Universe/universe-maps','baseBranch':'master','reviewedBaseCommit':'adabef710832cbb4a1662a8b9f77a493b4e5ecf3','engineContractCommit':'5e7670be6c79efc575a7193e8a1a1c8c379b293f','files':manifest,'tileSize':32,'mapSize':[128,104],'audioEnabled':False,'audioCompatibilityCommit':'3fccc2890dbd30ed48bdefe79b00be0e0c915af8','laterNativeAudioHead':'8380a80f60f3427807257cdaaabd1b11580dadbf','laterNativeAudioHeadRetested':False,'nativeMediaAndBots':'Prepared areas only; deployment setup pending','protectedExistingVersions':'No earlier map or engine file is part of this addition'}
release['runtimeBundleSha256']=hashlib.sha256(''.join(f['path']+'\0'+f['sha256']+'\n' for f in manifest if f['path'] in refs).encode()).hexdigest()
release['bundleSha256']=hashlib.sha256(''.join(f['path']+'\0'+f['sha256']+'\n' for f in manifest).encode()).hexdigest()
(D/'RELEASE.json').write_text(json.dumps(release,indent=2));(R/'RELEASE.json').write_text(json.dumps(release,indent=2));(D/'SHA256SUMS.txt').write_text(''.join(f"{f['sha256']}  {f['path']}\n" for f in manifest))
print(json.dumps({'files':len(manifest),'bytes':sum(f['bytes'] for f in manifest),'mapSha':next(f['sha256'] for f in manifest if f['path']=='butterfly-campus.tmj')}))
