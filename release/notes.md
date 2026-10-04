English/Chinese game names are now included in the NES Catalog, with game identity resolved before parent/clone name inheritance. Storage remains v3; the name extension is v4.

- Retains all 4,453 CSV records and 1,875 unique Chinese names.
- Confirms 4,420 source records; keeps 22 sources for disambiguation and 11 unmatched records for review.
- Provides Chinese names for 4,087 releases and 8,100 local-ROM identities through direct matches or documented group inheritance.
- Parent Chinese coverage: 1,721/3,477 (49.50%); clone coverage: 2,366/3,908 (60.54%).
- Corrects the NHK upper/lower-volume associations and removes 488 previous cross-game source links. Publishers, volumes and cartridge identifiers remain matching evidence.
- Preserves 167 groups with multiple confirmed translations for standard-name review.
- Includes the importer, SQL views, bilingual documentation, decision evidence, review CSVs and validation reports. All 94 embedded tests pass.

The attached Catalog is built from the checksum-pinned previous public Catalog. The release build checks all 53 original data tables, verifies that the new name tables match the local Catalog, checks SQLite integrity and foreign keys, and reruns the embedded test suite.

**No ROM payloads are published.** `compression_groups`, `chunks` and `object_chunks` are empty. The populated `RetroBoxDB.sqlite` remains local. Use the SQLite release attachment and `SHA256SUMS`; the source archive contains code, documentation and name metadata.

[中文说明](https://github.com/rshi0212/RetroBoxDB-NES/blob/main/README.zh-CN.md) · [Matching review](https://github.com/rshi0212/RetroBoxDB-NES/blob/main/reports/game-names-match-review.csv) · [Standard-name review](https://github.com/rshi0212/RetroBoxDB-NES/blob/main/reports/game-names-review.csv)
