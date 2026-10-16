# Azure Archipelago — unpublished draft

Separate expanded-map work; compact published checkpoint7336e66639a1264936a1bda311fcfd76fd0e0e1d is preserved.

5120×5120 world pixels,160×160 native32px tiles. Four1216×1216 islands connect by256px clear bridges to768×768 hub. Intended areas: café north, garden south, lounge west, gathering east. No baked text. Woka scale1 and default camera.

This is a development checkpoint, not an accepted playable release. The map loads in the actual local release engine with a visible avatar and zero walking popups at spawn. Structural flood fill reaches all4598 free cells;43 provisional seats. Independent early layout review found no disconnection. This is not a substitute for actual route/seat/table tests.

Final artwork is provisional: image generation shifted some furniture and terrace boundaries from guides. Collision, seating targets, shoreline joins, fountain basins and water animation MUST be reconciled with final rendered artwork. Hub now includes eight seats and a fountain court; four bridge viewing bays provide eight more seats. Landing aprons and lounge north entrance are visible paving layers. Continuous water footage and final independent gameplay review are pending. Do not publish or deploy this revision.

`source/layout.cjs` makes geometry guides; `source/build-map.cjs` makes the runtime scaffold. The builder preserves existing island PNGs and only supplies guides if missing. Rebuilding is not acceptance.

Sound starts silent and offers deliberate Play sea sound/Stop sea sound menu commands. It uses the validated WA.sound fallback, whose separate sound channel is not controlled by native audio master controls. No walking-triggered popup code exists.
