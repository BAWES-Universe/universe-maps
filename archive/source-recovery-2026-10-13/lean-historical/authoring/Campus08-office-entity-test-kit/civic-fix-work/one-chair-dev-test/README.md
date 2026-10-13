# One original chair back: authorized dev-test preparation only

Ready file: **civic-audience-backrest-native.png**, 28×20 pixels, transparent PNG, scale1. It is the original chair's above-player backrest component, not a redesigned full chair. The existing below-player furniture image contains the other chair pixels. All 24 audience backrest crops are RGBA-identical, so one prefab can eventually represent them; only this single test asset was prepared.

The asset is an exact crop of civic foreground `[131,819,159,839)` with no pixel edits, resize, or padding. SHA256: `8a5c0e246bf4a3ed953e1818da7637b9de08c1e1a7357c10121db944180d2fde`.

## Exact native import settings

Use the actual room's authorized Entity editor / Add your own upload route, choose this PNG, enable **Floating Object**, choose **Custom** depth, and set the positive UI selector to **6**. The stored prefab must have `depthOffset: -6` and no `collisionGrid`. Use native size, with no scaling.

There is **no mandatory32px padding** on this floating image. At pinned f00b, `UploadGuide.svelte:78–81` computes a32px-fit suggestion, but upload `:86–105` transmits the original file bytes, and the upload button `:286` is disabled only while naturalWidth is zero. The renderer loads the image at its actual dimensions. Padding would change its depth calculation and is neither needed nor supplied here.

The upload UI generates the actual prefab ID, image filename, and world-scoped asset reference. Record those returned values; do not assume the illustrative file-based prefab ID in example-collection.json will be assigned by editor upload.

## Placement and depth recipe

For a seated player origin `(X,Y)`, set the entity's final **top-left** to `(X−13,Y+3)`. Its28×20 image and depthOffset−6 yield depth `Y+17`; local Player depth is `Y+16` at the seat. These are final WAM top-left coordinates, not an assumed pointer-click coordinate.

Original attendee-1 position:

- Player origin `(144,1952)` in current campus world coordinates
- Entity top-left `(131,1955)`
- Entity native size28×20; depthOffset−6; resulting depth1969
- Local seated-player depth1968

Illustrative clear-floor render test, only after verifying that the test room rectangle is actually clear:

- Player origin `(320,320)`
- Entity top-left `(307,323)`
- Entity depth337; seated local-player depth336
- Move south and north across the sprite and verify the existing engine depth order changes. This alone tests rendering, not physical chair access.

## Separate physical collision acceptance

A Floating Object supplies **no physical blocking**. A clear-floor placement alone does not prove rear-foot collision, seating access, or native tap route acceptance.

For the original campus chair test variant, retain the existing below-player chair artwork and add/retain the fixed16px rear-foot rectangle world `(128,1968,32,16)`. This is grid cells `(8,123)` and `(9,123)` for the16px map. The seated native body at `(144,1952)` occupies x136–151, y1952–1967 and remains clear. These cells are backed by the full original chair base/back pixels, with no extra empty rear strip.

If the complete original chair/base scene is translated to the illustrative seat `(320,320)`, the corresponding foot rectangle is `(304,336,32,16)`, grid cells `(19,21)` and `(20,21)`. The isolated backrest PNG does not include that full base artwork or create these cells. A physical test needs an authorized isolated map variant with the base and the permanent cells; do not infer physical acceptance from the render-only clear-floor test.

The existing engine's runtime entity grids also use actual map tiles, but its upload collision editor and initial colliding-object snapping assume32px. Floating visual backrest plus independently authored permanent16px Tiled collision is the supported arrangement that avoids this UI mismatch.

## Avoid duplicate fixed drawing

When testing at the original campus chair, remove **exactly the backrest source foreground rectangle `[131,819,159,839)`** from the separate companion test variant and all derived fixed above-layer atlases. In world pixels that is `[131,1955,159,1975)`. Keep the below-player furniture pixels. The above layer is fixed at depth1,000,000, so leaving the original backrest there would still cover the player's head regardless of the entity's depth.

The candidate TMJ-only package was not changed and must remain preserved. Testing on verified clear floor avoids a duplicate baked-backrest problem, but is only the limited render test described above.

## Acceptance limits to check in the actual room

1. Confirm saved image28×20 and scale1; exact native pixels with transparency.
2. Confirm local seated torso remains behind the original backrest and protected head is clear.
3. Confirm local movement on both sides uses the expected depth change.
4. For physical acceptance, confirm the exact permanent16px foot cells, lateral seat access, collision-free native tap paths, and reverse exits.
5. Test another client. At pinned f00b, local Player uses depth `y+16`, but RemotePlayer.updatePosition uses `y`. This known discrepancy can still obscure remote heads. No multiplayer fix is claimed.

## WAM and room portability

The new object is persisted through **WAM entity data + prefab collection + image asset URL**. A standalone TMJ does not contain or recreate it. Editor-uploaded custom assets are scoped to the actual universe/world (`CustomEntityCollectionService.ts:52–73`), and the room automatically loads that custom collection (`GameScene.ts:1815–1825`).

For file-based transfer, package the PNG and collection JSON at reachable persistent paths, register the collection in the target WAM, and retain each entity's `prefabRef`, top-left position, and depthOffset in the prefab. Keep collection `version: "1.0"` so migration does not rewrite its IDs. A different room/world must have valid accessible references; the original room's private/scoped asset URL cannot be assumed portable.

example-collection.json and example-wam-fragment.json are illustrative file-based configuration fragments, not complete room files and not substitutes for returned editor-upload IDs. Merge with existing collections/entities; do not overwrite the actual room WAM with the fragment.

No upload, room mutation, browser action, bulk migration, or publication has occurred.
