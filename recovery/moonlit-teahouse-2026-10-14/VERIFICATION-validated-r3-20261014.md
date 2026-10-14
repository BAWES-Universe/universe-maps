# Moonlit validated-r3 verification — 2026-10-14

New recovery subtree: validated-r3/. Baseline sealed-r2 is preserved.

Source baseline: universe-maps 6db977fcb576be429e1c147f59226f62641efae7; engine aa3ca1d60801172bfd97b6619bbf351c17eb3dba. Runtime controller SHA-256: 1692831cd58e13238c3bb2023119cf4f841120752cfd4e4f3352206ce1c95546. Map SHA-256: 3ea059084a3d84352302a8d9d0d139444d4c79622b98b8a8cead5d4903500d7c.

Two map-side fixes: browser-global timer wrappers, and supported explicit menu keys matching labels so this engine's natural iframe-close cleanup removes them. No engine source edits.

Actual Chromium: 28 final journey checks passed, including roofs, single-client demo door frames/collision, timed camera return, natural departure/rejoin with zero stale menus, routes, water and audio. Source/model checks: 17 existing controller tests, 2 new regressions, 25 structure checks and 41 adaptor route cases passed. Both new regressions fail against unchanged r2. Original seal: all 47 entries verified unchanged. See validated-r3/REPORT.md for controls, harness corrections and limitations.

This compact recovery backup includes exact candidate source/runtime, regressions, reports, manifests, logs, result JSON, sampled timelines and screenshots. Large trace ZIPs/caches are excluded as documented in BACKUP-README.md. No secrets, deployments or releases are intended. BACKUP-MANIFEST.sha256 is the compact subtree inventory. The operation verifies uploaded Git blob IDs and SHA-256 bytes before reporting the exact commit.
