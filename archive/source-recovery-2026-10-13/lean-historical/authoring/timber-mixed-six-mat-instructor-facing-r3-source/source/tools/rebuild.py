"""One-command clean r3 source/art compilation and verification."""
from pathlib import Path
import shutil, subprocess, sys
R = Path(__file__).resolve().parents[1]
SLUG = 'timber-mixed-six-mat-instructor-facing-r3'
O = R / SLUG
steps = [
    ['reorient_source_mats.py'], ['repair_runtime_doorways.py'],
    ['build_native32.py'], ['check_geometry.py', str(O)],
    ['check_scenery.py'], ['check_spawn_outcomes.py'],
    ['check_room_floors.py'], ['check_r3_correction.py'],
]
for script, *args in steps:
    subprocess.run([sys.executable, str(R / 'tools' / script), *args], check=True, cwd=R)
shutil.copy2(R / 'geometry-checks' / SLUG / 'independent-checks.json', O / 'HEAD-GEOMETRY.json')
shutil.copy2(R / 'evidence/r2-accepted/NATIVE-ROUTES.json', O / 'NATIVE-ROUTES.json')
subprocess.run([sys.executable, str(R / 'tools/verify_expected.py')], check=True, cwd=R)
print('R3 clean rebuild and all expected-output checks passed.')
