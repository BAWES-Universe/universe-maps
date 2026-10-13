# Circuit Arena: safe room setup

This package is a local template. It does not create a room, configure a live meeting service or establish media acceptance.

## Create a separate room, then reconcile its real WAM

1. After publication is separately authorized and verified, create a new room using the actual versioned Custom TMJ URL. Obtain the real room/share URL; do not guess one.
2. Export/back up the actual room WAM through an authorized supported interface. Preserve its absolute map URL, existing areas, entities, collections and settings.
3. Add the two team rectangles below using the native editor's Video call option. Its detail header is Meeting Room. Each must use its own distinct room name.
4. If the deployment exposes Stage/Podium and Audience controls, add the caster and spectator areas below. Link the listener to the actual created podium AREA ID, not its display label or broadcast name.
5. Verify the saved actual-room WAM and perform multi-participant acceptance before describing media as active.

## Exact proposed rectangles

Coordinates are native pixels. Native WAM membership uses the player's feet at `(player.x, player.y + 16)` and includes far edges. Widths/heights below already use exclusive artwork bounds minus one where appropriate.

| Area | x | y | width | height | Role / name |
|---|---:|---:|---:|---:|---|
| West team | 128 | 192 | 383 | 447 | Video call room `esports-arena-v01-west-team` |
| East team | 1504 | 192 | 383 | 447 | Video call room `esports-arena-v01-east-team` |
| Caster / presentation | 736 | 256 | 575 | 191 | Speaker/podium area ID `esports-caster-podium` |
| Spectators | 736 | 608 | 575 | 415 | Audience listener references `esports-caster-podium` |
| Arrival | 1000 | 1352 | 31 | 31 | Default start |

The companion's two Video call properties use `livekitRoomProperty`. This is the native Video call/Meeting Room feature, not a newly purchased or separately created service. A successfully joined named room changes ordinary proximity behavior; schema validity alone is not proof that joining works. Both teams have distinct room names. Leave/rejoin and device permissions require live testing.

Native Stage/Audience editor controls require `FEATURE_FLAG_BROADCAST_AREAS`. The deployment flag and account permissions are unverified. If those controls are absent, ask the authorized administrator for a supported setup route. This guide does not authorize changing security/settings, retrieving credentials or bypassing restrictions.

## Arrival silence and casual conversation

One native transparent silent tile layer covers exactly x992–1055 and y1344–1407, four tiles. Native silence uses player position, without the WAM feet offset. Every other common route and social seat is outside authored silence. Do not add whole-lobby silence.

The two casual pairs are 56px apart, below the inspected source's 64px ordinary-proximity start distance. Service pairs are 49px apart. Source defaults may be overridden by deployment. Walls and furniture do not provide private audio isolation.

## Companion WAM is not an automatic import

The inspected Custom TMJ creation flow saves the external map URL and normally creates a separate room-specific WAM with empty areas/entities. It does not discover or import an adjacent companion WAM. The package's relative `./esports-arena.tmj` mapUrl is only for portability and must not replace an actual room's absolute map URL.

An explicit mapUrl update can regenerate the WAM and reset live configuration, even when the URL value is unchanged. ZIP upload can replace destination contents and supplied WAM files. Back up the actual isolated destination and reconcile configuration before using either route. Do not blindly upload this package into a live room or root directory.

Pinned inspected admin sources:
- [Room creation](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/admin/rooms/route.ts#L390-L399)
- [Room WAM resolution](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/map/route.ts#L186-L265)
- [Empty WAM construction](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/lib/map-storage.ts#L152-L200)
- [Map URL reset handler](https://github.com/BAWES-Universe/workadventure-universe-admin/blob/e1a9f1b48f0c8579ebfdf4a4eab2c1fbd730e6e1/app/api/admin/rooms/%5Bid%5D/route.ts#L503-L540)

## Required live acceptance

- Verify actual deployed native32 behavior, fresh spawn, keyboard movement, touch/pointer clicks and both team door approaches.
- Inspect local and remote avatar/chairback depth, the caster desk, screen, service counters and social sofas on desktop and narrow mobile displays.
- Confirm the two team calls remain independent, the spectator audience listens to the caster role, and ordinary social pairs still use intended proximity.
- Test leave/rejoin, permissions, reconnects, device selection and realistic participant load.
- Confirm the actual room WAM still preserves unrelated settings and points to the intended absolute published TMJ.

There is no camera focus/reveal script and no true multilevel movement. All compilation and source-route tests are offline evidence, not live media or performance acceptance.
