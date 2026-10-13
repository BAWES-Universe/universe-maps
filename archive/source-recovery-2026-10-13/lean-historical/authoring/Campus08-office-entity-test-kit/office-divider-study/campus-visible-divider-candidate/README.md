# Wider-office live-comparison candidate

This is a separate compiled derivative of lush08. The original08 and published versions are unchanged. It is local, unpublished and awaiting actual in-game review.

Changes are confined to the office: each desk island and its two occupants move16px outward, with no scaling. Four low stone dividers use retained native stone/trim and small original foliage ends. Their fixed32×128 footprints leave64px central lanes. North/south cross-aisles remain open. The dividers are below players; they introduce no head occluder.

The compiled map remains2944×2624 with four16px tile layers and120,704 tile objects. The runtime-package folder contains only the15 referenced files,18,718,109bytes. All assets resolve relatively; no new script, authentication or service dependency is added. Native fountain/fire audio, animation and fountain-front arrival are retained.

All40 full-map source-selected tap paths from the actual arrival to office work/reception/meeting targets and back reach their destinations. Analytical body checks have zero overlap; all16 work-seat paths avoid other stationary work-seat capture disks. These use the isolated proposed native path correction, not deployed engine behavior. See docs/compiled-office64-paths.json.

Original fixed chair-back foreground still has movement-head grazes. The existing native floating-entity solution is prepared for one-chair testing, but no entity is configured here. Room conferencing, stage broadcasting, bot identities and personal claims remain unconfigured. This derivative is a live comparison, not final acceptance.

Rebuild in order: tools/build08.py, tools/compile16.py, tools/install_native_audio08.py. The office-input folder is the exact composed variant. Original source lineage and the main08 checkpoint are documented in the surrounding study folder and Library libfile_f1c24134f01081918ea0b84ea8daced4 version2.
