#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p runtime review validation
python tools/build.py > validation/build-log.txt
node tools/spawn.cjs "$PWD" "$PWD/tools/native-source" > validation/spawn-log.txt
node tools/trace.cjs > validation/route-log.txt
python tools/test-geometry.py > validation/full-floor-log.txt
node tools/test-controller.cjs > validation/interaction-log.txt
node tools/regression-probe.cjs tools/regression-adapter.cjs validation/common-interaction-regressions.json > validation/common-interaction-log.txt
node tools/test-transition.cjs "$PWD" validation/transition.json > validation/transition-log.txt
python tools/proof.py
python tools/extended-proof.py > validation/full-width-log.txt
python tools/make-spec.py
python tools/run-native-extrema.py > validation/extrema-log.txt
python tools/source-contract.py > validation/source-contract-log.txt
