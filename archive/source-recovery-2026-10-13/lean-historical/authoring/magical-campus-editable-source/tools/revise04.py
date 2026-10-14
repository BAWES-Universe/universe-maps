from pathlib import Path
import shutil,json,hashlib
R=Path(__file__).resolve().parents[1];O=R.parent/'universe-expanded-office';G=O/'geometry-work/revision-04-social-egress'
h=R/'history/revision03';h.mkdir(parents=True,exist_ok=True)
for f in ['sources/office','docs/campus-source-overview.png','map/compile-manifest.json','map/route-plan.json','map16/route-plan.json']:
 p=R/f;d=h/f
 if p.exists() and not d.exists():
  d.parent.mkdir(parents=True,exist_ok=True)
  if p.is_dir():shutil.copytree(p,d)
  else:shutil.copy2(p,d)
p=R/'tools/build_campus.py';s=p.read_text();s=s.replace("freeze=read(office/'docs/RUNTIME-LAYER-FREEZE-03.json')", "revision=office/'revisions/04-social-reception'; geometry=office/'geometry-work/revision-04-social-egress';freeze=read(revision/'RUNTIME-LAYER-FREEZE-04.json')")
s=s.replace("sha(office/f)==h","sha(revision/f)==h").replace("office/f'layers/office-v2-{layer}.png'","revision/f'layers/office-v4-{layer}.png'").replace("office/'geometry-work/revision-03/collision-grid.json'","geometry/'collision-grid.json'").replace("office/'geometry-work/revision-03'/f","geometry/f").replace("snapshot('office',office/'docs/RUNTIME-LAYER-FREEZE-03.json')","snapshot('office',revision/'RUNTIME-LAYER-FREEZE-04.json')").replace("'losslessGridPromotion':True","'losslessGridPromotion':True,'revision':'04-social-reception'")
s=s.replace("'personal-areas.offline-draft.wam']:","'personal-areas.offline-draft.wam','social-egress-route-manifest-full-canvas.json','reception-social-route-manifest.json','social-source-contract.json','social-distance-and-group-validation.json']:")
s=s.replace("physics['layers']=[dict(collision) if False else next(l for l in layers if l['name']=='collision-permanent')]","physics['layers']=[next(l for l in layers if l['name']=='collision-permanent')]")
p.write_text(s)
