# Map mock archive

Every recoverable design has its own folder with a representative image, editable source where it exists, local assets, and a status note. These are preserved for iteration and future space-template selection. Rejected main-map directions are intentionally retained.

**13 design folders: 10 Tiled candidates and 3 visual-only proposals.** The archive does not populate the live template list or deploy any candidate. All candidates remain `catalogReady: false` until selected, refined and tested. Existing published maps remain at their original paths.

## Browse candidates

| Candidate | Preview | Source | Status |
|---|---|---|---|
| [Butterfly Campus · dark interior version](./butterfly-campus-v3-dark/README.md) | [Image](./butterfly-campus-v3-dark/screenshot.png) | [TMJ](./butterfly-campus-v3-dark/map/butterfly-campus.tmj) | rejected-main-direction-preserved |
| [Butterfly Campus · light sandstone version](./butterfly-campus-v3-light/README.md) | [Image](./butterfly-campus-v3-light/screenshot.png) | [TMJ](./butterfly-campus-v3-light/map/butterfly-campus.tmj) | experimental |
| [Butterfly Gate · monumental journey revision](./butterfly-gate-journey/README.md) | [Image](./butterfly-gate-journey/screenshot.png) | [TMJ](./butterfly-gate-journey/map/butterfly-campus.tmj) | experimental |
| [Butterfly Town · frozen v1](./butterfly-town-v1/README.md) | [Image](./butterfly-town-v1/screenshot.png) | [TMJ](./butterfly-town-v1/map/butterfly-town.tmj) | historical-published-source |
| [Butterfly Town · scenery and water v2](./butterfly-town-v2/README.md) | [Image](./butterfly-town-v2/screenshot.png) | [TMJ](./butterfly-town-v2/map/butterfly-town.tmj) | experimental |
| [Lantern Courtyard · original mock](./lantern-courtyard-01-original/README.md) | [Image](./lantern-courtyard-01-original/screenshot.png) | [TMJ](./lantern-courtyard-01-original/map/lantern-courtyard.tmj) | experimental |
| [Lantern Courtyard · depth proof](./lantern-courtyard-02-depth/README.md) | [Image](./lantern-courtyard-02-depth/screenshot.png) | [TMJ](./lantern-courtyard-02-depth/map/lantern-courtyard.tmj) | experimental |
| [Lantern Courtyard · aligned olive beds](./lantern-courtyard-03-aligned/README.md) | [Image](./lantern-courtyard-03-aligned/screenshot.jpg) | [TMJ](./lantern-courtyard-03-aligned/map/lantern-courtyard.tmj) | experimental |
| [StudentHub · connected glass workplace proof](./studenthub-connected-glass-proof/README.md) | [Image](./studenthub-connected-glass-proof/screenshot.png) | [TMJ](./studenthub-connected-glass-proof/map/studenthub-proof.tmj) | rejected-mechanism-proof-preserved |
| [StudentHub · first interior composition](./studenthub-interior-01-prototype/README.md) | [Image](./studenthub-interior-01-prototype/screenshot.png) | Visual compositor; no TMJ | visual-only-preserved |
| [StudentHub · refined dark composition](./studenthub-interior-02-refined-dark/README.md) | [Image](./studenthub-interior-02-refined-dark/screenshot.png) | Visual compositor; no TMJ | visual-only-preserved |
| [StudentHub · light sandstone room proposal](./studenthub-interior-03-light/README.md) | [Image](./studenthub-interior-03-light/screenshot.png) | Visual compositor; no TMJ | visual-only-preserved |
| [StudentHub · roofless outdoor office](./studenthub-roofless-outdoor-office/README.md) | [Image](./studenthub-roofless-outdoor-office/screenshot.png) | [TMJ](./studenthub-roofless-outdoor-office/map/studenthub-outdoor-office.tmj) | future-template-candidate |

## What is preserved

- Original, depth-corrected and olive-aligned Lantern Courtyard versions
- Frozen Butterfly Town v1 and the completed v2 scenery/water revision
- Dark and light full campus snapshots, plus the monumental gate-journey revision
- Connected glass workplace proof and its separate roofless outdoor-office derivative
- First, refined dark, and light standalone StudentHub interior visual proposals

The three visual proposals have Python compositor sources and their required local art inputs. They never had importable TMJs; none has been invented. The roofless template also includes its portable source generator. Other maps are editable directly in Tiled using their included PNG assets; the full large source-review/video bundles are not duplicated here.

A partial pre-water v2 technical checkpoint is retained under `butterfly-town-v2/history/` with an explicit incomplete-assets warning. It is not a standalone template or part of the candidate catalog. Duplicate build copies, dependencies, videos and temporary test artifacts are omitted.

## Known limits

- The original connected-glass proof contains an unintended `silent: true` area that disables proximity conversations. Its defect is preserved and prominently flagged. The roofless derivative removes that property.
- Both StudentHub TMJs preserve three area objects without explicit visibility booleans. The repository’s pinned import schema rejects them; normalize a separately named derivative before publishing.
- The dark campus has a historical return-portal overlap and an unaccepted interior direction.
- Historical screenshots/compositions and source-harness checks do not establish full Universe, current-engine, multiplayer or physical-device acceptance. Native meetings, bots, account links and live catalog integration are not enabled.
- Ambient water audio remains deployment-gated in relevant candidates. Quiet ambience must not be implemented by disabling people's conversation.
- WAM hosting references were made relative for safe local reuse. TMJ bytes remain unchanged from their canonical snapshots.

## Verify and iterate

Run `python3 map-mocks/tools/validate.py` from the repository root. Each candidate has `template.json` for future catalog use and `SHA256SUMS.txt` for file integrity. The root `catalog.json` is an archive index only.

Copy a candidate into a new named folder to iterate; preserve its source snapshot. Keep the complete `map/` folder together. Read the candidate README and provenance notices before reuse. Promote a candidate to the live template list only after explicit selection and complete runtime acceptance.

`vite.config.ts` uses `map-discovery.ts` to skip only the repository-root `map-mocks/` directory before reading any archived maps. The published build input list is unchanged by this archive. No map or asset under existing published paths is edited.
