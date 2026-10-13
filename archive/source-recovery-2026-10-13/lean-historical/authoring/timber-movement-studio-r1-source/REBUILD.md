# Rebuild Timber Movement Studio r1

Requirements: Python 3 with Pillow and NumPy; Node.js. These are already available in the task environment.

From this package root:

1. python tools/build_movement.py
2. node tools/verify_native_routes.cjs timber-movement-studio-r1
3. python tools/check_head_geometry.py timber-movement-studio-r1

Step 1 writes the native TMJ/WAM/atlas, source layers/layout and static occupied review images. Step 2 replays pinned unmodified native path methods in a portable stub scene, including every admitted floor cell, target offsets, exact authored arrivals, returns and sequential destinations. Step 3 independently decodes the actual TMJ and checks all clear integer body positions against the frozen varied-Woka upper-head union. These are source/static checks, not a live browser test.

The proof overlay and head mask are derived from unchanged native repository Wokas, with sheet hashes, frames, positions and source pin in source-assets/WOKA-PROOF.json. Standalone Pipoya sheets are excluded. Rebuilding the fixed proof needs only this included composed overlay; reauthoring actor poses or independently regenerating the head union requires the original licensed local repository assets. They are not runtime dependencies.

The original 1536×1024 Movement concept is uniformly reduced to 768×512, without stretching or interior editing. The existing 1536×192 Timber north-context strip is uniformly reduced to 768×96. Source artwork and semantic layouts are preserved; the layer split changes no empty-scene pixels.

This package does not update old maps, install software, contact services, publish or activate integrations. Preserve all third-party notices. See ASSET-PROVENANCE.md and licenses/.
