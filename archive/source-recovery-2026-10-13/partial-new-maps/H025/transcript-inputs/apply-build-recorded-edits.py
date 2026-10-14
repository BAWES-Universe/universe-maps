from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'transcript-inputs/build.H024-observed.py').read_text().replace("assert im.size==(1536,1024);base.paste(im,(ox,oy))","assert im.size==(1254,1254);im=im.crop((0,0,1248,1248));base.paste(im,(ox,oy))")
s=s.replace("gg=np.ones((32,48),np.uint8)","gg=np.ones((39,39),np.uint8)").replace('range(32):','range(39):').replace('range(48):','range(39):').replace('oy//32+32,ox//32:ox//32+48','oy//32+39,ox//32:ox//32+39').replace('bounds=[ox,oy,1536,1024]','bounds=[ox,oy,1248,1248]')
s=s.replace("interactive[a]['action']='Enter lookout';interactive[b]['action']='Return to causeway'","interactive[a]['action']='Enter '+interactive[b]['room'];interactive[b]['action']='Return to courtyard'")
s=s.replace('causeway-popup-','caravan-popup-').replace('causeway.js','caravan.js').replace('CausewayLayout','CaravanLayout')
s=s.replace("base.paste(im,(ox,oy));m=", "base.paste(im,(ox,oy));m=")
s=s.replace("g[oy//32:oy//32+39,ox//32:ox//32+39]=gg", "g[oy//32:oy//32+39,ox//32:ox//32+39]&=gg")
s=s.replace("above.paste(fg,(ox,oy));rooms.append", "above.alpha_composite(fg,(ox,oy));rooms.append")
s=s.replace("bounds=[ox,oy,1248,1248]", "bounds=d.get('bounds',[ox,oy,1248,1248])")
s=s.replace("for k,im in overlays.items():pack(k,im,False)","for k,im in overlays.items():pack(k,im,k in D.get('initialLayers',[]))")
s=s.replace("empty=Image.alpha_composite(dec['ground-and-architecture'],dec['foreground']);assert empty.tobytes()==base.tobytes();dec['ground-and-architecture'].save(R/'review/decoded-ground.png');dec['foreground'].save(R/'review/decoded-foreground.png')", "assert Image.alpha_composite(dec['ground-and-architecture'],dec['foreground']).tobytes()==base.tobytes();initial=dec['ground-and-architecture'].copy()\nfor name in D.get('initialLayers',[]):initial=Image.alpha_composite(initial,dec[name])\nempty=Image.alpha_composite(initial,dec['foreground']);initial.save(R/'review/decoded-ground.png');dec['foreground'].save(R/'review/decoded-foreground.png')")
s=s.replace("'foregroundPixels':int(f.sum())","'foregroundPixels':int(f.sum()),'allIntegerBodyClearOrigins':int(clear.sum())")
p=R/'tools/build.py';assert not p.exists();p.write_text(s)
