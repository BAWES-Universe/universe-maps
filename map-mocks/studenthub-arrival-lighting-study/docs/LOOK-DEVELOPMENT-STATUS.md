# Arrival/Commons look development

This folder is an original offline art experiment. It is not an accepted main-world map and is not yet playable. The existing gate remains the visual baseline and has not been changed.

The new source uses one calibrated orthographic Blender scene for the court, connected shared workplace, glass meeting room, reception, furniture, planting and actual lighting. It replaces the earlier disconnected sprite assembly with shared geometry, receivers and physical material joins. Four original painted albedo materials and a separate original painted water material were created with the built-in image tool and applied to the scene. Their source pixels are retained. These are surface inputs, not an enlarged finished map painting.

The first brown maquette is retained under `experiments/brown-maquette/`. The later native images change the palette, leaf density, furniture heights, stone rhythm, entrance shape and water surface. They include the unchanged32px Greg only as a scale reference. That image composition is not a browser/game capture.

## What this experiment establishes

- Both ground axes project at exactly32 native pixels per logical unit. The output is1536×1152, with no scene enlargement.
- Walls, planted edges, tables and chairs share one light setup and cast real contact/receiver shadows.
- The source has independent ground, furniture, foliage/structure, chair-back, lectern-rim, glass and roof groups. Visibility masks and physical footprints are separate authoring data.
- Original textures are surface materials on geometry, not imported third-party map art. The source Blender file packs its material images.

## What it does not establish

The art review still determines whether it carries the v1/gate atmosphere. A coherent lighting model is not sufficient evidence of an aesthetic upgrade. The source scene uses procedural shapes, and the initial reviews found the result too regular and generic, with insufficient authored surface/shape detail and magical richness.

No TMJ or gameplay atlas has been produced from this experiment. The compiler and Phaser harness are prepared source only. There is no actual browser visit, seating/glass/lectern proof, mobile proof, water animation, sound validation or live integration claim for this new section. Prior completed proofs belong to their own earlier folders.

The exact next decision is whether the final bounded painted-material and covered-roof still clears the visual bar. If it does not, preserve this as a construction/lighting experiment and stop before full export. A new art pass would need deliberate painted shape/material design on the real architecture and furnishings, not another round of global color changes, extra flowers or noise textures.
