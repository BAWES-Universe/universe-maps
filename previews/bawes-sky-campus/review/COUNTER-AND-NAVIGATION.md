# Counter source inspection and navigation correction

## Counter: no clean existing-source correction

The existing counter can be traced and resized uniformly. A complete assembly envelope of source `(216,676)-(400,746)` is 552×210 native world pixels; scaling it to 384px wide gives approximately 384×146 including tall props, with a front body around38–46px. That is plausible beside a32px Woka and32px stool seat. Scale alone is not the blocker.

Shrinking would expose hidden rear floor, cabinet ends, shelf supports and canopy-post overlaps. The nearby visible floor is in front of the counter; repeating it behind would erase the structural junction and make shelves appear unsupported. The alternate cafe ground image also has a large counter and differs in perspective. The separate furniture sheet has no counter. `source/reused/cafe-interior.png` is a different enclosed room, not a matching background. No visibly patched counter was installed.

`counter-source-inspection.png` is an annotated source crop, not a proposed scene edit. The earlier `(198,688)-(390,744)` box includes the left canopy pier but clips upper/right props and return. The exact complete delivery rectangle is now `(216,676)-(400,746)`, world `(2440,4076,552,210)`. It must be registered to the current source, with a selective removal mask preserving canopy posts, shelves and plants inside the rectangular crop. Supply the counter-free rear structure/floor plus a transparent same-camera counter assembly (top, apron, both ends, attached props) and a separate foreground apron. Target384px width, no more than146px total height including props,40–48px body height and20–28px top depth. Only this fixed front/three-quarter view is needed. Full details are in `source/cafe-candidates/counter-adaptation-blocker.json`.

No counter or stool geometry changed. Existing native occupancy evidence remains applicable; the96px swept route is rechecked. The cafe is unfinished.

## Stage traversal defect

The prior settled retries concealed a reproducible defect. Instrumentation recorded the outdoor route passing at y3112, opening the office entrance because the original80px proximity included the cross-campus route. Each gate layer change prompted the pinned client's `subscribeToGameMapChanged` to replan. Replanned target y shifted3104→3120→3136→3152 and beyond. This is not an ordinary asynchronous pathfinding delay or an impassable stage aisle.

The map-local correction reduces exterior office-front proximity from80 to64px and defers exterior gate layer changes until the approach movement stops. The smaller radius alone fixed the crossing but did not fix a deliberate approach: opening during movement still shifted that target. Deferring those exterior changes addresses that second reproduction. Interior proximity and meeting doors retain80px. The frontage route no longer triggers gate animation; a deliberate approach stops at y3088 before opening it; crossing an already-open threshold remains available. No engine file, accepted interior artwork, furniture, collision or gate animation changed. The engine's replan behavior itself remains unchanged.

`stage-navigation-before.json` records the original sequence (its first traverse supplies the unambiguous gate/replan evidence; later diagnostic commands interrupted replacement paths and are not counted as completed traversal tests); `stage-navigation-after.json` tests three uninterrupted west-terrace-to-stage traversals without retries and `entrance-proximity-check.json` checks normal entry. The prior retry-based district check remains historical evidence, not proof that the underlying issue was harmless timing.

## Bounded visual cleanup

Removed the unrelated laptop desk from the stage; it was a restoration substitute, not required functionality. No microphone was invented. Alcove rim/tread highlights are quieter; only silhouette edges receive a2px transition/contact shadow and the last8px of the east landing blend into the registered floor. Cafe grain remains sharp, with only a1.4px boundary transition. Both retain their existing strict masks and outside-mask pixel assertions. These are limited transition improvements, not visual acceptance of the cafe or conservatory.

Visual review remains required: the alcove still uses a geometric oval and the cafe bar/deck border still reflects the inherited source silhouette. The small edge changes do not solve the underlying difference in scene softness or substitute for the missing counter plate.
