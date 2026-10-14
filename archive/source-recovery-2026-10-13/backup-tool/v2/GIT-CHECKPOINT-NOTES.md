# Selected Git source for the durable backup tool

Eleven files are copied byte-for-byte from the frozen v2 implementation. FROZEN-MANIFEST.json describes the larger 22-file Library package; not every listed evidence/configuration file is embedded in Git. LIBRARY-PROVENANCE.json pins the complete package and separate detailed archive audit, both verified by read-back. Restore the full reviewed package from authenticated Library before using omitted configurations/evidence referenced by the original README.

The tool is implemented and locally tested, including 60 unit tests and a 101 MiB /13-chunk clean restore/retry fixture. It has not configured or contacted R2, uploaded the real dataset, completed a real-bucket restore, or installed a watcher. The default 128 MiB new-upload budget is unchanged. The 200 original ZIP archives remain outside this script's extracted-source selection and require separate asset preservation. Example/local configuration contains no usable credentials.

Configure credentials only through an appropriate secure environment setup, never in Git or chat. Preserve the original snapshot and source manifest when making later revisions.
