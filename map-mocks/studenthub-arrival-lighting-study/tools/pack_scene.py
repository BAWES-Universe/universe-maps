import bpy,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for im in bpy.data.images:
 if im.source=='FILE' and not im.packed_file:
  p=R/'art-source'/Path(im.filepath).name
  if p.exists():im.filepath=str(p)
bpy.ops.file.pack_all()
missing=[im.name for im in bpy.data.images if im.source=='FILE' and not im.packed_file]
assert not missing,missing
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=True)
print('PACKED VERIFIED',len([im for im in bpy.data.images if im.packed_file]))
