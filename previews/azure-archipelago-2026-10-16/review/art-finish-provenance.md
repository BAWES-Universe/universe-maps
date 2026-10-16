# Finish-pass artwork provenance

Generated artwork was inspected, normalized to native map dimensions, registered to existing seat centers and then tested in the actual engine. Runtime PNGs and registered transparent island PNGs are the canonical build inputs; no paid service or production engine change was introduced. The image-generation source files remain in this workspace's generated_images directory. Registration scripts record the local import recipe, not a requirement to regenerate images during a map build.

- Café: b0a40f6c-73d5-451a-b751-075f70d99ea4, normalized1203×1206, offset−1,−2 in1216canvas.
- Garden:3ffc087d-a02a-4de8-a0b8-da11e77a4c83,1200×1198,offset0,+2.
- Lounge:30231f6b-61c8-4a86-8ff7-39eb138a1f93,1197×1199,offset+1,−1. Three rear chairs moved32px south for shelf clearance.
- Gathering:9cb7f787-6a45-4293-8f16-5aeff28dd3f7,1205×1203,offset−3,−2.
- Hub:2f2f58c9-6f07-4be6-9ca2-65e01cd762c8,768×768.
- Bridge:79d30b27-ca8b-4562-a17c-d11ef5eb5e0a. Native320×896 bands48/224/48 registered as32/256/32 to retain the full256px walking corridor.
- Viewing bay:948a02ea-8071-4977-a938-c48519546ee6,576×320. Transparent exterior replaces opaque old cyan water corners; existing chair targets retained pending fresh visual sit review.
- Sea:ba9e57ff-f88e-4f56-b471-77dbb283d58d,512×512. Native animated shimmer stroke opacity reduced to.10/.07 after independent review found.24/.18 too conspicuous on the darker base. Timing remains24frames×100ms.

No island dimensions, camera zoom, Woka scale or number of destinations changed. No quests or walking-triggered audio UI added. Native map routes, seats, table collision and roof cutaway require the fresh report accompanying this artifact, rather than relying on historical acceptance.
