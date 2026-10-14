# Additive Moonlit r3 repair candidate

Derived from sealed-r2 at universe-maps 6db977fcb576be429e1c147f59226f62641efae7. The original seal remains in /workspace/scratch/moonlit-validation/sealed-r2 and is not edited. Copied README, STATUS and verification documents describe the historical r2 baseline; this note and ../REPORT.md describe r3. BASELINE-MANIFEST.sha256 is historical only; MANIFEST.sha256 hashes this candidate.

The authored JavaScript source is runtime/moonlit.js (there is no separate transpilation step). source/build.py builds the map, not this controller. runtime/moonlit.tmj, art and audio are unchanged.

Changes: wrap browser default timers through globalThis; use the public registerMenuCommand options API with key equal to its label. Engine aa3ca1d60801172bfd97b6619bbf351c17eb3dba unregisters menus by label during iframe close, while its menu store deletes by key. Matching these identifiers lets the engine perform natural departure cleanup without relying on pagehide delivery. The public API's default random key caused the stale entries. This compatibility fix is tied to the inspected engine contract and should be retested on engine upgrades.

The original 17 controller tests now accept the supported options form. tests/repair-regression.cjs adds timer receiver/cancellation and departure/rejoin key-contract regressions; both fail against the original controller and pass here. These model contracts; actual Chromium evidence is retained one directory above. Public passage stays fail-open. Closing is still single-client demonstration only.
