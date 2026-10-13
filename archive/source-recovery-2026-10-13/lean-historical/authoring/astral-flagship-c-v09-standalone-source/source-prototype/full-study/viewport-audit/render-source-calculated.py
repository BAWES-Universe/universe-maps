"""Make labeled source-calculated crops from the exact approved study image.
No browser, engine, camera implementation, art resizing, or publication.
The output viewport uses only the source-calculated integer CSS canvas scale.
"""
from pathlib import Path
import argparse, hashlib, json, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--outside', type=Path, required=True, help='Empty full-world exterior composite at2816x2432')
p.add_argument('--inside', type=Path, help='Optional empty full-world revealed composite')
p.add_argument('--greg', type=Path, default=Path('/workspace/shared/grand-auditorium-07-clean/assets/greg-reference.png'))
p.add_argument('--shell-top', type=int, help='Optional confirmed world y of broader shell upper extent')
p.add_argument('--shell-mask', type=Path, help='Native full-world shell alpha mask for exact bounds')
a = p.parse_args()
shell_bbox=None
if a.shell_mask:
    mask=Image.open(a.shell_mask).convert('L')
    if mask.size != (2816,2432): raise ValueError('Shell mask dimensions differ')
    shell_bbox=mask.getbbox()
    a.shell_top=shell_bbox[1]
plans=json.loads((ROOT/'source-calculated-viewports.json').read_text())
outside=Image.open(a.outside).convert('RGBA')
if outside.size != (2816,2432):
    raise ValueError(f'Outside image must be native2816x2432, got{outside.size}')
inside=None
if a.inside:
    inside=Image.open(a.inside).convert('RGBA')
    if inside.size != outside.size: raise ValueError('Inside image dimensions differ')
greg=Image.open(a.greg).convert('RGBA').crop((32,96,64,128))
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,bold=False): return ImageFont.truetype(font_bold if bold else font_path,size)

selected=['recommended-outside','closer-outside','entry-reveal-boundary']
records=[]

def wrap(draw,text,chosen_font,width):
    result=[]
    for paragraph in text.split('\n'):
        line=''
        for word in paragraph.split():
            trial=f'{line} {word}'.strip()
            if line and draw.textlength(trial,font=chosen_font)>width:
                result.append(line);line=word
            else: line=trial
        result.append(line)
    return result

def render(plan,optional=False):
    name=plan['name']; vp=plan['cssViewport']; c=plan['camera']; s=plan['cssScale']; xy=plan['spawn']
    boundary=name=='entry-reveal-boundary'
    source=inside if boundary and inside is not None else outside
    # The Greg frame is placed at its native32x32 world size. Every requested
    # outside position lies south of entrance alpha2054. Final shell overlap,
    # if any, must be reviewed separately; no fake engine depth claim is made.
    world=source.copy()
    world.alpha_composite(greg,(xy['x']-16,xy['y']-16))
    bounds=(c['x'],c['y'],c['x']+c['width'],c['y']+c['height'])
    if any(int(v)!=v for v in bounds): raise ValueError('Fractional crop needs explicit policy')
    bounds=tuple(int(v) for v in bounds)
    view=world.crop(bounds).resize((vp['width'],vp['height']),Image.Resampling.NEAREST)
    basename=f"source-calculated-{name}-{plan['kind']}"
    plain=ROOT/(basename+'-viewport.png');view.save(plain)
    small=plan['kind']=='portrait'
    pad=14 if small else 24
    fs=14 if small else 20
    caption_font=font(fs); heading_font=font(14 if small else 22,True)
    heading='SOURCE-CALCULATED PREVIEW'
    subtitle={'recommended-outside':'OUTSIDE SPAWN: Y2176','closer-outside':'NORTHWARD APPROACH: Y2160','entry-reveal-boundary':'REVEALED AT BOUNDARY: Y2112'}.get(name,name.replace('-',' ').upper())
    state='Exterior shown.'
    if boundary:
        state='Revealed image at the proposed hide boundary.' if inside is not None else 'Pre-hide exterior reference at the boundary. The proposed facade hides here.'
    if optional: raise ValueError('No exterior framing state is authorized for this study')
    body=f"{vp['width']}x{vp['height']} CSS viewport; {s:g} CSS px/world px.\nPlayer({xy['x']},{xy['y']}); world x{bounds[0]}..{bounds[2]}, y{bounds[1]}..{bounds[3]}.\n{state} No browser or live-session evidence."
    if not optional and not (boundary and inside is not None):
        clip=max(0,bounds[1]-1778)
        body+=f' Entrance upper alpha clipped by {clip} world px.'
    if boundary and inside is not None:
        body+=' Original 256px opening and approach remain visible.'
    else:
        body+=' Full 256px approach and central 128px clear portal fit horizontally.'
        if small:
            body+=' Entrance module width is cropped by 125px on each side.'
        else:
            body+=' Entire entrance module width fits.'
    if a.shell_top is not None and not (boundary and inside is not None):
        body+=f' Broader shell begins at y{a.shell_top}; northern crop clips {max(0,bounds[1]-a.shell_top)} world px of its vertical extent.'
    temp=Image.new('RGB',(vp['width'],100));d=ImageDraw.Draw(temp)
    titles=wrap(d,subtitle,caption_font,vp['width']-2*pad)
    lines=wrap(d,body,caption_font,vp['width']-2*pad)
    line_height=fs+6
    top=pad*2+(heading_font.size+8)+len(titles)*line_height
    bottom=pad*2+len(lines)*line_height
    labeled=Image.new('RGBA',(vp['width'],top+vp['height']+bottom),'#101c28')
    labeled.alpha_composite(view,(0,top));d=ImageDraw.Draw(labeled)
    d.text((pad,pad),heading,font=heading_font,fill='#f4cf74')
    y=pad+heading_font.size+8
    for line in titles:d.text((pad,y),line,font=caption_font,fill='#eaf0f5');y+=line_height
    y=top+vp['height']+pad
    for line in lines:d.text((pad,y),line,font=caption_font,fill='#d9e4ed');y+=line_height
    labeled_path=ROOT/(basename+'-labeled.png');labeled.convert('RGB').save(labeled_path)
    return {'case':name,'kind':plan['kind'],'source':str(a.inside if boundary and inside is not None else a.outside),'viewport':plain.name,'labeled':labeled_path.name,'cssViewport':vp,'cssScale':s,'worldViewXYXY':bounds,'spawn':xy,'viewportRegionInLabeledXYXY':[0,top,vp['width'],top+vp['height']],'state':state,'browserScreenshot':False,'cameraBehaviorImplemented':False}

for plan in plans['cases']:
    if plan['dpr']==1 and plan['name'] in selected: records.append(render(plan))
sha=lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
manifest={'evidence':'Source-calculated preview. No browser or live engine.', 'world':[2816,2432], 'outside':{'path':str(a.outside),'sha256':sha(a.outside)},'inside':{'path':str(a.inside),'sha256':sha(a.inside)} if a.inside else None,'greg':{'path':str(a.greg),'sha256':sha(a.greg),'cropXYXY':[32,96,64,128],'nativeFrame':[32,32]},'shellMask':{'path':str(a.shell_mask),'sha256':sha(a.shell_mask),'alphaBboxHalfOpen':shell_bbox} if a.shell_mask else None,'plansSha256':sha(ROOT/'source-calculated-viewports.json'),'rendered':records}
(ROOT/'rendered-inputs-and-outputs.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'outside':str(a.outside),'rendered':len(records),'output':str(ROOT)},indent=2))
