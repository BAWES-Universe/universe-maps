# Lantern Congress

A new, calm contemporary three-hall conference template. Native 32px grid, 3072 × 2048 pixels, warm oak acoustic walls, recessed windows, terrazzo, green textile seating and useful staffed coffee/check-in spaces.

## Included

- Summit: 48 seats in three banks
- Forum: 24 seats in a horseshoe/panel arrangement
- Lab: 24 seats around six four-person tables
- Two independent four-person networking bays and three casual pairs
- Three independent authored Podium/Audience links in the portable companion WAM
- Native entry focus for each talk room; a small eight-cell quiet arrival only

These are furniture counts, not tested concurrent capacity. This is a conference venue template, without a real schedule, streaming service, room creation or live-media configuration.

Open `map32/conference.tmj` in Tiled. All runtime references are relative and included. The companion `conference.wam` is a candidate for an authorized room setup; Custom TMJ does not automatically import it. Follow `integration/ROOM-SETUP.md` before using communication areas.

## Review

- `review/overview.png`: 50% source-composited overview
- `review/networking-occupied-native32.png`: unscaled occupied networking/counter detail
- `review/workshop-occupied-native32.png`: unscaled occupied workshop detail
- `review/focus-source-calculated.png`: source-calculated initial camera fit, not a device screenshot

## Verification

The final lectern-depth freeze passed root visual review and independent source/static review. The independent reviewer reran all 4,392 native routes and confirmed 12,965,240 swept samples with no failures. See `validation/independent/REVIEW.md`. This is an unpublished local template.

## Local verification

`CORE-FREEZE.json` pins the tested runtime, geometry, artwork and proof. The source runner uses unchanged methods from engine commit 60e7afdc3f96ef32525597cd46bd41175d61a2ef and real EasyStar. It tests native tap destinations/returns, desktop/touch dispatch, body/head sweeps and unwanted room entry. Directional doorway vectors are geometric source checks, not live keyboard-physics acceptance. See `validation/` for exact final counts and limitations.

Every stage tread is open single-level 2D floor. Solid-looking stair endcaps were removed. The low platform, shallow steps, walls and shadows are visual depth rather than multiple physical heights. No map script, layer toggle, engine patch or exterior camera state is used.

Initial focus fits each complete room on desktop, landscape and portrait at DPR 1/2/3; portrait avatar frames are about 9.4 CSS pixels high at the whole-room fit. Manual zoom remains available. Existing focused rotation/resize behavior does not fully pass and is explicitly recorded. Live rendering, phone behavior, multi-user media and concurrency remain untested.

## Rebuild

Python 3.12 with Pillow 12.3.0 and NumPy 2.3.5 was used. Run `python tools/build_all.py` from this folder. Native route replay additionally needs Node and uses the bundled source extraction/EasyStar fixture. Camera math proof needs the pinned packages listed in `tools/focus-dependencies.json`, or an existing matching checkout supplied through `ENGINE_AUDIT_REPO`.

All generation masters, prompt specifications, proportional asset registrations, masks, fonts/licence and rebuild tools are retained. No existing flagship is modified. See `PROVENANCE.json`.
