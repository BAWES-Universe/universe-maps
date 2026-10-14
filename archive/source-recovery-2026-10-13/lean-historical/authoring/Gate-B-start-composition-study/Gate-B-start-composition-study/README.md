# Gate B off-axis spawn study

Decision: preserve the centered functional spawn. The x384 crop is a composition reference only. No gate TMJ, collision, script, atlas or published file changed.

The images compare nominal centered (496,1136), left (336,1136) and intermediate (384,1136) positions. They use the exact gate layers, unchanged north-facing Greg frame10 at32×32 world pixels, and390×844 display crops derived from the full pinned native CameraManager/scale classes with deterministic adapters. All pixels, including Greg, receive the same camera scaling. The bottom96px panel merely reserves the known test-HUD space and explicitly is not the live Universe HUD. These are offline compositions, not browser screenshots or camera-motion proof.

The initial source camera footprint is416×901 world pixels. The x336 composition reveals the lower left waterfall, but holding up hits the corridor shoulder after16px. At x384, horizontal clearance within its row is56px, but the nearby diagonal shoulder is only28.84px from the body. It misses a32px minimum-clearance requirement; a straight ascent stops at the next narrowing after240px. The exact mask requires x>=456 to reach the door on a straight line, and x>=488 to retain32px body clearance throughout. The functional centered route therefore wins. Tap path alternatives and reverse routes are recorded by the independent route audit.

Greg's display bounds are approximately30×30px, because the native32px frame and world share the same390/416 camera scale. Its bottom is574.2px, leaving173.8px above the reserved bottom HUD region in both compared frames. No sprite-only enlargement was used.

The old64×32 classified start area allows a small horizontal native random range; (496,1136) is the nominal central sample, not a claim that every untouched native spawn is precisely identical. Any future spawn change would need consistent classified start-area and fallback start-layer edits. This study makes none.

Reduced-motion source inspection also confirms the base artwork retains waterfalls and pools after all reducedMotionHide overlays are omitted. Those layers remove water motion, not the underlying scenery. Do not add duplicate fallback art based only on the property names.

Later framing may reveal more scenery while keeping the player on the centered route. Finish the existing Follow-preserving smooth zoom investigation before adding any further camera control.
