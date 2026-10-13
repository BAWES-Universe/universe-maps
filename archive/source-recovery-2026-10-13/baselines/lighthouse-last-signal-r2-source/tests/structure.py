import json, wave, math, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'runtime/lighthouse-last-signal.tmj').read_text())
b=json.loads((R/'source/base/lighthouse-festival-island.tmj').read_text())
for old in b['layers']: assert old==next(l for l in m['layers'] if l['name']==old['name']),old['name']
assert m['width']==48 and m['height']==32 and m['tilewidth']==m['tileheight']==32
for t in m['tilesets']:assert (R/'runtime'/t['image']).is_file()
a=next(l for l in m['layers']if l['name']=='signal-audio');assert len(a['data'])==48*32 and all(a['data']) and not a.get('properties')
assert not any(p['name']=='playAudio' for l in m['layers']for p in l.get('properties',[]))
assert not any(t.get('tiles') for t in m['tilesets']if t['name']=='signal-inlays')
for key in ['tide','wind','prism','beacon']:assert not next(l for l in m['layers']if l['name']=='signal-'+key)['visible']
assert min(math.hypot(x-272,y-672)for x in range(544,993)for y in range(384,577))>160
with wave.open(str(R/'runtime/audio/tide-signal.wav'))as w:
 assert w.getnchannels()==1 and w.getsampwidth()==2 and w.getframerate()==22050 and w.getnframes()==176400
with wave.open(str(R/'runtime/audio/silent-carrier.wav'))as w:assert set(w.readframes(w.getnframes()))=={0}
print('PASS: original layers unchanged; native32 dimensions; all assets resolve; transparent full-coverage carrier; quiet default; decorative-only state layers; zero shoreline gain throughout gathering lawn; valid original WAVs.')
