# Flagship foyer: two spatial choices

These drawings are for choosing a direction. The colored floor plans are schematic, not new map art. The small full-hall image and the rear-row strip are cropped from the existing Flagship image to show how each proposal meets the auditorium.

## A. Deep indoor concourse — recommended

The new interior is **44 × 22 native tiles**, or **1408 × 704 native pixels**. It is a substantial room below the auditorium, not furniture added to the old narrow strip.

- Three lounge bays are 11 × 7 tiles; the middle upper bay is 7 × 7. Each has four chairs around a table, with varied orientation and open space inside the bay.
- The two existing 3-tile hall openings keep their positions. Each meets a proposed 4-tile receiving landing and approach. The existing doors are not claimed to have been widened.
- A 4-tile cross-concourse connects these approaches. A direct 4-tile arrival route comes from an 8-tile south opening, with extra unoccupied floor on either side. Furniture and coffee service sit outside this route.
- An 11 × 7 coffee bay contains four café seats, a counter, and a separate 3-tile-deep customer apron. The counter has a small staff-side allowance. Exact service equipment and operational staffing are not prescribed.
- A modest welcome/information point sits beside the arrival route. It does not obstruct the center line or imply that a live host, check-in service, or event schedule exists.
- There are **20 proposed social seat symbols**: 16 lounge seats and four café seats. This is not a claim that all 210 auditorium users can sit in the foyer.

**Trade-off:** the indoor footprint grows considerably, but the hall and foyer can remain one continuous room. The clear arrival path supports a quieter approach in spatial terms; audio/silence behavior would need a separate implementation and test.

## B. Covered garden and café forecourt

This is an **offset L-shaped exterior plan**, rather than another arrangement inside the same rectangle. Its illustrated site envelope is **64 × 40 native tiles**, or **2048 × 1280 native pixels** below the schematic hall threshold. That envelope includes open garden, so it must not be interpreted as a 64 × 40 enclosed room.

- The auditorium remains north-west of the expanded site. A 3-tile façade-depth reserve gives later artwork room to develop a deeper, taller-looking building front without drawing or generating it now.
- A covered landing has two lounge bays: 11 × 6 and 10 × 6 tiles. Both hall-door approaches are open and remain aligned with the existing 3-tile openings.
- A broad terrace stair leads to an **8-tile-deep promenade**. A separate 3-tile-wide side ramp/path is diagrammed at the east edge of the landing. Its grade, exact collision shape, and accessibility behavior are not validated by this plan.
- The café is a separate 16 × 11-tile east pavilion, with four café seats and a 3.5-tile customer apron in front of its counter.
- Two 11 × 7 garden-facing lounge bays occupy the lower east wing. A 5-tile route runs beside them, connecting the promenade to a second south arrival. Staying to talk does not require standing in the promenade or the coffee queue.
- Open garden occupies the south-west portion. Its path continues off the drawing and joins the promenade; the plan is attached to continuous land, with no detached island.
- A dashed outline indicates proposed canopy coverage. It is not a collision boundary or a drawn roof.
- There are again **20 proposed social seat symbols**. These represent a visual social program, not verified occupancy or simultaneous conferencing capacity.

**Trade-off:** this uses more site area and requires more exterior composition. It can inform a continuous-map exterior or a separate linked-room approach later. No room URL, working transition, operational destination, or link has been configured or claimed.

## What informed both plans

The actual Conference Campus interior and outdoor reference crops were inspected before drawing. Their useful lesson is that furniture groups are given recognizable bays and central movement space is deliberately generous.

- The reference's two rear lounge rugs are exactly 8 × 5 native tiles. About 10 × 7 is a reasonable planning envelope only when surrounding furniture and an approach allowance are included.
- Its separate arrival rug is 9 × 6 tiles.
- Its outdoor cross-band is eight source collision-grid rows deep, except for one sign tile. Visible stool edges overlap the upper edge, so the completely clear visual strip is closer to seven tiles in places.
- The observed desk has a laptop/device and plant. A café counter was not established in that source. Coffee service is included here because the user asked for it.
- The proposed dimensions in these drawings are new planning choices. They do not purport to reproduce the reference layout or its functionality.

No third-party reference pixels appear in the new diagrams. The reference study images are evidence only and are not included in this deliverable package.

## Scale, context crops and assumptions

1. The native planning grid is **32 × 32 pixels per tile**. No real-world meter conversion is implied.
2. Option A is drawn at **28 output pixels per tile, 87.5% of native pixel scale**. Option B is drawn at **20 output pixels per tile, 62.5% of native pixel scale**. The rear-row context strip in each uses the same respective scale as its plan. The full-hall sidebar inset is a context thumbnail and is not at plan scale.
3. The small person symbol is a neutral vector scale guide enclosed by a 1 × 1-tile dashed square. It is not a final character sprite, proof of actor collision bounds, or a runtime occupancy fixture. The 32px sprite envelope is distinct from the native 16px physics body; the diagram does not draw that body. Furniture symbols are likewise planning footprints rather than final art.
4. Source image: `grand-auditorium-01/review/flagship-empty-native.png`, 1536 × 1280 pixels.
5. Full auditorium/stage context crop: **[0, 0, 1536, 944)** in original native pixels. File: `context/unchanged-auditorium-context.png`.
6. Rear-row context crop: **[64, 720, 1472, 944)** in original native pixels. File: `context/unchanged-rear-hall-context.png`. All crop coordinates are half-open: right and bottom are excluded.
7. The foyer mirror crowns begin intruding into the original image below this crop. To omit both mirrors entirely, original pixels y944–1007 are not shown as a photographic/raster context band. Instead, that 64-pixel threshold depth is represented by a plainly schematic strip with the two existing door x-ranges. The original source file itself is unchanged.
8. Original hall door x-ranges remain **[512, 608)** and **[928, 1024)** native pixels. Relative to the interior starting at x64, these are tile columns **[14, 17)** and **[27, 30)**.
9. The stage and 210-chair arrangement are preserved. No new plan proposes shifting hall chairs, shrinking people or objects to fit the old strip, retaining either side mirror, or substituting a fake portal.
10. Open routes are design intent, not a certified egress calculation. Collisions, approach clearances, actor depth, seated interaction, proximity networking, quiet zones, accessibility, and crowd behavior would all require review after a direction is approved.
11. v01 remains untouched. No new TMJ/WAM, map artwork, live configuration, GitHub change, publication, or approval to implement is part of this delivery.

## Files

- `option-a-deep-indoor-concourse.png`: primary A review image, 1800 × 1460.
- `option-b-covered-garden-forecourt.png`: primary B review image, 1800 × 1560.
- Matching `.svg` files: editable vector floor plans with the original-hall context embedded as raster images. All new geometry, labels, furniture, routes, and guides remain editable SVG elements.
- `draw_layout_options.py`: reproducible source; uses Pillow for the authorized context crops and Inkscape for SVG rendering.
- `layout-manifest.json`: crop coordinates, scale, principal dimensions, and stage status.
- `context/`: the two exact unchanged context crops.

The next decision is which spatial direction to develop. New asset generation or implementation should wait for the user's visual choice.

## Source provenance

- Original project hall image SHA256: `75512832621467fbbf24b54fbc8e0931e0a80bf17160b0fcbe82a0863a966c9c`.
- Inspected reference source: https://workadventure-chat-uploads.s3.eu-west-1.amazonaws.com/upload/map-parteners/partners-162.map-storage.staging.workadventu.re/100-roads/conference-campus.tmj
- Reference source SHA256 from the measured study: `5495f6f502208e486905adea889932e26c14e092d2cc5a3a53848c86ac1934e9`. Its original pixels are not bundled here.
- The generator can run from this folder using the included context crops, Pillow, and Inkscape. It never requires or reconstructs third-party reference artwork.

## Later implementation check

Chair symbols are room-program markers, not finalized resting anchors. Later native proximity testing should check the source defaults of 64px start radius and 48px group radius, plus body clearance and actor-depth routes; deployed overrides are unknown. The illustrated four-person pods are not already configured for automatic or private meetings.
