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
        let newPavilionInside = false, seating = false;
        // Native occupancy: feet align with chair cushion; final approach faces the table.
        const seats = [
            {id:'upper-west-left',x:216,y:250,side:-1}, {id:'upper-west-right',x:268,y:250,side:1},
            {id:'upper-east-left',x:408,y:250,side:-1}, {id:'upper-east-right',x:456,y:250,side:1},
            {id:'terrace-left',x:1168,y:536,side:-1}, {id:'terrace-right',x:1240,y:536,side:1},
            {id:'lower-west-left',x:1104,y:1464,side:-1}, {id:'lower-west-right',x:1168,y:1464,side:1},
            {id:'lower-east-left',x:1360,y:1464,side:-1}, {id:'lower-east-right',x:1424,y:1464,side:1}
        ];
        async function takeSeat() {
            if (disposed || seating || !position) return false;
            const distance = s => Math.hypot(position.x-s.x, position.y+16-s.y);
            const seat = seats.reduce((a,b) => distance(a)<distance(b) ? a : b);
            if (distance(seat)>96) return false;
            seating = true;
            try {
                const approach = await WA.player.moveTo(seat.x + seat.side*32, seat.y, 3);
                if (disposed || approach.cancelled) return false;
                const result = await WA.player.moveTo(seat.x, seat.y, 3);
                return !result.cancelled;
            } catch (error) { console.warn('Moonlit seat approach interrupted', error); return false; }
            finally { seating = false; }
        }
        const timers = new Set(), menus = [], subscriptions = [], visibility = new Map();
        const near = (point, radius) => position && (Math.hypot(position.x-point.x,position.y-point.y)<=radius || (point===geometry.counter && Math.hypot(position.x-1264,position.y-1392)<=radius) || (point===geometry.terrace && Math.hypot(position.x-1400,position.y-1520)<=radius));
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
            const anchor = position && position.y > 1000
                ? (key === 'guide' ? 'garden-guide' : key === 'serve' ? 'new-terrace-actions' : 'new-counter-actions')
                : (key === 'serve' ? 'terrace-tea-touch' : 'counter-tea-touch');
            const identity = key + ':' + anchor;
            if (identity === promptKey) return;
            promptKey = identity; removePrompt();
            const labels = { brew: 'Brew tea', collect: 'Collect tea', serve: 'Serve tea', again: 'Brew another pot', guide: 'Walk to fountain' };
            if (!labels[key]) return;
            const buttons = [];
            if (labels[key]) buttons.push({ label: labels[key], callback: () => {
                if (!disposed && identity === promptKey) callback();
            }});
            buttons.push({label: 'Dismiss', callback: removePrompt});

            prompt = WA.ui.openPopup(anchor,
                key === 'serve' ? 'Water garden' : 'Moonflower tea', buttons);
        }
        function doorFrame(index) {
            // Open doorway is baked into the base artwork; frame 2 hides both overlays.
            ['Door Closed', 'Door Half'].forEach((name, i) => layer(name, i === index));
            frame = index;
        }
        function fadeRoof(inside) {
            // One renderer transition rather than four timer-driven opacity jumps.
            roofEpoch++; roofFrame = inside ? -1 : 3;
            layer('Original pavilion exterior', !inside);
            for (let i = 0; i < 4; i++) layer('Pavilion Roof ' + i, !inside && i === 3);
        }
        function animateDoor(open) {
            if (disposed || (open && (door === 'open' || door === 'opening')) || (!open && door === 'closed')) return;
            doorEpoch++;
            // Collision opens immediately. Existing half-open art provides a brief visual transition only.
            layer('Door Collision', false);
            if (open) {
                const token = doorEpoch; door = 'opening'; doorFrame(1);
                later(() => { if (token === doorEpoch) { doorFrame(2); door = 'open'; } }, 90);
            } else { doorFrame(0); door = 'closed'; } // Visual door only; never make pathfinding reject the doorway.
        }
        function refreshTea() {
            layer('Tea Ready', tea === 'ready'); layer('Tea Served', tea === 'served');
            layer('Tea Ready Steam', tea === 'ready'); layer('Tea Served Steam', tea === 'served');
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
            } else if (near({x:576,y:1264},90)) showPrompt('guide','', () => { removePrompt(); WA.player.moveTo(992,1472,4); });
            else showPrompt('', '', () => {});
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
            const margin = newPavilionInside ? -8 : 8;
            const pInside = p.x > 1056+margin && p.x < 1504-margin && p.y+16 > 1280+margin && p.y+16 < 1632-margin;
            if (pInside !== newPavilionInside || moves === 1) {
                newPavilionInside = pInside;
                layer('New pavilion glass exterior', !pInside);
                layer('Expanded pavilion exterior', !pInside);
                layer('Expanded pavilion junction exterior', !pInside);
                layer('Expanded pavilion furniture cutouts', true);
                layer('New pavilion translucent roof', !pInside);
            }
            // Registered exterior architecture is removed completely with the roof inside.
            // Keep the exit path available throughout the interior, including the counter.
            if (roofInside || near(geometry.door, 220)) animateDoor(true);
            else if (!near(geometry.door, 280)) animateDoor(false);
            refreshTea();
        }
        function audio(on) {
            if (disposed && on) return;
            audioEnabled = !!on;
            // User opt-in only. The standard player owns mute, pause and volume.
            // No walking event changes playback or opens audio UI.
            WA.room.setProperty('native-audio', 'nativeSoundscape', undefined);
            if (!on) {
                WA.room.setProperty('native-audio', 'playAudio', undefined);
                return;
            }
            WA.room.setProperty('native-audio', 'audioVolume', 0.22);
            WA.room.setProperty('native-audio', 'audioLoop', true);
            WA.room.setProperty('native-audio', 'playAudio', 'audio/fountain.mp3');
        }
        function menu(label, callback) {
            // This engine cleans up menus by label on iframe departure: key must match.
            menus.push(WA.ui.registerMenuCommand(label, { key: label, callback: () => { if (!disposed) callback(); } }));
        }
        async function init() {
            layer('Door Collision', false); doorFrame(2);
            for (let i = 0; i < 4; i++) layer('Pavilion Roof ' + i, false);
            layer('Tea Ready', false); layer('Tea Served', false);
            layer('Tea Ready Steam', false); layer('Tea Served Steam', false);
            subscriptions.push(WA.player.onPlayerMove(move));
            menu('Enable water sound', () => audio(true));
            menu('Mute water', () => audio(false));
            menu('Brew a fresh pot', resetTea);
            menu('Take nearest seat', takeSeat);
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
        return { init, dispose, prepare, collect, serve, resetTea, audio, takeSeat, seats, geometry,
            status: () => ({ door, frame, roofInside, roofFrame, newPavilionInside, tea, audioEnabled, position, disposed }) };
    }
    if (typeof module !== 'undefined' && module.exports) module.exports = { createExperience };
    else if (root.WA) {
        let app;
        root.WA.onInit().then(async () => { app = createExperience(root.WA); root.moonlitExperience = app; await app.init(); })
            .catch(error => { console.error('Moonlit pavilion initialization failed', error); app?.dispose(); });
        root.addEventListener('pagehide', () => app?.dispose());
    }
})(typeof globalThis !== 'undefined' ? globalThis : this);
