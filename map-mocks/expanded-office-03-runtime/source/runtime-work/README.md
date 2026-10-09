# Expanded StudentHub native preview

This is a bounded Phaser 3.86 source harness. It loads the same finite TMJ collision and art tile layers supplied as the map artifact. It does not connect to Universe or claim live multiplayer, personal-area claimability, bots, conference services or audio isolation.

The full world remains 2496 × 1408 native pixels. The TMJ is 156 × 88 cells of 16px. Art is sliced into cells and packed losslessly with no resizing. The 32 × 32 Greg spritesheet is unchanged at scale 1. The source character body is 16 × 16 at x ±8, y through y +16, with immovable=true. The physics harness uses genuine Phaser tile collisions loaded from the TMJ. There are no preview-only rectangle bodies and no 32px rounding of table edges.

All below-character layers precede the source `floorLayer` marker. Selective foreground, glass, the calibrated overhead shade and labels follow it. The shade PNG already contains its intended low alpha; the runtime layer remains at alpha 1. The copied source depth primitive sets the character depth to y +16 and the foreground layers to 1,000,000. Collision is on a permanently visible, zero-opacity tile layer independent of visual foreground.

## Compile and plan

The frozen build uses `python runtime-work/compile_office.py --geometry-dir geometry-work/revision-03 --collision-full-canvas --final` from the office root. Running without these options defaults to provisional revision-02 geometry. An updated grid can be supplied with `--collision-grid`; use `--collision-full-canvas` only when that input already includes the 32px margin. Extra rectangles can be supplied with `--extra-obstacles`. The compiler rejects non-16px-aligned rectangles instead of rounding them. Use `--final` only after the map author confirms a source freeze.

Then run `python runtime-work/plan_routes.py`. It computes one continuous route visiting all 28 exact table contacts, then all 26 authored meeting, conference, reception and lounge positions (54 destinations total). It samples the unchanged body at every pixel along all compressed segments against the compiled collision grid. Final shared destination anchors may be specified in `runtime-work/shared-destinations.json` as objects with id, name and target{x,y}; these anchors are in translated final-world coordinates.

The compiler writes only compiled-work. The planner writes compiled-work/route-plan.json. Neither modifies source art or source geometry. Source hashes and lossless round-trip checks are recorded in compile-manifest.json.

## Browser-host route

On the cloud browser host, run `python3 ../universe-expanded-office/runtime-work/server.py --port 8846` through the visible desktop terminal. Open `http://127.0.0.1:8846/runtime-work/`. Do not substitute an exec-host loopback, tunnel, shell browser or security-setting change.

The server binds only to 127.0.0.1 and writes bounded PNG, JSON and WebM evidence under runtime-work/results. The full map is rendered in a 1024 × 704 camera at zoom 1. Native captures preserve that pixel scale. The short recording physically walks to Operations first, then records four exact contact stops and exits. Reset before running the complete continuous proof. The full proof visits all 54 furniture/reception goals, with no teleporting between them. Travel runs at 120px/s, exactly 2px per 60Hz physics step. Paths use 1px extra travel clearance where possible; the authored 16px sofa access uses the exact zero-clearance path. Final seat contacts remain exact. The first 96px/s trial accumulated fractional-coordinate rounding at a tangent wall turn; its failed report is retained under results/attempt-01-tangent-corner. The corrected harness changes only its test route and walk velocity, preserving source engine/body primitives and the real TMJ cells.

Static compilation and route planning are distinct from runtime QA. Do not call a source provisional compile a final geometry pass, or an offline route sweep a browser physics pass.

Run `python runtime-work/audit_captures.py` after browser verification to compare actual captured head pixels with the frozen layer stack. It distinguishes low-alpha shadow tint from forbidden hard foreground overlap and emits native (unscaled) tight crops.

## Verified result

The final cloud-browser run passed all91 assertions across54 continuous furniture/reception goals, including28 exact workbench contacts and6,953 recorded motion samples. No solid-tile overlap or runtime errors were recorded. The separate short walk passed17 assertions and records23.634seconds at1024×704 native resolution. The WebM master and H.264 MP4 are in results. All36 actual native screenshots pass the head/alpha audit: no hard foreground/glass/label head overlap;1,866 robustly measurable head pixels show the intended overhead shade; the maximum head RGB difference from the frozen reference composition is1channel level. All8 frozen source layers remained byte-identical.

See DELIVERY.json for hashes, scope and limitations.
