"""Rebuild the isolated registered revision10 sources without touching09."""
from pathlib import Path
import json, subprocess, sys, time

root = Path(__file__).resolve().parents[1]
commands = [
    [sys.executable, str(root/'tools/build10.py')],
    [sys.executable, str(root/'sources/exterior10/apply_exterior.py'), str(root/'layers')],
    [sys.executable, str(root/'tools/compile32.py')],
    [sys.executable, str(root/'tools/install_native_audio10.py')],
]
results = []
for command in commands:
    start = time.monotonic()
    process = subprocess.run(command, cwd=root, text=True, capture_output=True)
    results.append({'program':Path(command[1]).name, 'exitCode':process.returncode,
                    'seconds':round(time.monotonic()-start,3), 'stdout':process.stdout,
                    'stderr':process.stderr})
    (root/'docs/build10-receipt.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:results[-1][k] for k in ['program','exitCode','seconds']}),flush=True)
    if process.returncode:
        print(process.stderr, file=sys.stderr)
        raise SystemExit(process.returncode)
