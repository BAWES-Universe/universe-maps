#!/usr/bin/env python3
"""Rebuild only in a new, empty destination; preserve input and candidate checkpoints."""
from pathlib import Path
import argparse,json,subprocess,zipfile,hashlib
p=Path(__file__).resolve().parent;root=p.parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();out=a.output_dir.resolve();assert not out.exists() or not any(out.iterdir()),'Choose an empty output directory';out.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'source/motion-layout.json').read_text());slug=meta['slug'];zipin=root/'inputs'/f'{slug}-source-replay.zip';assert hashlib.sha256(zipin.read_bytes()).hexdigest()==meta['staticSourceReplaySHA256']
static=out/'static-input';static.mkdir()
with zipfile.ZipFile(zipin) as z:
 for n in z.namelist():assert not Path(n).is_absolute() and '..' not in Path(n).parts,'Unsafe ZIP path'
 z.extractall(static)
# The original static source ZIP deliberately excludes its own ZIP/FREEZE; restore only the exact ZIP input needed by the additive builder.
import shutil
shutil.copy2(zipin,static/slug/zipin.name)
accept=json.loads((root/'source/static-geometry-acceptance.json').read_text());accept['inputSHA256']={k:v for k,v in accept.get('inputSHA256',{}).items() if (static/slug/k).is_file()}
acceptpath=out/'static-geometry-acceptance.json';acceptpath.write_text(json.dumps(accept,indent=2)+'\n')
subprocess.run(['python',str(p/'build_motion_variant.py'),'--static',str(static/slug),'--acceptance',str(acceptpath),'--output',str(out/(slug+'-motion-r01'))],check=True)
