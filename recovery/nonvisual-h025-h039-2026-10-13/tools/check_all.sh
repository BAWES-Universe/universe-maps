#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python tools/recover_nonvisual.py
python tools/check_geometry.py
node tools/run_controller_checks.cjs H025
node tools/run_controller_checks.cjs H039
python tools/check_reproducibility.py
