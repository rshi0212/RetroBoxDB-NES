# RetroBoxDB NES

English | [中文说明](README.zh-CN.md)

A single-file SQLite archive design for NES preservation: exact ROM identities, shared bodies and headers, block deduplication, lossless grouped compression, DAT validation, dump provenance, and checksummed TorrentZip exports.

**The public Catalog contains no ROM bodies, original DAT/DB/Dumplog file payloads, compressed content groups, or media payloads.** The populated `RetroBoxDB.sqlite` remains local. The Catalog retains metadata, expected checksums, small NES header fields, reconstruction recipes, and processing source code. It cannot independently restore or export the missing files.

| Download / document | Purpose |
| --- | --- |
| [RetroBoxDB.NES.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-NES/releases/latest/download/RetroBoxDB.NES.Catalog.sqlite) | Current metadata-only SQLite, distributed through GitHub Releases |
| [Technical design](RetroBoxDB.NES.Technical-Design.en.md) | Storage format, invariants, migration, and validation |
| [中文说明](README.zh-CN.md) | Chinese guide, extraction, and maintenance commands |
| [Platform assessment — English](RetroBoxDB.Platform-Assessment.en.md) / [中文](RetroBoxDB.Platform-Assessment.zh-CN.md) | No-Intro, Redump, MAME, FBNeo, HBMAME, Demul and Visual Pinball; 172 local DAT archives |

The Catalog exceeds GitHub's 100 MiB regular Git file limit. Download the SQLite attachment from Releases; the repository's source-code ZIP contains documentation and assessment tools/data, not the database attachment. The attachment remains one ordinary SQLite file.

## Platform research

The [English assessment](RetroBoxDB.Platform-Assessment.en.md) and [Chinese assessment](RetroBoxDB.Platform-Assessment.zh-CN.md) cover 329 DAT members and distinguish measured NES results from metadata-derived estimates and proposed platform work. Reproducible aggregate evidence and a read-only survey tool are in `assessment/`; no original DAT, ROM or media files are included. NES remains the implemented platform. The research update does not replace the Catalog release.

## English / Chinese CSV names

Both local databases retain all **4,453 rows** from `Nintendo - Nintendo Entertainment System.csv`, including **3,703 rows** with Chinese names. Name extension v4 resolves game identity before accepting matches: **4,420 source rows** match **4,429 releases, 2,023 games and 8,896 ROM records**; **3,698 releases** have directly matched Chinese names. **22 rows** remain review candidates and **11 rows** have no base-title candidates. These are name associations, not new checksum verification or ROM payloads. The storage format remains v3.

The **3,703 translated rows share 1,875 unique Chinese names** in `game_chinese_names`, referenced by `game_name_entries.name_cn_id`. Identical Chinese names are stored once across English titles, regions and revisions. `v_release_chinese_names` returns deduplicated Chinese names for each release. `game_name_imports` and `game_name_entries` retain original and cleaned English names, source record numbers and SHA256 provenance; `release_name_links` records associations. The original CSV text, including original Chinese strings, any BOM and original newlines, is embedded in `resources` for provenance.

Removing parentheses now generates search candidates and concise display names; it does not establish identity across different games. Matching tries complete titles, equivalent parsed qualifiers, then compatible identifying fields. Every confirmed source row resolves to exactly one `game_id`. Parsed evidence retains regions, languages, versions and identity tags. Unknown tags remain identifying evidence, including volumes, publishers and cartridge IDs. The known publisher aliases `Bulletproof`/`Bullet-Proof` are normalized and qualifier order is ignored. Regions and Beta/Proto stages can disambiguate independent games. Unresolved candidates are excluded from standard-name and inheritance evidence.

NHK sixth-grade `(Jou)`/`(Ge)` now receive only the upper/lower translation respectively. The independent `Baseball (USA) (Intellivision)` no longer receives the Nintendo Baseball translation from another game. This correction removes **488 previous cross-game source links**; some other version-level matches become explicitly inherited names. Original CSV rows, deduplicated Chinese names and game groups remain intact. `game_name_match_decisions` records parsed evidence and decisions. [game-names-match-review.csv](reports/game-names-match-review.csv) lists unresolved sources, and [game-names-matching-changes.json](reports/game-names-matching-changes.json) records changed name associations.

Parent/clone releases share Chinese names through their existing `game_id`. **1,556 groups** have exactly one confirmed translation, used as their automatic standard name. **14 parents and 375 clones** inherit names. Effective coverage reaches **4,087 releases and 8,100 local ROM records**. At the release level, parent Chinese coverage is **49.50%** (1,721/3,477), and clone coverage is **60.54%** (2,366/3,908). These percentages measure Chinese coverage, not direct English-title matching. The previous 4,112-release figure included associations without sufficient identity evidence and is superseded.

The **167 groups with multiple confirmed translations** remain `needs_review` with no selected standard; their confirmed aliases remain available. **1,754 groups** have no confirmed Chinese name. [game-names-review.csv](reports/game-names-review.csv) lists standard-name candidates and their source titles, separately from the 22 sources with unresolved game identity. SQLite views derive standards and inheritance dynamically, without duplicating Chinese strings or claiming inherited names as direct CSV matches. Adding a conflicting translation automatically stops inheritance for that group. `v_game_chinese_name_evidence` traces each group alias to its source release and CSV record.

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
python3 -B tools/import_game_names.py "$HOME/下载/Nintendo - Nintendo Entertainment System.csv" RetroBoxDB.sqlite RetroBoxDB.NES.Catalog.sqlite
python3 -B -m unittest discover -s tests -v
```

## Storage v3: grouped compression

Storage schema v3 places eligible independent LZMA blocks into lossless groups of at most **2 MiB uncompressed**, with a 4 MiB LZMA2 dictionary. It retains each logical block's ID, size and SHA256. Objects still assemble those blocks; Headered files still reference an exact 16-byte header and a shared complete body. Fill, raw, zlib, independent LZMA and bounded XOR-delta representations remain supported.

The reference migration grouped **125,016 blocks into 489 groups**. Their encoded data decreased from 435,766,697 to 342,419,600 bytes: **89.02 MiB saved in compressed streams**. After migration, SQLite compaction and the final documentation/report refresh, the populated database decreased from **629.88 to 534.50 MiB**, a **95.38 MiB / 15.14%** reduction (660,471,808 → 560,463,872 bytes). The release notes and embedded `release-manifest` record final artifact sizes. These measurements are not a promise of the same ratio for other collections.

Export decompresses only the required groups, verifies group and block hashes, assembles the selected ROM/header variant, and checks its full size/CRC32/MD5/SHA1/SHA256. TorrentZip bytes are generated from the existing archive plan and checked against its separately registered output identity. Groups do not change ROM bytes, DAT identities or ZIP checksums. The decoded group cache is bounded to 16 MiB in addition to the existing 64 MiB block cache; individual small reads may decode an entire group. Encoding uses additional temporary memory and at most four workers.

New imports continue to deduplicate and encode ordinary blocks. Run `compact` after a batch to group eligible new blocks and reclaim SQLite free pages. Existing groups are left intact. Compaction is transactional and only adopts groups that save space after a reference/metadata allowance. Schema v2 files remain readable by the v3 engine, but must be migrated before group compaction. Old v2-only engines cannot read v3 databases.

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

## Batocera / ScreenScraper

All 7,385 frontend releases have virtual placeholders for 17 game-information fields, 8 local-state fields and 15 media roles. Unknown descriptions, dates, ratings, provider IDs, URLs and checksums remain NULL. No live scraping, media download or credential storage has occurred. Media roles include screenshots, boxes, logos, video, fan art, title screens, manuals, magazines, maps, bezels, cartridges, alternate boxes, box backs, wheels and composites.

`frontend_game_values` supports locales; `scraper_game_links` records confirmed provider identities; `frontend_media_slots` links complete future assets through the existing media/files/objects model. This supplies schemas and mappings, not a live scraping client or Batocera `gamelist.xml` exporter. References: [Batocera fields](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/MetaData.cpp), [ScreenScraper API](https://www.screenscraper.fr/webapi2.php), [Batocera adapter](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/scrapers/ScreenScraper.cpp).

```sql
SELECT * FROM v_screenscraper_games WHERE release_id = 1;
SELECT * FROM v_batocera_game_fields WHERE release_id = 1;
SELECT * FROM v_batocera_media_slots WHERE release_id = 1;
```

## Embedded code and validation

Python 3.10+, SQLite 3.37+, and standard-library `lzma` are required. SQLite itself does not execute Python. Query the Catalog without extracting source:

```bash
python3 -B -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); s=c.execute("SELECT content FROM resources WHERE name=?",("engine.py",)).fetchone()[0]; c.close(); exec(compile(s,"RetroBoxDB:engine.py","exec"))' ./RetroBoxDB.NES.Catalog.sqlite stats
```

Use `checksums FILE_ID`, `audit`, or `help` in place of `stats`. The catalog engine enables `query_only`, rejects content operations, and reports `payloads_verified=false`.

The resources include the catalog engine (`engine.py`), production engine (`engine.full.py`), `schema.sql`, `build_v3.py`, the compatibility alias `build_v2.py`, `seed.json`, `group_schema.sql`, `migrate_v3.py`, `nointro.py`, `nointro_schema.sql`, `build_catalog.py`, and five synthetic test modules. The [Chinese guide](README.zh-CN.md) has a complete extraction command. Extract the production resource as **`engine.py`** to run:

```bash
python3 -B -m unittest -v tests tests_storage tests_frontend tests_nointro tests_groups
```

All **70 synthetic tests** pass. The group migration additionally verifies all 165,019 block identities/content, 17,734 available logical objects and 24,487 generated archive plans. Group checks include compressed and uncompressed SHA256; object/archive checks include the full registered checksum set. Tests cover corruption, cross-group reads, grouped delta bases, rollback, duplicate imports, source anomalies and Catalog payload exclusion.

With extracted production code and separately supplied inputs:

```bash
# Build a separate v3 file; the old populated database is opened read-only.
python3 -B migrate_v3.py OLD.sqlite NEW.sqlite
python3 -B engine.py NEW.sqlite audit-all

# Import a No-Intro snapshot into a populated database, then compact new blocks.
python3 -B nointro.py RetroBoxDB.sqlite '/path/NES DB Export.zip' '/path/NES Dump Log.zip'
python3 -B engine.py RetroBoxDB.sqlite compact

# Export an existing file identity, or generate its checksummed archive plan.
python3 -B engine.py RetroBoxDB.sqlite export FILE_ID '/path/output.nes'
```

`migrate_v3.py` refuses an existing output path and does not overwrite its input. Migration temporarily requires both files; ordinary writes use a transient rollback journal. After committing and closing, the working archive has one persistent SQLite file. Current documentation is indexed by the embedded `documentation-index`; older reports and `legacy/` resources are historical evidence, not current size/test claims.
