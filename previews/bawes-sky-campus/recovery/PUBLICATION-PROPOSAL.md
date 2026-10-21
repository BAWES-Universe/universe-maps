# Proposed isolated preview publication — not executed

Target branch observed: `gh-pages` at `17cd44edbfbcdbf5af965e1e8abf0dde1c4f40ce`.
New directory: `previews/bawes-sky-campus-recovery-20261021/` (absent in the checked branch).

After separate publication authorization, extract the verified recovery ZIP and add its contents under this directory only. Preserve every existing gh-pages entry. Commit the additive tree on the current gh-pages head and update that ref with an expected-head check and `force:false`. If the head changes, reread and rebuild the additive tree. Do not merge this PR into master, overwrite another preview, publish a release, or change any permissions.

The proposed TMJ location after successful publication is:
`https://bawes-universe.github.io/universe-maps/previews/bawes-sky-campus-recovery-20261021/campus.tmj`

The index and `PUBLICATION.json` sit beside the map; all referenced atlases and runtime must be uploaded together. The URL above is a proposal, not a currently working link. Verify Pages delivery, every map dependency, and actual Universe loading after publication. No publication action has been performed by this recovery task.
