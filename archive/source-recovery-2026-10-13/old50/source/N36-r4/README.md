# Desert Caravan Crossroads

Saffron stone, lapis textiles, teal domes and oasis crossroads

- Local candidate; independent review and live browser/gameplay pending.
- Standing native32 Woka proofs; benches have approach anchors, no sitting animation.
- No live services, automated event, transport or puzzle mechanics configured.
- Areas are editor-ready metadata, with no broadcast/audio configuration.

Host complete map32 folder. Runtime uses native32 orthogonal TMJ and WAM without external dependencies. Rebuild: python tools/build_one.py desert-caravan-crossroads from source archive root. Python3, Pillow, NumPy; Node24 for source-extracted native checks.

Lesson: An actual imagegen repair removed obstructing corral clutter instead of repeatedly moving an anchor onto nearby objects. Clear visual approaches are now authored explicitly.
