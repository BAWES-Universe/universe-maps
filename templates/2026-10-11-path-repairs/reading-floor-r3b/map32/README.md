# reading-r3b: native floor repair candidate

Unpublished additive candidate, awaiting independent review. Earlier delivered freezes are unchanged. All native all-admitted-floor source routes and targeted visible-floor/fixture probes pass. Native 32px grid edges at real furniture, window sills, posts and curved borders retain normal body-clearance margins; this does not mean every pixel next to a fixture is walkable. No engine modifications.

Changes: the complete four-cell-wide entrance was restored with a bounded generated gate/lamp alignment patch. Reading desks, chairs, counter, distant vista and all art outside [256,352,512,512] stay exact. A clear standing-desk nook gap was opened.

Proofs use decoded current TMJ artwork and unchanged native standing frames. They are not live browser screenshots or a sitting-animation claim. Automatic facing is not implemented. Media/service integration is not configured or tested.

## Replay
Requires Python 3 with Pillow and NumPy, and Node. Run `python tools/replay_current.py` from this extracted source root. It rebuilds runtime from bundled authoring inputs, runs unchanged pinned native source movement, and compares exact runtime SHA-256 values. Generation is not rerun: generated source images are preserved.

Review FLOOR-AUDIT.json, NATIVE-ROUTES.json or validation/native-routes.json, STATIC-CHECKS.json or validation/geometry.json, and review/floor-before-proof.png, floor-after-proof.png, art-before-after.png. Historical baseline evidence is explicitly isolated.

Packaging-only follow-up: corrected runtime README; all engine/art/layout bytes are identical to the independently reviewed reading-r3 candidate.
