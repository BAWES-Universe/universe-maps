import { HdpiManager } from './HdpiManager.js';
import { createFixtureController } from './FixtureLifecycle.js';
const $ = id => document.getElementById(id);
const percentile = (values, p) => {
    const sorted = [...values].sort((a, b) => a - b);
    return sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * p))] ?? null;
};
function syncInputBounds(game) {
    game.scale.updateBounds();
    game.scale.displayScale.set(
        game.scale.baseSize.width / game.scale.canvasBounds.width,
        game.scale.baseSize.height / game.scale.canvasBounds.height
    );
}
const controller = createFixtureController({
    start: startFixture,
    async destroy(record) {
        record.removeErrorListeners();
        if (!record.game) return;
        const game = record.game;
        await new Promise(resolve => {
            game.events.once(Phaser.Core.Events.DESTROY, resolve);
            game.destroy(true);
        });
        // The await continuation runs after Phaser's synchronous runDestroy has finished.
    },
    onWaiting(record) {
        $('save').disabled = true;
        $('output').textContent = JSON.stringify({
            status: 'waiting-for-previous-game-destroy', previousMode: record.report?.mode,
            note: 'Recreation waits for Phaser DESTROY. Keep this tab visible. If a failed boot cannot finish destruction, reload this local page.'
        }, null, 2);
    },
    onError(error) {
        $('output').textContent = JSON.stringify({ status: 'lifecycle-failed', error: String(error), note: 'Reload this local page before continuing.' }, null, 2);
    }
});
window.renderQualityFixture = { get report() { return controller.active?.report; } };
function startFixture(record, isCurrent) {
    $('stage').replaceChildren();
    $('save').disabled = true;
    const samples = [], renderSamples = [];
    const mapName = $('map').value, mode = $('mode').value, renderer = $('renderer').value;
    const width = Math.max(100, Math.min(2560, Number($('width').value) || 1180));
    const height = Math.max(100, Math.min(1440, Number($('height').value) || 757));
    const dpr = window.devicePixelRatio || 1, zoomModifier = Number($('zoom').value), offset = Number($('offset').value) || 0;
    const hdpi = new HdpiManager(640 * 480, 196 * 196);
    hdpi.zoomModifier = zoomModifier;
    hdpi.maxZoomOut = 0;
    hdpi.zoomOutPastMapFit = 0.1;
    const sizes = hdpi.getOptimalGameSize({ width: width * dpr, height: height * dpr });
    const canvasBranch = sizes.game.width <= sizes.real.width && sizes.game.height <= sizes.real.height;
    const legacyCamera = canvasBranch ? 1 : hdpi.zoomModifier * hdpi.getOptimalZoomLevel(sizes.real.width * sizes.real.height);
    const legacyBitmap = canvasBranch ? sizes.game : sizes.real;
    const native = mode.startsWith('native'), linear = mode === 'filter' || mode === 'native-linear';
    const bitmap = native ? { width: Math.ceil(sizes.real.width), height: Math.ceil(sizes.real.height) }
        : { width: Math.floor(legacyBitmap.width), height: Math.floor(legacyBitmap.height) };
    const css = { width: Math.ceil(sizes.real.width / dpr), height: Math.ceil(sizes.real.height / dpr) };
    const cameraZoom = { x: legacyCamera * bitmap.width / legacyBitmap.width, y: legacyCamera * bitmap.height / legacyBitmap.height };
    const report = record.report = { status: 'initializing', scope: 'isolated Phaser fixture; not full WorkAdventure acceptance', phaser: Phaser.VERSION,
        mapName, mode, rendererRequested: renderer, devicePixelRatio: dpr, cssViewport: { width, height }, zoomModifier, offset,
        sizes, legacyCamera, bitmapRequested: bitmap, cssRequested: css, cameraZoom, linearRequested: linear };
    const show = () => { if (isCurrent()) $('output').textContent = JSON.stringify(report, null, 2); };
    const fail = (stage, error) => {
        if (!isCurrent()) return;
        report.status = 'failed'; report.failedStage = stage; report.error = String(error);
        $('save').disabled = false; show();
    };
    const guard = (stage, callback) => (...args) => {
        if (!isCurrent() || report.status === 'failed') return;
        try { return callback(...args); } catch (error) { fail(stage, error); }
    };
    const onWindowError = event => fail('asynchronous-runtime', event.error || event.message);
    const onRejection = event => fail('asynchronous-rejection', event.reason);
    window.addEventListener('error', onWindowError);
    window.addEventListener('unhandledrejection', onRejection);
    record.removeErrorListeners = () => {
        window.removeEventListener('error', onWindowError);
        window.removeEventListener('unhandledrejection', onRejection);
    };
    show();
    try {
        record.game = new Phaser.Game({
            type: renderer === 'canvas' ? Phaser.CANVAS : Phaser.WEBGL, parent: 'stage', width: bitmap.width, height: bitmap.height,
            backgroundColor: '#252830', banner: false, audio: { noAudio: true },
            render: { antialias: false, antialiasGL: false, pixelArt: false, roundPixels: false },
            scene: {
                preload() {
                    guard('preload', () => {
                        this.load.on('loaderror', guard('asset-load', file => fail('asset-load', `Could not load ${file.url}`)));
                        if (mapName !== 'pixel-control') {
                            this.load.tilemapTiledJSON('map', `assets/${mapName}/map.tmj`);
                            const names = mapName === 'studio' ? ['environment', 'foreground', 'logic'] : ['architecture-and-furniture', 'foreground', 'logic'];
                            for (const name of names) this.load.image(`${mapName}/${name}`, `assets/${mapName}/${name}.png`);
                        }
                        this.load.spritesheet('woka', 'assets/woka.png', { frameWidth: 32, frameHeight: 32 });
                    })();
                },
                create() {
                    guard('scene-create', () => {
                        const game = this.game;
                        const camera = this.cameras.main;
                        camera.setZoom(cameraZoom.x, cameraZoom.y);
                        let center = { x: 480 + offset, y: 432 + offset };
                        if (mapName === 'pixel-control') {
                            const texture = this.textures.createCanvas('control', 64, 32), ctx = texture.context;
                            ctx.fillStyle = '#316d58'; ctx.fillRect(0, 0, 32, 32); ctx.fillStyle = '#c2bc73'; ctx.fillRect(32, 0, 32, 32);
                            ctx.fillStyle = '#203c48';
                            for (let n = 0; n < 32; n += 4) { ctx.fillRect(n, n, 2, 2); ctx.fillRect(32 + n, 31 - n, 2, 2); }
                            texture.refresh(); texture.setFilter(Phaser.Textures.FilterMode.NEAREST);
                            const map = this.make.tilemap({ data: Array.from({ length: 27 }, (_, y) => Array.from({ length: 30 }, (_, x) => (x + y) % 2)), tileWidth: 32, tileHeight: 32 });
                            const tiles = map.addTilesetImage('control', 'control', 32, 32);
                            if (!tiles || !map.createLayer(0, tiles, 0, 0)) throw Error('Could not create pixel-art control layer');
                        } else {
                            const map = this.make.tilemap({ key: 'map' });
                            center = { x: map.widthInPixels / 2 + offset, y: map.heightInPixels / 2 + offset };
                            const sets = map.tilesets.map(t => {
                                const original = this.cache.tilemap.get('map').data.tilesets.find(s => s.name === t.name);
                                const image = original.image.replace(/\.png$/, ''), key = `${mapName}/${image}`;
                                this.textures.get(key).setFilter(linear && image !== 'logic' ? Phaser.Textures.FilterMode.LINEAR : Phaser.Textures.FilterMode.NEAREST);
                                const set = map.addTilesetImage(t.name, key, t.tileWidth, t.tileHeight, t.tileMargin, t.tileSpacing);
                                if (!set) throw Error(`Could not bind tileset ${t.name}`);
                                return set;
                            });
                            for (const data of map.layers) {
                                const layer = map.createLayer(data.name, sets, 0, 0);
                                if (!layer) throw Error(`Could not create layer ${data.name}`);
                                layer.setDepth(data.name === 'foreground' ? 20 : 0); layer.setVisible(data.visible); layer.setAlpha(data.alpha);
                            }
                        }
                        this.textures.get('woka').setFilter(Phaser.Textures.FilterMode.NEAREST);
                        const actor = this.add.sprite(center.x, center.y, 'woka', 1).setDepth(10);
                        this.anims.create({ key: 'walk', frames: this.anims.generateFrameNumbers('woka', { start: 0, end: 2 }), frameRate: 6, repeat: -1 });
                        actor.play('walk'); camera.centerOn(center.x, center.y);
                        const keys = this.input.keyboard.createCursorKeys(), marker = this.add.graphics().setDepth(30);
                        this.input.on('pointerdown', guard('pointer', pointer => {
                            const world = camera.getWorldPoint(pointer.x, pointer.y);
                            marker.clear().lineStyle(1, 0xff4b5c, 1).strokeCircle(world.x, world.y, 6);
                            report.lastPointer = { canvas: { x: pointer.x, y: pointer.y }, world: { x: world.x, y: world.y }, screen: { x: pointer.event.clientX, y: pointer.event.clientY } };
                        }));
                        this.events.on('update', guard('update', (_time, delta) => {
                            const amount = 100 * Math.min(delta, 100) / 1000;
                            actor.x += (Number(keys.right.isDown) - Number(keys.left.isDown)) * amount;
                            actor.y += (Number(keys.down.isDown) - Number(keys.up.isDown)) * amount;
                            if (samples.length < 600) samples.push(delta);
                            report.woka = { x: actor.x, y: actor.y, textureScaleMode: actor.frame.source.scaleMode };
                        }));
                        let start = 0;
                        game.events.on(Phaser.Core.Events.PRE_RENDER, guard('pre-render', () => { start = performance.now(); }));
                        game.events.on(Phaser.Core.Events.POST_RENDER, guard('post-render', () => { if (renderSamples.length < 600) renderSamples.push(performance.now() - start); }));
                        game.canvas.style.width = `${css.width}px`; game.canvas.style.height = `${css.height}px`;
                        syncInputBounds(game);
                        report.status = 'running'; report.renderer = game.renderer.type === Phaser.CANVAS ? 'Canvas' : 'WebGL';
                        report.filterEffectiveForTileLayers = mapName !== 'pixel-control' && linear && report.renderer === 'WebGL'; report.textureKeys = game.textures.getTextureKeys();
                        $('save').disabled = false;
                        this.time.addEvent({ delay: 500, loop: true, callback: guard('measurements', () => {
                            const rect = game.canvas.getBoundingClientRect();
                            report.measured = { bitmap: { width: game.canvas.width, height: game.canvas.height }, css: { width: rect.width, height: rect.height },
                                imageRendering: getComputedStyle(game.canvas).imageRendering,
                                camera: { zoomX: camera.zoomX, zoomY: camera.zoomY, worldView: { x: camera.worldView.x, y: camera.worldView.y, width: camera.worldView.width, height: camera.worldView.height } },
                                frames: samples.length, frameDeltaMs: { median: percentile(samples.slice(60), .5), p95: percentile(samples.slice(60), .95) },
                                renderSubmissionCpuMs: { median: percentile(renderSamples.slice(60), .5), p95: percentile(renderSamples.slice(60), .95) } };
                            show();
                        }) });
                    })();
                }
            }
        });
    } catch (error) { fail('game-constructor', error); }
}
window.addEventListener('scroll', () => {
    const record = controller.active;
    if (record && controller.isCurrent(record) && record.game?.scale?.canvas) syncInputBounds(record.game);
}, true);
$('apply').onclick = controller.request;
for (const id of ['map', 'mode', 'renderer', 'zoom']) $(id).onchange = controller.request;
$('save').onclick = () => {
    const report = controller.active?.report;
    if (!report) return;
    const anchor = document.createElement('a');
    anchor.href = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }));
    anchor.download = `render-quality-${report.mapName}-${report.mode}-${report.rendererRequested}.json`;
    anchor.click(); setTimeout(() => URL.revokeObjectURL(anchor.href), 1000);
};
controller.request();
