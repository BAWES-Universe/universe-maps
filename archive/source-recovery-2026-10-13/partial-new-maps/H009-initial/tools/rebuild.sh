#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python tools/define-layout.py
python tools/build.py
node --check runtime/mechanical-orchard.js
node --test tests/interaction.cjs > evidence/interaction-tests.txt
node tests/transition-contract.cjs > evidence/transition-contract-tests.txt
python tests/structure.py > evidence/structure-tests.txt
python tests/model-geometry.py > evidence/model-geometry-tests.txt
python tests/physical-footprints.py > evidence/physical-footprints-tests.txt
node tests/spawn.cjs > evidence/spawn-tests.txt
node tests/native/routes.cjs > evidence/native-tests.txt
node tests/native/coverage.cjs > evidence/native-coverage-tests.txt
python tools/render.py
python tests/seat-contact.py > evidence/seat-contact-tests.txt
python tests/head-audit.py > evidence/head-audit-tests.txt
python tests/static-scales.py > evidence/static-scales-tests.txt
python tests/six-scale-states.py > evidence/six-scale-states-tests.txt
# Intentionally remains red until the real full-width aisles are repaired.
python tests/full-floor.py > evidence/full-floor-tests.txt
