'use strict';
// Deterministic intentionally failing regression for an inherited controller race.
// Usage: node rejected-teleport-newer-movement.test.cjs [path/to/keeper.js]
// This uses mocked APIs. It does not move a real player or establish a live-game defect.
const assert = require('node:assert/strict');
const path = require('node:path');
const runtimePath = process.argv[2] || path.resolve(__dirname, '../../build/runtime/keeper.js');
const { createExperience, layout } = require(runtimePath);
const flush = () => new Promise(resolve => setImmediate(resolve));
let popup, onMove, resolveRecovery, getPositionCalls = 0;
const messages = [];
const WA = {
  onInit: async () => {},
  room: { showLayer() {}, hideLayer() {} },
  ui: {
    openPopup(id, text, buttons) { popup = { id, text, buttons, close() {} }; return popup; },
    displayActionMessage(args) { messages.push(args.message); return { remove() {} }; },
    registerMenuCommand() { return { remove() {} }; }
  },
  player: {
    teleport: async () => { throw new Error('Simulated rejected teleport'); },
    getPosition: async () => {
      getPositionCalls += 1;
      if (getPositionCalls === 1) return layout.anchors.houseDoor;
      return new Promise(resolve => { resolveRecovery = resolve; });
    },
    onPlayerMove(fn) { onMove = fn; return { unsubscribe() {} }; }
  }
};
(async () => {
  const app = createExperience(WA, layout);
  await app.init();
  popup.buttons.find(button => button.label === layout.anchors.houseDoor.action).callback();
  await flush();
  assert.equal(typeof resolveRecovery, 'function');
  onMove(layout.anchors.chart);
  const before = app.snapshot();
  assert.equal(before.current, 'chart');
  const expected = { ...before, signal: [...before.signal] };
  resolveRecovery(layout.anchors.houseDoor);
  await flush();
  const observed = app.snapshot();
  const report = {
    scope: 'Mock-only diagnostic of unchanged original controller',
    sequence: [
      'Initialize at houseDoor',
      'Invoke Enter keeper’s house; reject teleport',
      'Hold rejection-recovery getPosition() pending',
      'Emit a newer onPlayerMove at chart',
      'Resolve older recovery position as houseDoor'
    ],
    expected,
    observed,
    diagnosis: 'Delayed rejection-recovery position overwrites the newer movement because this path checks disposed/transitionId but does not guard moveCount.',
    messages
  };
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  app.dispose();
  assert.deepEqual(observed, expected, 'Newer onPlayerMove must win over delayed rejection-recovery getPosition');
})().catch(error => { console.error(error); process.exitCode = 1; });
