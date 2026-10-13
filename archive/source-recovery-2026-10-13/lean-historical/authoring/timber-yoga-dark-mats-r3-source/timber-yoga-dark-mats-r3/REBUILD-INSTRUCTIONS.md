# Yoga dark mats r3 - compact source

Run `python tools/build_dark_mats.py`. This deterministically rebuilds the map artwork, runtime, layout, occupied proof and preservation report. Run `python tools/check_head_geometry.py timber-yoga-dark-mats-r3` and then `cp geometry-checks/timber-yoga-dark-mats-r3/independent-checks.json timber-yoga-dark-mats-r3/HEAD-GEOMETRY.json` to install the fresh geometry result. Python 3, Pillow and NumPy are required. No network, generation, secrets, paid service or engine modification.

EXPECTED-FREEZE.json records the full frozen file hashes. All generated outputs, including fresh HEAD-GEOMETRY.json, rebuild byte-exactly. NATIVE-ROUTES.json is supplemental evidence from the separately executed pinned native movement fixture, not a generated output of this compact bundle. The report records the exact engine commit, input hashes and scope. Full native test engine code and runner are deliberately excluded from distribution; ignore the full-suite native runner command in the generated GUIDE when using this compact bundle.

Inputs are frozen previous runtime atlases, previous layout and a composited occupied proof, plus 13 exact floor-restoration patches. The new mat material is deterministic source-owned sprite code. There are no raw avatar sheets. Prior input atlas bytes, geometry and WAM remain exact.

This is a separate unpublished review direction, pending user approval and live tests. Compiled previews are not browser screenshots or a deployed room.
