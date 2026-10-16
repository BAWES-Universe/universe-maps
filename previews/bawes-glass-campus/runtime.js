/* Local shell reveal: permanent floor, furniture and collision remain. */
(async () => {
    await WA.onInit();
    const cover = 'tower-glass-cover';
    const inside = ({x,y}) => x >= 352 && x < 1056 && y >= 288 && y < 832;
    const apply = value => value ? WA.room.hideLayer(cover) : WA.room.showLayer(cover);
    apply(inside(await WA.player.getPosition()));
    WA.room.onEnterLayer('tower-interior').subscribe(() => apply(true));
    WA.room.onLeaveLayer('tower-interior').subscribe(() => apply(false));
})().catch(error => console.error('Campus reveal initialization failed', error));
