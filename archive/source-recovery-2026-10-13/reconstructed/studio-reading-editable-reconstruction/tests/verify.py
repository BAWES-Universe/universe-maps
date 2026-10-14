#!/usr/bin/env python3
"""Clean source-only rebuild, structural checks, and authored-grid mutation test."""
import csv,hashlib,importlib.util,json,shutil,struct,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build',ROOT/'tools/build.py');compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
def check(condition,message):
    if not condition:raise AssertionError(message)
def run():
    expected=json.loads((ROOT/'source/runtime-baseline.json').read_text());report={'classification':'fresh reconstruction verification','maps':{},'limitations':['No live GPU, native physical-body routes, avatar/head/depth, touch, or multiplayer acceptance.','Grid connectivity is diagnostic, not a native route certification.']}
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp);src=temp/'source';shutil.copytree(ROOT/'source',src);out=temp/'built';compiler.build(src,out)
        for name,files in expected.items():
            target=out/name;check(set(p.name for p in target.iterdir())==set(files),'file inventory differs')
            for f,info in files.items():check(hashlib.sha256((target/f).read_bytes()).hexdigest()==info['sha256'],f'{name}/{f} byte mismatch')
            m=json.loads((target/'map.tmj').read_text());w,h=m['width'],m['height'];gids={0};collision=set()
            for t in m['tilesets']:
                gids.update(range(t['firstgid'],t['firstgid']+t['tilecount']))
                png=(target/t['image']).read_bytes();check(png[:8]==b'\x89PNG\r\n\x1a\n','not png')
                check(struct.unpack('>II',png[16:24])==(t['imagewidth'],t['imageheight']),'image dimensions')
                for tile in t.get('tiles',[]):
                    if any(p['name']=='collides' and p['value'] is True for p in tile.get('properties',[])):collision.add(t['firstgid']+tile['id'])
            blocked=set();start=[]
            for layer in m['layers']:
                if 'data' in layer:
                    check(len(layer['data'])==w*h,'layer dimension')
                    check(all((gid&0x0fffffff)in gids for gid in layer['data']),'unresolved GID')
                    blocked.update(i for i,gid in enumerate(layer['data'])if gid in collision)
                for obj in layer.get('objects',[]):
                    if any(p['name']=='start' and p['value'] is True for p in obj.get('properties',[])):start.append(int(obj['y']//m['tileheight'])*w+int(obj['x']//m['tilewidth']))
            check(len(start)==1 and start[0]not in blocked,'start blocked or absent')
            visited={start[0]};queue=list(visited)
            for i in queue:
                x,y=i%w,i//w
                for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    j=yy*w+xx
                    if 0<=xx<w and 0<=yy<h and j not in blocked and j not in visited:visited.add(j);queue.append(j)
            wam=json.loads((target/'map.wam').read_text());check(wam['mapUrl']=='./map.tmj','wrong map target')
            report['maps'][name]={'byte_exact_files':len(files),'width':w,'height':h,'blocked_cells':len(blocked),'spawn_connected_cells':len(visited),'unblocked_cells':w*h-len(blocked),'wam_areas':len(wam['areas'])}
        grid=next((src/'studio/layers').glob('*.csv'));rows=list(csv.reader(grid.open()));before=rows[0][0];rows[0][0]='0' if before!='0' else '1'
        with grid.open('w',newline='')as f:csv.writer(f,lineterminator='\n').writerows(rows)
        compiler.build(src,temp/'edited');check((temp/'edited/studio/map.tmj').read_bytes()!=(out/'studio/map.tmj').read_bytes(),'grid edits not compiled')
        rows.pop()
        with grid.open('w',newline='')as f:csv.writer(f,lineterminator='\n').writerows(rows)
        try:compiler.build(src,temp/'invalid')
        except ValueError:pass
        else:raise AssertionError('invalid grid was accepted')
        report['source_only_rebuild']='PASS';report['editable_grid_test']='PASS';report['invalid_grid_rejection']='PASS'
    return report
if __name__=='__main__':print(json.dumps(run(),indent=2))
