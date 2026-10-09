/* Lantern Courtyard proof. No remote services, analytics, or player-control lock. */
(() => {
  'use strict';
  const zone = { name: 'butterfly-gathering', x: 480, y: 288, width: 160, height: 160 };
  const subscriptions = [];
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  let active = false;
  let disposed = false;
  let cameraChanged = false;
  const inside = p => p.x >= zone.x && p.x < zone.x + zone.width && p.y >= zone.y && p.y < zone.y + zone.height;
  function enter() {
    if (active || disposed) return;
    active = true;
    WA.room.showLayer('gathering-glow');
    if (!media.matches) {
      WA.room.showLayer('gathering-butterflies');
      // One focus only: repeated locked camera changes overwrite Universe's saved zoom.
      WA.camera.set(384, 304, 640, 416, true, true, 900);
      cameraChanged = true;
    }
  }
  function leave() {
    if (!active) return;
    active = false;
    WA.room.hideLayer('gathering-glow');
    WA.room.hideLayer('gathering-butterflies');
    if (cameraChanged) WA.camera.followPlayer(!media.matches, media.matches ? 0 : 650);
    cameraChanged = false;
  }
  function dispose() {
    leave();
    disposed = true;
    subscriptions.splice(0).forEach(s => s.unsubscribe());
  }
  WA.onInit().then(async () => {
    if (disposed) return;
    WA.room.hideLayer('gathering-glow');
    WA.room.hideLayer('gathering-butterflies');
    subscriptions.push(WA.room.area.onEnter(zone.name).subscribe(enter));
    subscriptions.push(WA.room.area.onLeave(zone.name).subscribe(leave));
    // Covers reconnect or reload while already inside the zone.
    const position = await WA.player.getPosition();
    if (!disposed && inside(position)) enter();
  }).catch(error => console.error('Courtyard interaction could not initialize', error));
  window.addEventListener('pagehide', dispose, {once:true});
})();
