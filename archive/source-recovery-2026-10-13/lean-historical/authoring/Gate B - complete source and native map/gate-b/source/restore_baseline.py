#!/usr/bin/env python3
"""Reconstruct the exact preserved A source from this self-contained B backup."""
from pathlib import Path
import argparse,json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
def restore(out):
 out=Path(out).resolve(); assert not out.exists(),'Choose a fresh directory'
 manifest=json.loads((ROOT/'originals/baseline-sha256.json').read_text())
 for rel,expected in manifest.items():
  src=ROOT/'gate'/rel
  if rel=='map/gate.tmj':src=ROOT/'originals/gate.tmj'
  if rel=='map/native-audio/gate-with-native-audio.js':src=ROOT/'originals/gate-with-native-audio.js'
  assert hashlib.sha256(src.read_bytes()).hexdigest()==expected,rel
  dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 return len(manifest)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('output');a=p.parse_args();print('Restored',restore(a.output),'exact baseline files')
