# Implemented interaction inventory

This is one compact, connected social map on a 40×32 tile grid (1280×1024 native pixels). Artwork has no place-name lettering; owners can reuse and rename it. The descriptive map name and object IDs are internal metadata.

| Area | Furniture / intended use | Implemented behavior |
| --- | --- | --- |
| Main promenade | Broad connected paving; arrival and circulation | Keyboard and native right-click movement around both sides of the fountain and café groups. Four planted beds and fountain basin block walking. |
| Central fountain | Visual meeting landmark | Native tiled animation of descending droplets and expanding ripples, below Woka rendering. No quest, trigger popup, or automatic audio. |
| Two café groups | Two chairs and one table per group; casual conversation | Four occupancy targets, with open north approaches. Tables block walking. No serving/minigame feature. |
| Glass lounge | Four individual chairs, two side tables, three-place settee and coffee table | Seven occupancy targets. Glass canopy hides when entering and returns when leaving. Tables and planting are solid. |
| Overlook | Two chairs and a small table; quieter visual setting | Two occupancy targets; table solid. Connected to promenade by broad opening. No acoustic/private-room isolation. |
| Ocean | Coastal backdrop | Native animated transparent caustics over fixed ocean artwork; land/furniture remain stationary. Motion fades before the shoreline and vegetation. |

## Audio and actions

Spawn is silent. The profile's **All settings** menu contains one optional action: **Play sea sound**, which changes to **Stop sea sound** while playing. It uses `WA.sound` at fixed volume0.45 and loops a local12-second synthesized WAV. There is no audio popup, walking-triggered selection, per-area sound, or distance attenuation.

The release's native audio player was tested first: Play/Pause/Mute worked, but native Stop cleared the active property cache and walking reselected the full-map audio URL. Reliable Stop persistence therefore is not available through that map-only integration on the pinned release. The explicit menu fallback avoids this defect without changing the engine. Native master audio controls do not govern this separate `WA.sound` channel; use the explicit Stop action. Physical speaker output remains unverified; actual Phaser output is captured for listening.

**Take nearest seat** uses the closest of 13 occupancy targets within 112 map pixels. It approaches from the north and moves onto the cushion, leaving the native Woka upright and downward-facing. A final native position adjustment of at most12 pixels aligns the feet with the painted cushion center, only after the path finishes successfully. The settee uses a16-pixel approach within the cushion row so the rear wall remains solid. Walking exits. This is positioning on a seat, not a custom seated Woka animation. Selecting the action too far from furniture shows one dismissible guidance popup; walking alone never shows it.

The map adds no meeting/private/silent zones, Jitsi rooms, doors, quests, teleport destinations, embedded websites or special chat rules. Standard engine proximity communication remains available, but multi-participant voice/chat behavior was not independently tested for this map. No per-area sound or distance attenuation is configured.

## Rendering and limitations

Native grid32, Woka scale1 and camera zoom1. Floor artwork, collisions and water effects render below `floorLayer`; glass canopy is the only above-avatar map layer. Ocean uses a3.84-second periodic overlay; fountain uses a1.12-second cycle. These durations describe configuration; actual rendering evidence is linked separately. Ocean motion is an overlay, not displacement of the underlying painted water. Physical audio devices and mobile Safari are not validated.
