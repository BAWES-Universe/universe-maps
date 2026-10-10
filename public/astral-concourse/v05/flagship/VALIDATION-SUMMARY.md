# Flagship v05 Roofless Garden: validation

Checked2026-10-10 against unpatched engine source `90a148c03e03401e26d236eaac9bea4123b42c57`. This is offline source, geometry and pixel-depth evidence, not live browser/media/load acceptance.

## Passed map checks

- Complete native32 orthogonal 80×60 runtime: nine local files,6,778,158 bytes, no script or toggle group.
- All2,100 walkable cells connect to arrival. All238 seats/resting anchors and19 landmarks have clear native16×16 bodies.
- All210 hall seat records and24 existing social anchors remain unchanged. Two visible low planter wings add four solid cells; one overconservative doorway-corner cell opens after its foliage sliver is trimmed. The lounge03 entrance remains192px wide.
- Exhaustive1,813,500 reachable integer body-clear positions: zero opaque foreground/head conflicts using all12 Greg32 upper14px masks. All4,356 conservative spawn points are safe and silent.
- 11,742 normal native movement legs pass, covering all seats, returns, three hall banks, stage, coffee, both garden doors, path junction and pavilion. At32,152,912 sampled positions, no collision, head conflict, unintended meeting entry or loop occurs.
- Twelve doorway/junction/meeting-boundary checks pass, with physical route sweeps and forward/reverse garden circuits.
- Independent current-schema/zone checks:29/29. Independent garden/delta checks:24/24. Existing media rectangles and333 quiet tiles remain unchanged; four new garden seats are outside all communication/silent areas.
- Package checks:33/33, including visible-RGBA atlas roundtrip, exact local closure and no review-avatar dependency. The public runtime-manifest verifier also passes under ordinary Python and Python `-O`.
- A separate-directory, network-free rebuild reproduces all13 checked art/geometry/runtime identities, including every runtime file, byte-for-byte.

## Known native pointer limitation

The test executed11,758 total commands. Sixteen are explicitly recorded same-cell baseline exceptions, rather than passing normal movement legs:13 pointer commands choose a neighbouring tile and3 exact-nearest-disabled controls return no path. This reproduces unpatched native behavior independently of map scripts; see [issue798](https://github.com/BAWES-Universe/workadventure-universe/issues/798) and the separate [PR799](https://github.com/BAWES-Universe/workadventure-universe/pull/799). No claim is made that every pointer command reaches its intended tile.

The initial off-center terrace-corner test also reproduced on the old map geometry. Opening one visibly clear cell resolves that recorded route without changing the engine. A synthetic junction sweep that originally extended beyond the paved route was corrected to test the actual junction; surrounding scenery remains blocked.

This roofless runtime does not emit visibility changes or active-path replans. It does not require the proposed engine patch. Deployed source/settings may differ from the pinned source.

## Identities and live acceptance

- TMJ SHA256: `876a5dbb825b45a5d7d7f105070ab105d6280d314b8a56a7b2ae472b0426c3e8`
- WAM SHA256: `6b14ccf7218971e5645ed1c68527d7ccbcd99355c55ecd7ee2b51ea8ddc6d3dd`
- All runtime identities: `RUNTIME-MANIFEST.json`

The standalone source backup includes portable native replay, exact source pins, per-command compressed records, selected full traces and minimal controls. Native-source sweeps do not substitute for actual Phaser keyboard collision resolution, desktop/mobile rendering, local/remote avatar depth or network transitions.

A Custom TMJ room does not import companion WAM areas automatically. Follow `integration/ROOM-SETUP.md`; preserve the actual room map URL and existing configuration. Live meeting/broadcast operation, permissions, feature-flag visibility, reconnection behavior and concurrent capacity remain unverified.
