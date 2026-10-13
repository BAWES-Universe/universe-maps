"""Rebuild the separate Gym-inspired charcoal Yoga mat variant.
Only existing source-authored mat sprites change. No generation or network.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,shutil,hashlib,random,numpy as np,sys,math,copy
R=Path(__file__).resolve().parents[1]
SLUG='timber-yoga-dark-mats-r3';OUT=R/SLUG;IN=R/'inputs/previous';T=32
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def mat_sprite(instructor=False,floor=None):
    w,h=(62,46) if instructor else (44,74)
    im=Image.new('RGBA',(w+8,h+8));shadow=Image.new('RGBA',im.size)
    d=ImageDraw.Draw(shadow);d.rounded_rectangle((3,4,w+2,h+3),radius=5,fill=(30,22,16,47))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(1.0)))
    # Low-profile rubber silhouette with a 1px lower edge and softened corners.
    edge=Image.new('RGBA',im.size);d=ImageDraw.Draw(edge)
    d.rounded_rectangle((1,1,w,h),radius=4,fill=(49,44,39,238))
    im.alpha_composite(edge.filter(ImageFilter.GaussianBlur(.28)))
    face=Image.new('RGBA',im.size);d=ImageDraw.Draw(face)
    face_mask=Image.new('L',im.size);md=ImageDraw.Draw(face_mask)
    md.rounded_rectangle((1,1,w-1,h-2),radius=4,fill=255)
    rng=random.Random(871 if instructor else 441)
    lightmap=np.array(floor.convert('RGB').filter(ImageFilter.GaussianBlur(5))) if floor else None
    for yy in range(1,h-1):
        for xx in range(1,w):
            # A faint warm top-left highlight follows the scene's window light.
            directional=5*(1-(xx/w+yy/h)/2)
            ambient=0 if lightmap is None else (float(lightmap[yy,xx].dot([.2126,.7152,.0722]))-155)/11
            grain=rng.choice((-2,-1,0,0,0,1,2))
            n=round(directional+ambient+grain)
            d.point((xx,yy),fill=(74+n,68+n,60+n,255))
    # Short, thin highlights blend into the rubber rather than outlining it.
    d.line((6,1,w-7,1),fill=(98,91,80,175))
    d.line((1,6,1,h-9),fill=(86,79,70,150))
    face.putalpha(face_mask.filter(ImageFilter.GaussianBlur(.35)))
    im.alpha_composite(face)
    return im

def decode(root,m):
    size=(m['width']*T,m['height']*T);ims={s['image']:Image.open(root/'map32'/s['image']).convert('RGBA') for s in m['tilesets']};below=Image.new('RGBA',size);above=Image.new('RGBA',size);dest=below;layers={}
    for l in m['layers']:
        if l['name']=='floorLayer':dest=above
        if l['type']!='tilelayer':continue
        canvas=Image.new('RGBA',size)
        for i,gid in enumerate(l['data']):
            if not gid:continue
            ts=max((s for s in m['tilesets'] if s['firstgid']<=gid),key=lambda s:s['firstgid']);j=gid-ts['firstgid'];assert j<ts['tilecount'];sx=j%ts['columns']*T;sy=j//ts['columns']*T
            canvas.alpha_composite(ims[ts['image']].crop((sx,sy,sx+T,sy+T)),(i%m['width']*T,i//m['width']*T))
        layers[l['name']]=canvas
        if l.get('visible',True) and l.get('opacity',1)>0:dest.alpha_composite(canvas)
    return below,above,layers

def build():
    for d in ['map32','source','assets','review']:(OUT/d).mkdir(parents=True,exist_ok=True)
    for p in (IN/'map32').iterdir():shutil.copy2(p,OUT/'map32'/p.name)
    shutil.copy2(IN/'source/layout.json',OUT/'source/layout.json')
    m=load(IN/'map32/map.tmj');before_below,above,layers=decode(IN,m);base=layers['architecture-and-furniture'].copy();oldbase=base.copy();oldempty=Image.alpha_composite(before_below,above);beforeocc=Image.open(IN/'review/occupied-native.png').convert('RGBA')
    regions=load(R/'mat-regions.json');mask=np.zeros((m['height']*T,m['width']*T),bool)
    for i,(x,y,w,h) in enumerate(regions):
        floor=Image.open(R/f'source-assets/floor-restoration/{i:02}.png').convert('RGBA');assert floor.size==(w,h)
        base.paste(floor,(x,y));sprite=mat_sprite(i==12,floor);assert sprite.size==(w,h);base.alpha_composite(sprite,(x,y));mask[y:y+h,x:x+w]=True
    for name,instructor in [('student-charcoal-mat',False),('instructor-charcoal-mat',True)]:mat_sprite(instructor).save(OUT/'assets'/(name+'.png'))
    # Leave all previous atlases untouched; override only the native32 art
    # cells touched by mats. Separate slots permit scene-specific warm lighting.
    oldmap=copy.deepcopy(m);gid=max(ts['firstgid']+ts['tilecount'] for ts in m['tilesets']);tiles=[];lookup={};changed_cells=[]
    l=next(l for l in m['layers'] if l['name']=='architecture-and-furniture')
    for i,oldgid in enumerate(l['data']):
        if not oldgid:continue
        x=i%m['width']*T;y=i//m['width']*T;tile=base.crop((x,y,x+T,y+T));raw=tile.tobytes()
        if raw==oldbase.crop((x,y,x+T,y+T)).tobytes():continue
        if raw not in lookup:lookup[raw]=len(tiles);tiles.append(tile)
        l['data'][i]=gid+lookup[raw];changed_cells.append([x//T,y//T])
    cols=min(16,len(tiles));atlas=Image.new('RGBA',(cols*T,math.ceil(len(tiles)/cols)*T))
    for j,tile in enumerate(tiles):atlas.paste(tile,(j%cols*T,j//cols*T))
    atlas_name='charcoal-mat-overrides.png';atlas.save(OUT/'map32'/atlas_name)
    m['tilesets'].append(dict(firstgid=gid,name='charcoal-mat-overrides',image=atlas_name,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=T,tileheight=T,margin=0,spacing=0,columns=cols,tilecount=len(tiles)))
    save(OUT/'map32/map.tmj',m)
    restored=copy.deepcopy(m);restored['tilesets']=restored['tilesets'][:-1]
    next(x for x in restored['layers'] if x['name']=='architecture-and-furniture')['data']=next(x for x in oldmap['layers'] if x['name']=='architecture-and-furniture')['data']
    assert restored==oldmap,'Non-art TMJ fields changed'
    for p in (IN/'map32').glob('*.png'):assert sha(p)==sha(OUT/'map32'/p.name),'Previous atlas changed'
    base.save(OUT/'assets/base.png');above.save(OUT/'assets/above.png')
    below,compiled_above,decoded=decode(OUT,m);empty=Image.alpha_composite(below,compiled_above)
    assert decoded['architecture-and-furniture'].tobytes()==base.tobytes();assert compiled_above.tobytes()==above.tobytes()
    oldarray,newarray,occarray=np.array(oldempty),np.array(empty),np.array(beforeocc);unchanged_actor_background=np.all(oldarray==occarray,axis=2);occarray[unchanged_actor_background]=newarray[unchanged_actor_background]
    empty.save(OUT/'review/empty-native.png');Image.fromarray(occarray).save(OUT/'review/occupied-native.png');Image.fromarray(occarray).save(OUT/'review/overview.png')
    changed=np.any(oldarray!=newarray,axis=2);assert not np.any(changed&~mask)
    layout=load(IN/'source/layout.json');assert len([a for a in layout['anchors'] if 'practice mat' in a['name']])==12;assert len([a for a in layout['anchors'] if a['name']=='instructor position'])==1
    assert sha(IN/'map32/map.wam')==sha(OUT/'map32/map.wam');assert sha(IN/'source/layout.json')==sha(OUT/'source/layout.json')
    checks={'variant':SLUG,'previousVariant':'timber-yoga-context-r2','nativeTileSize':32,'dimensions':[48,38],'practiceMats':12,'instructorMats':1,'matRegions':regions,'roomAndOutdoorsPixelExactOutsideMats':True,'centralMedallionPixelExact':True,'runtimeNonArtTmjFieldsExact':True,'previousAtlasesByteExact':True,'runtimeWamByteExact':True,'layoutByteExact':True,'foregroundPixelExact':True,'actorProofPixelsPreserved':True,'atlasRoundTripExact':True,'changedPixels':int(changed.sum()),'newArtAtlas':atlas_name,'changedTileCells':changed_cells,'newGenerationCalls':0,'equipmentOrDeskAdditions':0,'preservationInputHashes':load(R/'PROVENANCE.json')['inputHashes'],'liveBrowserDevicesMedia':'Not run; compiled static evidence and native movement fixture only.'}
    save(OUT/'SOURCE-PRESERVATION.json',checks)
    guide='''# Timber Yoga - charcoal mats r3\n\nA separate unpublished native32 revision of timber-yoga-context-r2. Replaces the 12 student mats and front instructor mat with source-authored Gym-inspired warm charcoal material, a thin edge and a restrained shadow. No new generation. The approved room, outdoor context, medallion, mats\' positions and dimensions, collision, anchors, spawn and WAM areas stay identical. No desks or Gym equipment are added. Previous versions are unchanged.\n\n## Runtime\nHost the complete map32 directory together. Map is 48 x 38 native32 tiles (1536 x 1216 pixels). Mats are walk-to visual destinations; standing reference actors in the occupied proof do not implement yoga poses. The existing bounded instructor/listener and lower conversation areas are retained unchanged. Live browser/device, multi-user media and deployment testing remain pending.\n\n## Rebuild\nRun python tools/build_dark_mats.py from the source bundle root, then node tools/verify_native_routes.cjs timber-yoga-dark-mats-r3 and python tools/check_head_geometry.py timber-yoga-dark-mats-r3. Requires Python 3, Pillow, NumPy and Node.js. No network, credentials, paid service, image generation or engine change. Input contains the previous compiled map, source layout, composited occupied proof and exact floor restoration patches; no raw avatar sprite sheet.\n\nSOURCE-PRESERVATION.json verifies every pixel outside the 13 mat rectangles plus exact non-art TMJ fields, byte-exact previous atlases, WAM and layout preservation. Runtime atlas reconstruction is pixel-exact. Native route/geometry checks are source checks, not a live room test.\n'''
    (OUT/'GUIDE.md').write_text(guide)
    print(json.dumps({k:v for k,v in checks.items() if k not in ['preservationInputHashes','changedTileCells','matRegions']},indent=2))
if __name__=='__main__':build()
