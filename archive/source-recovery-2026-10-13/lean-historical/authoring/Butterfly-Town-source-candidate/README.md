# The Butterfly Gate · StudentHub Town

Ready-to-review source candidate. Deployable TMJ and relative assets are in `map/`. Existing maps are unchanged.

## Reproduce
- Python3 + Pillow: `python tools/build_map.py` rebuilds original source art into the deployable TMJ.
- Node: `node tests/run-state-tests.cjs` runs31 independent lifecycle/structure checks.
- Node: `node tools/validate-engine.cjs` runs the pinned Universe validator.
- Serve locally: `python qa/server.py`, then open http://127.0.0.1:8798/qa/. The browser harness uses Phaser3.86 and extracted source rules. Run rendered checks, review frames, depth proof or record tour with explicit buttons.
- Repository: copy map/ to public/butterfly-town/ and run the existing repository npm run build.

## Verified
31/31 state/structure checks;30/30 rendered checks; complete63-second physics journey; map validator and repository build passed. Read RELEASE.json and evidence reports for exact scope. The MP4 is supplied separately.

## Limits
This remains a local candidate, not a deployed Universe session. Two-client multiplayer, production reconnect and device acceptance must be verified in the actual hosted fork. Fixed TMJ split-depth furniture is not editor-draggable WAM furniture. Peripheral cliff/garden art is scenery outside authored walk paths.

See DRAFT-PR.md for the publication handoff. No push, merge or deployment was performed.
