"""Build the isolated native32 Campus11 repair from preserved Campus10 sources."""
from pathlib import Path
import json, subprocess, sys, time
R=Path(__file__).resolve().parents[1]
commands=[
 [sys.executable,str(R/'tools/build10.py')],
 [sys.executable,str(R/'sources/exterior10/apply_exterior.py'),str(R/'layers')],
 [sys.executable,str(R/'sources/fire11/apply_fire_access.py'),str(R)],
 [sys.executable,str(R/'sources/arrival11/apply_arrival.py'),str(R)],
 [sys.executable,str(R/'tools/compile32.py')],
 [sys.executable,str(R/'tools/install_native_audio10.py')],
]
results=[]
for command in commands:
 start=time.monotonic();p=subprocess.run(command,cwd=R,text=True,capture_output=True)
 results.append({'program':Path(command[1]).name,'exitCode':p.returncode,'seconds':round(time.monotonic()-start,3),'stdout':p.stdout,'stderr':p.stderr})
 (R/'docs/build11-receipt.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({k:results[-1][k] for k in ['program','exitCode','seconds']}),flush=True)
 if p.returncode:
  print(p.stderr,file=sys.stderr);raise SystemExit(p.returncode)
