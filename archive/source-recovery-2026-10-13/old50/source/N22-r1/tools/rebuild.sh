#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
python "$ROOT/tools/build.py"
node "$ROOT/tools/spawn.cjs" "$ROOT" "$ROOT/tools/native-source"
node "$ROOT/tools/trace.cjs" "$ROOT"
python "$ROOT/tools/proof.py"
