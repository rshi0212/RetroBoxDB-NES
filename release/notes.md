NES Catalog, storage v4 (8 KiB blocks, 9 solid LZMA2 groups of up to 256 MiB). Metadata only: **no ROM payloads are published**; `compression_groups`, `chunks` and `object_chunks` are empty.

- One schema for all twenty-three platforms: the header tables of the eight new platforms (Game Gear, PC Engine, SuperGrafx, MSX, MSX2, Virtual Boy, Game & Watch, Super A'Can: `pce_hardware`, `msx_hardware`, `vb_hardware`) and `rom_annotations` exist in every Catalog; tables of other platforms and provider tables have no rows.
- RetroAchievements reports look up sibling databases (NES<->FDS, SNES<->Satellaview, WonderSwan<->WonderSwan Color, NeoGeo Pocket<->NeoGeo Pocket Color, PC Engine<->SuperGrafx, MSX<->MSX2): a game whose ROM is stored there is `local_other_platform`, not a gap.
- Source: 23,765 ZIPs (nointro 21,792, retroachievements 1,973), 4.35 GiB (23,766 ROM files, 11.18 GiB uncompressed). Populated database: 530.1 MiB (11.9% of the ZIPs). All source ZIPs are reproduced byte-for-byte.
- Contents: 18,414 ROM records, 3,477 games, 7,385 releases; DAT versions: 20260713-141345, 20261002-002752.
- RetroAchievements: 1,110 of 1,123 games with achievements have a local ROM.
- Export (Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz, idle, all checks): whole newest-DAT set with export_set.py 71.7 MiB/s (7,090 files); single file with a cold cache 2.325 s (ROM) / 1.983 s (TorrentZip) on average.
- Full audit of the populated database: 19,069 objects, 9 groups, 25,368 archive plans, no errors.

The release workflow starts from the base Catalog pinned by SHA256 in `release/catalog-release.json`, injects the engine and documents of the tagged commit, checks every data-table digest, SQLite integrity and foreign keys, runs the Catalog audit and the repository tests and the embedded NES suite. Verify the download with `SHA256SUMS`.

[中文说明](https://github.com/rshi0212/RetroBoxDB-NES/blob/main/README.zh-CN.md)
