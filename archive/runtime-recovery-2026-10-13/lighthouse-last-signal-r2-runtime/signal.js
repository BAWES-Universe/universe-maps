/* Lighthouse: The Last Signal. Map-only script; no engine modifications or external services. */
(function (root) {
  'use strict';
  const stations = {
    dock: { x: 784, y: 800 }, tide: { x: 272, y: 672 },
    wind: { x: 752, y: 256 }, prism: { x: 1296, y: 576 }, beacon: { x: 336, y: 288 }
  };
  const clues = {
    tide: ['Tide / low', 'At the sunset deck, the sea carries the FIRST note: LOW.'],
    wind: ['Wind / middle', 'Above the north terrace, the wind carries the SECOND note: MIDDLE.'],
    prism: ['Prism / high', 'Beside the east cottage, the glass carries the LAST note: HIGH.']
  };
  function createExperience(WA) {
    let phase = 'idle', found = new Set(), sequence = [], sound = false;
    let current = null, popup = null, generation = 0, disposed = false, moveSub, menus = [], moves = 0, notice = null, confirmationMenu = null;
    function close() {
      generation++;
      if (confirmationMenu) { confirmationMenu.remove(); confirmationMenu = null; }
      if (popup) { popup.close(); popup = null; }
      if (notice) {
        const old = notice; notice = null;
        Promise.resolve(old.remove()).catch(e => console.error('Could not remove signal message:', e));
      }
    }
    // The pinned API documents this as bottom-of-screen UI, independent of map/camera position.
    function screenMessage(message, action = () => {}) {
      if (disposed) return;
      close(); const token = generation;
      notice = WA.ui.displayActionMessage({ message, callback: () => {
        if (disposed || token !== generation) return;
        close(); action();
      } });
    }
    function globalJournal() {
      if (disposed) return;
      const status = phase === 'idle' ? 'Ready to begin' : phase === 'complete' ? 'Signal restored' : `${found.size}/3 notes found`;
      const notes = [...found].map(x => clues[x][0]).join(', ') || 'No notes yet';
      screenMessage(`SIGNAL JOURNAL / ${status}. ${notes}. Rings: west sunset deck, north terrace, east cottage, lighthouse. Use Inspect nearby ring for local controls; Shore signal off or Restart signal from anywhere. Close dismisses this message.`);
    }
    function requestRestart() {
      screenMessage('Restart this visit and clear its notes? Choose Confirm signal restart in the menu. Close, movement or opening the journal cancels.');
      const token = generation;
      if (disposed) return;
      confirmationMenu = WA.ui.registerMenuCommand('Confirm signal restart', () => {
        if (disposed || token !== generation) return;
        close(); reset();
      });
    }

    function audio(enabled) {
      sound = enabled;
      if (!enabled) {
        WA.room.setProperty('signal-audio', 'playAudio', undefined);
        WA.room.setProperty('signal-audio', 'nativeSoundscape', undefined);
        return;
      }
      // Descriptor precedes first source selection. Native controls retain mute/pause/master.
      WA.room.setProperty('signal-audio', 'nativeSoundscape', JSON.stringify({
        url: 'audio/tide-signal.wav', volume: 0.09, x: 272, y: 672, innerRadius: 16, outerRadius: 160
      }));
      WA.room.setProperty('signal-audio', 'audioVolume', 0);
      WA.room.setProperty('signal-audio', 'audioLoop', true);
      WA.room.setProperty('signal-audio', 'playAudio', 'audio/silent-carrier.wav');
    }
    function show(id, text, actions) {
      close(); const token = generation;
      popup = WA.ui.openPopup('signal-popup-' + id, text, actions.map(([label, fn]) => ({
        label, callback: () => { if (!disposed && token === generation) fn(); }
      })).concat([{ label: 'Close', callback: () => { if (token === generation) close(); } }]));
    }
    function markers() {
      for (const id of ['tide', 'wind', 'prism']) WA.room[found.has(id) ? 'showLayer' : 'hideLayer']('signal-' + id);
      WA.room[phase === 'complete' ? 'showLayer' : 'hideLayer']('signal-beacon');
    }
    function start(withSound) { phase = 'exploring'; found.clear(); sequence = []; markers(); audio(withSound); close(); }
    function reset() { phase = 'idle'; found.clear(); sequence = []; markers(); audio(false); close(); if (current) visit(current); }
    function capture(id) { if (phase !== 'exploring') return; found.add(id); markers(); visit(id); }
    function note(value) {
      if (phase !== 'exploring' || found.size !== 3 || current !== 'beacon') return;
      const expected = ['Low', 'Middle', 'High'];
      if (value !== expected[sequence.length]) {
        sequence = []; show('beacon', 'The signal scattered. Your three notes are safe. Try LOW, then MIDDLE, then HIGH.', [['Try again', () => visit('beacon')]]); return;
      }
      sequence.push(value);
      if (sequence.length === 3) { phase = 'complete'; markers(); audio(false); }
      visit('beacon');
    }
    function visit(id) {
      if (disposed) return;
      if (phase === 'idle') {
        show(id, 'THE LAST SIGNAL\nThe lighthouse has lost its signal. Find three brass rings: sunset deck, north terrace, east cottage. Then return to the lighthouse. Tap/right-click a ring to walk there; use its buttons. No timer. Sound is optional.', [
          ['Begin quietly', () => start(false)], ['Begin + shore signal', () => start(true)]
        ]); return;
      }
      if (id === 'dock') { journal(); return; }
      if (id === 'beacon') {
        if (phase === 'complete') { show(id, 'SIGNAL RESTORED\nThe lighthouse is lit for your visit. The island is quiet again. Explore freely, or replay from your Signal journal.', [['Journal', journal]]); return; }
        if (found.size < 3) { show(id, `The beacon needs three notes. You have ${found.size}/3. Look for the rings at the sunset deck, north terrace and east cottage.`, [['Journal', journal]]); return; }
        show(id, `TRANSMIT / ${sequence.length}/3\nPlay the notes in the order you discovered in the clues. ${sequence.length ? 'So far: ' + sequence.join(' → ') : 'First note?'}`, ['Low', 'Middle', 'High'].map(v => [v, () => note(v)])); return;
      }
      if (clues[id]) {
        const [title, clue] = clues[id];
        show(id, `${title.toUpperCase()}\n${clue}\n${found.has(id) ? 'Captured. The inlay now glows. ' : ''}${found.size}/3 notes collected.`,
          found.has(id) || phase === 'complete' ? [['Journal', journal]] : [['Capture note', () => capture(id)]]);
      }
    }
    function journal() {
      if (!current) { globalJournal(); return; }
      const id = current;
      const status = phase === 'idle' ? 'Ready to begin' : phase === 'complete' ? 'Signal restored' : `${found.size}/3 notes found`;
      const notes = [...found].map(x => clues[x][0]).join(', ') || 'None yet';
      show(id, `SIGNAL JOURNAL / ${status}\n${notes}\nRoute: sunset deck (west), north terrace, east cottage, lighthouse (northwest). Rings turn mint when captured. Progress belongs to this visit; reloading resets it.`, [
        ...(phase === 'idle' ? [['Begin quietly', () => start(false)]] : []),
        ...(current && current !== 'dock' && phase === 'exploring' ? [['Inspect this ring', () => visit(current)]] : []),
        ...(phase === 'exploring' ? [[sound ? 'Shore signal off' : 'Shore signal on', () => { audio(!sound); journal(); }]] : []),
        ['Restart', () => show(id, 'Restart this visit? Your captured notes and beacon will reset.', [['Restart quietly', reset]])]
      ]);
    }
    function position(p) {
      if (disposed) return;
      moves++;
      if (notice) close(); // Movement cancels screen-space confirmations, even within the same station.
      // WA reports sprite/map coordinates. Visible rings are centered at feet (+16px).
      const id = Object.keys(stations).find(k => Math.hypot(p.x - stations[k].x, p.y - stations[k].y) <= 38) || null;
      if (id === current) return;
      close(); current = id;
      if (id) visit(id);
    }
    async function init() {
      await WA.onInit(); if (disposed) return;
      markers();
      menus = [
        WA.ui.registerMenuCommand('Signal journal', globalJournal),
        WA.ui.registerMenuCommand('Inspect nearby ring', () => {
          if (disposed) return;
          if (current) journal(); else screenMessage('Walk to any brass ring to inspect it: dock, west sunset deck, north terrace, east cottage or lighthouse. Close dismisses this message.');
        }),
        WA.ui.registerMenuCommand('Shore signal off', () => {
          if (disposed) return;
          audio(false); screenMessage('Shore signal is off. Close dismisses this message.');
        }),
        WA.ui.registerMenuCommand('Restart signal', requestRestart)
      ];
      moveSub = WA.player.onPlayerMove(position);
      const before = moves;
      const p = await WA.player.getPosition(); if (!disposed && moves === before) position(p);
    }
    function dispose() { if (disposed) return; disposed = true; close(); audio(false); moveSub?.unsubscribe(); menus.forEach(menu => menu.remove()); menus = []; }
    return { init, dispose, position, snapshot: () => ({ phase, found: [...found], sequence: [...sequence], sound, current }) };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { createExperience, stations };
  if (root.WA) { const experience = createExperience(root.WA); root.addEventListener('pagehide', () => experience.dispose(), { once: true }); experience.init().catch(e => console.error('Signal quest could not initialize:', e)); }
})(typeof globalThis !== 'undefined' ? globalThis : this);
