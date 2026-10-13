# Rebuild and verify

Requirements: Python3, Pillow and NumPy. No network access, raw engine source, original repository, generated images service or absolute input path is required.

Run from any directory:

    python tools/rebuild.py

The build creates timber-mixed-six-mat-instructor-facing-r4/ from baseline/ and source-assets/. It verifies the frozen accepted r3 input hashes, preserves existing packed atlases and GIDs, packs the outside-only border, translates geometry, creates the new outdoor landing and quiet start, and decodes the actual runtime TMJ for empty/occupied reviews.

The geometry verifier independently decodes TMJ atlases and collision properties. It verifies preservation, every old anchor and role, one quiet start cell, all1024 conservative startup rectangle integer positions, cardinal connectivity, runtime proof reconstruction and exhaustive reachable body/head geometry. It also verifies the three unscaled outdoor crops against the retained compiled native32 actor overlay.

The native movement report is immutable captured evidence from a fresh4,420-route run. The compact package does not contain raw native engine or the optional runner. The rebuild checks every native report input hash before restoring the report; it never pretends to execute absent engine code. If map/layout/start capture changes, evidence attachment fails and fresh native replay is required. Startup semantics are transparently inherited from a hash-pinned authentic capture, not freshly rerun.

Finally EXPECTED-OUTPUTS.json checks every generated runtime file byte-for-byte. A clean extraction rebuild was also performed before freezing delivery. See GUIDE.md for remaining live-test and user-approval gates.
