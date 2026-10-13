from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'tools/build.py';s=p.read_text()
a=s.index("art=Image.open");b=s.index('g=np.ones',a)
s=s[:a]+'''art=Image.new('RGBA',(W,H),(255,255,255,255));art.alpha_composite(Image.open(R/D['art']).convert('RGBA').resize((1152,768),Image.Resampling.LANCZOS));art.alpha_composite(Image.open(R/'art/masters/pattern-room-r1.png').convert('RGBA').resize((768,768),Image.Resampling.LANCZOS),(1152,0))
stoolSheet=Image.open(R/'art/masters/stools-r1.png').convert('RGBA');stoolProof=[]
for i,(x,y,w,h)in enumerate(D['stoolPlacements']):
 b=([92,330,668,707],[923,350,1457,707])[i];piece=stoolSheet.crop(b);art.alpha_composite(piece.resize((w,h),Image.Resampling.LANCZOS),(x,y));stoolProof.append(dict(index=i,wholeBounds=b,placement=[x,y,w,h],originalAlpha=True))
art.save(R/D['nativeArt']);js(R/'validation/whole-stool-crops.json',dict(components=stoolProof,scope='Original built-in raster stools with original alpha, mechanically cropped to whole wooden stool including every foot.'))
''' +s[b:]
a=s.index('overlays={};');b=s.index('# Full dynamic footprint',a)
s=s[:a]+'''overlays={};formMeta=[]
sheet=Image.open(R/'art/masters/patterns-r1.png').convert('RGBA');specimens=[];cropProof=[]
boxes=[[30,128,373,474],[405,128,750,474],[783,128,1129,474],[1162,129,1510,474],[30,536,373,907],[405,536,750,907],[783,536,1129,907],[1162,536,1510,907]]
for i,b in enumerate(boxes):
 piece=sheet.crop(b);specimens.append(piece);cropProof.append(dict(index=i,wholeBounds=b,sourceSHA256=hashlib.sha256(piece.tobytes()).hexdigest()))
def placeAll(piece,boxes):
 im=Image.new('RGBA',(W,H))
 for x,y,w,h in boxes:im.alpha_composite(piece.resize((w,h),Image.Resampling.LANCZOS),(x,y))
 return im
# Exact same local bitmask has the same original sample on both shallow trays and the pattern table.
for i,piece in enumerate(specimens):
 name='wet-'+str(i);overlays[name]=placeAll(piece,[[200,339,111,60],[487,339,110,60],[1428,311,212,99]]);formMeta.append(dict(layer=name,mask=i,originalCell=i))
for i,piece in enumerate(specimens):
 name='print-'+str(i);overlays[name]=placeAll(piece,[[976,243,54,64],[1040,243,54,64]]);formMeta.append(dict(layer=name,mask=i,originalCell=i,role='Explicitly lifted and hung print'))
js(R/'validation/whole-pattern-crops.json',dict(scope='Original generated patterns, whole sheets mechanically cropped and placed; no generated procedural paint or recoloring.',components=cropProof))
''' +s[b:]
s=s.replace("name=='clue-0'","name in ['wet-0','print-0']").replace("'scent-popup-'","'marble-popup-'").replace('globalThis.ScentLayout','globalThis.MarbleLayout')
a=s.index('bare=Image.alpha_composite');b=s.index('checks=dict',a)
s=s[:a]+'''bare=Image.alpha_composite(decoded['ground-and-architecture'],decoded['foreground']);assert bare.tobytes()==art.tobytes();empty=base.copy()
for name in ['wet-0','print-0']:empty=Image.alpha_composite(empty,decoded[name])
empty=Image.alpha_composite(empty,above);empty.save(R/'review/decoded-art.png');decoded['ground-and-architecture'].save(R/'review/decoded-ground.png')
stateHashes={};logical=[];contact=Image.new('RGB',(1024,768),'#243029');cd=ImageDraw.Draw(contact)
for wet in range(8):
 for printed in range(8):
  names=['wet-'+str(wet),'print-'+str(printed)];state=base.copy()
  for n in names:state=Image.alpha_composite(state,decoded[n])
  state=Image.alpha_composite(state,above);key=f'wet-{wet}-print-{printed}';stateHashes[key]=hashlib.sha256(state.tobytes()).hexdigest();logical.append(dict(name=key,wet=wet,printed=printed,showLayers=names,complete=printed>0))
  crop=Image.new('RGBA',(256,96));crop.alpha_composite(state.crop((193,333,321,403)),(0,0));crop.alpha_composite(state.crop((970,236,1100,310)).resize((128,70)),(128,0));cd.text((0,0),'',fill='white');i=wet*8+printed;contact.paste(crop,((i%4)*256,(i//4)*48))
assert len(set(stateHashes.values()))==64
contact.save(R/'review/all64-states.png')
''' +s[b:]
s=s.replace("scope='Two illustrated clue specimens and eight original bottled botanical profiles plus unbottled:18 pixel-unique physical displays. Three family amounts are independently1or2; a sample copies the balance only on explicit bottle action.'","scope='Eight wet pass subsets and eight separately copied drying-rack print states, including blank:64 unique physical displays. All three tools are explicit, each applied at most once per sheet. Applying tool order commutes deliberately; fresh sheet and visit reset are explicit.'")
p.write_text(s)
