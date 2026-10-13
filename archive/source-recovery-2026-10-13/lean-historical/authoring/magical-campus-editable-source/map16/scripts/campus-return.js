/* Native campus return action. gateRoomUrl stays blank until a real PLAY room is registered. */
(() => {
  'use strict';
  const subscriptions = [];
  const prop = (object, name) => object.properties?.find(p => p.name === name)?.value;
  const flatten = layers => layers.flatMap(l => l.type === 'group' ? flatten(l.layers) : [l]);
  const inside = (position, area) => position && area && position.x >= area.x && position.x <= area.x + area.width && position.y + 16 >= area.y && position.y + 16 <= area.y + area.height;
  let disposed = false, pad = null, destination = null, action = null, lastPosition = null;
  let revision = 0, actionEpoch = 0, attempt = 0, busy = false, armed = true;
  function clearAction() {
    ++actionEpoch;
    const old = action; action = null;
    if (old) Promise.resolve(old.remove()).catch(error => console.warn('Campus return action removal failed.', error));
  }
  function reconcile(position) {
    if (disposed) return;
    lastPosition = position;
    if (!inside(position, pad)) {
      ++attempt; busy = false; armed = true; clearAction(); return;
    }
    if (!destination || busy || !armed || action) return;
    const epoch = ++actionEpoch;
    action = WA.ui.displayActionMessage({
      message: 'Return to the giant gate',
      callback: () => { void activate(epoch); }
    });
  }
  async function activate(epoch) {
    if (disposed || !destination || busy || !armed || epoch !== actionEpoch || !inside(lastPosition, pad)) return;
    busy = true; armed = false;
    const sequence = ++attempt, at = revision;
    clearAction();
    try {
      const read = await WA.player.getPosition();
      if (disposed || sequence !== attempt) return;
      // A newer movement event is authoritative over a delayed getPosition result.
      const current = at === revision ? read : lastPosition;
      if (!inside(current, pad)) { busy = false; armed = true; reconcile(current); return; }
      // Configuration must be an actual registered absolute HTTPS PLAY room URL.
      await WA.nav.goToRoom(destination);
    } catch (error) {
      if (!disposed && sequence === attempt) console.warn('Return navigation did not complete. Leave the pad before retrying.', error);
    } finally {
      // Remaining on the pad never reopens or repeats the action, even when transport fails.
      if (!disposed && sequence === attempt) busy = false;
    }
  }
  async function refresh() {
    const at = ++revision;
    try {
      const position = await WA.player.getPosition();
      if (!disposed && at === revision) reconcile(position);
    } catch (error) { if (!disposed) console.warn('Campus return position refresh failed.', error); }
  }
  function dispose() {
    if (disposed) return;
    disposed = true; ++revision; ++attempt; busy = false;
    clearAction(); subscriptions.splice(0).forEach(s => s?.unsubscribe?.());
  }
  WA.onInit().then(async () => {
    const map = await WA.room.getTiledMap();
    if (disposed) return;
    pad = flatten(map.layers).flatMap(layer => layer.objects ?? []).find(object => object.name === 'gate-return-pad');
    if (!pad || ![pad.x,pad.y,pad.width,pad.height].every(Number.isFinite) || pad.width <= 0 || pad.height <= 0) return;
    const configured = prop(map, 'gateRoomUrl');
    if (typeof configured === 'string' && configured.trim()) {
      try {
        const url = new URL(configured.trim());
        if (url.protocol === 'https:' && !url.username && !url.password) destination = url.href;
      } catch { console.warn('gateRoomUrl must be a registered absolute HTTPS PLAY room URL.'); }
    }
    subscriptions.push(WA.player.onPlayerMove(position => { ++revision; reconcile(position); }));
    for (const edge of ['onEnter','onLeave']) subscriptions.push(WA.room.area[edge]('gate-return-pad').subscribe(refresh));
    await refresh();
  }).catch(error => console.error('Campus return initialization failed.', error));
  window.addEventListener('pagehide', dispose, {once:true});
})();
