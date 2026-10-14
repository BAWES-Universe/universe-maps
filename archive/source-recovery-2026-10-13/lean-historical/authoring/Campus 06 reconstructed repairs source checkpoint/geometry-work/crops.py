from render_source import *
full=Image.open(WORK/'source-map.png').convert('RGBA'); c=next(l for l in m['layers'] if l['name']=='collision-permanent')
for name,box in [('fountain',(1184,1648,1712,2064)),('market',(2544,2816,3344,3200))]:
 crop=full.crop(box);crop.resize((crop.width*2,crop.height*2)).save(WORK/(name+'-source-2x.png'))
 d=ImageDraw.Draw(crop,'RGBA')
 for y in range(box[1]//16,box[3]//16):
  for x in range(box[0]//16,box[2]//16):
   xx=x*16-box[0];yy=y*16-box[1]
   if c['data'][y*m['width']+x]:d.rectangle((xx,yy,xx+15,yy+15),fill=(255,0,0,95))
   d.rectangle((xx,yy,xx+15,yy+15),outline=(255,255,255,60))
   if (x+y)%2==0:d.text((xx,yy),str(x)+','+str(y),fill=(255,255,255,170),font_size=5)
 crop.resize((crop.width*2,crop.height*2)).save(WORK/(name+'-collision-2x.png'))
 for lname in ['base','fixed-foreground','campus-effects']:
  im=Image.open(WORK/(lname+'.png')).crop(box);bg=Image.new('RGBA',im.size,(100,100,100));bg.alpha_composite(im);bg.resize((im.width*2,im.height*2)).save(WORK/(name+'-'+lname+'-2x.png'))
