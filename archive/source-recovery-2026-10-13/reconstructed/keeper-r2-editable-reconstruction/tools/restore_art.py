#!/usr/bin/env python3
"""Restore exact retained artwork from an already-materialized authorized Library ZIP.
No network, URL construction, image generation or replacement imagery is used.
"""
import argparse,hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('archive',type=pathlib.Path,help='Already-materialized lighthouse-keepers-return-r2-runtime.zip');args=parser.parse_args()
 provenance=json.loads((ROOT/'source/art-provenance.json').read_text());data=args.archive.read_bytes()
 if len(data)!=provenance['archive_bytes'] or hashlib.sha256(data).hexdigest()!=provenance['archive_sha256']:raise ValueError('Archive does not match the retained original runtime')
 staged=[]
 with zipfile.ZipFile(args.archive) as z:
  for item in provenance['assets']:
   data=z.read(item['archive_member']);destination=(ROOT/item['source_path']).resolve()
   if not destination.is_relative_to((ROOT/'source/art').resolve()):raise ValueError('Invalid asset destination')
   if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:raise ValueError('Original image checksum mismatch: '+item['archive_member'])
   if destination.exists() and destination.read_bytes()!=data:raise ValueError('Refusing to replace modified artwork: '+str(destination))
   staged.append((destination,data))
 for destination,data in staged:destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
 print(json.dumps({'restored_original_textures':len(staged),'library_file_id':provenance['library_file_id']}))
