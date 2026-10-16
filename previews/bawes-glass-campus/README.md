# BAWES glass campus

An isolated 96×88 campus at native 32px scale, with a folded colored-glass BAWES tower facing an open square. Outdoor spawn is beside the entrance and meeting room; seated occupants remain visible through the front glazing. Stepped planted wings, stone piers and deep eaves give the tower a complete architectural mass. A coworking house, staff house and curved glass portal pavilion form the northern district.

The visual pass adds reference-atlas furniture and materials, furnished work and meeting clusters, a lounge, presentation boards, planting, terraces, a stage and a beach with parasols, boardwalks and shoreline. The StudentHub court remains open for shared use and later configuration. Wide connected routes link every district. This is a local-client-tested draft for owner review; it has not been deployed.

## Behavior

- Four independent full-footprint cutaways preserve floors, furniture and permanent collision. The tower's entire 24×19 projected footprint becomes usable interior.
- Six-tile tower entrances; 6,395 connected walkable cells, 88 statically reachable seats and six reachable portal bays.
- Front/rear tower doors open on approach and permit safe exit. The meeting room has an explicit Apps-menu courtesy lock, also available in the mobile profile menu. Shared state propagates to visitors and reconnects; occupants retain exit, the owner can unlock from outside, and a 15-minute lease expires abandoned locks. This is not authorization or audio isolation.
- Six portal arches await destination binding through the existing area editor's “Portal to any room”. `source/portal-areas.json` supplies pixel rectangles with empty properties, not installed WAM areas. No invented destination URLs or engine feature.
- No baked labels, walking popups, quests, background audio or conversation-disabling `silent` property. Furnishing does not automatically configure live media/events.

## Current evidence

- `review/polished-campus-routes.json`: 26/26 actual-client routes through the tower, meeting room, rear street, coworking, portals, staff terrace, stage, beach and StudentHub.
- `review/polished-doors.json`: 10/10 two-client checks for lock control, late join, collision, reconnect, safe exit, propagated unlock, touch controls and independent cutaways.
- `review/polished-district.json`: 5/5 checks of the final occupied glass frontage, independent interior reveal and lounge seating/exit.
- `review/polished-coast.json`: current spawn, beach/shore collision and cowork terrace checks.
- `review/static-validation.json`: connected walkable cells, seats, portal bays and complete reveal masks. Static reachability does not certify every seat's native avatar overlap.
- `review/polished-*.png` are actual game captures. Normal desktop captures use 1440×900 viewport, native Woka scale and camera zoom 1. Files named `overview` and `northern-district` use the client's zoom-out control; narrow mobile captures test touch UI. `review/outside.png` and `inside.png` are offline full-map layer exports, not gameplay screenshots.

The route/door sweep used the final furniture and collision layout before the last exterior-only tower/pavilion substitutions. District and northern captures use those final shells. Historical `town-*`, `geometry-*` and `client-*` evidence belongs to prior revisions and does not certify this visual pass. Source and generated-file hashes are recorded in `review/polished-validated-inputs.json`.

Build from this directory with `python3 source/build.py`, then run `python3 source/validate.py` and `node source/test-reveal.cjs`. Repository `npm run build` passed all 11 maps without deployment. Local runtime setup is in `source/runtime/README.md`; engine revision is `274114560c5ec95fdf8e51e67986a53069f3cf06`.

## Provenance and scope

`source/ASSET-PROVENANCE.md`, `asset-manifest.json` and `REFERENCE-CONTRACTS.md` document selected WA Village/100 Roads atlases used under the user's reported WorkAdventure partnership permission. No general/open license is asserted. Campus layout/code and generated architecture are separately authored; retained generation inputs support rebuilding. `ART-PROVENANCE.md` retains historical first-generation notes.

All work stays under `previews/bawes-glass-campus/` on `feat/bawes-glass-campus`, draft PR #21. Existing maps, Azure and tracked engine source remain unchanged. No merge, deployment or world registration. Portal destination binding and owner visual acceptance remain outstanding.
