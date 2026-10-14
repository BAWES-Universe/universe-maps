#!/usr/bin/env python3
"""Add a versioned, native alpha-only animation overlay to an accepted static map."""
from pathlib import Path
from PIL import Image
import argparse, copy, hashlib, json, shutil, subprocess, zipfile
from ambient_sprites import build_atlas
HERE=Path(__file__).resolve().parent
j=lambda p:json.loads(p.read_text())
def jw(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def filesha(root): return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file()}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--static',type=Path,required=True);ap.add_argument('--acceptance',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    src=args.static.resolve();dst=args.output.resolve();slug=src.name;specall=j(HERE/'animation-spec.json');spec=specall['maps'][slug];accept=j(args.acceptance)
    assert dst.name==slug+'-motion-r01', 'Output must explicitly version the candidate'
    assert not dst.exists(), 'Never overwrite a candidate; preserve all checkpoints'
    assert dst!=src and src not in dst.parents, 'Candidate must be a sibling/separate directory'
    assert accept.get('geometryAccepted') is True and accept.get('slug')==slug, 'Explicit geometry acceptance required'
    mapfile=src/'map32'/f'{slug}.tmj';assert sha(mapfile)==accept['mapSHA256'],'Accepted static map changed; re-accept its geometry'
    for rel,h in accept.get('inputSHA256',{}).items(): assert sha(src/rel)==h,f'Accepted static input changed: {rel}'
    initial=filesha(src);m=j(mapfile);layout=j(src/'source/layout.json');g=layout['grid'];assert m['tilewidth']==m['tileheight']==32
    assert j(src/'validation/geometry.json')['allPass'];assert j(src/'validation/native-routes.json')['allPass']
    for p in spec['placements']:
        x,y=p['cell'];assert g[y][x]==1,f'Animation on walkable cell {x},{y}'
        cl=next(l for l in m['layers'] if l['name']=='collision-permanent');assert cl['data'][y*m['width']+x]>0
    dst.mkdir();shutil.copytree(src/'map32',dst/'map32');(dst/'source').mkdir();(dst/'review').mkdir();(dst/'validation').mkdir();(dst/'inputs').mkdir()
    shutil.copy2(mapfile,dst/'source/static-map.tmj');shutil.copy2(args.acceptance,dst/'source/static-geometry-acceptance.json')
    for fn in ['layout.json','greg-reference.png']:shutil.copy2(src/'source'/fn,dst/'source'/fn)
    shutil.copytree(src/'validation',dst/'validation/static-checkpoint')
    staticzip=src/f'{slug}-source-replay.zip';shutil.copy2(staticzip,dst/'inputs'/staticzip.name)
    jw(dst/'source/static-input-SHA256.json',initial);shutil.copy2(HERE/'animation-spec.json',dst/'source/animation-spec.json')
    shutil.copytree(HERE,dst/'motion-tools',ignore=shutil.ignore_patterns('__pycache__','_unreleased*','_rebuild*','*-build.log','*-preview.png','*-stats.json','*-study*.png','*-native-cells.png','acceptance-*.json'))
    atlas,stats=build_atlas(spec);atlasname='ambient-native-r01.png';atlas.save(dst/'map32'/atlasname)
    firstgid=max(ts['firstgid']+ts['tilecount'] for ts in m['tilesets']);layername=f'{slug}-ambient-native-r01';data=[0]*(m['width']*m['height']);tiles=[]
    for i,p in enumerate(spec['placements']):
        x,y=p['cell'];data[y*m['width']+x]=firstgid+i*8
        durations=spec['durationsMs'];phase=p['phase'];tiles.append(dict(id=i*8,animation=[dict(tileid=i*8+k,duration=durations[(k+phase)%8]) for k in range(8)]))
    ts=dict(firstgid=firstgid,name='ambient-native-r01',image=atlasname,imagewidth=atlas.width,imageheight=atlas.height,tilewidth=32,tileheight=32,columns=8,tilecount=len(spec['placements'])*8,margin=0,spacing=0,tiles=tiles)
    layer=dict(id=m['nextlayerid'],name=layername,type='tilelayer',width=m['width'],height=m['height'],x=0,y=0,visible=True,opacity=1,data=data)
    m['nextlayerid']+=1;m['layers'].insert(next(i for i,l in enumerate(m['layers']) if l['name']=='floorLayer'),layer);m['tilesets'].append(ts)
    jw(dst/'map32'/f'{slug}.tmj',m)
    jw(dst/'source/motion-layout.json',dict(slug=slug,revision='motion-r01',kind=spec['kind'],layerName=layername,firstgid=firstgid,placements=spec['placements'],frameStats=stats,originalSHA256=initial,staticSourceReplaySHA256=sha(staticzip)))
    subprocess.run(['node',str(dst/'motion-tools/validate_native_motion.cjs'),str(dst)],check=True)
    subprocess.run(['python',str(dst/'motion-tools/render_motion_review.py'),str(dst)],check=True)
    assert filesha(src)==initial,'Static source changed during candidate build'
    (dst/'README.md').write_text(f'''# {layout['title']} · native ambient motion r01\n\nExplicitly versioned local candidate based on the accepted static checkpoint. The static package is untouched and bundled as a byte-exact input ZIP. Select `{slug}.tmj` in `map32/`; its adjacent WAM is unchanged and not automatically imported by Custom TMJ.\n\n## Motion\n{len(spec['placements'])} alpha-only {'pond ripple/reflection' if spec['kind']=='water' else 'lantern-glass flicker'} placements; eight distinct frames per placement. The overlay is below floorLayer and only on permanent-collision cells. Original visual atlases, all original layers and map properties, WAM areas, collisions, anchors, quiet tile and camera behavior are unchanged. No scripts or extra engine configuration are required. This does not animate the whole water surface, waterfalls or foliage.\n\n## Validation\nThe accepted static replay contains{j(src/'validation/native-routes.json')['legs']} legs; its report is preserved under `validation/static-checkpoint/`. The separate motion-delta replay contains{j(dst/'validation/native-motion.json')['nativeMovement']['legs']} legs (desktop/touch spawn-anchor round trips and every walkable floor cell plus return). It does not rerun the static ordered-anchor-pair and edge-sample matrix. See `validation/native-motion.json` for actual pinned phaser-animated-tiles replay, native collision checks, property identity checks, no map-change emissions, and native movement legs while animation advances. The plugin runs in a fixture with a test-double Phaser scene. Review frames are decoded at native32 scale from the actual runtime TMJ/atlases using plugin-emitted frame indices; these are not screenshots from a deployed Phaser browser or live room. No live browser, keyboard physics, multi-user or service validation is claimed.\n\n## Review\n`review/occupied-native-frame-00.png`, `review/native-motion-contact-sheet.png`, `review/ambient-loop.gif`, and `review/placement-motion-contact-sheet.png`. The loop is a cropped detail preview driven by captured plugin states. Greg is a review-only fixture and is not in runtime.\n\n## Portable rebuild\nPython3 + Pillow and Node.js are required. No network, API, paid assets or npm install is needed. Extract the supplied source replay ZIP. Run `python motion-tools/rebuild.py --output-dir /path/to/empty-output`. This extracts the exact accepted static input and creates a fresh `{slug}-motion-r01` candidate under your output directory. Source and existing candidates are never overwritten.\n\n## Release status\nLocal review candidate only. Nothing was published, merged or installed. No audio, bots, portals, media services or commerce capabilities were activated. Preserve the static checkpoint as the fallback.\n''')
    runtimefiles={p.name:sha(p) for p in sorted((dst/'map32').iterdir()) if p.is_file()}
    manifest=dict(slug=slug,revision='motion-r01',engineCommit=specall['engineCommit'],staticSourceSHA256=sha(mapfile),staticSourceReplaySHA256=sha(staticzip),runtime=runtimefiles,validation=j(dst/'validation/native-motion.json'),render=j(dst/'validation/native-render.json'),status=dict(localCandidate=True,staticCheckpointPreserved=True,nativeAnimatedTiles=True,livePlaytest=False,published=False,geometryAccepted=True))
    jw(dst/'MANIFEST.json',manifest)
    with zipfile.ZipFile(dst/f'{slug}-motion-r01-runtime.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((dst/'map32').iterdir()):z.write(p,p.name)
    with zipfile.ZipFile(dst/f'{slug}-motion-r01-source-replay.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dst.rglob('*')):
            if p.is_file() and p.name!='FREEZE.json' and '__pycache__' not in p.parts and (p.suffix!='.zip' or p.parent==dst/'inputs'):z.write(p,str(p.relative_to(dst)))
    jw(dst/'FREEZE.json',dict(revision='motion-r01',staticCheckpointPreserved=True,immutableUntilExplicitRevision=True,manifestSHA256=sha(dst/'MANIFEST.json'),runtimeZipSHA256=sha(dst/f'{slug}-motion-r01-runtime.zip'),sourceZipSHA256=sha(dst/f'{slug}-motion-r01-source-replay.zip')))
    print(json.dumps(dict(candidate=str(dst),pass_=True,runtimeZip=str(dst/f'{slug}-motion-r01-runtime.zip')),indent=2))
if __name__=='__main__':main()
