from pathlib import Path
import json,base64,hashlib,sys
R=Path(__file__).resolve().parents[1]/'runtime/results';name=sys.argv[1];m=json.loads((R/(name+'-recording-manifest.json')).read_text());out=R/(name+'.webm');total=0
with out.open('wb') as target:
 for i in range(m['chunks']):
  chunk=json.loads((R/(m['chunkPrefix']+'-chunk-'+str(i).zfill(5)+'.json')).read_text());assert chunk['index']==i;b=base64.b64decode(chunk['base64']);assert len(b)==chunk['bytes'];target.write(b);total+=len(b)
assert total==m['bytes'];m.update(output=out.name,sha256=hashlib.sha256(out.read_bytes()).hexdigest());(R/(name+'-recording-manifest.json')).write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m,indent=2))
