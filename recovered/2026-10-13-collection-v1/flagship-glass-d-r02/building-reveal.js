/* Original map-only native32 building reveal. No camera, movement, collision,
 * audio, media or quiet writes. Areas use native (x,y+16) membership.
 * All shell children are hidden in the TMJ: failed startup leaves a safe cutaway.
 * The ordinary outside facade appears only after initial membership is known.
 */
const OWNERS = [
  {
    "id": "hall",
    "hide": [
      "v09-hall-shadow",
      "v09-hall-shell",
      "v09-foyer-roof"
    ],
    "entry": [
      "v09-hall-entry-core",
      "v09-hall-entry-east"
    ],
    "hold": [
      "v09-hall-hold-core",
      "v09-hall-hold-east"
    ]
  },
  {
    "id": "foyer",
    "hide": [
      "v09-foyer-shadow",
      "v09-foyer-wings",
      "v09-foyer-roof",
      "v09-foyer-front"
    ],
    "entry": [
      "v09-foyer-entry-core",
      "v09-foyer-entry-south",
      "v09-foyer-entry-east"
    ],
    "hold": [
      "v09-foyer-hold-core",
      "v09-foyer-hold-south",
      "v09-foyer-hold-east"
    ]
  }
];
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
