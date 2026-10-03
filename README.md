# RetroBoxDB NES

English | [中文说明](README.zh-CN.md)

A SQLite metadata catalog for NES ROM preservation, DAT validation, hardware documentation, and reproducible archive identities. **This public database contains no ROM payloads, original DAT file payloads, or media files.** It preserves the catalog, expected checksums, processing source code, and frontend metadata placeholders.

| File | Purpose |
| --- | --- |
| [RetroBoxDB.NES.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-NES/releases/latest/download/RetroBoxDB.NES.Catalog.sqlite) | Metadata catalog with embedded processing code |
| [RetroBoxDB.NES.Technical-Design.en.md](RetroBoxDB.NES.Technical-Design.en.md) | Detailed technical design |
| [README.zh-CN.md](README.zh-CN.md) | Chinese guide and reproducibility instructions |

Download the single SQLite file from the link above (GitHub Releases). The expanded catalog exceeds the 100 MiB regular Git file limit; the repository keeps the documentation and release download link.

The catalog retains 58,935 file records, 17,726 ROM records, 22,065 DAT ROM entries, and 24,487 archive plans. It includes source filenames, game/release associations, parsed DAT entries, validation outcomes, hardware declarations, header variants, and repair history. Small NES header fields and parsed DAT entry XML are retained as metadata.

The payload tables `chunks` and `object_chunks` are empty. The catalog was built into a fresh file, so deleted ROM/DAT content is not left in free pages. The populated database is not included in this repository. **The catalog cannot independently reconstruct or export the original files.**

Existing checksums were preserved and compared against the populated database. Logical file identities include size, CRC32, MD5, SHA1, and SHA256. Headered ROMs and their shared bodies have separate identities. Original ZIP checksums and generated TorrentZip checksums remain distinct. Missing checksum fields in a source DAT are not invented.

```sql
SELECT * FROM v_file_checksums WHERE file_id = 1;
SELECT * FROM v_rom_checksums WHERE rom_id = 1;
SELECT * FROM archive_plans WHERE id = 1;
SELECT content FROM resources WHERE name = 'catalog-report';
```

Batocera / ScreenScraper placeholders cover all 7,385 catalog releases: 17 game-information fields, 8 local frontend-state fields, and 15 media roles. These are virtual placeholders generated from shared definitions, avoiding repeated empty rows. Descriptions, dates, ratings, languages/regions, provider IDs, artwork paths, and media checksums remain unknown until populated. A catalog title fallback is explicitly labeled. No live scraping has been performed and no API credentials are stored.

Media slots include screenshots, thumbnails/boxes, logos, videos, fan art, title screens, manuals, magazines, maps, bezels, cartridges, alternate box art, box backs, wheels, and composite images. Initial provider mappings are configurable; unsupported or unconfirmed mappings remain NULL. The definitions follow [Batocera metadata fields](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/MetaData.cpp), with provider mappings informed by the [ScreenScraper API](https://www.screenscraper.fr/webapi2.php) and [Batocera's adapter](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/scrapers/ScreenScraper.cpp).

```sql
SELECT * FROM v_screenscraper_games WHERE release_id = 1;
SELECT * FROM v_batocera_game_fields WHERE release_id = 1;
SELECT * FROM v_batocera_media_slots WHERE release_id = 1;
SELECT * FROM frontend_fields WHERE category = 'media';
```

`frontend_game_values` supports language and region variants. `scraper_game_links` records confirmed provider identities and provenance. `frontend_media_slots` can link to `media`, whose complete asset bytes and checksums use the existing `files → objects → chunks` model in a populated database. The extension supplies schemas, mappings, states, and constraints; it does not implement a live ScreenScraper client or a Batocera gamelist exporter. A future adapter must select a concrete ROM variant and convert provider values to the required frontend representation.

Python 3.10+, SQLite 3.37+, and the Python standard-library `lzma` module are required to run the embedded engine. SQLite itself does not execute Python. From the downloaded files' directory:

```bash
python3 -B -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); s=c.execute("SELECT content FROM resources WHERE name=?",("engine.py",)).fetchone()[0]; c.close(); exec(compile(s,"RetroBoxDB:engine.py","exec"))' ./RetroBoxDB.NES.Catalog.sqlite stats
```

Replace `stats` with `checksums 1`, `audit`, or `help`. The catalog engine enables `query_only` and rejects content operations. Its audit checks metadata integrity and explicitly reports `payloads_verified=false`.

The `resources` table contains the catalog engine (`engine.py`), production engine (`engine.full.py`), complete schema, frontend extension, fixture builder, configuration, and four test modules. To reproduce the tests, extract `engine.full.py` as **`engine.py`**, plus `schema.sql`, `build_v2.py`, `seed.json`, `tests.py`, `tests_storage.py`, `tests_frontend.py`, `tests_nointro.py`, `nointro.py`, and `nointro_schema.sql` into a separate directory, then run:

```bash
python3 -B -m unittest -v tests tests_storage tests_frontend tests_nointro
```

All 58 tests passed using synthetic fixtures. The [Chinese guide](README.zh-CN.md) includes a complete extraction command. Reproducing the original collection requires the same ROM/DAT inputs and a separate populated working database. The test builder uses 4 KiB NES blocks; the populated reference collection selected 8 KiB blocks after measurement.

The full storage design combines shared NES bodies and independent headers, block deduplication, lossless compression, and bounded delta references. ZIP plans are encoded once to calculate expected output checksums, then regenerated and verified on export. Historical reference reports describe the populated collection; `catalog-report` and `frontend-report` describe this edition and its frontend extension.


## NES DB Export and Dumplog snapshot

The `20261002-002752` import adds 7,704 No-Intro archive identities, 16,154 distinct file records, 13,930 dump sources, 898 Scene release records, and 7,674 Dumplog status rows. Scene releases have their own ID namespace and are not frontend release IDs. Source files are linked through a many-to-many relation, preserving repeated independent dump evidence without duplicating ROM bytes.

The snapshot retains 8,026 declared 16-byte headers (including one on a Headerless-classified record), 245 complete historical headers extracted from notes, and one incomplete historical-header note as an anomaly. Header declarations are distinct from documented PCB/chip evidence. All 6,414 source records with serial information are retained; 6,412 can also anchor a `hardware_assertions` record to an existing ROM or release. Their confidence is `documented`, not independently hardware-verified.

The populated companion reconstructed 178 additional Headered objects using existing bodies and supplied headers, checking size, CRC32, MD5, SHA1, and SHA256. Of these, 30 retain the source's Bad flag. Six previously missing old-DAT targets were recovered and have new TorrentZip plans with complete output checksums. Old Headered coverage is now 7,100/7,288; current Headered remains 7,091/7,387 and current Headerless remains 7,094/7,390. These describe the populated companion; this catalog still contains no ROM body bytes.

Source relationships remain separate from verified reconstruction relationships. There are 15 failed candidate pairings (including ambiguous cross-products), 11 Dumplog hardware-review cases, one Headerless header-field anomaly, and one incomplete historical-header note. Two Steel Legion demo associations cross-match after full checksum validation. Pressing Buttons has extra non-padding bytes in its Headerless record; no bytes were discarded. DB per-source serials take precedence over conflicting Dumplog hardware columns. Official Dumplog verification status is retained separately from local DAT match status.

```sql
SELECT * FROM ni_snapshots;
SELECT status, COUNT(*) FROM v_nointro_status GROUP BY status;
SELECT * FROM v_nointro_headers WHERE file_id = '12868';
SELECT * FROM v_nointro_hardware WHERE archive_id = '1214';
SELECT * FROM ni_reconstructions;
SELECT category, COUNT(*) FROM ni_anomalies GROUP BY category;
SELECT content FROM resources WHERE name = 'nointro-import-report';
```

New embedded resources include `nointro.py`, `nointro_schema.sql`, `tests_nointro.py`, and `build_catalog.py`. After extracting these and the production engine as `engine.py`, import your own inputs into a populated working database with:

```bash
python3 -B nointro.py RetroBoxDB.sqlite '/path/NES DB Export.zip' '/path/NES Dump Log.zip'
```

The importer is transactional and idempotent for the same pair of input hashes. It handles the DB export's sibling top-level XML nodes, escaped semicolon CSV, multi-file rows, and no-file placeholders. It rejects catalog imports, conflicting file IDs, malformed hashes, and entity declarations. The original DB XML and Dumplog CSV are stored only in the populated companion's deduplicated content store. Source ZIP identities and canonical export checksums are preserved separately; ZIP streams are regenerated on export. The public catalog excludes those raw source payloads, ROM bodies, and all media payloads.
