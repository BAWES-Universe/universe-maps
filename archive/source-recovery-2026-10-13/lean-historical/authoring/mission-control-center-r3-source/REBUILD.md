# Mission Control r3 | Console-chair alignment

Build with `python tools/build_mission.py`, then `python tools/render_closeups.py`. Test with `node tools/verify_native_routes.cjs mission-control-center` and `python tools/check_head_geometry.py mission-control-center`. Python3, Pillow, NumPy and Node required. No network or image generation needed.

Only six operator-chair footprints change relative to approved r2. The setting, night sky, exterior, architecture, consoles, briefing furniture, collisions and native room properties remain byte-identical. Individually measured console centers are x492,768,1048 in the first row and x560,768,984 in the second. The two middle chairs are placed at x776 to match native tap fitting,8px right of the console axis but within the keyboard width. Other chairs match their measured console centers. Artwork is tucked closer to the console working edge. Valid body anchors are at the northern collision boundary of their existing floor tile.

Occupied proofs show six different actual repository Wokas with existing north-facing standing idle frames. There is no new sitting pose or seated animation. All six actual native tap endpoints now exactly match their chair/body anchors and are collision-free. Native endpoint proofs are primary; no idealized manual placement is substituted. No engine changes.

480 native route legs /694,257 body samples pass. Exhaustive reachable head checks against108 frames from9reference sheets report zero conflicts. Full chair silhouettes are preserved with safe native foreground layering. All non-operator-chair pixels, collision and properties match r2. Live AV/multi-user tests remain unperformed.

## Review sprite licensing
Raw Pipoya sheets are omitted from source archives. The derived head-occupancy mask preserves geometry QA and runtime output. Optional varied previews use the named licensed repository sheets in source-assets/WOKA-PROOF.json, placed as source-assets/woka-proof-0.png through7.png. Without them, previews use the pre-existing reference sprite and runtime output remains byte-exact. Do not distribute standalone Pipoya sheets.
