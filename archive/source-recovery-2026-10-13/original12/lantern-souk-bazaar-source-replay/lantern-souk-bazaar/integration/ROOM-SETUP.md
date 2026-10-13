# Safe setup

1. Create a new review room; do not replace an existing production room. Serve the complete map32 closure at one origin with relative PNG paths preserved.
2. Choose the TMJ as Custom TMJ. This produces a room-specific WAM and does not import the companion WAM automatically. Keep the real room mapUrl and any existing areas unless deliberately migrating them with backup.
3. The Tiled start rectangle is32×32, with native margin16 selecting its center. The WAM receiver is8×8 and remains fully inside that same silent tile (WAM has no native margin). Only the center tile is silent. No broad social silence, scripts, focus zones, proximity-radius overrides or runtime visibility changes are installed.
4. Companion WAM areas without properties are named editor placeholders, not activated capabilities. Add and test native meeting/media/website/portal properties through supported room editing after choosing destinations and services. Do not enter fake URLs or credentials.
5. Portal links, bots, ecommerce, Imagine and ImagineMusic need real configuration and relevant user permission. This package does not provision or imply those services.
6. Test the arrival, every doorway/bridge in both directions, every seat approach/exit, mobile touch, viewport changes and multi-user communication in the actual deployment before production use.
7. Keep the original source/manifest. Publication and live URL verification remain separate release steps.
