"""Translate frozen B at native scale; add only declared outside approach cells."""
from pathlib import Path
import json,copy,hashlib
R=Path(__file__).resolve().parents[1];F=R/'source/frozen-b';S=R/'source';DX,DY=128,256;W,H=88,76
read=lambda n:json.loads((F/n).read_text());write=lambda n,d:(S/n).write_text(json.dumps(d,indent=2)+'\n')
point=lambda p:[p[0]+DX,p[1]+DY]
rect=lambda r:point(r[:2])+r[2:]
box=lambda r:point(r[:2])+point(r[2:])
# Names below are world-coordinate contracts, not arbitrary numeric arrays.
pointkeys={'xy','anchor','center','artAnchor','floorClick','rowFront','staffAnchor','staffFloorClick','customerAnchor','customerFloorClick','customerVisualAnchor'}
boxkeys={'bounds','foyerInterior','terraceDoor','mainArrivalOpening','terraceInterior','coffeeCounterBounds','coffeeCustomerApron','coffeeStaffAllowance','preservedHallXYXY'}
def translated(v,key=''):
 if isinstance(v,dict):
  d={k:translated(x,k)for k,x in v.items()}
  if isinstance(v.get('x'),(int,float)):d['x']=v['x']+DX
  if isinstance(v.get('y'),(int,float)):d['y']=v['y']+DY
  return d
 if isinstance(v,list):
  if 'local' in key.lower():return copy.deepcopy(v)
  if key in pointkeys:return point(v)
  if key.lower().endswith('xyxy')or key in boxkeys or key=='xyxy':return box(v)
  if key.lower().endswith('xywh')or key in {'xywh','floorClickRect'}:return rect(v)
  if key=='hallDoors':return[box(x)for x in v]
  if key=='centerline':return[point(x)for x in v]
  if key in {'closedCells','openedCells','addedSolidCells'}:return[[x+4,y+8]for x,y in v]
  return[translated(x)for x in v]
 return v
b=read('collision-grid.json');g=[[1]*W for _ in range(H)]
for y,row in enumerate(b['grid']):g[y+8][4:84]=row
for y in range(68,76):
 for x in range(24,32):g[y][x]=0
c=translated({k:v for k,v in b.items()if k not in {'grid','anchors','start','speaker'}})
c.update(width=W,height=H,tileSize=32,grid=g,start=[896,2176],speaker=point(b['speaker']),anchors=[[a,x+DX,y+DY]for a,x,y in b['anchors']])
c['landmarks'].extend([{'id':'south-exterior-spawn','x':896,'y':2176},{'id':'south-reveal-approach','x':896,'y':2112},{'id':'south-path-end','x':896,'y':2384}]);write('collision-grid.json',c)
q=[[0]*W for _ in range(H)]
for y in range(66,70):
 for x in range(26,30):q[y][x]=1
write('quiet-grid.json',{'width':W,'height':H,'tileSize':32,'grid':q,'quietRectangles':[{'id':'outside-spawn-only','xywh':[832,2112,128,128]}],'note':'Sole native TMJ silent layer. No WAM silent properties; all previous circulation silence removed.'})
seats=translated(read('seats.json'));write('seats.json',seats)
garden=translated(read('garden-layout.json'));garden.update(worldPixels=[2816,2432],status='C translated frozen B garden; exact pavilion/collision preserved',roofless=False,canopyIntent='Pavilion remains open-center and fixed; building shell is a separate dynamic owner.');write('garden-layout.json',garden)
l=read('runtime-layout.json');keys=['preservedHallXYXY','foyerInterior','foyerInteriorTiles','hallDoors','terraceDoor','mainArrivalOpening','terraceInterior','groupBays','coffeeCounterBounds','coffeeCustomerApron','coffeeStaffAllowance','informalPairs','furniture','socialAnchors','reviewActors','solidTileRectangles','reception','sourceMeetingDistanceDefaults']
l=translated({k:l[k]for k in keys});l.update(status='Local Building C candidate; final tests and review pending',tileSize=32,worldPixels=[2816,2432],worldTiles=[88,76],spawn=[896,2176],spawnRectangle=[864,2144,64,64],quietTileRectangles=[{'id':'outside-spawn-only','xywh':[832,2112,128,128]}],garden=garden,nativeFocus={'bounds':[128,256,1536,1008],'zoomMargin':.15,'cameraOwner':'Existing native focus only; no exterior camera scripting','rotationLimitation':True},zonesNote='Four companion native meeting areas and podium/audience require actual room setup; Custom TMJ alone does not import companion WAM.',translation=[DX,DY],addedExteriorWalkableXYXY=[768,2176,1024,2432]);write('runtime-layout.json',l)
a=read('animation-placement.json');a['asset']='assets/garden-leaf-accent-native.png'
for p in a['placements']:p['cell']=[p['cell'][0]+4,p['cell'][1]+8]
write('animation-placement.json',a)
wam=json.loads((F/'grand-auditorium.wam').read_text().replace('v08','v09'));wam=translated(wam)
for area in wam['areas']:
 if any(p['type']=='start'for p in area['properties']):area.update(x=864,y=2144,width=64,height=64)
write('companion.wam',wam)
assert all(g[y+8][4:84]==row for y,row in enumerate(b['grid']))
assert sum(v==0 for row in g for v in row)==sum(v==0 for row in b['grid']for v in row)+64
write('geometry-translation-contract.json',{'sourceVersion':'v08 frozen Garden B','translationPixels':[DX,DY],'translationTiles':[4,8],'worldPixels':[2816,2432],'preservedSourceRectXYXY':[128,256,2688,2176],'newWalkableCells':[[x,y]for y in range(68,76)for x in range(24,32)],'allOtherAddedCellsBlocked':True,'quietCells':16,'quietXYWH':[832,2112,128,128],'spawn':[896,2176],'spawnXYWH':[864,2144,64,64],'nativeBodyAtSpawnXYXY':[888,2176,904,2192],'counts':{'hallSeats':len(seats),'meetingSeats':sum(bool(s.get('group'))for s in c['socialAnchors']),'casualSeats':sum(not s.get('group')for s in c['socialAnchors'])},'frozenInputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(F.iterdir())if p.is_file()}})
print('Native translation complete; open cells',sum(v==0 for row in g for v in row))
