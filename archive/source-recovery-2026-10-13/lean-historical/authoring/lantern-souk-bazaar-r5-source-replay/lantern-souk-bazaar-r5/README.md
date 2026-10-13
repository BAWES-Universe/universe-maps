# Lantern Souk Bazaar r5

Original unlabelled court preserved, opposing east/west seats at the rug table, and expanded city panorama. Native tile size 32; canvas 1920x1280. Exactly two seats.

Runtime: serve map32/ as a relative closure. Select lantern-souk-bazaar-r5.tmj in a separate review room. Companion WAM is not auto-imported by Custom TMJ. No external services configured. Only the spawn tile is silent. Decorative outer city/sky is intentionally non-walkable. The new court is translated 192px east/south with unchanged native scale.

Rebuild from source ZIP root with Python3 + Pillow + NumPy and Node:

python tools/revise_souk.py
python tools/check_spawn_and_boundaries.py lantern-souk-bazaar-r5
node tools/native/route-audit.cjs lantern-souk-bazaar-r5

Optional occupied-proof regeneration requires an existing licensed WorkAdventure repository checkout: set SOUK_WOKA_REPO to its root, then python tools/render_seating_proof.py. Raw third-party Woka sheets are excluded; composited proof images are included. Runtime rebuild needs no Woka download. Pipoya permits use/edit in games and other productions but prohibits asset redistribution; see the official attribution link in PROVENANCE.md. Optional report regeneration requires reportlab: python tools/create_review_pdf.py. Package with python tools/package_revision.py. No paid API or remote asset is required for rebuild. Bundled generated panorama is used only outside the locked original court.

Validation is source-native replay plus static visual/geometry checks, not live Phaser/browser/keyboard/mobile/network/audio or real multi-user testing. Repo Wokas are review fixtures, excluded from runtime. Earlier optional motion-r01 is unchanged and belongs to the earlier coordinate layout; do not overlay it on r5. This revision is static. No publication, engine changes, bot, checkout, live audio, or market service is included.
