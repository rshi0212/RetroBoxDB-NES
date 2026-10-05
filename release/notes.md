NES Catalog, storage v4 (8 KiB blocks, 9 solid LZMA2 groups of up to 256 MiB). Metadata only: **no ROM payloads are published**; `compression_groups`, `chunks` and `object_chunks` are empty.

- RetroAchievements ROM set imported: 1,969 ZIPs; 1,256 ROM files are also in a No-Intro DAT, 691 are only in the RA set, 22 have a hash absent from the latest RA snapshot. RA games with achievements that have a local ROM: 933 → 1,110.
- Source collections (`source_collections`, `v_collection_files`) and RetroAchievements links per file (`v_ra_collection`).
- ROMs outside every DAT join the family of the stored ROMs they share the most blocks with (hacks next to their original).
- Imports and DAT packaging no longer decode solid groups for already stored blocks; DAT formats (e.g. FDS/QD, NES headered/headerless) are handled separately.
- Famicom Disk System images found in the RA NES folder are not imported here; they are in the new FDS database.
- Source: 23,761 ZIPs (nointro 21,792, retroachievements 1,969), 4.35 GiB (23,762 ROM files, 11.18 GiB uncompressed). Populated database: 536.8 MiB (12.1% of the ZIPs). All source ZIPs are reproduced byte-for-byte.
- Contents: 18,414 ROM records, 3,477 games, 7,385 releases; DAT versions: 20260713-141345, 20261002-002752.
- RetroAchievements: 1,110 of 1,123 games with achievements have a local ROM.
- Export (Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz, idle, all checks): whole newest-DAT set with export_set.py 71.7 MiB/s (7,090 files); single file with a cold cache 2.325 s (ROM) / 1.983 s (TorrentZip) on average.
- Full audit of the populated database: 19,069 objects, 9 groups, 25,368 archive plans, no errors.

The release workflow starts from the base Catalog pinned by SHA256 in `release/catalog-release.json`, injects the engine and documents of the tagged commit, checks every data-table digest, SQLite integrity and foreign keys, runs the Catalog audit and the repository tests and the embedded NES suite. Verify the download with `SHA256SUMS`.

[中文说明](https://github.com/rshi0212/RetroBoxDB-NES/blob/main/README.zh-CN.md)
