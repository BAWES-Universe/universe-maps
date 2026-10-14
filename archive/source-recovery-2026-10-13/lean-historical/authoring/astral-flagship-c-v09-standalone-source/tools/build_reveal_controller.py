"""Generate simple supported map-only area-event reveal controller and matching areas."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
owners=[
 {'id':'hall','entry':{'core':[128,256,1664,1344],'east':[1536,432,1832,880]},'hold':{'core':[96,224,1696,1376],'east':[1504,400,1864,912]},'hide':['v09-hall-shadow','v09-hall-shell','v09-foyer-roof']},
 {'id':'foyer','entry':{'core':[128,1280,1664,2032],'south':[512,1696,1280,2112],'east':[1536,1328,1832,1776]},'hold':{'core':[96,1248,1696,2064],'south':[480,1664,1312,2144],'east':[1504,1296,1864,1808]},'hide':['v09-foyer-shadow','v09-foyer-wings','v09-foyer-roof','v09-foyer-front']}
]
areas=[];cfg=[]
for owner in owners:
 c={'id':owner['id'],'hide':owner['hide'],'entry':[],'hold':[]}
 for mode in ['entry','hold']:
  for label,box in owner[mode].items():
   name=f"v09-{owner['id']}-{mode}-{label}";x0,y0,x1,y1=box
   # Engine area membership uses player.x/player.y+16, inclusive edges.
   areas.append({'name':name,'x':x0,'y':y0+16,'width':x1-x0,'height':y1-y0,'playerCenterXYXY':box})
   c[mode].append(name)
 cfg.append(c)
contract={'scope':'Native map-only area events; permanent collision/media/quiet. No camera calls.', 'coordinateRule':'Authored player-center rectangles convert area y+16; inclusive endpoints.', 'defaultChildrenVisible':False,'startup':'Fail open: all decorative shell children hidden until area and position initialization succeeds. Exterior may briefly show floor while scripts initialize.', 'owners':owners,'runtimeOwners':cfg,'areas':areas,'nativeFocusXYWH':[128,256,1536,1008],'hysteresisPx':32,'cameraOwner':'Native TMJ focusable area only; ordinary exterior camera.','dependency':'Hall owner hides foyer roof because its north projection overlaps lower hall. Foyer front can remain restored while hall is open.'}
(R/'source/reveal-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
js='''/* Original map-only native32 building reveal. No camera, movement, collision,
 * audio, media or quiet writes. Areas use native (x,y+16) membership.
 * All shell children are hidden in the TMJ: failed startup leaves a safe cutaway.
 * The ordinary outside facade appears only after initial membership is known.
 */
const OWNERS = '''+json.dumps(cfg,indent=2)+''';
const GROUPS = [...new Set(OWNERS.flatMap(owner => owner.hide))];
const subscriptions = [];
function containsNativePlayer(area, position) {
  const footY = position.y + 16;
  return position.x >= area.x && position.x <= area.x + area.width &&
    footY >= area.y && footY <= area.y + area.height;
}
async function main() {
  await WA.onInit();
  const names = [...new Set(OWNERS.flatMap(owner => [...owner.entry, ...owner.hold]))];
  const records = new Map(await Promise.all(names.map(async name => [name, {
    bounds: await WA.room.area.get(name), inside: false, revision: 0,
  }])));
  const owners = OWNERS.map(owner => ({...owner, open: false}));
  const visible = new Map(GROUPS.map(group => [group, false]));
  let initialized = false;
  let queued = false;
  function render() {
    queued = false;
    if (!initialized) return;
    for (const owner of owners) {
      if (owner.entry.some(name => records.get(name).inside)) owner.open = true;
      else if (!owner.hold.some(name => records.get(name).inside)) owner.open = false;
    }
    for (const group of GROUPS) {
      const wanted = !owners.some(owner => owner.open && owner.hide.includes(group));
      if (visible.get(group) === wanted) continue;
      if (wanted) WA.room.showLayer(group);
      else WA.room.hideLayer(group);
      visible.set(group, wanted);
    }
  }
  function schedule() {
    if (queued) return;
    queued = true;
    queueMicrotask(render);
  }
  for (const [name, record] of records) {
    const update = inside => {record.revision++; record.inside = inside; schedule();};
    subscriptions.push(WA.room.area.onEnter(name).subscribe(() => update(true)));
    subscriptions.push(WA.room.area.onLeave(name).subscribe(() => update(false)));
  }
  // Native enters precede leaves. Each iframe message can flush separately;
  // union/hold ownership, not cross-message batching, provides continuity.
  // A newer area event wins over a stale initial asynchronous position snapshot.
  const revisions = new Map([...records].map(([name, record]) => [name, record.revision]));
  const position = await WA.player.getPosition();
  for (const [name, record] of records) {
    if (record.revision === revisions.get(name)) record.inside = containsNativePlayer(record.bounds, position);
  }
  initialized = true;
  render();
  window.addEventListener('pagehide', () => subscriptions.forEach(subscription => subscription.unsubscribe()), {once: true});
}
main().catch(error => {
  subscriptions.forEach(subscription => subscription.unsubscribe());
  console.error('Flagship C reveal initialization failed; cutaway remains available', error);
});
'''
(R/'map32/building-reveal.js').write_text(js)
print('Generated',len(areas),'visual-only areas and',len(set(sum([o['hide']for o in owners],[]))),'decorative groups')
