# Azure paving revision2 — visual review candidate

Supersedes the rejected bridge flooring in0bffac61e1c2f991f968bef059faa3677f8f247a. Saved only to the authorized preview branch. Not deployed, not presented as owner visual acceptance.

Removed the generated128x128 slabs and all landing rectangles that painted over island or hub artwork. The shared bridge/bay surface now uses a90x54 module measured from existing court paving, with stone and grout sampled from hub.png. A shadow-free portion of stone supplies the tile interior instead of repeating the source tile's baked directional shadow. The atlas repeats in world coordinates, including horizontal bridges; the grout does not rotate or reset at bays.

The eight transitions now use a full32px court mosaic course, sampled from the actual hub artwork and contained entirely inside each bridge. Existing island and hub borders remain visible and untouched. The individual island paintings have varying tile dimensions and irregular painted grout; the mosaic course intentionally terminates the bridge grid at those surfaces. This is not a claim of pixel-identical grout continuing through every island painting.

The lounge grid removal and cutaway are retained unchanged. Island/hub image bytes, geometry,controller,bay furniture and glass.png match0bffac6 exactly; see unchanged-assets.json. No seat, collision, layout, water or audio changes.

[Revised native-game screenshots of both ends of every bridge](captures.md). All eight endpoint captures were visually inspected. Eleven viewpoints retained native Woka/camera scale1, visible alpha1 and zero sampled map popups. Captures are real local WorkAdventure in the selected cloud workspace, not a deployed owner session. Diagnostic viewpoint setup is separate from gameplay checks.

All16 edge-lane checks at eight landings passed native right-click crossings and keyboard return. Tests position the player near each lane to avoid repeating long inter-island traversal. Existing seat/rail checks are not relabeled as new tests: their defining assets and geometry are unchanged. The runtime-hashes.json manifest identifies the final tested bytes.

Matched1366x768, animated water enabled and forced continuous rendering, six-second samples:

| View | Base d0d9a80 FPS | Revision2 FPS |
|---|---:|---:|
| Bridge/bay |55.5|55.6|
| Lounge outside |39.8|45.2|
| Lounge inside |40.3|38.7|

p95 stayed33.3–33.4ms. These short samples show the bridge render rate preserved; the small interior variation is reported rather than hidden. They are not a universal FPS claim. The measured90x54 pattern requires a1440x864 repeating atlas to meet native32px tile boundaries without seams.

No additional agents, deployment or broad rework. Prior Library reference-download and upload failures remain documented in the earlier task; the screenshots here are committed native PNGs available for parent review.
