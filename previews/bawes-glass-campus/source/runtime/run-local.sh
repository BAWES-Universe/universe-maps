#!/usr/bin/env bash
set -euo pipefail
# Uses installed dependencies at the pinned engine revision; never deploys.
BAWES_ENGINE_ROOT="${BAWES_ENGINE_ROOT:-/workspace/workadventure-universe}"
BAWES_NODE_BIN="${BAWES_NODE_BIN:-/workspace/onboarding/toolchain/node_modules/node/bin/node}"
BAWES_RUN_DIR="${BAWES_RUN_DIR:-/workspace/bawes-runtime}"
BAWES_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$BAWES_RUN_DIR"
if [[ "$(git -C "$BAWES_ENGINE_ROOT" rev-parse HEAD)" != 274114560c5ec95fdf8e51e67986a53069f3cf06 ]]; then
    echo 'Use the recorded engine revision before reproducing these checks.' >&2
    exit 1
fi
# Workaround for the installed workspace layout, confined to ignored dependencies.
if [[ ! -e "$BAWES_ENGINE_ROOT/node_modules/sass" ]]; then
    ln -s ../play/node_modules/sass "$BAWES_ENGINE_ROOT/node_modules/sass"
fi
python3 - "$BAWES_ENGINE_ROOT" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])/'play'
s=(p/'vite.config.mts').read_text()
s=s.replace('import { sveltePreprocess } from "svelte-preprocess";', 'import sveltePreprocess from "svelte-preprocess";')
s=s.replace('clientPort: 80', 'clientPort: 8080')
(p/'bawes-local.vite.mts').write_text(s)
PY
pids=()
cleanup() { for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done; }
trap cleanup EXIT INT TERM
(
    cd "$BAWES_ENGINE_ROOT/back"
    exec env PLAY_URL=http://localhost:8000 ENABLE_TELEMETRY=false HTTP_PORT=8082 GRPC_PORT=50051 \
        "$BAWES_NODE_BIN" ../node_modules/tsx/dist/cli.mjs src/server.ts
) > "$BAWES_RUN_DIR/back.log" 2>&1 & pids+=("$!")
(
    cd "$BAWES_ENGINE_ROOT/play"
    exec env SECRET_KEY=bawes-local-synthetic-only MAP_STORAGE_API_TOKEN=local-unused API_URL=localhost:50051 \
        PUSHER_HTTP_PORT=8000 PUSHER_WS_PORT=8001 PUSHER_URL=http://localhost:8000 WS_URL=http://localhost:8001 \
        FRONT_URL=http://localhost:8000 VITE_URL=http://localhost:8080 UPLOADER_URL='' ICON_URL='' \
        START_ROOM_URL=/_/global/localhost:8090/campus.tmj DISABLE_ANONYMOUS=false ENABLE_CHAT=false \
        ENABLE_MAP_EDITOR=false ALLOWED_CORS_ORIGIN='*' TSX_TSCONFIG_PATH=tsconfig-pusher.json \
        "$BAWES_NODE_BIN" ../node_modules/tsx/dist/cli.mjs src/server.ts
) > "$BAWES_RUN_DIR/pusher.log" 2>&1 & pids+=("$!")
(
    cd "$BAWES_ENGINE_ROOT/play"
    exec env DISABLE_LEGACY_BROWSERS=true "$BAWES_NODE_BIN" node_modules/vite/bin/vite.js --config bawes-local.vite.mts
) > "$BAWES_RUN_DIR/front.log" 2>&1 & pids+=("$!")
python3 "$BAWES_SCRIPT_DIR/serve-map.py" > "$BAWES_RUN_DIR/maps.log" 2>&1 & pids+=("$!")
echo 'Local game: http://localhost:8000/_/global/localhost:8090/campus.tmj'
wait
