# Astral Concourse: Flagship v03

A separate flagship variation with a deep indoor foyer, four lounge meeting squares and a right-side coffee terrace overlooking gardens. The original giant stage and all 210 audience chairs are preserved. Both former decorative foyer mirrors are removed.

**Separate versioned static A/B preview. Actual room setup remains pending.** No engine changes, live-room edits, media-service setup, purchases or background audio are included.

## What is here

- `map32/grand-auditorium.tmj`: finite 80×60 tile map, native 32px tiles, 2560×1920 world. Five atlas images, collision marker and a transparent non-colliding quiet marker are local dependencies.
- `map32/grand-auditorium.wam`: portable schema-valid area candidate, with independent auditorium podium/audience and four distinct native meeting-room names. Relative map URL supports standalone serving, but must not replace an actual room's stored absolute map URL.
- `integration/ROOM-SETUP.md`: safe native editor steps, exact rectangles, feature-flag caveat, Custom TMJ behavior, backup/reset/import warnings and live acceptance checklist.
- `SOURCE-PROVENANCE.md`: exact complete-source archive identity, provenance and rebuild instructions. The large source archive is delivered separately to the owner.
- Review images and native occupied close-ups are in the separately delivered complete-source archive.
- `validation/package-verification.json`: the final offline package report. Detailed source-matched movement, geometry and independent zone evidence is in the complete-source archive. These are not browser/network/media/load tests.
- `RUNTIME-MANIFEST.json` and `tools/verify_runtime_manifest.py`: exact portable runtime identity and standalone dependency/hash validation.

Counts are 210 auditorium seats, 16 lounge resting places and 8 casual resting places. They do not establish supported concurrent users or a native seated-state interaction. Coffee is a solid illustrated counter with a clear approach; there is no pretend purchase flow. The garden beyond the closed terrace railing is scenery, not an extra walkable route.

## Conversation areas

Four visibly grouped rugs are intended for native **Video call / Meeting Room** areas. Each companion room name is distinct. Successfully joined participants share that square's native space regardless of their distance inside it. Casual pairs lie outside those areas and the quiet path,56px apart against the known64px source proximity-start default. Actual deployment settings, user availability, permissions and live behavior remain unverified; these are not private-audio guarantees.

One transparent nonzero TMJ tile layer owns silence for the arrival spine, hall approaches and cross-concourse. It deliberately does not cover conversation seating. Native tile membership is player x/y; WAM membership is player x/y+16. The package does not overlap a silent WAM rectangle onto the foyer.

Low planted bay edges make the lounge squares intentional destinations while leaving broad entrances onto the shared concourse. Their collision is visible, rather than an invisible obstacle or silence over meeting areas. Automatic click routes are tested separately from fixed anchor membership.

## URLs and standalone verification

- [TMJ preview](https://bawes-universe.github.io/universe-maps/astral-concourse/v03/flagship/map32/grand-auditorium.tmj)
- [Companion WAM candidate](https://bawes-universe.github.io/universe-maps/astral-concourse/v03/flagship/map32/grand-auditorium.wam)
- [Original v01 TMJ](https://bawes-universe.github.io/universe-maps/astral-concourse/v01/flagship/map32/grand-auditorium.tmj)

Run `python tools/verify_runtime_manifest.py` from this package to check all nine frozen files, hashes, relative references and native tile dimensions. Full art rebuild and offline movement replay use the separate source backup described in [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md).

The adjacent WAM is a portable setup candidate. Loading the Custom TMJ does not import its areas into an actual room. See [ROOM-SETUP.md](integration/ROOM-SETUP.md) before activation. Publishing these static assets does not create a room or enable live media.

## Provenance and limits

The new lounge furniture, rugs, plants, welcome desk, garden scenery, pergola, railings and low bay dividers were generated for this project using the built-in image tool, then registered into native-scale components. Existing hall/chair/podium art and café components are reused project-authored assets. No Conference Campus pixels are redistributed, and no new CC0 or other licence is invented.

Greg Gulf-outfitv3 is the unchanged project-authored native-scale review fixture, SHA256e88ba016c58f6bc7616c831c3c56a4656e66772794940af93c0c0835e85a987d. It is not an upstream WorkAdventure sprite and is not included in the runtime dependency closure. Original portrait inputs are not in this package.

The current source-matched adapter was checked against engine commit b1ca7023fd1d8ddbb20911e5a6234ad5d0bd30af. Source default WOKA_SPEED is9; deployed overrides remain unknown. Offline movement and pixel-depth checks do not substitute for local/remote avatar rendering, multi-user media transitions or load acceptance.

Original authored furniture records: [civic project provenance](https://github.com/BAWES-Universe/universe-maps/blob/03d83f2/map-mocks/civic-rooms-01/source/provenance.json), [chair generation record](https://github.com/BAWES-Universe/universe-maps/blob/03d83f2/map-mocks/expanded-office-02/source/frozen-review-package/art-meeting/source/generation-record.json). [Greg reference provenance](https://github.com/BAWES-Universe/universe-ai-creator-kit/blob/67382dc97f494c230e93f0cf67e478df6e5b6d17/docs/catalogue/wokas.md#reference-greg32-map-fixture).
