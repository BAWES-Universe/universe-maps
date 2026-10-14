from pathlib import Path
import json,hashlib
from offline_audit_lib import load_map,head_audit
R=Path(__file__).resolve().parents[1]
m,g,a,fg,layers,files=load_map(R/'runtime/mechanical-orchard.tmj',json.loads((R/'evidence/layout.json').read_text())['feedbackLayers'],[])
v=head_audit(g,fg,R/'source/native-head-union.json');v['tmjSHA256']=hashlib.sha256((R/'runtime/mechanical-orchard.tmj').read_bytes()).hexdigest();v['allFeedbackLayersShown']=True;v['executionBy']='Author replay of bundled project QA algorithm; independent review is separate.'
(R/'evidence/author-head-audit.json').write_text(json.dumps(v,indent=2));print(json.dumps(v,indent=2));assert v['pass']
