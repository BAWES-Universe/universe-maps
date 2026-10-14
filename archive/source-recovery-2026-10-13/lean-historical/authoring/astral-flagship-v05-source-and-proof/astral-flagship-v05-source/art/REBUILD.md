# Portable art rebuild

From this folder's root, run:

    python art/build_roofless_garden.py

The script resolves all paths relative to itself, so it also works from another current directory. Install the versions in art/requirements.txt only if your Python environment lacks them. All source inputs, the exact imagegen prompt, untouched generated master and supplied reference image are included. Rebuilding does not invoke imagegen, a network service, browser or engine.

The script writes only this candidate's assets/source/review folders. It does not regenerate runtime collision or compile TMJ. The tools/compile_runtime.py performs runtime compilation; run its validation afterward.

Canopy lintels/slats remain below actors. Only safe central column/stool strips remain in the above layer. Full source art is retained before splitting at source/pergola-authored-structure.png.

Review-board rendering also uses the standard DejaVu Sans font files at /usr/share/fonts/truetype/dejavu/. Native runtime images are supplied prebuilt.
