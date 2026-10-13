# Map source recovery and preservation

This source-backup branch is an additive, non-deploying preservation record. It must not be merged or deployed as a release without a separate review. Existing published maps remain untouched.

## Recovery status

- N01–N50: all 50 complete source packages and all 50 exact runtime packages were recovered from the delivered archives and hash-verified. They are being synchronized here as ordinary files.
- Lighthouse Last Signal r2: full source and runtime recovered.
- Lighthouse Keeper’s Return r2: runtime recovered; complete rebuild source remains missing.
- Studio r8 and Reading r4: runtime fixtures recovered in the rendering investigation; full rebuild source remains missing.
- H009-initial, H025 and H039: partial recovery only. Original generated artwork and complete final freezes have not been recovered. Their RECOVERY documents govern their current status; historical READMEs/READY receipts do not prove restored completeness.
- The other new H-series map source/art/freeze folders are missing from this recovery snapshot. The version-22 testing workbook records the recovery statuses. A historical scoped pass is not a recovered map.

An in-progress checkpoint preserves the recovery documentation and partial material first. SYNC-STATUS.json distinguishes this checkpoint from the completed source synchronization. No map is newly published or live-tested by this backup.

## Layout

- old50/source/<revision>/ contains authored artwork, build scripts, dependencies, and preserved source evidence.
- old50/runtime/<revision>/ contains exact TMJ, WAM, script and texture files.
- baselines/ contains recovered Lighthouse files.
- partial-new-maps/ contains explicitly incomplete H-series recoveries.
- rendering-investigation/ contains the preserved renderer investigation and fixtures.
- catalogue/ contains testing workbook version 22.

Source files are ordinary editable files; no ZIP extraction is required. Each source package documents its build command. Typical dependencies are Python 3, Pillow, NumPy, Node.js, and, for some review tools, ReportLab, pdftoppm and DejaVu Sans regular/bold fonts. No fresh generation or build is claimed in this recovery operation.
