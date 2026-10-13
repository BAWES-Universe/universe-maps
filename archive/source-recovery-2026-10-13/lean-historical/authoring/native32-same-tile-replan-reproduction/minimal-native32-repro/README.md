# Native32 same-tile replan reproduction

Run with Node.js18 or later: `node minimal-32px-fixture.cjs`.

No dependency installation, network, map art, engine change or live client is required. This fixture uses an8×8 native32 grid, exact source-extracted engine methods pinned to b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af, and EasyStar0.4.4. Rendering, body services and the async timer clock are stubbed explicitly. `extracted-current-source.cjs` is the verified transpilation of pinned methods, not a proposed fix. The adapter paths alone were made portable.

The fixture succeeds when it REPRODUCES the BUG: one decorative hide changes a requested sprite endpoint from(80,128) to(80,96). Two no-visibility baseline cases reproduce the same-cell nearest-tile fallback. JSON results are written beside the fixture. Successful process exit is evidence of reproduction, not map release acceptance.

See source-method-manifest.json for exact method hashes and the source-pinned issue description in the containing checkpoint. No engine PR or deployed behavior is claimed.
