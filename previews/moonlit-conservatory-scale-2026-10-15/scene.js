/* Moonlit Glasshouse: private, per-player interactions. No shared writes or camera changes.
 * Authored map must have an open doorway on script failure (Door Collision hidden).
 * Artwork layers and geometry are intentionally independent from this controller.
 */
(function (root) {
    'use strict';
    function createExperience(WA, clock = root) {
        const geometry = {
            pavilion: { x: 70, y: 60, width: 515, height: 370 },
            pavilionInterior: [[110,180],[200,90],[430,100],[535,220],[390,370],[370,425],[290,425],[275,355],[110,295]],
            door: { x: 335, y: 410 }, counter: { x: 300, y: 220 },
            terrace: { x: 1200, y: 570 }
        };
        let disposed = false, position = null, moves = 0, roofInside = false, roofFrame = -1, roofEpoch = 0;
        let door = 'open', frame = 2, doorEpoch = 0, tea = 'idle', teaEpoch = 0;
        let prompt = null, promptKey = '', audioEnabled = false;
        const touch = (root.navigator?.maxTouchPoints || 0) > 0;
        const timers = new Set(), menus = [], subscriptions = [], visibility = new Map();
        const near = (point, radius) => position && Math.hypot(position.x - point.x, position.y - point.y) <= radius;
        function inPavilion(x, y) {
            const polygon = geometry.pavilionInterior;
            let inside = false, distance = Infinity;
            for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
                const [ax, ay] = polygon[j], [bx, by] = polygon[i];
                if ((ay > y) !== (by > y) && x < (bx - ax) * (y - ay) / (by - ay) + ax) inside = !inside;
                const dx = bx - ax, dy = by - ay;
                const t = Math.max(0, Math.min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)));
                distance = Math.min(distance, Math.hypot(x - ax - t * dx, y - ay - t * dy));
            }
            // Keep the previous state within eight pixels of the perimeter.
            return distance <= 8 ? roofInside : inside;
        }
        function later(callback, ms) {
            const id = clock.setTimeout(() => { timers.delete(id); if (!disposed) callback(); }, ms);
            timers.add(id); return id;
        }
        function layer(name, visible) {
            if (visibility.get(name) === visible) return;
            WA.room[visible ? 'showLayer' : 'hideLayer'](name); visibility.set(name, visible);
        }
        function removePrompt() {
            const old = prompt; prompt = null;
            if (old) Promise.resolve(old.close ? old.close() : old.remove()).catch(() => {});
        }
        function showPrompt(key, message, callback) {
            if (key === promptKey) return;
            promptKey = key; removePrompt();
            if (touch) {
                const labels = { brew: 'Brew tea', collect: 'Collect tea', serve: 'Serve tea', again: 'Brew another pot' };
                // Informational states never leave an overlay over phone navigation.
                if (!disposed && labels[key]) prompt = WA.ui.openPopup(
                    key === 'serve' ? 'terrace-tea-touch' : 'counter-tea-touch',
                    key === 'serve' ? 'Tea by the water' : 'Moonflower tea',
                    [{ label: labels[key], callback: () => {
                        if (!disposed && key === promptKey) callback();
                    } }, { label: 'Dismiss', callback: removePrompt }]
                );
                return;
            }
            if (message && !disposed) prompt = WA.ui.displayActionMessage({ message, callback: () => {
                if (!disposed && key === promptKey) callback();
            }});
        }
        function doorFrame(index) {
            // Open doorway is baked into the base artwork; frame 2 hides both overlays.
            ['Door Closed', 'Door Half'].forEach((name, i) => layer(name, i === index));
            frame = index;
        }
        function fadeRoof(inside) {
            const target = inside ? -1 : 3, token = ++roofEpoch;
            function step() {
                if (token !== roofEpoch || roofFrame === target) return;
                roofFrame += Math.sign(target - roofFrame);
                for (let i = 0; i < 4; i++) layer('Pavilion Roof ' + i, i === roofFrame);
                if (roofFrame !== target) later(step, 70);
            }
            if (roofFrame !== target) later(step, 70);
        }
        function animateDoor(open) {
            if (disposed || (open && (door === 'open' || door === 'opening')) || (!open && (door === 'closed' || door === 'closing'))) return;
            const token = ++doorEpoch;
            door = open ? 'opening' : 'closing';
            // Never introduce collision during the animation or around the player.
            layer('Door Collision', false);
            function tick() {
                if (token !== doorEpoch) return;
                if (!open && near(geometry.door, 112)) { animateDoor(true); return; }
                const target = open ? 2 : 0;
                if (frame !== target) doorFrame(frame + Math.sign(target - frame));
                if (frame === target) { door = open ? 'open' : 'closed'; layer('Door Collision', !open); }
                else later(tick, 140);
            }
            later(tick, 140);
        }
        function refreshTea() {
            layer('Tea Ready', tea === 'ready'); layer('Tea Served', tea === 'served');
            if (near(geometry.counter, 88)) {
                if (tea === 'idle') showPrompt('brew', 'SPACE · Brew a pot of moonflower tea', prepare);
                else if (tea === 'brewing') showPrompt('brewing', 'The moonflower leaves are steeping…', () => {});
                else if (tea === 'ready') showPrompt('collect', 'SPACE · Take your tea to the waterside table', collect);
                else if (tea === 'carrying') showPrompt('carrying', 'Your tea is ready to serve at the waterside terrace.', () => {});
                else showPrompt('again', 'SPACE · Prepare another pot', resetTea);
            } else if (near(geometry.terrace, 96)) {
                if (tea === 'carrying') showPrompt('serve', 'SPACE · Set down your tea and enjoy the water', serve);
                else if (tea === 'served') showPrompt('served', 'Moonflower tea, served beneath the stars.', () => {});
                else showPrompt('terrace', 'Bring a warm cup from the glass pavilion.', () => {});
            } else showPrompt('', '', () => {});
        }
        function prepare() {
            if (disposed || tea !== 'idle' || !near(geometry.counter, 88)) return false;
            tea = 'brewing'; const token = ++teaEpoch; refreshTea();
            later(() => { if (token === teaEpoch) { tea = 'ready'; refreshTea(); } }, 2600);
            return true;
        }
        function collect() {
            if (disposed || tea !== 'ready' || !near(geometry.counter, 88)) return false;
            tea = 'carrying'; refreshTea(); return true;
        }
        function serve() {
            if (disposed || tea !== 'carrying' || !near(geometry.terrace, 96)) return false;
            tea = 'served'; refreshTea(); return true;
        }
        function resetTea() { if (disposed) return; teaEpoch++; tea = 'idle'; refreshTea(); }
        function move(p) {
            if (disposed) return;
            moves++; position = { x: p.x, y: p.y };
            const inside = inPavilion(p.x, p.y + 16);
            if (inside !== roofInside || moves === 1) { roofInside = inside; fadeRoof(inside); }
            // Fixed glass is baked into the base artwork; only the roof is dynamic.
            // Keep the exit path available throughout the interior, including the counter.
            if (roofInside || near(geometry.door, 104)) animateDoor(true);
            else if (!near(geometry.door, 144)) animateDoor(false);
            refreshTea();
        }
        function audio(on) {
            if (disposed && on) return;
            audioEnabled = !!on;
            if (!on) {
                WA.room.setProperty('native-audio', 'playAudio', undefined);
                WA.room.setProperty('native-audio', 'nativeSoundscape', undefined);
                return;
            }
            WA.room.setProperty('native-audio', 'nativeSoundscape', JSON.stringify({
                url: 'audio/tide-signal.wav', volume: 0.05, x: 1200, y: 570, innerRadius: 48, outerRadius: 440
            }));
            WA.room.setProperty('native-audio', 'audioVolume', 0);
            WA.room.setProperty('native-audio', 'audioLoop', true);
            WA.room.setProperty('native-audio', 'playAudio', 'audio/silent-carrier.wav');
        }
        function menu(label, callback) {
            // This engine cleans up menus by label on iframe departure: key must match.
            menus.push(WA.ui.registerMenuCommand(label, { key: label, callback: () => { if (!disposed) callback(); } }));
        }
        async function init() {
            layer('Door Collision', false); doorFrame(2);
            for (let i = 0; i < 4; i++) layer('Pavilion Roof ' + i, false);
            layer('Tea Ready', false); layer('Tea Served', false);
            subscriptions.push(WA.player.onPlayerMove(move));
            menu('Enable quiet waterside ambience', () => audio(true));
            menu('Silence waterside ambience', () => audio(false));
            menu('Brew a fresh pot', resetTea);
            const before = moves, p = await WA.player.getPosition();
            if (!disposed && before === moves) move(p);
        }
        function dispose() {
            disposed = true; doorEpoch++; teaEpoch++; roofEpoch++;
            const attempt = fn => { try { Promise.resolve(fn()).catch(() => {}); } catch (_) {} };
            // Restore passage before any optional UI/audio cleanup can fail.
            attempt(() => WA.room.hideLayer('Door Collision'));
            for (const id of timers) clock.clearTimeout(id); timers.clear();
            attempt(removePrompt);
            subscriptions.forEach(s => attempt(() => s && s.unsubscribe()));
            menus.forEach(m => attempt(() => m.remove()));
            attempt(() => audio(false));
        }
        return { init, dispose, prepare, collect, serve, resetTea, audio, geometry,
            status: () => ({ door, frame, roofInside, roofFrame, tea, audioEnabled, position, disposed }) };
    }
    if (typeof module !== 'undefined' && module.exports) module.exports = { createExperience };
    else if (root.WA) {
        let app;
        root.WA.onInit().then(async () => { app = createExperience(root.WA); root.moonlitExperience = app; await app.init(); })
            .catch(error => { console.error('Moonlit pavilion initialization failed', error); app?.dispose(); });
        root.addEventListener('pagehide', () => app?.dispose());
    }
})(typeof globalThis !== 'undefined' ? globalThis : this);
