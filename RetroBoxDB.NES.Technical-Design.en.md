# RetroBoxDB NES — Storage v3 technical design

> **Historical document.** This describes NES storage v3 as used until 2026-10-05. The NES database now uses storage v4 (family-ordered solid groups, same 16-byte header recipes and 8 KiB blocks); see the [storage v4 technical design](RetroBoxDB.Storage-v4.Technical-Design.en.md). Figures below are the v3-era measurements.

RetroBoxDB is a single-file SQLite archive for exact NES ROM preservation, DAT validation, reversible header variants, hardware provenance, and reproducible export. The populated companion stores payloads and processing code. The public Catalog stores metadata and code without payloads. Python executes the embedded engine; SQLite itself does not execute Python. Runtime requirements are Python 3.10+, SQLite 3.37+, and standard-library `lzma`.

## Logical identity remains independent of encoding

`objects` stores complete file size, CRC32, MD5, SHA1 and SHA256. `files` stores filenames, original paths, origins and archive membership. Multiple file records can share one content identity. Existing object IDs, file IDs, hashes, paths, and game/release associations survive storage migration unchanged. Missing hashes in input DATs remain NULL rather than being invented.

`chunks` retains each plaintext block's immutable ID, SHA256 and size. `object_chunks` retains object offsets, block references, ordering and repetition counts. Storage v3 changes how a block is encoded, not the bytes it identifies or the object topology. Historical source ZIP identities remain distinct from generated ZIP identities. SQL views expose both through `v_file_checksums`, and complete ROM/body identities through `v_rom_checksums`.

## Compression groups

The reference collection uses component-aligned 8 KiB NES blocks. Individual blocks retain support for raw, repeated-byte fill, zlib, raw LZMA2, and compressed XOR differences. Delta chains have at most two dependencies. Complete media and metadata objects use the existing bounded streaming chunk path.

Storage v3 adds `compression_groups` and the `group` chunk codec. A group row contains its ID, uncompressed size, uncompressed SHA256, encoded SHA256, fixed codec identifier `lzma2-4m`, and compressed bytes. The schema caps a group's uncompressed content at **2,097,152 bytes**. The codec uses raw LZMA2 with a 4 MiB dictionary, lc=3, lp=0, pb=0, normal mode, BT4 matching and nice_len=273.

A grouped chunk retains its ID/hash/size and stores a group ID plus a byte offset. Its own data BLOB is empty, base_id is NULL, and delta depth is zero. A unique partial index prevents duplicate group/offset assignments. SQL constraints and insert/update guards check group existence, bounds, mutually exclusive encoding fields, and immutable plaintext identity. An existing XOR block can reference a grouped base because the base's plaintext and depth remain unchanged.

`DB.compact_groups()` selects independent LZMA blocks up to 64 KiB, in block-ID order, and builds groups with at most 2 MiB of plaintext. Fill and existing XOR blocks are not expanded into groups. Eligible ordinary blocks imported after migration can be compacted later. Existing groups are not continually recompressed. This policy is a measured design choice, not proof of a globally minimal representation.

Compression runs in at most four worker threads; database writes remain on the connection's owning thread. Every proposed group is decompressed and byte-compared before acceptance. A group must beat the original encoded lengths by more than a per-member and per-group metadata allowance. This avoids accepting tiny groups with negative practical benefit. The exact resulting SQLite size is measured after VACUUM, since encoded-byte savings do not directly predict page allocation. The existing `v_storage.stored_chunk_bytes` total includes both ordinary chunk BLOBs and shared group BLOBs, without counting group data once per member.

Repacking uses a savepoint. The maintenance operation temporarily removes the general chunk-update prohibition inside that transaction, while retaining the independent plaintext-identity and slice-bound guards. It restores the prohibition before completion. Errors roll back group rows, chunk representation updates and DDL together, then clear decoded caches and the similarity index. Ordinary application writes remain subject to archival immutability. Logical bytes and identities are never intentionally overwritten.

The `compact` CLI commits the repack and runs VACUUM if groups were added, reclaiming free pages. There are no permanent loose compression files. A transient SQLite DELETE journal and temporary migration output are expected during writes; after completion the archive is one persistent database file.

## Reading and verification

The reader first checks the encoded group's SHA256, performs bounded decompression, requires an exact plaintext length and end-of-stream without trailing input, then checks the group's plaintext SHA256. Requested block slices are bounds-checked and independently verified against the original block SHA256. Objects are assembled in original extent order and checked against their complete registered checksum set on audit/export.

Decoded groups use a 16 MiB LRU cache. Existing decoded blocks use a separate 64 MiB cache. These are cache budgets, not a bound on total interpreter or encoder memory. Group metadata is consulted without repeatedly fetching a large compressed BLOB on cache hits. Audits clear both caches before checking stored content. An individual small request may need an entire group to be decompressed; the group limit bounds that amplification.

The v3 engine reads both v2 and v3 populated databases. Group compaction requires v3. A v2-only engine rejects v3 via the storage version marker. `schema.sql` creates v3 fixtures; `build_v3.py` is the current builder, and `build_v2.py` remains a compatibility import alias used by older synthetic test modules. Archived v2 resources remain explicitly historical.

## NES reconstruction

`nes_recipes` stores the exact 16-byte header and complete body-object reference for each Headered identity. Headerless files and multiple Headered variants share a body only when its complete bytes match. Trainer, PRG, CHR, miscellaneous and trailing data retain their exact order and content. Grouping operates below this representation and does not change header bytes, body hashes or file checksums.

Sharing content does not imply identical physical cartridges or releases. `nes_hardware` holds parsed header declarations; `hardware_assertions` holds separately sourced documented claims. A game can have multiple PCB/chip revisions. Header declarations must not silently replace evidence about an actual cartridge.

## Archive identities and TorrentZip

ZIP streams are not retained. `archive_plans` and `archive_entries` describe member names/order, object references, directory topology, profile, and encoder information. A plan is encoded once to calculate size, CRC32, MD5, SHA1 and SHA256, then the stream is discarded. Export regenerates and verifies that byte identity. Existing source ZIP hashes are retained as historical facts, even if canonical re-encoding differs.

The TorrentZip profile normalizes ordering, separators, timestamps, compression settings and the central-directory checksum comment. DAT packages preserve exact member-name case. The implementation supports classic ZIP rather than ZIP64. ROM import has a 256 MiB per-member bound and a 2 GiB expanded ZIP bound; large media uses its separate streaming path. A zlib version change that alters output bytes causes verification failure, not silent replacement of expected checksums.

The exported file is selected by file ID. A filename extension alone does not convert a naked ROM into an archive. Use an archive file ID, or create a package for the chosen DAT game, when a checksummed TorrentZip is required.

## No-Intro DB Export and Dumplog

The No-Intro extension remains version 1. It includes `ni_snapshots`, `ni_archives`, `ni_files`, `ni_sources`, `ni_source_files`, `ni_headers`, `ni_dat_links`, `ni_archive_releases`, `ni_dumplog`, `ni_dumplog_files`, `ni_pair_checks`, `ni_reconstructions`, and `ni_anomalies`. Text IDs preserve leading zeroes; snapshot and source-kind scopes prevent identity collisions. Scene releases are not frontend release IDs. Archive-to-existing-release links have an explicit exact-title association basis.

The importer parses the supplied XML's sibling header/datafile roots without changing the original bytes, rejects entity/DTD declarations, and handles semicolon CSV escaping, parallel multi-file size/MD5 lists and !no_file placeholders. Repeated file IDs must have identical source attributes. A snapshot is atomic and idempotent by its uncompressed XML/CSV SHA256 pair. Raw source members reside only in the populated payload store. ZIP hashes and canonical metadata-archive export plans remain separate.

Snapshot `20261002-002752` retains 7,704 archives, 16,154 independent file identities, 13,930 dump sources, 898 Scene sources and 7,674 Dumplog rows. All current Headered/Headerless DAT targets have matching DB identities, but only 6,298/7,288 old Headered identities appear in this newer DB snapshot. Old DATs and old header history therefore remain necessary.

There are 8,026 declared 16-byte headers and 245 complete historical headers extracted from notes. One Headerless record also carries a header attribute; an incomplete historical header remains text, not guessed bytes. Header interpretation metadata is a declaration, not independent physical verification. All 6,414 serial-bearing source records remain queryable; 6,412 additionally anchor core documented hardware assertions to an existing ROM or release. Official Dumplog verification status is preserved separately from local DAT matching.

Independent reconstruction uses CRC32 algebra only to narrow candidates, then requires actual bytes to satisfy size, CRC32, MD5, SHA1 and SHA256. The companion retains 178 reconstructed Headered variants, including 30 source-marked Bad variants. Six recovered old-DAT targets moved coverage to 7,100/7,288; current Headered/Headerless coverage remains 7,091/7,387 and 7,094/7,390. No missing ROM is created from a hash alone.

Source pairing results remain 7,442 verified pairs, 15 failed candidates, 580 unavailable bodies and three pairs lacking a usable declared header. Failed ambiguous cross-products do not automatically imply erroneous source data. Two Steel Legion date variants cross-match after validation; original associations remain. Pressing Buttons preserves its extra Headerless data. Eleven Dumplog hardware cases remain under review; source-level DB serials take precedence over conflicting CSV fields. All these records survive group migration unchanged.

## Batocera and ScreenScraper placeholders

The frontend extension remains version 1, exposing 17 game-information fields, 8 local-state fields and 15 media roles for all 7,385 existing releases. Shared definitions and views avoid storing repeated empty values. Unknown provider IDs, descriptions, dates, ratings, paths, URLs and checksums remain NULL; a catalog title fallback is labeled. No scraping or media download has occurred and no API credentials are stored.

`frontend_game_values` supports language/region values; `scraper_game_links` tracks confirmed identities and provenance; `frontend_media_slots` links future assets through media/files/objects. Availability requires an actual linked asset, and ownership constraints prevent assigning artwork from unrelated releases. Public Catalog views report payload availability as false.

Initial provider mappings are configurable and distinguish a ScreenScraper game-ID attribute from XML elements. Unsupported mappings remain unknown. The extension supplies schemas and constraints, not a live API client or Batocera gamelist exporter. References: [Batocera fields](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/MetaData.cpp), [ScreenScraper API](https://www.screenscraper.fr/webapi2.php), [Batocera adapter](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/scrapers/ScreenScraper.cpp).

## Public Catalog boundary

The builder creates a fresh SQLite file and copies application metadata while omitting every row of `compression_groups`, `chunks`, and `object_chunks`. Consequently neither independent compressed blocks nor solid group BLOBs enter the public artifact. Free pages are absent after construction. Object identities, ROM/header recipes, archive plans, source paths, parsed DAT entries, all checksum fields and provenance remain available.

Small NES header BLOBs and parsed DAT entry XML are metadata; original ROM bodies, complete DAT/DB/Dumplog files, original ZIP streams and media bytes are not. The catalog is not a standalone content backup. No content operation should claim success from metadata alone.

The public `engine.py` wraps the production engine with `query_only`, rejects content reads/imports/exports/compaction, and restricts its CLI to stats/checksums/audit/help. Its audit verifies SQLite structure, foreign keys, expected checksum-field availability and empty payload tables, explicitly reporting `payloads_verified=false`. The populated engine is retained as `engine.full.py`.

The Catalog exceeds the 100 MiB regular Git limit, so the single SQLite file is a GitHub Release asset linked from the English homepage and Chinese guide. The populated database is not published. Historical public releases remain metadata-only snapshots of their documented storage versions.

## Migration and reproducibility

`migrate_v3.py OLD.sqlite NEW.sqlite` opens the populated v2 source read-only, copies its complete schema and records into a new v3 file, adds the group encoding schema, compacts eligible blocks, and vacuums the output. It refuses an existing output path and removes its failed partial output. It does not overwrite the source. Application tables and logical identities must be compared before installing the migrated file. Use `engine.py NEW.sqlite audit-all` to validate stored contents and every registered generated archive identity.

The reference migration grouped 125,016 blocks into 489 groups. Their encoded streams shrank from 435,766,697 to 342,419,600 bytes (89.02 MiB). After compaction and the final documentation/report refresh, the file shrank from 660,471,808 bytes (629.88 MiB) to 560,463,872 bytes (534.50 MiB), saving 95.38 MiB (15.14%). The release manifest records final artifact byte lengths. Earlier 8 KiB/64 KiB measurements and the v1-to-v2 reduction from 7.95 GiB remain historical collection measurements, not global optimum claims.

Seventy synthetic tests cover the core engine, per-block storage, frontend extension, No-Intro importer and group layer. Group tests exercise preserved block IDs, exact output bytes, header recipes crossing groups, XOR bases moved into groups, repeated compaction, duplicate imports, rollback after encoder failure, corrupted group bytes, invalid offsets, decompression bounds, trailing encoded data, cache reuse, and Catalog exclusion of group payloads.

The reference collection verification compares all pre-existing application tables and block identities, checks every one of 165,019 plaintext blocks, reconstructs all 17,734 available logical objects against their full checksums, and regenerates all 24,487 archive plans against their registered identities. It also checks SQLite integrity and foreign keys. File/ROM/DAT counts and coverage remain unchanged from the preceding No-Intro import.

Current resources include `engine.py`, `schema.sql`, `group_schema.sql`, `migrate_v3.py`, `build_v3.py`, the `build_v2.py` compatibility alias, `seed.json`, `build_catalog.py`, No-Intro sources, five test modules, and the active documentation. In the Catalog, extract `engine.full.py` as `engine.py` for tests or populated-database work. Extract its query wrapper separately as `catalog_engine.py` when reproducing a metadata-only catalog. The Chinese guide provides complete extraction and execution commands.

`group-migration-report`, `group-verification-report`, `test-report`, and `catalog-report` describe the current release. `documentation-index` identifies active documentation and historical resources. Archived v1/v2 designs and reports remain provenance evidence and must not be read as claims about the current storage size, engine compatibility or test count.

## Related platform research

The [English platform assessment](RetroBoxDB.Platform-Assessment.en.md) and [Chinese version](RetroBoxDB.Platform-Assessment.zh-CN.md) evaluate the complete local DAT inventory, including No-Intro, Redump and emulator/media collections. They provide aggregate evidence and future adapter requirements; they do not change the implemented NES schema, engine capabilities or current release assets described here.
