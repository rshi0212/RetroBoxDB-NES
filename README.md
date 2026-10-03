# RetroBoxDB NES

English | [中文说明](README.zh-CN.md)

A SQLite metadata catalog for NES ROM preservation, DAT validation, hardware documentation, and reproducible archive identities. **This public database contains no ROM payloads, original DAT file payloads, or media files.** It preserves the catalog, expected checksums, processing source code, and frontend metadata placeholders.

| File | Purpose |
| --- | --- |
| [RetroBoxDB.NES.Catalog.sqlite](RetroBoxDB.NES.Catalog.sqlite) | Metadata catalog with embedded processing code |
| [RetroBoxDB.NES.Technical-Design.en.md](RetroBoxDB.NES.Technical-Design.en.md) | Detailed technical design |
| [README.zh-CN.md](README.zh-CN.md) | Chinese guide and reproducibility instructions |

The catalog retains 58,747 file records, 17,548 ROM records, 22,065 DAT ROM entries, and 24,479 archive plans. It includes source filenames, game/release associations, parsed DAT entries, validation outcomes, hardware declarations, header variants, and repair history. Small NES header fields and parsed DAT entry XML are retained as metadata.

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

The `resources` table contains the catalog engine (`engine.py`), production engine (`engine.full.py`), complete schema, frontend extension, fixture builder, configuration, and three test modules. To reproduce the tests, extract `engine.full.py` as **`engine.py`**, plus `schema.sql`, `build_v2.py`, `seed.json`, `tests.py`, `tests_storage.py`, and `tests_frontend.py` into a separate directory, then run:

```bash
python3 -B -m unittest -v tests tests_storage tests_frontend
```

All 47 tests passed using synthetic fixtures. The [Chinese guide](README.zh-CN.md) includes a complete extraction command. Reproducing the original collection requires the same ROM/DAT inputs and a separate populated working database. The test builder uses 4 KiB NES blocks; the populated reference collection selected 8 KiB blocks after measurement.

The full storage design combines shared NES bodies and independent headers, block deduplication, lossless compression, and bounded delta references. ZIP plans are encoded once to calculate expected output checksums, then regenerated and verified on export. Historical reference reports describe the populated collection; `catalog-report` and `frontend-report` describe this edition and its frontend extension.
