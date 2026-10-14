#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p validation review map32
python tools/author-layout.py
python tools/author-floor.py
python tools/build.py
python tools/verify-whole-footprints.py
node tools/spawn.cjs "$PWD" "$PWD/tools/native-source"
node tools/trace.cjs "$PWD"
python tools/proof.py
python tools/verify-native-all.py
python tools/verify-floor.py
node tools/test-controller.cjs
node tools/test-transition.cjs
python tools/author-review.py
