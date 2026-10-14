import render_runtime_proofs as p
from PIL import Image,ImageDraw
chairs=[a for a in p.layout['anchors'] if a['id'].startswith(('editor-','screen-viewer-','keyboard-','listen-'))];out=Image.new('RGB',(5*192,2*192),'#202020');d=ImageDraw.Draw(out)
for i,a in enumerate(chairs):
 x,y=a['x'],a['y'];im=p.scene([a]).crop((x-32,y-32,x+32,y+32)).resize((192,192),Image.Resampling.NEAREST);pos=(i%5*192,i//5*192);out.paste(im,pos);d.text((pos[0]+2,pos[1]+2),a['id']+' '+a['direction'],fill='white')
out.save(p.P/'review/actual-seat-facings.png')
