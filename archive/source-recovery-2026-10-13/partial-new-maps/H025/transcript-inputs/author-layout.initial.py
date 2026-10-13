from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def rect(p):x,y,u,v=p;return[[x,y],[u,y],[u,v],[x,v]]
def room(id,art,offset,spawn,bounds=None):return dict(id=id,art=art,offset=offset,spawn=spawn,bounds=bounds or[offset[0],offset[1],1248,1248],walkCoverageRequired=1,walkPolygons=[],solidRects=[],solidPolygons=[],fullFixturePolygons=[],openCells=[],blockedCells=[],foregroundPolygons=[],seats=[],anchors=[],fixtureNegatives=[])
def fixture(r,n,p):
 if isinstance(p[0],int):p=rect(p)
 r['fullFixturePolygons'].append(p);r['fixtureNegatives'].append(dict(name=n,point=[sum(q[0]for q in p)//len(p),sum(q[1]for q in p)//len(p)]))
def anchor(r,id,n,x,y,rad=24):r['anchors'].append(dict(id=id,name=n,anchor=[x,y],radius=rad))
a=room('courtyard','courtyard-r3.png',[0,0],[624,944])
a['walkPolygons']=[[[224,300],[420,301],[449,302],[484,307],[611,307],[626,299],[692,299],[738,312],[805,302],[1014,302],[1059,338],[1075,393],[1040,453],[1038,593],[1119,623],[1119,682],[1087,743],[1050,805],[1006,830],[794,836],[780,900],[728,1001],[632,1016],[547,1000],[513,960],[540,900],[544,829],[263,829],[213,785],[167,721],[129,648],[95,548],[109,479],[139,417],[164,356]],rect([320,288,383,328]),rect([628,288,703,328]),rect([880,288,960,328])]
for n,p in [
 ('Whole north-west facade, pots and ground rocks',[[207,229],[318,229],[318,280],[307,300],[285,308],[265,300],[240,295],[208,281]]),
 ('West guest right facade and pot group',[[374,242],[453,231],[469,246],[461,278],[442,292],[427,304],[396,300],[374,281]]),
 ('Central building full rooted western planting',[[472,222],[627,222],[627,282],[615,306],[597,312],[576,305],[553,312],[527,304],[508,306],[489,292],[477,270]]),
 ('Central door east pot and base',[[694,238],[782,237],[795,277],[780,304],[754,307],[735,318],[716,309],[697,293]]),
 ('Eastern guest west planting and facade',[[787,238],[882,236],[882,279],[861,290],[842,302],[823,300],[805,287]]),
 ('Eastern guest bench and right planted facade',[[940,237],[1038,239],[1046,283],[1025,310],[1008,302],[999,292],[962,293],[942,283]]),
 ('Complete covered cistern stone base and peripheral pottery',[[288,448],[418,447],[437,474],[440,507],[425,533],[398,550],[362,556],[328,553],[305,555],[290,546],[275,528],[266,504],[268,477]]),
 ('Whole cistern eastern rock and rooted shrub group',[[428,459],[466,470],[477,509],[508,527],[520,554],[500,570],[469,573],[450,560],[427,559],[413,545],[437,512]]),
 ('Whole packing canopy, table, feet, baskets and rooted plants',[[1050,353],[1184,361],[1184,585],[1176,606],[1142,618],[1095,605],[1067,584],[1045,569],[1032,530],[1034,492],[1026,460],[1030,417]]),
 ('West woven bench entire low support base',[298,736,387,767]),('East woven bench entire low support base',[890,744,977,775]),
 ('West inside wall whole palm and rooted boulder return',[[100,579],[160,586],[188,616],[217,642],[235,672],[209,697],[188,713],[174,716],[153,688],[130,661]]),
 ('East inside wall rooted scrub return',[[1126,613],[1192,619],[1187,717],[1163,752],[1140,779],[1110,807],[1078,818],[1051,810],[1060,786],[1075,750],[1097,719],[1090,694],[1100,666]]),
 ('North loose shrub grounded patch',[[543,347],[561,343],[574,354],[568,370],[548,374],[534,366]]),
 ('East map-mosaic nearby shrub',[[862,448],[883,450],[895,467],[886,481],[863,481],[851,470]]),
]:fixture(a,n,p)
# Full low perimeter and native scene frontier are audited separately from fixture samples.
for n,p in [('West and south-west full adobe footing',[[173,310],[197,313],[175,391],[141,471],[123,542],[142,613],[183,710],[217,774],[255,823],[512,832],[528,863],[515,903],[482,924],[441,922],[409,904],[258,901],[213,878],[182,839],[157,773],[121,711],[96,646],[72,576],[69,533],[84,458],[117,373]]),('South-east curb and whole gatepost footing',[[745,831],[1070,831],[1106,807],[1146,759],[1185,711],[1220,719],[1217,786],[1186,850],[1148,882],[1092,901],[815,901],[778,919],[733,903]])]:fixture(a,n,p)
a['seats']=[dict(name='West woven saddle bench',anchor=[344,719],direction='south',facing='south',cushionBounds=[310,716,376,743],contactOffset=[0,9]),dict(name='East woven saddle bench',anchor=[936,735],direction='south',facing='south',cushionBounds=[902,725,965,751],contactOffset=[0,9])]
a['foregroundPolygons']=[rect([312,740,375,743]),rect([904,750,966,753])]
# Only actual seat landing tiles may contain the visual seating plane; support cells remain solid.
a['openCells']=[[10,22],[29,22],[29,23]]
for x in range(27,31):a['blockedCells'].append([x,24])
for id,n,x,y,rad in [('arrival','South gate arrival apron',624,944,24),('southGate','Open south gate',624,864,18),('water','Covered cistern reading side',496,480,26),('packing','Pannier packing bay',1008,544,28),('windDoor','West guest-cell threshold',344,288,24),('landmarkDoor','East guest-cell threshold',912,288,24),('roofDoor','Roof-stair room threshold',656,304,24),('westPass','Wide west courtyard route',240,576,16),('eastPass','Wide east courtyard route',1008,672,16),('northPass','North transverse route',656,352,16),('middlePass','Central transverse route',656,576,16)]:anchor(a,id,n,x,y,rad)
b=room('wind-cell','rooms-r2.png',[0,1248],[240,736],[0,1568,448,512]);c=room('landmark-cell','rooms-r2.png',[0,1248],[624,736],[448,1568,352,512]);d=room('roof-stair-room','rooms-r2.png',[0,1248],[1008,736],[800,1568,448,512])
b['walkPolygons']=[rect([82,436,406,695]),rect([164,688,318,769])]
c['walkPolygons']=[rect([484,436,768,695]),rect([563,688,695,769])]
d['walkPolygons']=[rect([846,437,1175,696]),rect([936,688,1085,769]),rect([1118,417,1175,653]),rect([1063,375,1175,410])]
for n,p in [('Wind desk whole legs and footing',[98,409,166,473]),('Blue bed complete headboard legs',[219,393,314,476]),('West cell chair full cushion',[113,469,152,502]),('West cell north plant and pot',[335,420,385,481]),('West cell south rooted pot',[78,643,118,702])]:fixture(b,n,p)
for n,p in [('Red bed complete foot supports',[520,393,621,476]),('West middle pot',[486,447,518,490]),('Landmark desk complete feet',[663,409,738,473]),('Landmark cushion complete base',[679,469,718,503]),('Middle plant whole pot',[721,429,765,501]),('Middle south pot',[483,659,518,703])]:fixture(c,n,p)
for n,p in [('Planning desk complete legs',[889,410,987,490]),('Planning cushion complete base',[914,476,952,515]),('Roof room north-west potted plant',[845,411,885,476]),('Roof room west ground jar',[849,459,884,502]),('Stair west complete raised retaining wall',[[1047,365],[1062,366],[1062,412],[1117,412],[1117,654],[1103,654],[1103,474],[1047,459]]),('Stair north curb',[1050,351,1179,374]),('Stair landing west raised edge',[1048,369,1062,412])]:fixture(d,n,p)
# Whole south cutaway walls reserve all physical bases, not a handpicked post pixel.
for r,lft,rgt,door in [(b,38,441,(161,321)),(c,448,802,(560,697)),(d,810,1218,(934,1088))]:
 fixture(r,'Whole west jamb and cutaway front-wall footing',[lft,698,door[0]-1,800]);fixture(r,'Whole east jamb and cutaway front-wall footing',[door[1],698,rgt,800])
for r,id,n,x,y in [(b,'windExit','West cell south return threshold',240,736),(b,'wind','Wind-ribbon clue',176,480),(b,'windAisle','West cell clear aisle',272,608),(c,'landmarkExit','East cell south return threshold',624,736),(c,'landmark','Landmark clue table',656,480),(c,'landmarkAisle','East cell clear aisle',624,608),(d,'roofExit','Roof room south return threshold',1008,736),(d,'planning','Itinerary chart table',1008,480),(d,'stairFoot','Stair bottom approach',1136,672),(d,'roofLanding','Stair upper usable landing',1136,384),(d,'roofAisle','Roof room clear aisle',1008,608)]:anchor(r,id,n,x,y)
D=dict(id='H025',title='Desert Star Caravanserai',world=[1248,2496],rooms=[a,b,c,d],doors=[['windDoor','windExit'],['landmarkDoor','landmarkExit'],['roofDoor','roofExit']],silentRects=[[576,928,672,992]],stateLayers=['packed-panniers'],completedLayers=['packed-panniers'],overlays=[dict(name='packed-panniers',art='packed-r1.png',rect=[1066,451,1169,537],offset=[0,0])]);(R/'source/design.json').write_text(json.dumps(D,indent=2)+'\n')
