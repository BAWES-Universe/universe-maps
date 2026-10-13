# Astral Concourse: Building C / v09

A separate native32 building variation. It preserves Garden B’s hall, meeting lounges, reception, garden materials, pavilion and restrained leaf accents, and adds a substantial gold/teal architectural shell with a clear south entrance and two attached side porches.

The map is 2816×2432 pixels. The entire B floor translates by (+128,+256), without scaling. Only 64 native cells extend the southern arrival path. A declared 128×4-pixel threshold strip is the sole changed pixel region inside the translated B base; all other predecessor base and foreground pixels remain exact. There are 210 hall chairs, 16 meeting chairs and 12 casual resting places; these are art/geometry counts, not concurrent-capacity claims.

## Room behavior

- The foyer and hall reveal independently. Hall entry also hides the foyer roof’s northern projection so it cannot cover the lower audience/exit area.
- Six decorative groups own roofs, façade sections and cast shadows. Permanent collision, furniture depth, media geometry, native focus and the sole quiet spawn receiver never toggle.
- Existing native area events drive a 32px hysteresis margin. No per-move camera script, roof fade, collision change or movement command is used.
- The whole hall, stage and speakers receive native entry focus. Outside, normal following and manual zoom remain available.
- Shell art defaults hidden while initialization resolves. Failed startup leaves the safe cutaway; outside visitors may briefly see the floor before the shell appears.

This dynamic reveal depends on the native32 replan fix in PR799. The public dev build was verified as `universe-develop@60e7afd` on 2026-10-10 at 20:04 UTC. Check other deployments independently. Served-version evidence is not authenticated map-play or media acceptance.

## Integration

Serve every file in `map32/` together. `grand-auditorium.tmj` is the Custom TMJ entry. Its sibling WAM is a portable configuration candidate. Custom TMJ does not automatically import companion meeting/podium/audience areas.

Follow [ROOM-SETUP.md](integration/ROOM-SETUP.md). Back up the actual room WAM, preserve its absolute map URL and unrelated configuration, and use the supported native editor. No Universe room or media service has been created by this package.

## Validation status

The frozen candidate passes 94 independent checks and 11,908 native-source route legs, including dynamic visibility replans. Static, lifecycle, route, camera and rebuild evidence is in `validation/`. Two native camera limitations are documented in [ACCEPTANCE.md](validation/ACCEPTANCE.md): focused rotation/resize and repeated rapid re-entry during zoom restoration. These do not establish real-device performance, authenticated gameplay, concurrent capacity or live media operation.

Initial whole-hall camera fit passes nine source-executed desktop, landscape and portrait cases at DPR1/2/3. Manual zoom remains available. Whole-hall portrait fit makes a native32 avatar about7CSSpx high. The existing focused rotation/resize limitation remains and is reported separately; do not read initial-entry fit as a full rotation pass.

The review panels are decoded tilemap compositions. They are not screenshots or proof of smooth live transitions.

## Standalone runtime rebuild

Python3 dependencies: Pillow, NumPy, SciPy. All consumed runtime inputs are bundled.

```sh
python3 tools/translate_geometry.py
python3 tools/import_shell_assets.py
python3 tools/build_reveal_controller.py
python3 tools/compile_runtime_c.py
python3 tools/verify_runtime_geometry.py
python3 tools/render_compiled_c.py
```

The proportional generated masters, prompts and deterministic native module assembly are retained in `source-prototype/`. `source/frozen-b/` preserves the predecessor raster/geometry inputs. Accepted A and B remain independent comparison versions.
