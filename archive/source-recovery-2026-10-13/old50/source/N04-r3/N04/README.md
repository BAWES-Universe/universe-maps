# Glassleaf Cooking Club

Host the complete map32 directory and load N04.wam in an editor-managed room. The companion defines default arrival; TMJ carries collision, default start, bounded quiet arrival, and ground/floorLayer/foreground.

Rebuild from the extracted archive root: python tools/build.py N04. Native arrival checks: node tools/native/arrival-audit.cjs N04. Dependencies: Python 3, Pillow; Node.js, bundled EasyStar.

Limits:
- Local authorable candidate, not live-tested or published.
- No gameplay, cooking, music, photography, video playback or activity integrations.
- No animation; fireplace and scenery are static.
- Standing repository frames in decoded proof; manually chosen display facings are not automatic seating.
- Collision is native32 tile-based; bounded object footprints are conservative at sprite margins.
- Pinned native source-extracted route tests are not a live browser, keyboard physics, conferencing or device test.
