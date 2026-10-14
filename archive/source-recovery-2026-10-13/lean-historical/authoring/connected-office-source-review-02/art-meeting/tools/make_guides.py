#!/usr/bin/env python3
"""Reproduce technical silhouette diagrams; no furniture texture is drawn here."""
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
wood='#97602a';teal='#135362';seat='#267483';brass='#b69149'
def guide(name,size,rects):
 im=Image.new('RGBA',size);d=ImageDraw.Draw(im)
 for box,col,r in rects:
  if r:d.rounded_rectangle(box,r,fill=col)
  else:d.rectangle(box,fill=col)
 im.resize((size[0]*16,size[1]*16),Image.Resampling.NEAREST).save(R/'guides'/f'{name}-geometry.png')
guide('chair-north',(48,64),[((10,32,14,43),wood,1),((33,32,37,43),wood,1),((9,10,38,39),wood,2),((11,8,36,24),seat,4),((10,17,37,38),teal,4),((12,18,35,19),brass,1)])
guide('chair-south',(48,64),[((10,30,14,43),wood,1),((33,30,37,43),wood,1),((9,8,38,31),wood,3),((11,9,36,24),teal,4),((12,23,35,38),seat,3),((9,27,12,38),teal,1),((35,27,38,38),teal,1)])
guide('chair-east',(48,64),[((11,32,15,43),wood,1),((32,32,36,43),wood,1),((9,8,19,36),wood,3),((10,9,18,31),teal,3),((17,23,36,36),seat,3),((14,34,38,38),teal,2),((18,22,37,25),wood,1)])
guide('chair-west',(48,64),[((11,32,15,43),wood,1),((32,32,36,43),wood,1),((28,8,38,36),wood,3),((29,9,37,31),teal,3),((11,23,30,36),seat,3),((9,34,33,38),teal,2),((10,22,29,25),wood,1)])
guide('table-small',(128,96),[((17,68,22,79),wood,1),((105,68,110,79),wood,1),((16,16,111,75),wood,2),((16,16,111,63),'#cb9147',2)])
guide('table-conference',(224,128),[((17,100,22,111),wood,1),((201,100,206,111),wood,1),((16,16,207,107),wood,2),((16,16,207,95),'#cb9147',2)])
