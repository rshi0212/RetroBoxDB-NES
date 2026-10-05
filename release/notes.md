NES Catalog, storage v4 (8 KiB blocks, 6 solid LZMA2 groups of up to 256 MiB). Metadata only: **no ROM payloads are published**; `compression_groups`, `chunks` and `object_chunks` are empty.

- Storage migrated from v3 (8 KiB blocks, XOR deltas, ≤ 2 MiB LZMA2 groups) to v4 (8 KiB blocks in No-Intro family order, solid LZMA2 groups). Block IDs, SHA256, object extents, header recipes and all metadata are unchanged.
- The NES database now uses the same engine as the other five platforms; the v3 engine and its documents remain as history.
- RetroAchievements snapshot (console 7) imported; RA hashes use the body MD5 without the 16-byte header.
- Source: 21,792 No-Intro ZIPs, 4.12 GiB (21,793 ROM files, 10.69 GiB uncompressed). Populated database: 506.2 MiB (12.0% of the ZIPs). All source ZIPs are reproduced byte-for-byte.
- Contents: 17,726 ROM records, 3,477 games, 7,385 releases; DAT versions: 20260713-141345, 20261002-002752.
- RetroAchievements: 933 of 1,123 games with achievements have a local ROM.
- Export (Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz, idle, all checks): whole set in storage order 54.1 MiB/s (22,943 ROM files); single file with a cold cache 2.339 s (ROM) / 2.216 s (TorrentZip) on average.
- Full audit of the populated database: 17,734 objects, 6 groups, 24,487 archive plans, no errors.

The release workflow starts from the base Catalog pinned by SHA256 in `release/catalog-release.json`, injects the engine and documents of the tagged commit, checks every data-table digest, SQLite integrity and foreign keys, runs the Catalog audit and the repository tests and the embedded NES suite. Verify the download with `SHA256SUMS`.

[中文说明](https://github.com/rshi0212/RetroBoxDB-NES/blob/main/README.zh-CN.md)
