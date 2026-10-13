#!/usr/bin/env python3
"""Two fresh destination builds; compare bytes, input pins, and shipped output."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
import PIL
import numpy

ROOT = Path(__file__).resolve().parents[1]
tmp = Path(tempfile.mkdtemp(prefix='nonvisual-map-rebuild-'))
receipts = []
for name in ['first', 'second']:
    result = subprocess.run([sys.executable, str(ROOT / 'tools/recover_nonvisual.py'), str(tmp / name)],
                            check=True, capture_output=True, text=True)
    receipts.append(json.loads(result.stdout))
assert receipts[0] == receipts[1]
assert receipts[0] == json.loads((ROOT / 'generated/DERIVATION.json').read_text())
for item in json.loads((ROOT / 'retained-inputs.json').read_text())['files']:
    assert hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() == item['sha256']
report = {'scope': 'New art-independent source-only regeneration in two fresh output directories; no map artwork or TMJ built.',
          'pass': True, 'buildCount': 2, 'comparedOutputs': len(receipts[0]['files']),
          'bothBuildsAndShippedOutputsIdentical': True, 'retainedInputsUnchanged': True,
          'versions': {'python': platform.python_version(), 'Pillow': PIL.__version__, 'numpy': numpy.__version__},
          'toolSHA256': hashlib.sha256((ROOT / 'tools/recover_nonvisual.py').read_bytes()).hexdigest(),
          'files': receipts[0]['files']}
(ROOT / 'REPRODUCIBILITY.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
