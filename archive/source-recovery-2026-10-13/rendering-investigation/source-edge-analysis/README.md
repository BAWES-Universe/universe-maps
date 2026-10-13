# Conditional cutout-alpha test — CPU model only

Both current maps use complementary binary-alpha base and foreground masks. The bundled planes are native world-coordinate reconstructions of the frozen TMJ/PNG assets in `../fixture/assets/`. Reading base holes cover2,160 world pixels; Studio base holes cover37,755. Every hole is exactly filled by foreground in native source composition. There is no pre-existing partial-alpha fringe in these PNGs.

Run `python3 -m pip install -r requirements.txt` in an authorized Python environment, then `python3 linear_cutout_model.py` from this directory. This uses pinned Pillow and NumPy. It regenerates the JSON and four enlarged proof crops. No external account/service is contacted by the script itself.

The model samples each complete, premultiplied layer at a half-pixel offset, then composites foreground over base. It excludes atlas contamination, GPU rasterization and browser scaling. When each layer’s interpolated alpha is0.5, foreground-over-base coverage is0.75, leaving25% background contribution. Adding atlas gutters alone cannot address this coverage mechanism.

- Reading example world point(462.5,309.5), tile(14,9): coverage0.75.
- Studio example world point(269.5,571.5), tile(8,17): coverage0.8125.
- This particular model contains775 Reading and2,507 Studio nonopaque samples; both reach minimum0.75 coverage.

The `independent` crop demonstrates the conditional effect. `composite-first` is a mathematical reference, not a proposed renderer change: flattening the foreground would lose Woka occlusion. A production solution must preserve foreground depth/occlusion and validate actual Canvas/WebGL behavior.

This does NOT establish the cause of the original black-edge complaint. Dark source contours, prior baked Studio r7 copy bands, packed-atlas bleed, quad gaps and post-composite pixelation are separate mechanisms. The existing r8 source repairs are unchanged.
