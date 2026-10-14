# Saltwind Performance Courtyard r1

Original Event Room visual proposal for performances and shared listening. This is a design review only, not a runnable map or published template. No earlier map was modified.

- Concept image: Saltwind-Performance-r1-concept.png
- Compact two-page review: Saltwind-Performance-r1-review.pdf
- Native32 standing-avatar reference provenance: scale-reference.json
- Generated with the built-in image_gen tool.
- Raster concept: 1536 x 1024. Proposed native composition: 768 x 512, 24 x 16 cells. This is a design target, not a grid-validated asset.
- Native32 Woka frames come from the existing project cache. They are placed only in the PDF scale study, not in the clean concept image.

Before implementation: widen/snap aisle clearances, reconcile diagonal ramp with orthogonal movement, verify visible collision at shore/planted edges, split foreground architecture and foliage, test real occupied routes and bench approaches. Stage audio, hosting, broadcast and media remain unconfigured. The piano and microphone stands are scenery, not implemented activities.

The first image generation was rejected for camera perspective drift. The selected concept uses the higher orthogonal game-map camera with no sky or vanishing point.

Rebuild: install ReportLab from PyPI, then run python rebuild_review.py. The PDF is reproducible from the frozen composed review-page PNGs. The original image prompt is recorded, but generative reruns are not deterministic. Composed proof pages contain standing avatar samples only; no raw character sheets or separately reusable character sprites are bundled. The earlier report-generation script is intentionally excluded.
