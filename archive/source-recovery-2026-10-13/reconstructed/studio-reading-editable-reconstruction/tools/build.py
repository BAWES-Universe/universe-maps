#!/usr/bin/env python3
"""Reconstructed authoring compiler. Uses only source/, never a runtime fixture."""
import argparse,csv,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build(source,out):
    if out.exists():
        raise ValueError('Output must be absent; choose a new output directory.')
    for name in ('studio','reading'):
        src=source/name;dest=out/name;dest.mkdir(parents=True)
        m=json.loads((src/'map.recipe.json').read_text())
        for layer in m['layers']:
            if isinstance(layer.get('data'),dict):
                grid=list(csv.reader((src/layer['data']['csv']).open()))
                if len(grid)!=m['height'] or any(len(row)!=m['width'] for row in grid):
                    raise ValueError(f'{name}/{layer["name"]}: invalid grid dimensions')
                layer['data']=[int(value) for row in grid for value in row]
                if any(value<0 for value in layer['data']):raise ValueError('Negative GID')
        (dest/'map.tmj').write_text(json.dumps(m,indent=2)+'\n')
        wam=json.loads((src/'areas.wam.json').read_text())
        (dest/'map.wam').write_text(json.dumps(wam,indent=2)+'\n')
        for folder in ('art','extras'):
            for file in sorted((src/folder).glob('*')):
                if file.is_file():shutil.copyfile(file,dest/file.name)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=ROOT/'source');p.add_argument('--out',required=True,type=Path);a=p.parse_args();build(a.source,a.out)
