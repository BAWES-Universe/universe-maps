# Built-in image-edit candidates, October20

Used the available built-in `image_gen.imagegen` tool, not a third-party service. Input: inspected exact `source/counter-repair-request/counter-source-exact.png`. Original generated files remain in `/workspace/generated_images`; copies and SHA256 hashes are supplied here. These assets are **not integrated into the map**.

Three edits:
1. `clean-background.png`: requested only counter/props removal with exact preserved framing, shelves/posts/plants and floor. Output2033×773 reconstructs a plausible supported wall but still alters protected features and floor detail. It is **not registered**. See `review/counter-new-registration-check.png`. The rejected rectangular/local-warp integration method was not repeated.
2. `counter-assembly.png`: requested one complete transparent same-camera counter,384px final width,44px body and24px top depth. First native preview `counter-native-384.png` is384×153; total height exceeded146px because of tall props.
3. `counter-refined.png`: built-in edit reduced the right pot/holder, retaining the deeper body. Alpha threshold32 gives crop `(110,120)-(1908,750)`; uniform384px calibration yields `counter-refined-native-384.png`,384×135. Estimated front body40–46px. One coherent top/ends/body/props assembly; no mismatched separate apron. Foreground segmentation must be derived from this main assembly if integrated later. These are offline proportion checks, not native Woka occupancy validation.

The refined assembly is a materially improved proportion candidate. The remaining blocker is the precisely registered background, including the overlaps directly under the original shelves and beside the posts. Preserve original protected pixels and match reconstructed backing/floor at those edges. Full exact source request and crops remain in `source/counter-repair-request/`. No blanket smoothing, full-scene replacement or forced patch was applied.

No automatic approval action was denied. Generation succeeded, but precise registration was not achieved; that limitation is explicit rather than a completion claim.
