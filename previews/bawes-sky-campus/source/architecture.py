"""Orthogonal architecture assembled from coordinated source detail, with real glazing.
Opaque glass/foliage pixels from the source sheet are never used as pane fill.
"""
def scaled_crop(box,scale=.5):
 im=candidate.crop(box);return im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
cap=scaled_crop((144,827,536,847))
plinth=scaled_crop((144,906,536,960))
pier=scaled_crop((48,800,128,966))
column=scaled_crop((1170,48,1260,432),.35555556)
# Slim straight metal detail, segmented from the horizontal source rail and rotated.
metal=scaled_crop((144,828,536,844)).transpose(Image.Transpose.ROTATE_90)
def repeat_strip(dest,im,x,y,w,h):
 for yy in range(y,y+h,im.height):
  for xx in range(x,x+w,im.width):dest.alpha_composite(im.crop((0,0,min(im.width,x+w-xx),min(im.height,y+h-yy))),(xx,yy))
def pane_image(w,h):
 im=Image.new('RGBA',(w,h));dr=ImageDraw.Draw(im)
 # Amber optical tint remains transmissive; subtle reflection streaks have independent alpha.
 for yy in range(h):
  a=56+round(22*yy/max(h-1,1));dr.line((0,yy,w-1,yy),fill=(241,169,38,a))
 for xx in range(18,w,96):dr.polygon([(xx,2),(xx+8,2),(xx+28,h-2),(xx+23,h-2)],fill=(255,238,188,65))
 return im
def detailed_horizontal(dest,x,y,w,h=64):
 # Source cap and plinth retain their illustrated highlights, stone grain and shadow.
 dest.alpha_composite(pane_image(w,h),(x,y))
 repeat_strip(dest,cap,x,y,w,cap.height)
 repeat_strip(dest,plinth,x,y+h-plinth.height,w,plinth.height)
 for px in range(x,x+w,112):repeat_strip(dest,metal,px,y+cap.height,min(metal.width,x+w-px),h-cap.height-plinth.height)
def stone_wall(x,y,w,h):
 rectwalk((OX+x,OY+y,w,h),0)
 if w>h:detailed_horizontal(walls,x,y,w,max(h,64))
 else:
  repeat_strip(walls,plinth.transpose(Image.Transpose.ROTATE_90),x,y,w,h)
def glass_run(x,y,w,h,block=True):
 if block:rectwalk((OX+x,OY+y,w,h),0)
 if w>h:detailed_horizontal(glazing,x,y-32 if block else y,w,48)
 else:
  glazing.alpha_composite(pane_image(w,h),(x,y))
  repeat_strip(glazing,metal,x,y,metal.width,h)
  repeat_strip(glazing,metal,x+w-metal.width,y,metal.width,h)
  for py in range(y,y+h,96):repeat_strip(glazing,cap,x,py,w,min(cap.height,y+h-py))
architecture_posts=[]
def architecture_post(x,y,tall=False):
 im=column if tall else pier
 # Soft ground shadow stays beneath furniture; the source object itself is foreground.
 shadow=Image.new('RGBA',(OW,OH));sd=ImageDraw.Draw(shadow);sd.ellipse((x+2,y+im.height-8,x+im.width+16,y+im.height+7),fill=(69,40,17,70));walls.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4)))
 architecture_posts.append((im,x,y))
 rectwalk((OX+(x//16)*16,OY+((y+im.height-16)//16)*16,32,16),0)
# Perimeter: full glass/plinth bays with individual column masses, no beige bands.
rectwalk((OX,OY,OW,96),0)
rectwalk((OX,OY,32,OH),0);rectwalk((OX+OW-32,OY,32,OH),0)
rectwalk((OX+2096,OY+96,32,32),0)
detailed_horizontal(walls,16,16,OW-32,80)
for x in (16,224,656,1216,1712,2096):architecture_post(x,0,True)
for x in (16,OW-32):
 rectwalk((OX+x,OY+48,16,OH-48),0);glass_run(x,96,16,OH-96)
for x,w in [(16,960),(1168,960)]:
 rectwalk((OX+x,OY+OH-16,w,16),0);detailed_horizontal(glazing,x,OH-64,w,64)
for x in (0,288,576,896,1168,1488,1776,OW-40):architecture_post(x,OH-83)
