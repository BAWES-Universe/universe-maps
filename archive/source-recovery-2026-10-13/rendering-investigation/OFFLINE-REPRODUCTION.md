# Reproduce the offline evidence

Browser fixture startup requires only Python 3 and an actual browser on the same authorized computer. Everything it loads is bundled under `fixture/`, including exact Phaser 3.86.0; no package installation, account, service or deployment is needed.

From the unzipped package root:

```sh
cd fixture
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/` in that computer's browser. Review `fixture/README.md` first. Stop the server with Ctrl-C when finished. This does not start a complete WorkAdventure server. The frozen map WAM/script behavior is not executed.

For optional regeneration of CPU evidence, place a checkout of BAWES-Universe/workadventure-universe at this package root's `repo/`, pinned to `adc13cffd4e57aca6bc0353ad108bba423c61de1`, and install its lockfile dependencies in an authorized development environment. The supplied script reads HdpiManager from that checkout and Phaser 3.86.0 / TypeScript / @napi-rs/canvas from its node_modules. Run `node render-offline.cjs` from the package root. The output is CPU reconstruction only, not browser acceptance. Source asset hashes are bundled in fixture/ASSET-SHA256.txt and the evidence JSON.

The GitHub draft PR is separate from the quality fixture: issue #841, PR #842, head44dda03e5108b6cd257ce8a3cdeb9630edb8d908. It changes only camera-resize handling and tests. No quality flag, source-art upscaling, global smoothing, deployment or room change is included.
