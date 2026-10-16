/* Experimental map-only local reveal. No audio, popups, teleports or shared state. */
(async () => {
    await WA.onInit();
    const cover = 'tower-glass-cover';
    const inside = ({ x, y }) => x >= 352 && x < 1056 && y >= 576 && y < 960;
    const apply = value => value ? WA.room.hideLayer(cover) : WA.room.showLayer(cover);
    apply(inside(await WA.player.getPosition()));
    WA.room.onEnterLayer('tower-interior').subscribe(() => apply(true));
    WA.room.onLeaveLayer('tower-interior').subscribe(() => apply(false));
})().catch(error => console.error('Campus reveal initialization failed', error));
