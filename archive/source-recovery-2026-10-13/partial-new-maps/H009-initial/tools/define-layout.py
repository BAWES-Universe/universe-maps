from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1]
D={'tileSize':32,'title':'Mechanical Orchard','slug':'mechanical-orchard','globalLayout':'MechanicalOrchardLayout','worldTiles':[88,36],'rooms':{'orchard':{'offset':[0,0],'size':[1536,1024],'source':'art/orchard-master-r5.png','rows':{}},'house':{'offset':[1792,96],'size':[768,512],'source':'art/cam-house-master-r1.png','rows':{}}},'physicalFootprints':{'orchard':[],'house':[]},'anchors':{},'seats':[],'quietRect':[23,28,26,30],'foregroundPolygons':{},'blockedCells':{},'scenic':['A complete original walled orchard, three individually cam-driven low sculptures and matching enterable cam house. Paved north and south crossovers connect two inter-island aisles and outer paths. Three tree projected envelopes remain wholly on blocked planted islands, including all foliage.','Both bent-branch benches retain continuous front aprons and complete feet. Contact proofs use unchanged native standing frames; no sitting or facing is claimed.','Initial wicket join alone is quiet. House doors preserve local visitor state. Full reload clears the temporary preset. No networking, vehicle physics, audio, deployed service or durable storage.'],'feedback':{'sourcePhases':{'1':'art/orchard-phase2-master.png','2':'art/orchard-phase3-master.png'},'phaseOffset':[0,23],'patches':{'petal':[[237,316],[425,316],[472,361],[475,455],[435,488],[226,488],[188,433],[192,365]],'leaf':[[676,316],[856,316],[923,358],[935,440],[886,482],[658,482],[612,428],[624,367]],'fruit':[[1117,316],[1294,316],[1356,363],[1354,444],[1323,483],[1090,483],[1058,443],[1061,371]]}}}
def rows(room,lo,hi,*spans):
 for y in range(lo,hi+1):D['rooms'][room]['rows'][str(y)]=[list(s)for s in spans]
rows('orchard',5,5,(10,13),(22,25),(35,38));rows('orchard',6,6,(8,16),(21,26),(31,40));rows('orchard',7,7,(6,42));rows('orchard',8,8,(4,43));rows('orchard',9,18,(3,44));rows('orchard',19,20,(6,41));rows('orchard',21,22,(7,13),(15,28),(30,40));rows('orchard',23,23,(8,12),(20,27),(33,39));rows('orchard',24,26,(22,25));rows('orchard',27,27,(21,27));rows('orchard',28,29,(21,27));rows('orchard',30,30,(23,26))
rows('house',4,4,(5,18));rows('house',5,5,(5,20));rows('house',6,8,(3,20));rows('house',9,9,(4,20));rows('house',10,11,(10,13));rows('house',12,12,(10,13));rows('house',13,14,(8,16));rows('house',15,15,(8,16))
def poly(room,name,p):D['physicalFootprints'][room].append({'name':name,'polygon':p})
def rect(room,name,x0,y0,x1,y1):poly(room,name,[[x0,y0],[x1,y0],[x1,y1],[x0,y1]])
# Complete island envelopes include plants, projected upright faces, rim, pedestal, and all aprons.
for name,cx,rx in [('west petal island',333,188),('central leaf island',772,179),('east fruit island',1203,187)]:
 poly('orchard',name+' complete bed and hard rim',[[round(cx+rx*math.cos(a*math.pi/180)),round(441+139*math.sin(a*math.pi/180))]for a in range(0,360,10)])
for name,x0,y0,x1,y1 in [('west island first upright',334,272,364,335),('west island second upright',416,283,445,347),('central first upright',708,273,737,337),('central second upright',828,283,857,341),('east first upright',1094,289,1121,350),('east second upright',1175,278,1206,350),('east third upright',1288,289,1318,350),('west crank whole pedestal',297,510,371,582),('center crank whole pedestal',747,508,828,583),('east crank whole pedestal',1188,509,1250,583)]:rect('orchard',name,x0,y0,x1,y1)
# Full solid boundaries: whole door leaves, front walls, planters and lower wall contacts.
rect('orchard','house west wall full projection',578,0,696,179);rect('orchard','house east wall full projection',840,0,956,180)
rect('orchard','house west open door full leaf',703,59,733,175);rect('orchard','house east open door full leaf',811,59,840,175)
poly('orchard','house west flowerbed complete frontier',[[442,121],[574,95],[682,141],[696,177],[668,201],[575,201],[549,177],[446,164]])
poly('orchard','house east flowerbed complete frontier',[[856,131],[971,109],[1074,118],[1100,157],[994,178],[972,200],[875,200],[850,176]])
poly('orchard','west lower corner greenery full envelope',[[52,602],[116,610],[157,620],[177,629],[189,669],[213,708],[211,761],[191,775],[0,836],[0,599]])
poly('orchard','east lower corner greenery full envelope',[[1351,611],[1464,586],[1535,601],[1535,845],[1329,787],[1320,745],[1319,685],[1343,667]])
poly('orchard','southwest complete wall and planted band',[[0,751],[442,748],[470,716],[497,718],[511,757],[542,720],[581,705],[634,741],[660,777],[697,769],[704,863],[0,905]])
poly('orchard','southeast complete wall and planted band',[[842,769],[921,776],[949,716],[982,708],[1006,752],[1105,766],[1120,750],[1329,754],[1535,789],[1535,928],[848,865]])
# Keep complete bench aprons hard; only the actual raised slab allows contact.
for name,x0,x1 in [('west branch bench',229,324),('east branch bench',1212,1308)]:
 rect('orchard',name+' continuous front apron and all feet',x0,711,x1,737)
 rect('orchard',name+' whole west grounded arm',x0,678,x0+11,735)
 rect('orchard',name+' whole east grounded arm',x1-11,678,x1,735)
# Native half-size interior full hard contacts, including shelf feet and cabinet plinth.
rect('house','north wall and shelf full projected envelope',169,0,589,125)
rect('house','left shelf foot',185,120,203,136);rect('house','right shelf foot',567,120,584,136)
poly('house','gear rack full envelope and all grounded feet',[[92,51],[161,52],[164,153],[158,170],[98,171],[92,154]])
poly('house','closed cupboard full envelope and grounded feet',[[611,47],[672,43],[673,141],[668,151],[614,152],[610,144]])
poly('house','west side wall full base',[[0,0],[88,0],[94,95],[70,313],[53,331],[0,327]])
poly('house','east side wall full base',[[681,0],[767,0],[767,334],[712,331],[691,316],[681,155]])
poly('house','southwest wall entire pier and garden projection',[[0,298],[49,288],[64,315],[120,311],[151,300],[215,318],[240,306],[283,318],[298,389],[282,433],[230,440],[120,421],[0,430]])
poly('house','southeast wall entire pier and garden projection',[[474,317],[521,306],[543,319],[618,304],[671,319],[710,288],[744,299],[767,421],[602,432],[533,437],[478,413]])
poly('house','west open door whole face and hinge foot',[[294,302],[309,297],[317,314],[318,383],[306,393],[296,390]])
poly('house','east open door whole face and hinge foot',[[461,297],[474,304],[476,390],[466,393],[455,380],[454,313]])
# Complete outer apron foliage frontiers, including the small near-camera cypress.
poly('orchard','west outside-wicket grass and tree frontier',[[0,859],[650,859],[653,905],[670,923],[711,951],[731,1023],[0,1023]])
poly('orchard','east outside-wicket grass and tree frontier',[[924,875],[1535,875],[1535,1023],[880,1023],[889,961],[925,929]])
poly('orchard','south approach cypress complete projected silhouette',[[689,914],[702,936],[713,974],[719,1023],[674,1023],[675,952]])
poly('house','south apron west garden frontier',[[0,464],[68,479],[146,467],[207,487],[284,498],[315,511],[0,511]])
poly('house','south apron middle garden frontier',[[350,511],[387,486],[419,478],[455,492],[456,511]])
poly('house','south apron east garden frontier',[[545,511],[598,489],[650,482],[699,472],[767,471],[767,511]])
def a(id,room,x,y,kind='route',radius=30,**extra):D['anchors'][id]={'room':room,'point':[x,y],'kind':kind,'radius':radius,**extra}
a('arrival','orchard',784,928,'arrival',26);a('houseDoor','orchard',784,192,'door',28,to='houseExit',action='Enter cam house');a('houseExit','house',384,432,'door',30,to='houseDoor',action='Return to orchard')
for id,x,y in [('northWest',272,224),('northMidWest',560,256),('northCenter',784,224),('northMidEast',976,256),('northEast',1232,224),('westOuter',112,448),('westSouthTurn',208,576),('westAisle',560,448),('eastAisle',976,448),('eastOuter',1424,448),('eastSouthTurn',1328,576),('southWest',432,640),('southCenter',784,640),('southEast',1104,640),('wicket',784,832),('viewingPlatform',784,736)]:a(id,'orchard',x,y)
for id,x,k in [('petalCrank',336,'petal'),('leafCrank',784,'leaf'),('fruitCrank',1200,'fruit')]:a(id,'orchard',x,608,k,32)
a('performance','orchard',784,688,'performance',28)
a('petalCam','house',240,176,'petal',32);a('leafCam','house',384,176,'leaf',32);a('fruitCam','house',528,176,'fruit',32);a('presetDesk','house',384,256,'preset',30)
for id,x,y in [('houseWestWidth',112,240),('houseEastWidth',624,240),('houseCenter',384,304),('houseThreshold',384,368),('houseApron',368,448)]:a(id,'house',x,y)
for name,x in [('West bent-branch bench',272),('East bent-branch bench',1264)]:
 D['seats'].append({'name':name,'room':'orchard','anchor':[x,687],'floorClick':[x,703],'cushionBounds':[241 if x==272 else 1225,695,311 if x==272 else 1296,711],'surfacePolygon':[[241 if x==272 else 1225,695],[311 if x==272 else 1296,695],[310 if x==272 else 1294,711],[242 if x==272 else 1226,711]],'contactOffset':[0,10],'facing':'south','contactDefinition':'Real pinned native32 central lower torso rows25..27 overlaps the traced bent-branch seat slab. Standing contact only; complete front apron and feet remain blocked.'})
# Semantic backs are actual original branch pixels, separated by raster color mask in build.
D['benchBackRegions']=[[240,690,312,695],[1224,690,1297,695]]
for a in D['anchors'].values():
 x,y=a['point'];a['point']=[x//32*32+16,y//32*32]
D['fixtureNegatives']={room:[{'name':p['name'],'point':p['polygon'][0]}for p in polygons]for room,polygons in D['physicalFootprints'].items()}
(R/'source/layout-definition.json').write_text(json.dumps(D,indent=2));print('Defined original orchard paths, whole projected islands, cam house, full apron solids and native contacts.')
