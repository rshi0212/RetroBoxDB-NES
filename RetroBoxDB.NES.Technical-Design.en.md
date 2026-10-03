RetroBoxDB v2 — Technical Design and Metadata Catalog

RetroBoxDB is a single-file SQLite archive for ROM preservation, DAT-based validation, reversible NES header variants, and reproducible export. All persistent application data and the Python processing engine live inside SQLite. Processing is executed by a host Python interpreter; SQLite itself does not execute the embedded Python code. The runtime requires Python 3.10 or later, SQLite 3.37 or later, and the standard-library lzma module.

Logical identity and physical storage are separate. The objects table records the complete logical file size, CRC32, MD5, SHA1, and SHA256. The files table records names, origins, and archive membership, allowing multiple source files to refer to one content identity. SHA256 identifies shared content. Immutable archival tables preserve previous identities; repairs create new versions rather than overwrite old bytes.

NES Headered files are represented as an exact 16-byte header plus a reference to the complete body. Headerless files and Headered variants can share that body when their bytes are identical. Each complete Headered variant retains its own file checksums. Trainer data, PRG, CHR, miscellaneous sections, and trailing bytes remain recoverable in their original order. Shared bytes do not imply identical cartridges, hardware, regions, or releases. Parsed mapper, submapper, memory, timing, and other header declarations remain separate from documented hardware assertions and their provenance.

The storage engine splits NES bodies at known component boundaries and then into configurable blocks. The populated database selects 8 KiB blocks. Identical blocks are shared across games and revisions. Each block uses the smallest selected representation among raw bytes, repeated-byte fill, zlib, and raw LZMA2; similar blocks may use a compressed XOR delta when it saves space. Delta chains are limited to two dependencies. Integer block references, offsets, and consecutive-repeat counts describe file assembly. Decoded blocks are verified against their plaintext SHA256, and reconstructed files are checked against their complete checksum set. Generic assets use larger streaming chunks rather than NES-specific splitting.

ZIP byte streams are not retained. An archive plan stores member names, order, content references, directory information, the packing profile, and encoder information. A new plan is actually encoded once so that its output size, CRC32, MD5, SHA1, and SHA256 can be calculated; the compressed stream is then discarded. Export rebuilds the ZIP and verifies it against these registered values. Original source ZIP checksums remain historical identities and are distinct from the generated ZIP checksums. v_file_checksums exposes source_* and export_* fields, while v_rom_checksums exposes complete ROM and body checksums. A compression-library change that alters output bytes causes verification to fail rather than silently change the expected archive identity.

The implemented TorrentZip profile normalizes member ordering, path separators, timestamps, compression settings, and the central-directory checksum comment. DAT packages use the DAT's exact member names, including case. The current writer supports classic ZIP rather than ZIP64. ROM processing has a 256 MiB per-member limit, with a 2 GiB expanded-size limit for ROM ZIP imports. Large media assets have a separate streaming import/export path.

DAT snapshots, parsed records, validation outcomes, naming decisions, repair evidence, and transformations have dedicated tables. Candidate CRC matches are insufficient for a repair: the result must satisfy all checksums supplied by the target DAT. Hardware assertions, game/release associations, scraping responses, and complete image, audio, and video data have storage and linkage interfaces. The current processing implementation focuses on NES; additional platform parsers can use the common object, metadata, and asset model.

Reference results describe the populated companion database, not this metadata catalog. The measured migration reduced its file from 8,541,569,024 to 623,771,648 bytes (594.88 MiB), a 92.70% reduction. Whole-corpus measurements selected 8 KiB blocks and 64 KiB SQLite pages among the implemented candidates. This is an empirical choice, not a proof of a globally minimal encoding. The populated collection passed 39 automated tests, full reconstruction checks for 17,554 available objects, generation and verification of 24,479 distinct ZIP plans, and 36 final export samples. All 14,181 pre-existing DAT packages retained their byte identities. These counts are historical validation evidence, not payload content included in this catalog.

This catalog is built into a fresh SQLite file by copying every application table except chunks and object_chunks. It preserves all game and release records, source filenames, paths, object identities, full checksum sets, parsed DAT entries, validation results, hardware declarations, NES header recipes, archive plans, and provenance. The complete ROM bodies, DAT source-file byte streams, auxiliary file payloads, and media payloads are absent. Small NES headers and parsed DAT XML entries remain metadata; there are no content blocks from which to reconstruct the original ROM or DAT files. Building a new file avoids deleted payload data remaining in SQLite free pages.

Every pre-existing logical file checksum, ROM/body checksum, and generated archive checksum is copied unchanged. The catalog retains expected values even though it cannot reproduce file contents independently. Source ZIP checksums and generated TorrentZip checksums remain separate in v_file_checksums. Parsed DAT fields retain the values supplied by each DAT; an absent DAT checksum is not invented. All current game-specific metadata remains available for browsing and comparing external files.

The embedded catalog engine supports stats, checksums, help, and metadata audit. It enables SQLite query_only for its connection and rejects import, repair, packaging, and export commands. Its audit explicitly reports payloads_verified=false: it checks database structure, foreign keys, and checksum-field availability, rather than claiming to revalidate missing file bytes. The original populated database is required for reconstruction, full content audits, and export. This catalog is not a standalone content backup.

The catalog retains the production engine as engine.full.py for reference. resources also contains the schema, design documentation, tests using synthetic data, and historical reports. Original collection and storage reports are reference evidence about the populated source, not current catalog storage measurements; catalog-report contains this edition's validation and size. SQLite uses DELETE journaling; after closing a committed connection, no persistent journal is required beside the database.

Read this document with:
SELECT content FROM resources WHERE name='TECHNICAL-DESIGN.en';

Inspect file or ROM identities with:
SELECT * FROM v_file_checksums WHERE file_id=1;
SELECT * FROM v_rom_checksums WHERE rom_id=1;
SELECT * FROM archive_plans WHERE id=1;
SELECT content FROM resources WHERE name='catalog-report';

Run the embedded catalog engine without extracting files:
python3 -B -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); s=c.execute("SELECT content FROM resources WHERE name=?",("engine.py",)).fetchone()[0]; c.close(); exec(compile(s,"RetroBoxDB:engine.py","exec"))' ./RetroBoxDB.NES.Catalog.sqlite stats

Replace stats with checksums FILE_ID, audit, or help. SQLite viewers can inspect the game catalog and expected checksums directly. The companion RetroBoxDB.sqlite is unchanged and retains all original payloads.
