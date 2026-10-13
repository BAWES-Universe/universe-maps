"""Whole-map solid scenery inventory. Pixel boxes use final extended-canvas coordinates.
Beds include raised bases and dense shrub silhouettes; walls include projecting posts.
Every box is rounded outward to complete native32 solid cells before compiling.
"""
FIXTURES=[
 ('north perimeter west wall and beds',(192,128,704,224)),
 ('north perimeter east wall and beds',(832,128,1344,224)),
 ('north materials storage rack',(248,160,448,244)),
 ('northwest corner flowering bed',(80,160,184,256)),
 ('northeast corner flowering bed',(1352,160,1472,256)),
 ('workshop north wall windows pipes and all left pots',(224,256,704,384)),
 ('workshop north wall windows pipes and all right pots',(808,256,1064,384)),
 ('north door left jamb and plant',(676,256,720,384)),
 ('north door right jamb and plant',(808,256,848,384)),
 ('northeast dividing wall and projecting post',(1064,256,1104,412)),
 ('workshop west upper wall cabinetry and pots',(192,256,288,544)),
 ('west door upper flowering return',(192,528,240,560)),
 ('workshop west lower wall cabinetry and pots',(192,616,288,912)),
 ('southwest interior floor plant',(272,728,320,784)),
 ('board west cabinet and small potted plant',(1104,280,1152,400)),
 ('board face and upper wall fixtures',(1136,264,1312,384)),
 ('board right continuous planter and shelving',(1256,376,1312,584)),
 ('board doorway left wall return',(1088,480,1152,544)),
 ('board doorway right wall return',(1248,480,1312,544)),
 ('east interior lower storage strip',(1280,536,1344,784)),
 ('collaboration north wall and shelf',(1064,592,1312,672)),
 ('collaboration northwest floor pot',(1064,632,1120,704)),
 ('collaboration northeast pot',(1280,608,1312,688)),
 ('main hall south doorway east plant',(1016,736,1088,784)),
 ('south workshop wall west and raised bed',(192,776,424,864)),
 ('south workshop wall east and raised beds',(600,776,1344,864)),
 ('southwest courtyard lamp planter',(192,896,256,992)),
 ('southwest courtyard raised bed',(224,960,416,1056)),
 ('southeast courtyard lamp planter',(1248,896,1344,992)),
 ('southeast courtyard raised bed',(1152,992,1280,1056)),
 ('south perimeter west wall and flowering beds',(256,1040,704,1152)),
 ('south perimeter east wall and flowering beds',(832,1040,1280,1152)),
 ('east upper lamp base and foliage',(1420,240,1488,336)),
 ('east second lamp base and foliage',(1420,328,1504,416)),
 ('east middle lamp base and foliage',(1420,592,1504,704)),
 ('east lower lamp base and foliage',(1420,848,1504,944)),
 ('west upper lamp base and foliage',(64,224,112,320)),
 ('west middle lamp base and foliage',(48,512,104,608)),
 ('west lower lamp base and foliage',(48,848,112,944)),
]
def apply(m):
 import math
 rows=[]
 for name,(x0,y0,x1,y1) in FIXTURES:
  x,y=x0//32,y0//32;w,h=math.ceil(x1/32)-x,math.ceil(y1/32)-y;m.block(x,y,w,h);rows.append(dict(name=name,pixelRect=[x0,y0,x1-x0,y1-y0],protectedTileRect=[x,y,w,h]))
 return rows
