from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[1]
for name in ['build_proposal.py','register_depth_assets.py','register_niche_assets.py','build_map.py','validate_static.py','verify_spawn_and_steps.py']:
 subprocess.run([sys.executable,str(R/'tools'/name)],cwd=R,check=True)
subprocess.run(['node',str(R/'tools/native-runner/run.cjs')],cwd=R,check=True)
print('Native artwork, runtime and geometry/routes rebuilt. Camera audit is a separate optional dependency-bound command.')
