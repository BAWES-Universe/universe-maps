# Astral Concourse: Flagship v05 Roofless Garden

The requested roofless option: the existing hall and coffee terrace now connect to a walkable garden path, ending at an open-center pergola with outdoor seating. The original stage, all 210 hall chairs, four lounge squares and existing terrace furniture are retained. Earlier map versions remain separate.

## Runtime

- `map32/grand-auditorium.tmj`: orthogonal 80×60 map with native 32px tiles, 2560×1920 pixels.
- `map32/grand-auditorium.wam`: portable companion with the auditorium roles, four uniquely named native meeting squares and the default arrival.
- Seven local PNG dependencies: five art atlases, collision marker and transparent quiet marker.
- No map script, roof toggle, automatic focus, camera transition, music, purchase interaction or external media service.

Counts are 210 hall chairs, 16 lounge resting places and 12 casual resting places, including four new garden seats. These are artwork/geometry counts, not concurrent-user capacity or an automated sit interaction.

The north garden paving is walkable. Planting and lawn beyond its edges remain scenery. The hall-side opening joins the right audience aisle; the terrace gate is east of the coffee pergola post. The path ends inside a shaded pergola turnaround, rather than running off the map. Visual steps, column height and shadows do not imply multi-height physics.

## Conversations and safe room setup

Read `integration/ROOM-SETUP.md` before activating media. A Custom TMJ room does **not** import the adjacent WAM automatically. Add the exact native areas in the actual room's editor, preserving its absolute map URL and unrelated configuration. Broadcast editor controls are feature-flagged; deployment visibility is unverified.

The four lounge squares have distinct native Video call / Meeting Room names in the companion. The six smaller casual pairs are outside all authored meeting/broadcast areas and silence. Their anchors are 56px apart, below the inspected 64px proximity-start default; deployed overrides and live behavior remain unverified. Furniture is not an audio privacy barrier.

The shaped TMJ silent layer covers arrival and main circulation, avoiding meeting squares and casual seats. It is one stable layer, with 333 non-colliding transparent cells. No broad WAM silence is added.

## Rebuild

The full standalone art/source backup is retained separately in the user-owned Library. The lean repository preview contains the complete runtime and setup/provenance/validation documents; the following art-rebuild commands apply to that full source backup. The lean preview can be checked independently with `python tools/verify_runtime_manifest.py`.

Python with Pillow and NumPy is required for local source work.

1. `python art/build_roofless_garden.py`
2. `python tools/compile_runtime.py`
3. `python tools/verify_runtime_geometry.py`
4. `python tools/verify_runtime_package.py`

The art source includes the actual input pixels and generation prompt/master. Native route validation is recorded separately under `validation/`, with exact engine-source identities and limitations. The runtime is independent of the test adapter.

## Verification and limits

See `VALIDATION-SUMMARY.md` and `VALIDATION-RESULTS.json` for final checks and file identities. Offline source/geometry tests do not establish browser rendering, remote-avatar behavior, live calls or multi-user capacity.

Current unpatched native code has a separate same-cell pointer fallback, documented in [issue798](https://github.com/BAWES-Universe/workadventure-universe/issues/798): clicking within the tile already occupied can select a neighbouring tile. This roofless map does not trigger visibility-driven replans and does not depend on the proposed engine fix. The normal source endpoint convention is retained; exact pointer pixels are not promised.

## Provenance

The pergola was generated for this project with the built-in image tool and registered into native-scale components. Garden, wall, foyer and furniture inputs are existing project-authored artwork. No Conference Campus pixels are redistributed and no CC0 or other new licence is invented.

Original furniture records: [civic provenance](https://github.com/BAWES-Universe/universe-maps/blob/03d83f2/map-mocks/civic-rooms-01/source/provenance.json), [chair generation](https://github.com/BAWES-Universe/universe-maps/blob/03d83f2/map-mocks/expanded-office-02/source/frozen-review-package/art-meeting/source/generation-record.json).

Greg Gulf-outfit v3 is a project-authored review fixture, reused byte-for-byte at native32 scale. It is not included in runtime dependencies; no original portrait input is bundled. [Reference provenance](https://github.com/BAWES-Universe/universe-ai-creator-kit/blob/67382dc97f494c230e93f0cf67e478df6e5b6d17/docs/catalogue/wokas.md#reference-greg32-map-fixture).
