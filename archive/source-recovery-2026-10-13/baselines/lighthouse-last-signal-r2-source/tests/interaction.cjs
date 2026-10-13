const { test } = require('node:test');
const assert = require('node:assert/strict');
const { createExperience, stations } = require('../runtime/signal.js');
function fixture(deferred = false) {
  let popup, notice, mover, resolvePosition; const menus = {}; const calls = [], layers = {};
  const WA = { onInit: async () => {}, room: {
    setProperty: (...args) => calls.push(args), showLayer: n => layers[n] = true, hideLayer: n => layers[n] = false
  }, ui: { openPopup: (target, message, buttons) => (popup = { target, message, buttons, close() { this.closed = true; } }),
    displayActionMessage: options => (notice = { ...options, remove() { this.removed = true; return Promise.resolve(); } }),
    registerMenuCommand: (name, fn) => { menus[name] = fn; return { remove() { calls.push(['remove-menu']); } }; }
  }, player: { onPlayerMove: fn => { mover = fn; return { unsubscribe() { calls.push(['unsubscribe']); } }; },
    getPosition: () => deferred ? new Promise(r => resolvePosition = r) : Promise.resolve(stations.dock) } };
  const app = createExperience(WA);
  return { app, calls, layers, get popup() { return popup; }, get notice() { return notice; }, move: id => mover(typeof id === 'string' ? stations[id] : id),
    click: label => { const b = popup.buttons.find(x => x.label === label); assert.ok(b, label + ' missing in ' + popup.message); b.callback(); },
    journal: () => menus['Inspect nearby ring'](), globalJournal: () => menus['Signal journal'](), command: name => menus[name](), resolve: p => resolvePosition(p) };
}
async function started(sound = false) { const f = fixture(); await f.app.init(); f.click(sound ? 'Begin + shore signal' : 'Begin quietly'); return f; }
test('quiet default, dock explanation, no audio playback on init', async () => { const f = fixture(); await f.app.init(); assert.match(f.popup.message, /No timer/); assert.equal(f.calls.length, 0); f.click('Begin quietly'); assert.equal(f.app.snapshot().sound, false); assert.ok(!f.calls.some(c => c[1] === 'playAudio' && c[2])); });
test('complete meaningful walk, wrong sequence recovery, beacon and automatic silence', async () => {
 const f = await started(true); for (const id of ['prism', 'tide', 'wind']) { f.move(id); f.click('Capture note'); assert.equal(f.layers['signal-' + id], true); }
 f.move('beacon'); f.click('High'); assert.deepEqual(f.app.snapshot().sequence, []); f.click('Try again');
 for(const note of ['Low','Middle','High'])f.click(note);
 assert.equal(f.app.snapshot().phase, 'complete'); assert.equal(f.layers['signal-beacon'], true); assert.equal(f.app.snapshot().sound,false);
 assert.match(f.popup.message,/SIGNAL RESTORED/);
});
test('cannot activate beacon early', async () => { const f = await started();f.move('beacon');assert.match(f.popup.message,/0\/3/);assert.ok(!f.popup.buttons.some(b=>b.label==='Low')); });
test('stale double capture and callbacks after walking away do nothing', async () => { const f = await started();f.move('tide');const button=f.popup.buttons[0];f.move('wind');button.callback();assert.equal(f.app.snapshot().found.length,0);f.click('Capture note');f.popup.buttons[0].callback();assert.deepEqual(f.app.snapshot().found,['wind']); });
test('reset cancels old completion and clears all lights and audio', async () => { const f=await started(true);f.move('tide');const old=f.popup.buttons[0];f.click('Capture note');f.journal();f.click('Restart');f.click('Restart quietly');old.callback();assert.equal(f.app.snapshot().phase,'idle');assert.deepEqual(f.app.snapshot().found,[]);assert.ok(Object.values(f.layers).every(v=>!v));assert.equal(f.app.snapshot().sound,false); });
test('audio selects descriptor before source, off removes using undefined', async () => { const f=await started(true);const d=f.calls.findIndex(c=>c[1]==='nativeSoundscape'&&c[2]);const p=f.calls.findIndex(c=>c[1]==='playAudio'&&c[2]);assert.ok(d>=0&&p>d);const descriptor=JSON.parse(f.calls[d][2]);assert.equal(descriptor.volume,.09);f.journal();f.click('Shore signal off');assert.ok(f.calls.some(c=>c[1]==='playAudio'&&c[2]===undefined)); });
test('dispose closes popup, removes subscription/menu, prevents stale actions', async()=>{const f=await started(true);f.move('tide');const button=f.popup.buttons[0];f.app.dispose();f.app.dispose();button.callback();assert.deepEqual(f.app.snapshot().found,[]);assert.equal(f.calls.filter(c=>c[0]==='unsubscribe').length,1);assert.equal(f.calls.filter(c=>c[0]==='remove-menu').length,4);});
test('two visitors have isolated progress',async()=>{const a=await started(),b=await started();a.move('tide');a.click('Capture note');assert.deepEqual(b.app.snapshot().found,[]);assert.equal(b.layers['signal-tide'],false);});
test('late initial position never replaces a newer movement event',async()=>{const f=fixture(true);const initializing=f.app.init();await Promise.resolve();f.move('wind');f.resolve(stations.dock);await initializing;assert.equal(f.app.snapshot().current,'wind');});
test('close then reenter works without forced movement or timer',async()=>{const f=await started();f.move('tide');f.click('Close');assert.equal(f.popup.closed,true);f.move({x:750,y:480});f.move('tide');assert.equal(f.popup.closed,undefined);});
test('journal reopens a closed station without requiring another step',async()=>{const f=await started();f.move('tide');f.click('Close');f.journal();f.click('Inspect this ring');f.click('Capture note');assert.deepEqual(f.app.snapshot().found,['tide']);});

test('away-from-station journal at (1050,320) uses only screen-space UI',async()=>{const f=await started();f.move({x:1050,y:320});const previous=f.popup;f.globalJournal();assert.equal(f.app.snapshot().current,null);assert.equal(f.popup,previous);assert.match(f.notice.message,/SIGNAL JOURNAL/);assert.match(f.notice.message,/Inspect nearby ring/);assert.match(f.notice.message,/Restart signal/);f.notice.callback();assert.equal(f.notice.removed,true);});
test('global sound-off is reachable away from all stations',async()=>{const f=await started(true);f.move({x:1050,y:320});f.command('Shore signal off');assert.equal(f.app.snapshot().sound,false);assert.match(f.notice.message,/off/);assert.ok(f.calls.some(c=>c[1]==='playAudio'&&c[2]===undefined));});
test('global restart confirms screen-space away from stations',async()=>{const f=await started(true);f.move('tide');f.click('Capture note');f.move({x:1050,y:320});f.command('Restart signal');assert.equal(f.app.snapshot().found.length,1);assert.match(f.notice.message,/Confirm signal restart/);f.command('Confirm signal restart');assert.equal(f.app.snapshot().phase,'idle');assert.deepEqual(f.app.snapshot().found,[]);assert.equal(f.app.snapshot().sound,false);});
test('movement cancels restart and its stale callback, even inside a station',async()=>{const f=await started();f.move('tide');f.click('Capture note');f.command('Restart signal');const old=f.notice;f.move({x:274,y:672});assert.equal(old.removed,true);old.callback();assert.deepEqual(f.app.snapshot().found,['tide']);});
test('opening global journal cancels a pending restart and dispose invalidates messages',async()=>{const f=await started();f.command('Restart signal');const old=f.notice;f.globalJournal();old.callback();assert.equal(f.app.snapshot().phase,'exploring');const journal=f.notice;f.app.dispose();journal.callback();assert.equal(journal.removed,true);assert.equal(f.calls.filter(c=>c[0]==='remove-menu').length,5);});

test('native Close button cancels restart instead of confirming destruction',async()=>{const f=await started();f.move('tide');f.click('Capture note');f.move({x:1050,y:320});f.command('Restart signal');f.notice.callback();f.command('Confirm signal restart');assert.equal(f.app.snapshot().phase,'exploring');assert.deepEqual(f.app.snapshot().found,['tide']);});
test('Inspect nearby ring outside stations uses screen-space directions, never dock popup',async()=>{const f=await started();f.move({x:1050,y:320});const old=f.popup;f.command('Inspect nearby ring');assert.equal(f.popup,old);assert.match(f.notice.message,/Walk to any brass ring/);});
