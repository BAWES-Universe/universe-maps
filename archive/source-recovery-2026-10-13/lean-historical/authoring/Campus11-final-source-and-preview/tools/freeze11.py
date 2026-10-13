from pathlib import Path
import hashlib,json,shutil,zipfile
R=Path(__file__).resolve().parents[1]
A=Path('/workspace/shared/campus11-fire-access-audit')
P=R/'publication/v11'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
(R/'docs/fire11').mkdir(exist_ok=True)
for n in ['INTEGRATED11-VERIFICATION-RECEIPT.json','integrated-compiled-pixel-verification.json','integrated-native-route-verification.json','integrated-visual-envelope-verification.json','integrated-all-contact-pixel-head-verification.json','integrated-deep-seat-native-taps.json','integrated-before-after-bottlenecks.png','integrated-campfire-empty-and-occupied.png','integrated-stationary-bench-contact-sheet.png']:
 shutil.copy2(A/n,R/'docs/fire11'/n)
shutil.copy2(A/'integrated-before-after-bottlenecks.png',P/'campfire-before-after.png')
shutil.copy2(A/'integrated-campfire-empty-and-occupied.png',P/'campfire-native.png')
summary={
 'revision':'Campus11','status':'Frozen map-only preview; no live-room or physical-phone acceptance claim',
 'baseline':'https://bawes-universe.github.io/universe-maps/butterfly-town/v10/map32/magical-campus.tmj',
 'sourceMapSHA256':sha(R/'map32/magical-campus.tmj'),'publicationMapSHA256':sha(P/'map32/magical-campus.tmj'),
 'worldPixels':[2944,2624],'tilePixels':32,'avatarPixels':32,'bodyPixels':[16,16],
 'changes':{'collisionCellsOpened':29,'spawnCenter':[1248,1536],'spawnArea':[1232,1520,32,32],'silentArea':[1200,1504,96,96],'signTopLeft':[1288,1656]},
 'checks':{'campfireTapLegs':748,'campfireDirectionalJourneys':20,'headClearPositions':72539,'headFramesEach':12,'arrivalLegs':14,'arrivalHeadFrames':6901,'fountainPointsOutsideSilence':39,'animationFramesByteIdentical':60,'preservedCivicAudioEffectFiles':79,'runtimeRebuildFilesIdentical':23,'publicationFrameComparisons':10860,'collisionMembershipEquivalent':True,'relativeAssetClosureValid':True},
 'preserved':{'eventSeats':24,'officeWorkSeats':8,'receptionPositions':2,'audio':True,'animationPositionTimingAndPixels':True,'previousVersions':True},
 'limits':['Bench access uses normal standing Woka frames; the south backrest provides static lower-body overlap. No sitting animation or automatic snapping.','Some fire-court bottlenecks remain one32px cell wide, giving16px of center travel for the16px body.','Native tap paths do not route around other people.','Only compiled-pixel, source-model and build checks are represented; live-room and physical-mobile acceptance remain pending.','Native spawn silence preserves ambient audio; the existing initial-connection grouping race tracked in issue735 is not changed.','Optional WAM broadcast configuration is not installed by a TMJ URL and requires supported room setup and a successful native space join.']}
dump(P/'validation-summary.json',summary)
readme='''# Campus11: campfire access and junction arrival\n\nA focused, separately versioned repair of the user-tested Campus10 map. The four fire-court bench positions, the northeast planter escape and both clockwise/counterclockwise loops are reachable on the existing32px native grid. Two small bench receivers were authored to match their fixed physical footprints; the fire, original water/lighting effects and surrounding scenery remain registered. Low rail/plant ownership is fixed per object; there are no player-following masks or conditional collision changes.\n\nThe arrival and its single silent area move together to the east diamond junction. A physical directional board sits beside the route with paths toward Student Hub, reception/meetings, classroom, stage, campfire and market. The fountain social area is outside the relocated silence. Native silence prevents ordinary proximity initiation while retaining ambience; it does not fix the game's separate initial-connection grouping race (#735).\n\n## Use\n\nImport map32/magical-campus.tmj. Its relative dependencies reuse hash-recorded, preserved Campus09/10 assets. Keep those served paths. This preview does not replace Campus10 or any gate. The giant gate remains a separate map that the owner can connect using the existing room editor.\n\nmap32/magical-campus.wam is an OPTIONAL fresh-room stage/audience template. A TMJ URL alone does not install it. Do not overwrite an existing room's WAM with this minimal file. Preserve unrelated areas/entities when merging. Native podium/audience controls depend on the deployment's broadcast-area feature flag; successful role/space connection is not verified here.\n\n## Verified and remaining limits\n\n748 tap-route legs and20 directional journeys pass against the pinned native32 path/body contract. Both full loops, the screenshot escape points and all four bench returns connect. The compiled foreground has zero opaque head cuts across72,539 valid fire-court positions and12 cardinal frames. Fourteen arrival/return legs and6,901 walking frames pass. All60 animation frames, positions and timing,24 event seats and native audio remain unchanged. The23-file standalone runtime rebuilds byte-identically.\n\nThese are source-model and compiled-pixel checks, not a live-room or physical-phone playtest. Bench positions use the ordinary Woka standing frames, with a static south backrest overlap; there is no animated sit pose or autosnap. Native paths ignore other people. Some fire-court gaps remain32px wide rather than a broad promenade.\n\n## Provenance and preservation\n\nThe bounded bench repair was authored with the built-in image tool from the project's own garden artwork. Only registered bench receivers are adopted; the original and intermediate masters remain in the separately preserved source checkpoint. The board is project-authored SVG. No Conference Campus or other third-party artwork was copied. Original asset rights and attribution are unchanged; no new blanket license is assigned.\n\nThe publication is additive and references preservedv9/v10 image/audio assets. The defined decoded texture footprint is49,811,456RGBA bytes; this avoids re-uploading the existing23.87MB of dependencies. The new TMJ plus atlas is393,757bytes. No engine change, deployment of game code, or PR merge is part of this update.\n'''
(P/'README.md').write_text(readme)
shutil.copy2(R/'companion-stage/README.md',P/'stage-setup.md')
dep=json.loads((P/'equivalence-and-dependencies.json').read_text())
for e in dep['sharedPreservedFiles']:e.pop('localPath',None)
dump(P/'asset-dependencies.json',dep)
# Machine/build-only reports remain in the durable source checkpoint rather than the hosted bundle.
publicnames=['README.md','validation-summary.json','asset-dependencies.json','overview.jpg','arrival-native390.png','campfire-before-after.png','campfire-native.png','stage-setup.md','map32/magical-campus.tmj','map32/magical-campus.wam','map32/campus11-changed-p0.png']
manifest={'revision':11,'sourceBase':'master','sourceBranch':'maps/campus11-fire-access-arrival','sourcePrefix':'public/butterfly-town/v11/','servedPrefix':'butterfly-town/v11/','files':[{'path':n,'bytes':(P/n).stat().st_size,'sha256':sha(P/n)} for n in publicnames], 'dependencyCount':len(dep['sharedPreservedFiles']), 'preserveEveryExistingSourceAndServedPath':True}
manifest['totalNewBytes']=sum(e['bytes'] for e in manifest['files']);dump(R/'publication/upload-manifest11.json',manifest)
# Durable overlay: apply to an isolated copy of the preserved corrected24 Campus10 source.
staging=R/'checkpoint11';staging.mkdir(exist_ok=True)
selected=[R/'BASELINE-CAMPUS10.json']
selected += list((R/'tools').glob('*11.py'))
selected += list((R/'sources/arrival11').glob('*'))
selected += [p for p in (R/'sources/fire11').glob('*') if p.is_file() and p.name not in ['bench-registration-master.png','south-fire-facing-master.png','garden-final-art-candidate.png']]
selected += [R/'sources/garden/collision-grid-8px.json']
selected += [R/'docs/rebuild11-verification.json',R/'docs/native32-pixel-verification.json',R/'docs/runtime11-closure-verification.json',R/'docs/spawn-silence11.json',R/'docs/preserved-scene-components11.json']
selected += [p for p in (R/'docs/fire11').glob('*.json')]
selected += [p for p in (R/'docs/arrival11').glob('*.json')]
selected += [R/'publication/upload-manifest11.json',P/'publication-equivalence-verification.json',P/'equivalence-and-dependencies.json']
selected += [P/n for n in publicnames]
selected=sorted(set(selected))
checkpoint={'baseRequired':'Corrected24 Campus10 preserved editable source; apply this overlay to an isolated copy, then python3 tools/build_revision11.py','basePublicationCommit':'6d53b7f4eac966679b4842424c622291cbdf0bf3','baseSourceLibrary':'libfile_2aeef041f6b48191922ce193951545df version1','basePublicationLibrary':'libfile_ec4429512ec48191b53298c85f1f3bd5 version1','originalBenchGenerationMasters':'libfile_147fc43558ac8191a573eb738dc7f061 version0','sourceMapSHA256':summary['sourceMapSHA256'],'leanMapSHA256':summary['publicationMapSHA256'],'files':[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size} for p in selected]}
dump(staging/'CHECKPOINT.json',checkpoint)
out=staging/'Campus11-final-source-and-preview.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 z.write(staging/'CHECKPOINT.json','CHECKPOINT.json')
 for p in selected:z.write(p,str(p.relative_to(R)))
dump(staging/'ZIP-RECEIPT.json',{'path':str(out),'sha256':sha(out),'bytes':out.stat().st_size,'files':len(selected)+1})
print(json.dumps({'zipBytes':out.stat().st_size,'zipSHA256':sha(out),'publicFiles':len(publicnames),'publicBytes':manifest['totalNewBytes'],'sourceMap':summary['sourceMapSHA256'],'leanMap':summary['publicationMapSHA256']}))
