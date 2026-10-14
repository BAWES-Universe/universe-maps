# Validated Moonlit r3 recovery backup

This is an additive backup of the tested r3 candidate. Start with REPORT.md and candidate/REPAIR-NOTES.md. candidate/runtime/moonlit.js is the authored controller source and deployed-local runtime; runtime/moonlit.tmj is unchanged from sealed r2. The original seal is not modified by this backup.

Candidate files, test scripts, reports, result JSON, logs, sample timelines and screenshots are retained byte-for-byte from the local validation directory. Full Playwright trace ZIPs (about 175 MB), caches, dependencies and ephemeral game state are excluded. LOCAL-FULL-EVIDENCE.sha256 records the local session's broader artifact inventory; missing trace ZIPs in that historical index are intentional. BACKUP-MANIFEST.sha256 covers exactly this compact backup, excluding itself. candidate/MANIFEST.sha256 covers the original candidate subtree.

Reports contain environment-local paths/URLs as historical evidence; localhost preview URLs are not remotely accessible. Test harness scripts use the original local stack paths and require that environment or adjusted paths to rerun. No public deployment is part of this backup. The dated verification record alongside validated-r3 records provenance; remote commit and blob verification results are returned by the backup operation.

Passed browser journeys include roof reversal, single-client door visual/collision synchronization, camera return, real departure/rejoin menu cleanup, routes, water, audio and phone emulation. Multiplayer-safe closing, physical devices and polished artwork remain unverified.
