# Magical campus06 native map payload

Entrypoints: `map16/magical-campus.tmj` for the finite town-center campus; `gate/map/gate.tmj` for the preserved bounded giant gate. All atlas, script and audio URLs are relative. Keep this directory structure when hosting in an isolated versioned folder. These are native Tiled tile-layer maps for the audited Universe fork. No browser harness, test video, engine vendor or historical map is included.

The campus starts at the fountain junction. Greg stays native32px with the normal16×16 body; maps do not resize the player. Permanent collisions are independent of roofs, glazing and signs. Office, classroom and event roofs have solid, approach-translucent and interior-cutaway states. Furniture is fixed Tiled artwork; its editable source layers and footprints are supplied separately. It is not auto-imported as movable WAM furniture.

Localized fountain, fire and gate-waterfall audio uses the current native music player through supported map properties. Choose Enable nearby sounds on each map visit. Native mute/volume remain effective; work, meeting, classroom and event interiors are quiet. Turn off nearby sounds for persistent silence. Browsers that do not support programmatic HTMLAudio volume, including affected iOS behavior, remain silent rather than playing unattenuated sound. Enable nearby sounds resets on gate-to-campus navigation because consent is per map. There is no global ambience or `silent` property affecting people.

The companion `companion-wam/native-meetings.wam` declares three native meeting rooms and points relatively at the campus TMJ. Follow its ACTIVATION.md: room registration must expose the WAM through the supported importer/room resolver. Loading the TMJ alone does not activate its companion WAM. Live multiplayer/media and stage broadcasting have not been tested or configured.

Both real room URLs remain blank. An owner must assign actual registered HTTPS PLAY room URLs to enable gate-to-campus travel and the deliberate return action. No invented destination is persisted. Local source-harness scene handoff is separate evidence, not live room navigation.

Owner-generated art and audio retain their existing provenance; this package grants no new license. Source references, compiler inputs and local validation evidence are kept separately. No existing published map needs to be modified.
