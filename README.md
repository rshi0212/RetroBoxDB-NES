# RetroBoxDB NES

English | [中文说明](README.zh-CN.md)

Single-file SQLite preservation database for NES / Famicom: ROM data, original DAT content, checksums, hardware provenance, reversible header variants and the processing code in one SQLite file. The public Catalog holds metadata only (checksums, DAT and provenance records, 16-byte headers, archive recipes and the code); it contains no ROM data and cannot restore files. The populated `RetroBoxDB.NES.sqlite` stays local.

| Item | Value |
| --- | --- |
| Original size | 23,765 source ZIPs, 4.35 GiB (21,792 from the No-Intro Headered and Headerless folders with their Aftermarket/Private folders, 1,973 from the RetroAchievements set); 23,766 ROM files, 11.18 GiB uncompressed |
| Stored size | populated `RetroBoxDB.NES.sqlite` 529.9 MiB; public Catalog 145.4 MiB (no ROM data) |
| Ratio | 11.9% of the source ZIPs, 4.6% of the uncompressed ROM files |
| Technology | storage v4: 16-byte headers stored apart from bodies, headered and headerless dumps share one body; bodies cut at header/PRG/CHR boundaries into 8 KiB blocks, deduplicated by SHA256 and packed in No-Intro family order into LZMA2 solid groups of up to 256 MiB (256 MiB dictionary); full per-block and per-object verification; source ZIPs reproduced byte-for-byte from TorrentZip plans |
| Export performance | Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz, idle, Python 3.14.4, all checks included. whole newest-DAT set with `export_set.py` (7,090 files, each checked against the DAT hashes): 71.7 MiB/s, 5 ms per file on average; single file with a cold cache (the group is decoded up to the file): ROM 2.325 s, TorrentZip 1.983 s on average |

## Downloads and documents

| File / document | Content |
| --- | --- |
| [RetroBoxDB.NES.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-NES/releases/latest/download/RetroBoxDB.NES.Catalog.sqlite) | Public Catalog (Release asset with `SHA256SUMS`) |
| [Storage v4 guide](RetroBoxDB.Storage-v4.en.md) / [中文](RetroBoxDB.Storage-v4.zh-CN.md), [technical design](RetroBoxDB.Storage-v4.Technical-Design.en.md) | Storage format, evaluation and maintenance shared by every platform |
| [NES v3 technical design (history)](RetroBoxDB.NES.Technical-Design.en.md) | Storage v3, used until 2026-10-05 |
| [Platform assessment](RetroBoxDB.Platform-Assessment.en.md) / [中文](RetroBoxDB.Platform-Assessment.zh-CN.md) | Survey of the 172 local DAT archives |

## Other platforms

| Platform | Repository and Catalog |
| --- | --- |
| SNES | [RetroBoxDB-SNES](https://github.com/rshi0212/RetroBoxDB-SNES) · [RetroBoxDB.SNES.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-SNES/releases/latest/download/RetroBoxDB.SNES.Catalog.sqlite) |
| Mega Drive | [RetroBoxDB-MegaDrive](https://github.com/rshi0212/RetroBoxDB-MegaDrive) · [RetroBoxDB.MegaDrive.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-MegaDrive/releases/latest/download/RetroBoxDB.MegaDrive.Catalog.sqlite) |
| Game Boy | [RetroBoxDB-GB](https://github.com/rshi0212/RetroBoxDB-GB) · [RetroBoxDB.GB.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-GB/releases/latest/download/RetroBoxDB.GB.Catalog.sqlite) |
| Game Boy Color | [RetroBoxDB-GBC](https://github.com/rshi0212/RetroBoxDB-GBC) · [RetroBoxDB.GBC.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-GBC/releases/latest/download/RetroBoxDB.GBC.Catalog.sqlite) |
| Game Boy Advance | [RetroBoxDB-GBA](https://github.com/rshi0212/RetroBoxDB-GBA) · [RetroBoxDB.GBA.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-GBA/releases/latest/download/RetroBoxDB.GBA.Catalog.sqlite) |
| Famicom Disk System | [RetroBoxDB-FDS](https://github.com/rshi0212/RetroBoxDB-FDS) · [RetroBoxDB.FDS.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-FDS/releases/latest/download/RetroBoxDB.FDS.Catalog.sqlite) |
| Satellaview | [RetroBoxDB-Satellaview](https://github.com/rshi0212/RetroBoxDB-Satellaview) · [RetroBoxDB.Satellaview.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-Satellaview/releases/latest/download/RetroBoxDB.Satellaview.Catalog.sqlite) |
| Master System | [RetroBoxDB-MasterSystem](https://github.com/rshi0212/RetroBoxDB-MasterSystem) · [RetroBoxDB.MasterSystem.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-MasterSystem/releases/latest/download/RetroBoxDB.MasterSystem.Catalog.sqlite) |
| 32X | [RetroBoxDB-32X](https://github.com/rshi0212/RetroBoxDB-32X) · [RetroBoxDB.32X.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-32X/releases/latest/download/RetroBoxDB.32X.Catalog.sqlite) |
| WonderSwan | [RetroBoxDB-WonderSwan](https://github.com/rshi0212/RetroBoxDB-WonderSwan) · [RetroBoxDB.WonderSwan.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-WonderSwan/releases/latest/download/RetroBoxDB.WonderSwan.Catalog.sqlite) |
| WonderSwan Color | [RetroBoxDB-WonderSwanColor](https://github.com/rshi0212/RetroBoxDB-WonderSwanColor) · [RetroBoxDB.WonderSwanColor.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-WonderSwanColor/releases/latest/download/RetroBoxDB.WonderSwanColor.Catalog.sqlite) |
| NeoGeo Pocket | [RetroBoxDB-NGP](https://github.com/rshi0212/RetroBoxDB-NGP) · [RetroBoxDB.NGP.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-NGP/releases/latest/download/RetroBoxDB.NGP.Catalog.sqlite) |
| NeoGeo Pocket Color | [RetroBoxDB-NGPC](https://github.com/rshi0212/RetroBoxDB-NGPC) · [RetroBoxDB.NGPC.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-NGPC/releases/latest/download/RetroBoxDB.NGPC.Catalog.sqlite) |
| Pokémon Mini | [RetroBoxDB-PokemonMini](https://github.com/rshi0212/RetroBoxDB-PokemonMini) · [RetroBoxDB.PokemonMini.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-PokemonMini/releases/latest/download/RetroBoxDB.PokemonMini.Catalog.sqlite) |

## Storage: migrated from v3 to v4

From 2026-10-05 the NES database uses storage v4 like the other platforms. Basis:

- **Sample** (600 families, 652.6 MiB of ZIPs): the unchanged NES v3 engine gives 91.8 MiB; v4 with 8 KiB blocks and 128 MiB family-ordered groups gives 81.9 MiB (block metadata estimate included). 4 KiB blocks add more metadata than they save, and 64 KiB blocks cannot follow PRG/CHR boundaries; both are larger.
- **Full data**: after migrating to 32 MiB groups, adjacent groups were merged and measured (against 32 MiB): 64 MiB −1.40%, 128 MiB −2.59%, 256 MiB −5.66%. Smaller caps stay more than 0.5% above the 256 MiB result, so 256 MiB groups were chosen by the rule.
- **Whole database**: ROM data went from 364.4 MiB in v3 (489 lzma2-4m groups plus XOR-delta loose blocks) to 328.3 MiB (−9.91%, 6 groups). A format migration must save at least 2%.
- **Cost**: a single file read with a cold cache decodes its group up to the file (about 2.3 s on average); set exports read groups in storage order with a bulk cache.

The migration (`tools/migrate_v4.py`) works on a copy: it relaxes the `compression_groups` constraint for solid groups, adds the v4 tables and views, records a family and an RA hash for every body object, decodes all body blocks in block-ID order (164,951 blocks), packs them in family order, verifies every block and removes the v3 groups left empty (489). Block IDs, SHA256, sizes, object extents, 16-byte header recipes and all metadata are unchanged. The full audit after migration passed: 19,069 objects, 9 groups, 25,368 archive plans.

See the [storage v4 guide](RetroBoxDB.Storage-v4.en.md) and [technical design](RetroBoxDB.Storage-v4.Technical-Design.en.md) for the format and the per-platform evaluation.

## Catalog contents

The catalog preserves **58,935 files, 17,726 ROM records, 22,065 DAT ROM entries, and 24,487 archive plans**. Every pre-existing logical file/ROM/body checksum, source ZIP identity, generated ZIP identity, DAT record, naming decision, transformation, game/release association and frontend placeholder is retained.

The public file is built from scratch by copying application metadata and **excluding `compression_groups`, `chunks`, and `object_chunks`**. All three tables are empty. It is not a populated database with its rows subsequently deleted. Parsed DAT entry XML and 16-byte NES headers remain metadata; no source-file or ROM content blocks are included. Compressed ROM bytes are ROM payloads and are excluded as well.

```sql
SELECT * FROM v_file_checksums WHERE file_id = 1;
SELECT * FROM v_rom_checksums WHERE rom_id = 1;
SELECT * FROM archive_plans WHERE id = 1;
SELECT dat_set_id, status, COUNT(*) FROM v_dat_coverage GROUP BY dat_set_id, status;
SELECT content FROM resources WHERE name = 'catalog-report';
SELECT content FROM resources WHERE name = 'group-migration-report';
SELECT content FROM resources WHERE name = 'group-verification-report';
```

Checksums describe expected byte identities. Missing hashes in a source DAT remain NULL; the Catalog does not claim to recalculate unavailable payloads.

## English / Chinese CSV names

Both local databases retain all **4,453 rows** from `Nintendo - Nintendo Entertainment System.csv`, including **3,703 rows** with Chinese names. Name extension v4 resolves game identity before accepting matches: **4,420 source rows** match **4,429 releases, 2,023 games and 8,896 ROM records**; **3,698 releases** have directly matched Chinese names. **22 rows** remain review candidates and **11 rows** have no base-title candidates. These are name associations, not new checksum verification or ROM payloads.

The **3,703 translated rows share 1,875 unique Chinese names** in `game_chinese_names`, referenced by `game_name_entries.name_cn_id`. Identical Chinese names are stored once across English titles, regions and revisions. `v_release_chinese_names` returns deduplicated Chinese names for each release. `game_name_imports` and `game_name_entries` retain original and cleaned English names, source record numbers and SHA256 provenance; `release_name_links` records associations. The original CSV text, including original Chinese strings, any BOM and original newlines, is embedded in `resources` for provenance.

Removing parentheses now generates search candidates and concise display names; it does not establish identity across different games. Matching tries complete titles, equivalent parsed qualifiers, then compatible identifying fields. Every confirmed source row resolves to exactly one `game_id`. Parsed evidence retains regions, languages, versions and identity tags. Unknown tags remain identifying evidence, including volumes, publishers and cartridge IDs. The known publisher aliases `Bulletproof`/`Bullet-Proof` are normalized and qualifier order is ignored. Regions and Beta/Proto stages can disambiguate independent games. Unresolved candidates are excluded from standard-name and inheritance evidence.

NHK sixth-grade `(Jou)`/`(Ge)` now receive only the upper/lower translation respectively. The independent `Baseball (USA) (Intellivision)` no longer receives the Nintendo Baseball translation from another game. This correction removes **488 previous cross-game source links**; some other version-level matches become explicitly inherited names. Original CSV rows, deduplicated Chinese names and game groups remain intact. `game_name_match_decisions` records parsed evidence and decisions. [nes-game-names-match-review.csv](reports/nes-game-names-match-review.csv) lists unresolved sources, and [nes-game-names-matching-changes.json](reports/nes-game-names-matching-changes.json) records changed name associations.

Parent/clone releases share Chinese names through their existing `game_id`. **1,556 groups** have exactly one confirmed translation, used as their automatic standard name. **14 parents and 375 clones** inherit names. Effective coverage reaches **4,087 releases and 8,100 local ROM records**. At the release level, parent Chinese coverage is **49.50%** (1,721/3,477), and clone coverage is **60.54%** (2,366/3,908). These percentages measure Chinese coverage, not direct English-title matching. The previous 4,112-release figure included associations without sufficient identity evidence and is superseded.

The **167 groups with multiple confirmed translations** remain `needs_review` with no selected standard; their confirmed aliases remain available. **1,754 groups** have no confirmed Chinese name. [nes-game-names-review.csv](reports/nes-game-names-review.csv) lists standard-name candidates and their source titles, separately from the 22 sources with unresolved game identity. SQLite views derive standards and inheritance dynamically, without duplicating Chinese strings or claiming inherited names as direct CSV matches. Adding a conflicting translation automatically stops inheritance for that group. `v_game_chinese_name_evidence` traces each group alias to its source release and CSV record.

All **11 unmatched rows** remain available for review. Two have Chinese names: `EarthBound Beginnings` (地球冒险) and `Baoxiao Sanguo` (爆笑三国). Blank Chinese names remain null. Existing titles, ROM data, checksums and frontend fields are unchanged. GitHub Releases distribute the payload-free Catalog; the populated database remains local. Storage sizes elsewhere describe the earlier v3 migration.

```sql
SELECT * FROM v_game_names WHERE name_cn LIKE '%魂斗罗%';
SELECT * FROM v_release_chinese_names WHERE name_cn LIKE '%魂斗罗%';
-- Display names, including direct and group_inherited evidence categories.
SELECT * FROM v_release_effective_chinese_names WHERE name_cn LIKE '%地球冒险%';
SELECT * FROM v_rom_effective_chinese_names WHERE rom_id = 1;
SELECT * FROM v_game_chinese_name_status WHERE status = 'needs_review';
SELECT DISTINCT rom_id, release_id, name_en, name_cn
FROM v_rom_game_names WHERE name_cn LIKE '%魂斗罗%';
SELECT * FROM v_game_name_import_status WHERE status != 'matched';
SELECT * FROM v_game_name_match_review;
SELECT content FROM resources WHERE name = 'game-names/import-report';
SELECT content FROM resources WHERE name = 'game-names/group-report';
```

Repeated imports preserve source/row identities by platform and CSV SHA256 and refresh all stored sources against the current catalog and rules, preventing older imports from retaining invalid cross-game matches. Each database is updated in a transaction; `--dry-run` rolls back all changes, including extension upgrades. The importer and schema are also embedded as `import_game_names.py` and `game_names_schema.sql`; extract both into one directory to run independently.

```bash
python3 -B tools/import_game_names.py "$HOME/下载/Nintendo - Nintendo Entertainment System.csv" RetroBoxDB.NES.sqlite RetroBoxDB.NES.Catalog.sqlite
python3 -B -m unittest discover -s tests -v
```

## No-Intro provenance

Snapshot `20261002-002752` contains **7,704 archive identities, 16,154 distinct file identities, 13,930 dump sources, 898 Scene records, and 7,674 Dumplog rows**. Source and Scene IDs have separate namespaces. Repeated file references preserve independent dump evidence without duplicating content.

The snapshot retains 8,026 declared headers, 245 complete historical headers extracted from notes, and one incomplete historical-header note as an anomaly. One declared header belongs to a Headerless-classified record. Header declarations are distinct from physical cartridge evidence. All 6,414 serial-bearing source records remain available; 6,412 also anchor documented hardware assertions to an existing ROM or release. Different PCB/chip revisions are not collapsed into one hardware claim.

The companion has 178 additional, fully hash-verified Headered reconstructions, including 30 source-marked Bad variants. Old Headered DAT coverage is **7,100/7,288**; current Headered is **7,091/7,387** and current Headerless is **7,094/7,390**. Six recovered old-DAT games have checksummed TorrentZip plans. Missing ROMs cannot be synthesized from a DAT hash alone.

Original source associations remain separate from verified reconstruction relationships. There are 15 failed candidate pairings, 11 Dumplog hardware-review cases, one Headerless header-field anomaly and one incomplete historical-header note. Steel Legion date variants cross-match after full validation; Pressing Buttons retains its extra non-padding Headerless bytes. Source-level DB hardware fields take precedence over conflicting CSV columns. Official Dumplog status remains separate from local DAT matching.

```sql
SELECT * FROM ni_snapshots;
SELECT status, COUNT(*) FROM v_nointro_status GROUP BY status;
SELECT * FROM v_nointro_headers WHERE file_id = '12868';
SELECT * FROM v_nointro_hardware WHERE archive_id = '1214';
SELECT * FROM ni_reconstructions;
SELECT category, COUNT(*) FROM ni_anomalies GROUP BY category;
```

## RetroAchievements

Each NES ROM has an RA hash (MD5 of the body without the 16-byte header, as rcheevos does) and imported an RA public-API snapshot for console 7. Of 1,123 RA games with achievements, 1,110 have a matching local ROM (3,385 ROMs), 0 are DAT-only, 0 match only a DB Export file and 13 have no No-Intro counterpart (9 hacks). Per-game list: [reports/ra-nes-games.csv](reports/ra-nes-games.csv).

The RetroAchievements-curated NES ROM folder (1,973 ZIPs) is imported with deduplication: 1,256 files that are in a DAT only gain a source link; 691 files found only in the RA set (mostly hacks, translations and homebrew) are stored block-deduplicated in the family of the original they share the most blocks with; 26 files whose hash is not in the latest RA snapshot are listed in [reports/ra-nes-collection-unknown.csv](reports/ra-nes-collection-unknown.csv). `v_ra_collection` gives each file's RA game, DAT entries and release. Famicom Disk System images in that folder belong to another platform and are in [RetroBoxDB-FDS](https://github.com/rshi0212/RetroBoxDB-FDS), not here.

## Batocera / ScreenScraper

All 7,385 frontend releases have virtual placeholders for 17 game-information fields, 8 local-state fields and 15 media roles. Media roles include screenshots, boxes, logos, video, fan art, title screens, manuals, magazines, maps, bezels, cartridges, alternate boxes, box backs, wheels and composites.

Provider-information tables are filled only in the local database; the public Catalog has the same tables without rows. `frontend_game_values` holds local overrides; `frontend_media_slots` links complete future assets through the existing media/files/objects model. No media files are downloaded and there is no Batocera `gamelist.xml` exporter yet. References: [Batocera fields](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/MetaData.cpp), [ScreenScraper API](https://www.screenscraper.fr/webapi2.php), [Batocera adapter](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/scrapers/ScreenScraper.cpp).

```sql
SELECT * FROM v_screenscraper_games WHERE release_id = 1;
SELECT * FROM v_batocera_game_fields WHERE release_id = 1;
SELECT * FROM v_batocera_media_slots WHERE release_id = 1;
```

## Export, maintenance and releases

```bash
# Export by DAT (headered / headerless), 1G1R, RA achievements, TorrentZip or plain ROMs
python3 -B tools/export_set.py RetroBoxDB.NES.sqlite OUT --dat-mode headered --set 1g1r --ra achievements --container torrentzip
# Add new DATs, DB Export / Dump Log snapshots, ROMs and RA snapshots (NES uses its headered/headerless import path and NES DB importer)
python3 -B tools/update_db.py RetroBoxDB.NES.sqlite --discover --ra
# Query-only audit with the Catalog's embedded engine (also: stats, checksums FILE_ID, help)
python3 -B -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); s=c.execute("SELECT content FROM resources WHERE name=?",("engine.py",)).fetchone()[0]; c.close(); exec(compile(s,"RetroBoxDB:engine.py","exec"))' ./RetroBoxDB.NES.Catalog.sqlite audit
```

Releases: a push of `release/catalog-release.json` runs `.github/workflows/publish-catalog.yml`, which starts from the base Catalog pinned by SHA256 in that manifest, injects the unified engine and documents of the commit, checks every data-table digest, integrity, foreign keys, the Catalog audit, the repository tests and the NES embedded test suite, confirms zero free pages and publishes the Release with `SHA256SUMS`. The programs in `resources` are executable code; run them only from a database you built or a Release asset whose SHA256 you verified.

## History

The NES database used formats v1 (1 MiB raw blocks), v2 (8 KiB blocks, XOR deltas) and v3 (2 MiB LZMA2 groups); their programs, reports and designs are kept under `legacy/` in `resources` and in the [NES v3 technical design](RetroBoxDB.NES.Technical-Design.en.md). The measurements recorded at the v3 grouping (original text):

Storage schema v3 places eligible independent LZMA blocks into lossless groups of at most **2 MiB uncompressed**, with a 4 MiB LZMA2 dictionary. It retains each logical block's ID, size and SHA256. Objects still assemble those blocks; Headered files still reference an exact 16-byte header and a shared complete body. Fill, raw, zlib, independent LZMA and bounded XOR-delta representations remain supported.

The reference migration grouped **125,016 blocks into 489 groups**. Their encoded data decreased from 435,766,697 to 342,419,600 bytes: **89.02 MiB saved in compressed streams**. After migration, SQLite compaction and the final documentation/report refresh, the populated database decreased from **629.88 to 534.50 MiB**, a **95.38 MiB / 15.14%** reduction (660,471,808 → 560,463,872 bytes). The release notes and embedded `release-manifest` record final artifact sizes. These measurements are not a promise of the same ratio for other collections.

Export decompresses only the required groups, verifies group and block hashes, assembles the selected ROM/header variant, and checks its full size/CRC32/MD5/SHA1/SHA256. TorrentZip bytes are generated from the existing archive plan and checked against its separately registered output identity. Groups do not change ROM bytes, DAT identities or ZIP checksums. The decoded group cache is bounded to 16 MiB in addition to the existing 64 MiB block cache; individual small reads may decode an entire group. Encoding uses additional temporary memory and at most four workers.

New imports continue to deduplicate and encode ordinary blocks. Run `compact` after a batch to group eligible new blocks and reclaim SQLite free pages. Existing groups are left intact. Compaction is transactional and only adopts groups that save space after a reference/metadata allowance. Schema v2 files remain readable by the v3 engine, but must be migrated before group compaction. Old v2-only engines cannot read v3 databases.

## Platform research

The [English assessment](RetroBoxDB.Platform-Assessment.en.md) and [Chinese assessment](RetroBoxDB.Platform-Assessment.zh-CN.md) cover 329 DAT members and distinguish measured NES results from metadata-derived estimates and proposed platform work. Reproducible aggregate evidence and a read-only survey tool are in `assessment/`; no original DAT, ROM or media files are included. NES remains the implemented platform. The research update does not replace the Catalog release.

