# Gate reduced-motion visibility audit

Read-only native Tiled composition of the preserved Gate B source. No map, script, atlas or animation definition was changed.

`gate-reduced-static.png` composes the ordinary visible tile layers with every `reducedMotionHide` layer omitted. Pixel inspection confirms that the base art still contains the waterfall columns, cascades, pools and portal water. Reduced motion removes the moving overlays; it does not remove the underlying scenery. A report that waterfalls cannot be seen must distinguish camera cropping from absence of water motion.

This is an offline source render, not a browser or physical-device observation. It uses each animated tile’s first declared frame and does not simulate time. The normal-state comparison is a frame-zero source composition, not a timed browser frame. No conclusions about pacing, camera smoothness or audio follow from this audit.
