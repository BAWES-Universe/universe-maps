# Native campus return action companion

`campus-return.js` adds one deliberate return action to the existing painted arrival ring. It contains no room URL. `metadata-patch.json` sets `gateRoomUrl` to an empty string; configure it only after the actual gate PLAY room has been registered. The packaged giant gate's `campusRoomUrl` also remains empty. No live connection is claimed.

The pad is `(1524,2912,24,32)`. The existing start area is `(1488,2896,32,32)`, separated by4px horizontally even with closed boundary comparisons. Initial native arrival `(1504,2912)` is outside the pad. The source uses feet `(x,y+16)`, so the origin `(1536,2912)` is inside the pad. Source pixels were checked in the actual native arrival screenshot with camera offset `(992,2368)`; the pad is within the painted ring on the avenue. All858 integer body-origin/pad and1px arrival-to-pad sweep checks pass against the unchanged16px collision grid. Greg remains32px; the body remains16×16, x−8 to x+8, y to y+16. No art, collision or start geometry changes.

An unconfigured/invalid destination produces no action or navigation. With a real absolute HTTPS URL configured, entering the pad shows native `WA.ui.displayActionMessage({message:'Return to the giant gate',callback})`. Only deliberately activating that action can call `WA.nav.goToRoom`. The callback re-reads position; leaving invalidates a pending callback even after re-entry. Movement revisions reject stale area-enter reads. Repeated callbacks cannot duplicate travel. After failed navigation, leave and re-enter before retrying. Exit/disposal calls the ActionMessage's `remove()` and unsubscribes all three listeners. There is no timed, automatic or proximity return.

## Apply after the active capture

The generator is deliberately opt-in and refuses to overwrite its input. It preserves all tile layers, tilesets, existing objects and spawn, adds the one area to `campus-zones-offline`, and adds the script/config properties. It refuses to replace another existing script or nonempty destination silently. It is idempotent.

```sh
python companion-campus/prepare_metadata.py \
  --input /path/to/map16/magical-campus.tmj \
  --collision-grid /path/to/map16/collision-grid.json \
  --output /path/to/map16/magical-campus.return-ready.tmj
```

The output must be a sibling of the original map, so unchanged relative atlas URLs remain correct. The command also installs the companion bytes at `/path/to/map16/scripts/campus-return.js`. Review that metadata-only output, then the integrator can replace the current TMJ or consume the patched in-memory map for a short source-harness test. Without `--output` the command only validates; the author used that mode and did not modify active campus files.

## Exact source-preview adapter requirements

Execute the companion's unmodified source bytes, with a scene-scoped WA/window adapter like the bounded gate harness. Do not invent a second return state machine.

- `WA.onInit(): Promise<void>`
- `WA.room.getTiledMap(): Promise<TiledMap>` returns the patched campus metadata
- `WA.player.getPosition(): Promise<{x,y}>` returns native32px character origin, not feet
- `WA.player.onPlayerMove(callback)` reports current origin and returns `{unsubscribe()}`
- `WA.room.area.onEnter('gate-return-pad').subscribe(callback)` and `.onLeave(...)` each return `{unsubscribe()}`. Movement remains authoritative; signal both area edges after updating position
- `WA.ui.displayActionMessage({message,callback})` returns `{remove():Promise<void>}`. The preview must present one visible button/action and call callback only on deliberate click or Space. Never activate it from an enter event or a timer. Removing a prompt disconnects its button/keyboard handler
- `WA.nav.goToRoom(url)` intercepts the explicitly marked in-memory preview test URL and starts the actual bounded gate scene at its original spawn. Do not navigate the browser to the test hostname
- Scoped `window.addEventListener('pagehide',fn,{once:true})` registers the source cleanup. Invoke those handlers before campus scene shutdown while its UI/body still exist; do not dispatch real window pagehide or dispose shared audio

For local browser testing only, clone the patched map in memory and set its gateRoomUrl to a documented reserved test destination, intercepted as a scene load. Keep all on-disk native URLs blank. Record that override and its local scope in the report. Reuse the existing canvas and audio controller; switch sound to `gate` and the original gate spawn during actual scene creation. A short browser acceptance should show: initial arrival has no prompt; walking32px right offers one prompt; leaving removes it; re-entry plus deliberate action loads the original gate at `(480,1336)` exactly once. An unconfigured clone should show no prompt even on the pad.

The updated bounded gate factory uses the vendor's required `AnimatedTiles`/`animatedTiles` scene registration and automatically runs script cleanup before `onNavigate`. An explicit `scene.gateQA.dispose()` before scene.start is safe and idempotent. Destroyed-layer lookups are guarded. These fixes are in the original `qa/gate-scene.mjs`; do not replace them with the earlier draft when repackaging.

## Evidence and limits

Run `node companion-campus/tests/check-return.cjs` for19 source lifecycle checks; run `python companion-campus/prepare_metadata.py --input … --collision-grid …` for geometry/integrity. Results are in `docs/lifecycle-checks.json` and `docs/geometry-checks.json`. These are Node/source checks, not browser or live transport proof.

The native UI API was verified in Universe commit `5e7670be6c79efc575a7193e8a1a1c8c379b293f`: `play/src/front/Api/Iframe/ui.ts` displayActionMessage, `Ui/ActionMessage.ts` remove/triggerCallback, and GameScene triggerActionMessage/removeActionMessage handlers. No engine files were edited. Live room registration, destination correctness, permissions and multiplayer are still pending.
