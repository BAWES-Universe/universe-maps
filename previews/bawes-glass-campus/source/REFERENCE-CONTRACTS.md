# Reference study and existing engine contracts

Source requested by the user: https://workadventure.github.io/wa-village/wa-headquarters.tmj (read through its public GitHub source when the Pages endpoint returned 403 in this environment). Retrieved source SHA256: `8577301f460758b6ff1081a3a7ca14a339cc195d4aab732db9eda208891d15cc`.

The 200×120, 32px reference separates `collision`, ground layers, `floorLayer`, `AboveWorld` layers, and removable `roof1` / `roof2` layers. The transferable technique is continuous usable interior beneath a removable full building shell, with exterior circulation between and behind buildings. The new original town uses four full-footprint interior masks and separate shells. Its tower remains on the same continuous map, with no teleport on entry.

The reference copyright identifies 100 Roads Inc. as sole owner and reserves reproduction/distribution/derivative rights. The user reports permission through an official WorkAdventure partnership. That statement is retained as user-provided authorization, not a general license. No reference map tiles, raster artwork, scripts or layout were incorporated in this candidate; source inspection files remain outside the repository.

Door study: `src/meeting/doors.ts` locally swaps the nearby meeting-door layers. The main office uses `doorOffice` and `doorOffice2` shared variables and doorstep areas with `autoOpen` / `autoClose`. That downloaded source does not establish a separate shared lock. The user-observed live lock may have different/newer configuration. This candidate's original map script uses existing `WA.state` subscriptions for its meeting lock, local visual/collision door layers, and an occupant exit allowance. This is a courtesy meeting lock, not authorization or audio isolation. No engine feature was added.

## Existing portal area editor

At engine commit `274114560c5ec95fdf8e51e67986a53069f3cf06`:

- `play/src/front/external-modules/teleport/index.ts` registers **Portal to any room**.
- `TeleportPropertyEditor.svelte` edits `data.url` and optional `data.startArea`.
- Entering an area finds `{type: "extensionModule", subtype: "teleport", data: {url, startArea}}`, ignores missing/empty URLs, and invokes existing room navigation.
- `libs/map-editor/src/types.ts` defines editor areas with `id`, pixel rectangle, `visible`, `name`, and `properties`. Every property also has an `id`.

The six original portal arches are placed in the glass pavilion. `portal-areas.json` supplies native pixel rectangles and empty properties for each bay. They are **unbound planning records, not installed editor areas**: this source TMJ is not a deployed WAM/editor room. In the existing area editor, draw a region over a bay, add “Portal to any room”, paste the chosen destination and optionally the start area. Artwork may likewise be placed elsewhere using the existing entity tools. No placeholder destinations, automatic room URLs, custom portal engine or mandatory portal spawn are introduced.

Main spawn remains beside the tower/team meeting space. Pavilion exploration is optional. Staff/coworking, outdoor stage, booths, promenade and beach are physical spaces; media permissions, staffing, live events and destinations require actual room configuration and are not claimed from artwork alone.
