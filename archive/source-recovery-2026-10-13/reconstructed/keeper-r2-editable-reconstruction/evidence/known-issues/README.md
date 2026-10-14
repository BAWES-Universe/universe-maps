# Known inherited controller issue

Run `node rejected-teleport-newer-movement.test.cjs [path/to/keeper.js]`. This read-only mocked regression intentionally exits 1 against both the retained original and exact rebuilt r2. It asserts that the newer movement event must remain current after an older rejection-recovery position resolves. Expected `current: chart`; observed `current: houseDoor`. All other snapshot fields are unchanged.

The original controller is deliberately preserved byte-for-byte. This diagnostic is separate from the passing reconstruction tests. No native-engine or live-game outcome is asserted. The stdout JSON records exact expected/observed states, and the failure logs retain the actual assertion.
