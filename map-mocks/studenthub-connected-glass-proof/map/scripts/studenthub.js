/* StudentHub map-side runtime. Uses public WA APIs; no engine patches. */
(() => {
  'use strict';
  const subscriptions = [];
  let disposed = false, bounds, inside = null, revision = 0;
  const flatten = layers => layers.flatMap(layer => [layer, ...flatten(layer.layers || [])]);
  const containsFeet = position => position.x >= bounds.x && position.x < bounds.x + bounds.width &&
    position.y + 16 >= bounds.y && position.y + 16 < bounds.y + bounds.height;
  function apply(next) {
    if (disposed || next === inside) return;
    inside = next;
    // Permanent collisions, glazing, furniture and structure are never addressed.
    if (inside) WA.room.hideLayer('roof');
    else WA.room.showLayer('roof');
  }
  async function reconcile() {
    const currentRevision = ++revision;
    const position = await WA.player.getPosition();
    if (!disposed && currentRevision === revision) apply(containsFeet(position));
  }
  function dispose() {
    disposed = true;
    ++revision;
    subscriptions.splice(0).forEach(subscription => subscription?.unsubscribe?.());
  }
  const ready = WA.onInit().then(async () => {
    const map = await WA.room.getTiledMap();
    bounds = flatten(map.layers).flatMap(layer => layer.objects || []).find(object => object.name === 'team-inside');
    if (!bounds || !(bounds.width > 0 && bounds.height > 0)) throw Error('Missing rectangular team-inside area.');
    for (const [event, value] of [['onEnter', true], ['onLeave', false]]) {
      subscriptions.push(WA.room.area[event]('team-inside').subscribe(() => {
        ++revision;
        apply(value);
      }));
    }
    // Catch up when a user spawns inside or the script initializes after entry.
    await reconcile();
  });
  window.StudentHubRuntime = { ready, reconcile, dispose, state: () => ({ inside, disposed }) };
  window.addEventListener('pagehide', dispose, { once: true });
})();
