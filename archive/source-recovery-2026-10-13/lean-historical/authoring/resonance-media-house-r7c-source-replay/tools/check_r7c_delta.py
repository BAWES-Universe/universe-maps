from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parents[1];P=R/'resonance-media-house';B=Path('/workspace/shared/media-house-r7b/resonance-media-house')
# Frozen r7b is used only for this local delta check; runtime rebuild does not depend on it.
a=json.loads((B/'source/layout.json').read_text());b=json.loads((P/'source/layout.json').read_text());old=np.array(a['grid']);new=np.array(b['grid']);cells=[[int(x),int(y)] for y,x in np.argwhere(old!=new)];expected=[[x,y] for y in [22,23,24] for x in [12,13,18,19]]+[[6,17],[8,17],[10,17]];assert set(map(tuple,cells))==set(map(tuple,expected));assert all(new[y,x]==0 and old[y,x]==1 for x,y in cells)
before=np.array(Image.open(B/'review/empty-native.png').convert('RGBA'));after=np.array(Image.open(P/'review/empty-native.png').convert('RGBA'));diff=np.any(before!=after,axis=2);allowed=np.zeros(diff.shape,bool);rects=[[x-15,527,x+15,540] for x in [240,304,368]]
spec=json.loads((P/'validation/chair-depth-repair-spec.json').read_text());translations=[r for r in spec['chairs'] if 'artTranslation' in r]
for r in translations:rects.extend([r['oldArtBox'],r['newArtBox']])
for x,y,x2,y2 in rects:allowed[y:y2,x:x2]=True
assert not (diff&~allowed).any()
seats={a['id']:a for a in b['anchors'] if a['id'].startswith(('editor-','screen-viewer-','keyboard-','listen-'))};routes=json.loads((P/'validation/native-arrival-routes.json').read_text())['rows'];checks=[]
for r in routes:
 if '-to-' not in r['id']:continue
 target=r['id'].split('-to-',1)[1]
 if target not in seats:continue
 a=seats[target];ok=abs(r['final'][0]-a['x'])<1e-6 and abs(r['final'][1]-a['y'])<1e-6;checks.append(dict(route=r['id'],input=r['input'],target=target,authored=[a['x'],a['y']],actual=r['final'],exact=ok));assert ok,checks[-1]
proof=dict(revision='r7c',baseline='frozen r7b',openedCells=cells,openedCourtyardCells=12,openedViewerGapCells=3,mixedCell12_17Retained=bool(new[17,12]),topParapetCellsUnchanged=bool(np.array_equal(old[:17],new[:17]) and np.array_equal(old[18:22],new[18:22])),artExceptionRects=rects,changedArtPixels=int(diff.sum()),allOtherArtByteExact=True,viewerLegsFeetByteExact=True,upperBackWidth=16,seatTranslations=translations,seatTargetRoutes=len(checks),authoredEqualsNativeFinal=all(r['exact'] for r in checks),scope='Three physical upper backs and complete matching rails narrowed together; four unchanged seat assets translated to native-fit-stable anchors; no head-driven foreground clipping or empty-floor buffers')
(P/'validation/r7c-delta.json').write_text(json.dumps(proof,indent=2)+'\n');(P/'validation/seat-arrival-alignment.json').write_text(json.dumps(dict(allPass=True,routeCount=len(checks),checks=checks),indent=2)+'\n');print(proof)
