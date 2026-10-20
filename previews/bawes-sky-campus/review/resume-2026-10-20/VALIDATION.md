# Fresh local validation, October20

The TMJ and its runtime/assets remain byte-identical to `de4ee87`. Runtime was restarted locally using the saved pinned engine. No public preview, engine source change or deployment was made.

- All ten café seating anchors (four lounge, two armchair, four stool) reached the exact native anchor within2px and passed native facing checks, Woka scale1.
- The original run passed four of six outdoor bench anchors, then anchor70 stopped3.98px off target. Targeted follow-up reached70 exactly, but71 stopped8.03px off target. This is **not a fully clean bench validation**. Cause remains uncertain; no claim of a new map defect or a test-only cause is made. Both failed runs and screenshots are retained.
- Three single-command west-terrace-to-stage traversals reached the exact target without cancellation or map-change replanning. Normal exterior approach opened the gate and reached the interior.
- Fresh runtime approach checks from the portal to café east, through the main café route and into the western lounge approach all pass.
- Static connectivity: all72 anchors connected. The continuous96px café route, blocked pedestal foot, and walkable space behind the lantern head pass.
- Accepted interior pixel/collision checks and unchanged-map comparisons pass. Gate/runtime bytes remain unchanged.

`before-cafe-from-de4ee87.png` is the saved earlier runtime view. `current-cafe.png` is the fresh current runtime capture following this assessment, **not a repaired-counter after image**. Camera/avatar differences do not indicate artwork changes.

No action was denied by automatic approval review. The unresolved result is counter-source feasibility and the exact-position check on bench71; no uncertain external write or deployment was attempted.
