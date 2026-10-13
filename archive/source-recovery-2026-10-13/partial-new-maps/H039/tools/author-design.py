from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=dict(id='H039',title='Paper Marbling Mill',world=[1920,768],art='art/masters/mill-r5.png',nativeArt='source/mill-native.png',spawn=[432,527],rooms=[dict(id='mill-yard',bounds=[0,0,1152,768],spawn=[432,527]),dict(id='pattern-room',bounds=[1152,0,1920,768],spawn=[1552,559])],openRects=[[7,8,7,8],[13,8,13,8],[34,11,34,11],[19,13,19,13],[38,7,57,17],[4,9,19,9],[4,10,4,14],[5,14,19,14],[12,15,15,15],[13,16,15,23],[11,10,13,13],[20,11,21,14],[20,10,20,10],[22,12,31,13],[32,11,33,14],[32,10,34,10]],blockedCells=[],seats=[],anchors=[],doors=[],foregroundPolygons=[],fixtureNegatives=[],visiblePaths=[],scenicBoundaries='Full original mill woods/canal scene and fully enclosed original limestone pattern-room scene. All projected hard fixture silhouettes remain away from admitted floor; the physically separate room has continuous stone enclosure.',stoolPlacements=[[245,465,38,20],[533,465,38,20]])
# Table entire projected footprint including feet.
D['blockedCells'] += [[x,y] for y in range(9,15)for x in range(43,53)]
# All low stool front aprons and supports are in the blocked cell below the actual contact.
D['blockedCells'] += [[x,15]for x in [7,8,16,17]]+[[21,11],[21,14],[34,10]]
for name,x in [('West round beech stool',264),('East rounded beech stool',552)]:
 D['seats'].append(dict(name=name,anchor=[x,463],room='mill-yard',direction='south',cushionBounds=[x-19,465,x+19,479],contactOffset=[0,10]))
 D['foregroundPolygons'].append([[x-14,477],[x+13,477],[x+13,479],[x-14,479]])
def a(id,name,x,y,room='mill-yard',radius=24,**kw):D['anchors'].append(dict(id=id,name=name,anchor=[x,y],room=room,radius=radius,**kw))
a('journal','Mill gate arrival',432,527,radius=24)
a('swirl','West marbling tray',264,303)
a('rake','East marbling tray',552,303)
a('comb','Pattern cabinet comb station',1552,256,room='pattern-room')
a('rack','Drying bridge print rack',1072,367)
a('enter','Mill exterior door approach',432,271,radius=20,to='exit',action='Enter pattern room',description='Enter the mill pattern cabinet room. Your wet pattern and hanging print are preserved.')
a('exit','Pattern room interior door approach',1552,559,room='pattern-room',radius=22,to='enter',action='Return to mill yard',description='Leave through the same mill door. Your marbling work stays unchanged.')
a('inspect','Pattern viewing table',1552,495,room='pattern-room')
for id,n,x,y,r in [('west','West tray side',144,399,'mill-yard'),('middle','Between trays',400,399,'mill-yard'),('east','East tray side',656,416,'mill-yard'),('bridge','Drying bridge deck',848,416,'mill-yard'),('bank','Right-bank landing',1040,431,'mill-yard'),('south','Gate winding return',432,623,'mill-yard'),('roomwest','Table west aisle',1296,399,'pattern-room'),('roomeast','Table east aisle',1776,399,'pattern-room')]:a(id,n,x,y,r,0)
for t in D['anchors']:
 if 'to'in t:D['doors'].append(dict(name=t['name'],id=t['id'],room=t['room'],approach=t['anchor'],to=t['to']))
contours=[('West tray whole base and projected rim',[184,324,327,429]),('East tray full upper rim and body',[471,325,610,416]),('East tray full lower apron and supports',[471,416,608,430]),('Drying rack full upper crossbar and sheets',[940,233,1116,312]),('Drying rack full west post foot',[947,233,965,331]),('Drying rack full east post foot',[1101,233,1116,331]),('North bridge rail entire projection',[688,332,1019,369]),('South bridge rail entire projection',[688,455,1024,499]),('Pattern table whole rim legs and base',[1380,291,1695,473]),('Pattern cabinet entire base',[1228,189,1840,218]),('West stool ground apron feet',[245,480,283,485]),('East stool ground apron feet',[533,480,571,485])]
D['fixtureContours']=[dict(name=n,bounds=b)for n,b in contours]
for n,(x0,y0,x1,y1)in contours:
 for suffix,x,y in [('NW',x0,y0),('NE',x1-1,y0),('SW',x0,y1-1),('SE',x1-1,y1-1),('center',(x0+x1)//2,(y0+y1)//2)]:D['fixtureNegatives'].append(dict(name=n+' '+suffix,point=[x,y],room='pattern-room'if x>=1152 else'mill-yard'))
# Explicit author floor bands, not auto-derived admitted cells.
bands=[('Northern mill-yard promenade',[136,288,632,304]),('Between marbling trays full width',[360,320,440,432]),('West tray incidental side',[136,320,152,432]),('East tray landing',[648,352,664,432]),('Drying bridge64px deck',[712,384,1016,432]),('Bridge west landing',[648,384,696,432]),('Bridge east landing',[1032,352,1080,464]),('Lower courtyard',[296,448,504,464]),('West stool actual approach',[248,448,264,464]),('East stool actual approach',[536,448,552,464]),('South yard walk',[424,512,504,528]),('Main gate64px run',[424,576,504,752]),('Pattern room north aisle',[1224,224,1848,272]),('Pattern room west aisle',[1224,288,1368,560]),('Pattern room east aisle',[1704,288,1848,560]),('Pattern room lower aisle',[1224,480,1848,560])]
D['fullWidthBands']=[dict(name=n,bounds=b)for n,b in bands]
for n,(x0,y0,x1,y1)in bands:D['visiblePaths'].append(dict(name=n,origins=[[x0,y0],[x1,y0],[x1,y1],[x0,y1],[x0,y0]],room='pattern-room'if x0>=1152 else'mill-yard'))
(R/'source/design.json').write_text(json.dumps(D,indent=2)+'\n')
