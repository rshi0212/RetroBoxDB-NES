# RetroBoxDB: platform suitability and local DAT assessment

English | [中文报告](RetroBoxDB.Platform-Assessment.zh-CN.md) | [Project homepage](README.md)

Published 2026-10-04; local inventory collected 2026-10-03, Asia/Shanghai. This is a research report and implementation roadmap. **NES is implemented; the other platform adapters described here are proposals, not newly supported import/export features.** This documentation update does not change the populated NES database or the public Catalog release.

## Findings and recommended order

For the actual collections found locally, prioritize **FBNeo → MAME ROMs → HBMAME ROMs** as a shared arcade workstream, and **GBA → SNES → Mega Drive → GB/GBC** as the next cartridge workstream. Arcade lists supply strong whole-file sharing evidence; cartridges are closer to the existing NES architecture. Continue with **PlayStation → Saturn → PC Engine CD / Mega CD / Neo Geo CD** once streaming disc support exists. Visual Pinball offers substantial shared assets but needs a separate dependency-aware frontend model. Large encrypted discs and timing-sensitive dumps require specialized preservation work.

These are engineering priorities, not a universal compression leaderboard. A tiny collection with a high duplicate percentage can save less space than a large collection with a modest percentage. No measured SQLite saving is claimed outside NES.

- Latest local FBNeo packaging lists: **13.511 GiB / 19.496%** repeated declared file bytes across 18 DAT members. Arcade-only: **26.179%**.
- Selected Demul, FBNeo, HBMAME and MAME ROM collections: **67.047 GiB** additional shared declared bytes across collections, after deduplicating each collection separately. The FBNeo scope includes its console lists, samples and HDD entries.
- Visual Pinball: **139.873 GiB / 8.550%** repeated declared file bytes, across a much larger catalog. These are not 139.873 GiB of measured recoverable space in the user's existing archives.
- MAME merged and split ROM manifests describe the **same eligible unique content set**. Do not count them as two independent collections or add their within-layout savings together.
- NES measured v3 migration: **629.875 → 534.500 MiB**, saving **95.375 MiB / 15.142%** relative to the previous deduplicated database. This is an incremental compression result, not the total saving against source ZIPs.

## Scope and evidence

The survey inventories **172 ZIP archives**, parses **329 DAT XML members**, and selects the latest available snapshot of **134 local series** containing **274 selected DAT members**. It retains 38 older archives in the inventory. A series can be a format, packaging layout or provenance role; it is not necessarily a platform. The 9 auxiliary archives comprise NES DB Export, NES Dumplog and 7 Redump layout bundles. DB Export and layout bundles are inventoried, not flattened into generic ROM statistics.

| Family / 来源 | ZIPs | Parsed DATs / 已解析 DAT | Latest series / 最新本地系列 | Selected DATs / 选用 DAT |
| --- | --- | --- | --- | --- |
| Demul | 2 | 2 | 2 | 2 |
| FBNeo | 2 | 36 | 1 | 18 |
| HBMAME | 3 | 4 | 3 | 4 |
| MAME | 4 | 4 | 4 | 4 |
| No-Intro | 85 | 83 | 60 | 58 |
| Redump | 75 | 68 | 63 | 56 |
| Visual Pinball | 1 | 132 | 1 | 132 |


Evidence is separated into: **measured** (existing NES verification and local directory sizes), **DAT-derived** (declared sizes and hashes), and **engineering inference** (expected usefulness of blocks, deltas and format adapters). “Latest” means latest in this directory, not latest available upstream. Provider packaging versions and embedded DAT versions are separate facts.

The public evidence consists of [all 172 archive rows](assessment/data/dat-inventory.csv), [aggregate and per-member statistics](assessment/data/dat-survey.json), [local directory size totals](assessment/data/local-collection-sizes.json), and the [survey implementation](assessment/tools/survey_datfiles.py). It contains no original DAT, ROM, disc, image or video payload. DAT/archive names, source SHA256 hashes and summary counts are retained. No per-game ROM hash list is exported by this survey.

### Meaning of the numbers

Eligible identity is `(declared size, SHA1)` for a non-`nodump` ROM/file record with a valid SHA1 and nonnegative size. `baddump` entries remain distinct preservation candidates; malformed/unknown identities are excluded. Repeated bytes = sum of eligible file occurrences − sum of unique eligible identities. These estimates require later verification against actual bytes and stronger internal identities; SHA1 equality in a DAT is not a byte-comparison proof. Missing hashes remain unknown.

For Redump, the media table excludes `.cue`, `.gdi`, `.sbi`, `.sub`, `.txt`, `.log`, `.mds` and `.ccd` from its estimator. Exclusion is only statistical: these files must still be preserved when present. “Media records” means eligible non-sidecar files, not necessarily CD tracks or whole discs. Separate CHD `disk` identities have no comparable declared file size here.

No compression experiment was performed on other platforms. Estimates do not include block sharing, regional/revision deltas, SQLite/index overhead, source ZIP savings, inherited emulator dependencies, CHD/RVZ compression, or scratch-space requirements. Never compare raw DAT totals directly with compressed SQLite and call the difference measured deduplication.

## Arcade: highest new whole-file sharing opportunity

| Local snapshot / 本地版本 | Sets | Files | Disk refs | Raw GiB | Repeated GiB | Repeated % |
| --- | --- | --- | --- | --- | --- | --- |
| Demul 0.7_180428 CHDs (split) | 106 | 0 | 106 | 0.000 | 0.000 | N/A |
| Demul 0.7_180428 ROMs (split) | 313 | 2025 | 0 | 23.911 | 0.199 | 0.834% |
| FBNeo 1.0.0.3 260723 GIT7a28a7d debug ROMs (split) | 25444 | 89621 | 0 | 69.303 | 13.511 | 19.496% |
| HBMAME 0.288.2 ROMs (merged) | 750 | 26102 | 0 | 51.654 | 1.112 | 2.152% |
| HBMAME 0.288.2 Rollback CHDs | 6 | 0 | 6 | 0.000 | 0.000 | N/A |
| HBMAME 0.288.2 Software List ROMs (merged) | 266 | 266 | 0 | 7.513 | 0.000 | 0.000% |
| MAME 0.288 CHDs (merged) (dir2dat) | 687 | 1042 | 0 | 1,049.274 | 2.817 | 0.268% |
| MAME 0.288 CHDs (merged) | 687 | 0 | 1042 | 0.000 | 0.000 | N/A |
| MAME 0.288 ROMs (merged) | 16146 | 169543 | 0 | 194.093 | 4.012 | 2.067% |
| MAME 0.288 ROMs (split) | 43220 | 184891 | 0 | 200.818 | 10.737 | 5.347% |
| Visual Pinball (2026-01-02) | 13670 | 298098 | 0 | 1,635.854 | 139.873 | 8.550% |


Raw and repeated columns concern eligible `rom` file records only. A CHD-only `disk` row has N/A savings, not proven zero benefit. MAME CHD dir2dat instead describes physical `.chd` files. Visual Pinball appears here for comparable file-level statistics, not because it is a MAME ROM set.

The selected manifests have **zero `cloneof`, `romof`, `device_ref` and ROM `merge` attributes**. They are flattened packaging inventories. They can specify the listed packages, but cannot alone reconstruct arbitrary merged/split/non-merged dependency rules. Obtain matching-build emulator `-listxml`, software lists or native FBNeo metadata, and preserve provider/build/list/set identities plus BIOS/device/parent relationships. [MAME set semantics](https://docs.mamedev.org/usingmame/aboutromsets.html), [MAME command line](https://docs.mamedev.org/commandline/commandline-all.html), [software lists](https://docs.mamedev.org/contributing/softlist.html), [FBNeo documentation](https://github.com/finalburnneo/FBNeo/wiki).

HBMAME's hacks and homebrew can share base ROMs with MAME and with each other. Whole-file sharing is evidenced; additional block/delta gains still need measurement. Its local software-list bundle is labeled **0.288.2**, while member headers say **0.245.31**. Preserve both. Its 266 software records include 265 `.neo` files and one `.7z`; a DAT-target `.7z` is itself a file whose bytes must be preserved, not automatically an expendable outer import wrapper. Rollback CHDs retain a historical role. Demul ROM overlap with MAME makes shared storage useful despite only 0.834% within-Demul repetition. [HBMAME project](https://hbmame.1emulation.com/).

### Cross-collection overlap

Sum of independently deduplicated selected collections: **320.127 GiB**. Their global union: **253.080 GiB**. Difference: **67.047 GiB**. Pairwise figures below are descriptive and **must not be added** because three-way and four-way overlaps would be counted repeatedly. MAME uses split only; HBMAME uses its ROM merged list only; FBNeo uses all 18 current members; Demul uses ROMs only. CHDs are excluded.

| Collection A | Collection B | Shared identities | Shared GiB |
| --- | --- | --- | --- |
| Demul ROMs | FBNeo | 73 | 2.746 |
| Demul ROMs | HBMAME ROMs merged | 22 | 0.826 |
| Demul ROMs | MAME ROMs split | 1994 | 23.424 |
| FBNeo | HBMAME ROMs merged | 10322 | 16.042 |
| FBNeo | MAME ROMs split | 55569 | 26.982 |
| HBMAME ROMs merged | MAME ROMs split | 8290 | 9.587 |


### CHD has two different checksum domains

MAME's `disk sha1` identifies CHD logical content according to the CHD format/version; CHD v5 distinguishes raw-data and overall data/metadata hashes. A dir2dat SHA1 hashes the encoded `.chd` file byte stream. Recompression can preserve logical content while changing the physical file hash. Record both identities, codec/version, metadata, parent dependency and source-file identity. Do not substitute one SHA1 for the other. [chdman documentation](https://docs.mamedev.org/tools/chdman.html).

For a concrete local example, `dvp-0027a` has disk SHA1 `da1aacee9e32e813844f4d434981e69cc5c80682`; dir2dat reports file SHA1 `d3ec0dd0532b4c362957c116dfcf39ff0293c855` and size 3,317,217,136 bytes. The MAME logical catalog has 1,042 disk references without sizes; the physical dir2dat catalog has 1,042 `.chd` file occurrences and only **0.268%** whole-file repetition. This says nothing about potential decoded block overlap.

Storing existing CHDs as opaque objects preserves exact encoded files with little integration risk. Sharing decoded blocks can improve cross-game reuse but adds a new adapter and cannot promise restoration of the original CHD encoding unless that encoding is separately preserved or reproducible exactly. CHD parent/delta chains must retain every required parent.

## No-Intro: cartridge priorities and format boundaries

| Profile | Suitability and action |
| --- | --- |
| N0 | NES implemented: shared full body, exact old/new headers, block sharing and lossless compression. |
| N1 | Next cartridge priorities: GBA, SNES, Mega Drive, GB/GBC; substantial local collections and relatively simple exact-byte reconstruction. |
| N2 | Good ordinary cartridge candidates; generally smaller absolute benefit. Preserve internal headers, mapper/bank/mirroring metadata and original chip order. |
| N2B | N64: canonical byte order can share content only when multiple byte-order representations actually exist. Record and reverse the exact transform. |
| N3 | Format-aware adapter first: multipart cartridges, FDS/QD, 64DD, mixed containers or required companion assets. |
| N4 | DS/DSi and decrypted 3DS/New 3DS: promising large-file/block research, but streaming, filesystems and crypto boundaries increase implementation cost. |
| N5 | IPF, flux and waveform preservation: exact-source storage first; do not infer lossless timing recovery from a normalized logical image. |

The local compressed collection totals are:

| Measured directory group / 已测量目录组 | Files | Stored GiB |
| --- | --- | --- |
| No-Intro | 48115 | 29.347 |
| FBNeo 1.0.0.3 260723 GIT7a28a7d debug ROMs (split) | 25446 | 33.617 |


These are file-size sums, not DAT-validated completion counts. No-Intro has 48,115 files (48,111 ZIPs and 4 text files); Aftermarket/Private directories are grouped with their base platform. GBA occupies about **14.422 GiB**, SNES **3.994**, Mega Drive **3.928**, GBC **1.056**, GB **0.289**. This supports the proposed local cartridge order. FBNeo has 25,446 files, approximately **33.617 GiB**, and is already a practical next source for a pilot. Directory presence does not prove every DAT-listed item is present.

Key constraints:

- **GBA / GB / GBC:** cartridge-internal headers are bytes of the ROM. They may be modeled as segments, but must not be discarded as external wrappers. Store save type, mapper and other hardware annotations with source and confidence. [Game Boy header specification](https://github.com/gbdev/pandocs/blob/master/src/The_Cartridge_Header.md).
- **SNES:** distinguish an external 512-byte copier header from the internal ROM header. LoROM/HiROM, enhancement chips, SRAM and region belong in metadata; neither “header correction” nor checksum repair may overwrite the preserved source. [SNES ROM formats](https://snes.nesdev.org/wiki/ROM_file_formats).
- **Mega Drive / 32X:** plain ROM blocks are straightforward; interleaved or byte-swapped alternate formats require detected, reversible transforms. Extension alone is insufficient, and no saving is claimed unless those variants are present.
- **Atari 7800 / Lynx:** local lists are BIN and LYX. If corresponding external-header variants are imported, share verified bodies and retain each original header. Do not assume such variants are already in the local collection.
- **N64:** byte-swap or word-swap using detected byte order; preserve the internal ROM header and exact length. The local No-Intro series is BigEndian, so a theoretical multi-order saving is not an observed saving. [N64 formats](http://n64dev.org/romformats.html).
- **FDS/QD:** an optional FDS wrapper is separate from disk-side data. QD is not merely FDS with another header: FDS commonly has 65,500-byte sides, while QD has 65,536-byte sides and CRC fields. Preserve checksums, ordering, padding and exceptions in a reversible recipe. [FDS file format](https://www.nesdev.org/wiki/FDS_file_format), [disk format](https://www.nesdev.org/wiki/FDS_disk_format).
- **DS/DSi/3DS:** preserve filesystem offsets, secure/encrypted areas, signatures, padding and exact trim status. Decrypted does not mean all contained data is highly compressible. A reconstructed playable image is insufficient if it fails the original DAT identity. [3DS RomFS](https://www.3dbrew.org/wiki/RomFS), [AES registers](https://3dbrew.org/wiki/AES_Registers).
- **Mixed and unusual sources:** Atari 2600 includes WAVs; Commodore 64 includes CRT/D64/PRG and chip data; VIC-20 may contain address-specific chips; Intellivision mixes BIN/INT/ROM. GP32 `.smc` is not automatically SNES. Game & Watch ROM dumps do not imply complete artwork preservation. NES and Satellaview lists also contain auxiliary files; retain them.
- **Timing-bearing sources:** Atari ST has 546 IPF files; Sharp X1 has 8 WAVs; the X68000 Flux set has 336 RAW members in one set. Logical-sector conversion may not preserve original timing, protection or signal data. Use exact blob/block compression first and retain raw source identities. [Greaseweazle image formats](https://github.com/keirf/greaseweazle/wiki/Supported-Image-Types/a8b5dc0199b156ef95bd9039277b3e9d4cde28d4).

### Complete latest-local No-Intro platform table

Profiles describe engineering suitability, not measured compression ratios. “Sets” are DAT records, not a normalized count of distinct games. Largest file size helps expose importer limits.

| No-Intro series / 系列 | Profile | Sets | File records | Largest file MiB |
| --- | --- | --- | --- | --- |
| Atari - Atari 2600 | N2 | 888 | 894 | 9.15 |
| Atari - Atari 5200 | N2 | 207 | 207 | 0.04 |
| Atari - Atari 7800 (BIN) | N2 | 243 | 243 | 0.50 |
| Atari - Atari Jaguar (J64) | N2 | 279 | 279 | 16.00 |
| Atari - Atari Lynx (LYX) | N2 | 434 | 434 | 0.50 |
| Atari - Atari ST | N5 | 404 | 546 | 1.06 |
| Bandai - WonderSwan | N2 | 257 | 257 | 16.00 |
| Bandai - WonderSwan Color | N2 | 253 | 253 | 8.00 |
| Coleco - ColecoVision | N2 | 201 | 201 | 0.03 |
| Commodore - Commodore 64 | N3 | 349 | 398 | 0.50 |
| Commodore - VIC-20 | N3 | 293 | 310 | 0.02 |
| Fairchild - Channel F | N2 | 37 | 37 | 0.01 |
| Funtech - Super Acan | N2 | 12 | 13 | 3.00 |
| GCE - Vectrex | N2 | 48 | 48 | 0.03 |
| GamePark - GP32 | N3 | 35 | 35 | 33.00 |
| Hartung - Game Master | N2 | 19 | 19 | 0.03 |
| Magnavox - Odyssey 2 | N2 | 133 | 133 | 0.01 |
| Mattel - Intellivision | N3 | 264 | 315 | 0.40 |
| Microsoft - MSX | N2 | 952 | 952 | 2.00 |
| Microsoft - MSX2 | N2 | 201 | 201 | 1.22 |
| NEC - PC Engine - TurboGrafx-16 | N2 | 509 | 509 | 2.50 |
| NEC - PC Engine SuperGrafx | N2 | 6 | 6 | 1.00 |
| Nintendo - Family Computer Disk System (FDS) | N3 | 407 | 407 | 0.12 |
| Nintendo - Family Computer Disk System (QD) | N3 | 296 | 296 | 0.12 |
| Nintendo - Game & Watch | N3 | 53 | 54 | 0.00 |
| Nintendo - Game Boy | N1 | 2292 | 2292 | 2.00 |
| Nintendo - Game Boy Advance | N1 | 3749 | 3749 | 32.00 |
| Nintendo - Game Boy Color | N1 | 2614 | 2614 | 16.00 |
| Nintendo - New Nintendo 3DS (Decrypted) | N4 | 11 | 11 | 4096.00 |
| Nintendo - Nintendo 3DS (Decrypted) | N4 | 2161 | 2161 | 4096.00 |
| Nintendo - Nintendo 64 (BigEndian) | N2B | 1261 | 1261 | 64.00 |
| Nintendo - Nintendo 64DD | N3 | 35 | 35 | 61.92 |
| Nintendo - Nintendo DS (Decrypted) | N4 | 7708 | 7708 | 512.00 |
| Nintendo - Nintendo DSi (Decrypted) | N4 | 68 | 78 | 512.00 |
| Nintendo - Nintendo Entertainment System (Headered) | N0 | 7385 | 7387 | 64.00 |
| Nintendo - Nintendo Entertainment System (Headerless) | N0 | 7388 | 7390 | 64.00 |
| Nintendo - Pokemon Mini | N2 | 46 | 46 | 0.50 |
| Nintendo - Satellaview | N2 | 603 | 604 | 1.00 |
| Nintendo - Sufami Turbo | N2 | 13 | 13 | 1.00 |
| Nintendo - Super Nintendo Entertainment System | N1 | 4318 | 4318 | 8.00 |
| Nintendo - Virtual Boy | N2 | 80 | 80 | 16.00 |
| Philips - Videopac+ | N2 | 34 | 34 | 0.02 |
| SNK - NeoGeo Pocket | N2 | 13 | 13 | 2.00 |
| SNK - NeoGeo Pocket Color | N2 | 128 | 128 | 4.00 |
| Sega - 32X | N2 | 227 | 227 | 4.00 |
| Sega - Beena | N2 | 58 | 58 | 8.00 |
| Sega - Game Gear | N2 | 928 | 928 | 1.00 |
| Sega - Master System - Mark III | N2 | 1240 | 1240 | 4.00 |
| Sega - Mega Drive - Genesis | N1 | 3485 | 3486 | 9.25 |
| Sega - PICO | N2 | 447 | 447 | 4.00 |
| Sega - SG-1000 - SC-3000 | N2 | 247 | 247 | 0.16 |
| Sharp - X1 (Waveform) | N5 | 8 | 8 | 23.25 |
| Sharp - X68000 (Flux) | N5 | 1 | 336 | 0.43 |
| Tiger - Game.com | N2 | 25 | 25 | 2.00 |
| VTech - CreatiVision | N2 | 39 | 39 | 0.02 |
| VTech - V.Smile | N2 | 454 | 455 | 16.00 |
| Watara - Supervision | N2 | 74 | 74 | 0.50 |
| Welback - Mega Duck | N2 | 26 | 26 | 0.12 |


## Redump: disc priorities

| Profile | Priority and required work |
| --- | --- |
| R1 | First disc pilots: PS1, Saturn, PCE CD, Mega CD and Neo Geo CD. Whole-track repetition and regional/revision sharing justify testing. |
| R2 | Other predominantly CD collections: same track/layout foundation, usually less absolute evidence or smaller collections. |
| R2D | Dreamcast: GD-ROM track geometry and GDI/CUE representations need a dedicated exact-layout adapter. |
| R3 | PS2/PSP and larger DVD-style images: streaming block deduplication; whole-image equality is a weak measure of shared internal content. |
| R3W | GameCube/Wii: investigate reversible junk/padding reconstruction and compare against RVZ, with exception storage and full round-trip verification. |
| R4 | Mixed PC/arcade packages, Xbox/Xbox 360 and PS3: protection, keys, unusual layouts or media formats require case-by-case adapters. |

PS1 has **394.661 GiB / 8.410%** repeated eligible media bytes; Saturn **140.174 GiB / 13.959%**; PCE CD **37.475 GiB / 15.762%**; Mega CD **25.139 GiB / 10.597%**; Neo Geo CD **6.610 GiB / 11.025%**. These are strong metadata-level reasons to test track sharing, not guaranteed gains over CHD. Konami System GV reaches 48.161%, but only two sets are listed: percentage alone would give a misleading priority.

For CD images, preserve every original track identity, sector mode, track order, index/pregap, and available CUE/GDI/SUB/SBI/MDS/CCD or other companion file. Any regenerated EDC/ECC, zero region or audio representation needs exact validation and exceptions for nonstandard sectors. A valid Redump BIN/ISO does not automatically contain all physical copy-protection information. [Redump MDF/MDS guide](https://wiki.redump.info/MDF/MDS_Dumping_Guide).

For GameCube/Wii, Dolphin's RVZ specification is a useful existing baseline: it models generated junk data and Wii-specific encoding details. Do not merely remove “unused” bytes and claim losslessness. Preserve all required seeds, parameters and exceptions; compare against the same actual RVZ collection. [WIA/RVZ specification](https://github.com/dolphin-emu/dolphin/blob/master/docs/WiaAndRvz.md).

For Xbox and PS3, explicitly distinguish dump variants and encrypted/decrypted bytes. Keys needed for exact transforms must have provenance and a private storage policy; the presence of a DAT does not provide missing keys. [Xbox disc structure](https://xboxdevwiki.net/Xbox_Game_Disc), [Redump PS3 guide](https://wiki.redump.info/Sony_PlayStation_3_Dumping_Guide).

The local layout bundles have unequal coverage: Dreamcast has **1,516 CUE members versus 1,427 GDI members**. Match layouts to disc identities instead of assuming one-to-one completeness. Redump set counts and media file counts in the appendix are not interchangeable.

### Complete latest-local Redump platform table

Zero whole-file repetition does not imply zero block sharing or poor compression. Values are rounded to three decimals; the JSON retains integer byte totals.

| Redump series / 系列 | Profile | Sets | Media records | Raw media GiB | Repeated GiB | Repeated % |
| --- | --- | --- | --- | --- | --- | --- |
| Acorn - Archimedes | R2 | 79 | 147 | 31.594 | 0.000 | 0.000% |
| Apple - Macintosh | R2 | 1357 | 2902 | 1,058.103 | 0.427 | 0.040% |
| Arcade - Konami - FireBeat | R4 | 10 | 10 | 15.496 | 0.000 | 0.000% |
| Arcade - Konami - System 573 | R4 | 44 | 281 | 11.289 | 0.288 | 2.549% |
| Arcade - Konami - System GV | R4 | 2 | 70 | 0.962 | 0.463 | 48.161% |
| Arcade - Konami - e-Amusement | R4 | 49 | 49 | 65.890 | 0.000 | 0.000% |
| Arcade - Namco - Sega - Nintendo - Triforce | R4 | 22 | 66 | 24.389 | 0.069 | 0.283% |
| Arcade - Namco - System 246 | R4 | 13 | 13 | 32.809 | 0.000 | 0.000% |
| Arcade - Sega - Chihiro | R4 | 19 | 57 | 21.098 | 0.059 | 0.281% |
| Arcade - Sega - Lindbergh | R4 | 71 | 71 | 186.056 | 0.000 | 0.000% |
| Arcade - Sega - Naomi | R4 | 34 | 102 | 37.793 | 0.155 | 0.410% |
| Arcade - Sega - Naomi 2 | R4 | 13 | 39 | 14.427 | 0.047 | 0.325% |
| Arcade - Sega - RingEdge | R4 | 49 | 49 | 216.573 | 0.000 | 0.000% |
| Arcade - Sega - RingEdge 2 | R4 | 42 | 42 | 193.498 | 0.000 | 0.000% |
| Atari - Jaguar CD Interactive Multimedia System | R2 | 38 | 479 | 10.484 | 0.681 | 6.498% |
| Bandai - Pippin | R2 | 34 | 34 | 15.754 | 0.000 | 0.000% |
| Bandai - Playdia Quick Interactive System | R2 | 38 | 74 | 23.899 | 0.000 | 0.000% |
| Commodore - Amiga CD | R2 | 596 | 942 | 343.500 | 0.631 | 0.184% |
| Commodore - Amiga CD32 | R2 | 207 | 1547 | 47.400 | 0.087 | 0.183% |
| Commodore - Amiga CDTV | R2 | 61 | 243 | 16.541 | 0.000 | 0.000% |
| Fujitsu - FM-Towns | R2 | 947 | 12408 | 300.241 | 5.646 | 1.880% |
| IBM - PC compatible | R4 | 58837 | 144393 | 71,844.839 | 311.094 | 0.433% |
| Incredible Technologies - Eagle | R4 | 7 | 7 | 3.693 | 0.000 | 0.000% |
| Mattel - Fisher-Price iXL | R2 | 26 | 26 | 2.848 | 0.000 | 0.000% |
| Mattel - HyperScan | R2 | 8 | 8 | 1.072 | 0.000 | 0.000% |
| Memorex - Visual Information System | R2 | 72 | 126 | 17.369 | 0.000 | 0.000% |
| Microsoft - Xbox | R4 | 2683 | 2683 | 19,288.165 | 0.000 | 0.000% |
| Microsoft - Xbox 360 | R4 | 3691 | 3691 | 27,420.571 | 0.000 | 0.000% |
| NEC - PC Engine CD & TurboGrafx CD | R1 | 551 | 15760 | 237.765 | 37.475 | 15.762% |
| NEC - PC-88 series | R2 | 4 | 100 | 1.938 | 0.123 | 6.351% |
| NEC - PC-98 series | R2 | 127 | 1135 | 28.559 | 0.000 | 0.000% |
| NEC - PC-FX & PC-FXGA | R2 | 79 | 867 | 44.392 | 0.910 | 2.051% |
| Nintendo - GameCube | R3W | 2019 | 2019 | 2,742.752 | 0.000 | 0.000% |
| Nintendo - Wii | R3W | 3780 | 3780 | 16,669.960 | 0.000 | 0.000% |
| Palm | R4 | 159 | 159 | 19.071 | 0.000 | 0.000% |
| Panasonic - 3DO Interactive Multiplayer | R2 | 672 | 672 | 322.097 | 0.000 | 0.000% |
| Philips - CD-i | R2 | 2425 | 3868 | 1,230.885 | 5.164 | 0.420% |
| Photo CD | R2 | 266 | 2053 | 103.796 | 0.437 | 0.421% |
| PlayStation GameShark Updates | R2 | 34 | 1249 | 7.656 | 0.211 | 2.752% |
| Pocket PC | R4 | 82 | 82 | 15.568 | 0.000 | 0.000% |
| SNK - Neo Geo CD | R1 | 111 | 3246 | 59.957 | 6.610 | 11.025% |
| Sega - Dreamcast | R2D | 1516 | 11090 | 1,625.357 | 65.855 | 4.052% |
| Sega - Mega CD & Sega CD | R1 | 549 | 7877 | 237.228 | 25.139 | 10.597% |
| Sega - Prologue 21 | R2 | 30 | 896 | 19.058 | 0.000 | 0.000% |
| Sega - Saturn | R1 | 2457 | 28118 | 1,004.188 | 140.174 | 13.959% |
| Sharp - X68000 | R2 | 30 | 155 | 12.197 | 0.000 | 0.000% |
| Sony - PlayStation | R1 | 10914 | 49254 | 4,693.035 | 394.661 | 8.410% |
| Sony - PlayStation 2 | R3 | 11774 | 11812 | 26,112.510 | 0.643 | 0.002% |
| Sony - PlayStation 3 | R4 | 4503 | 4503 | 38,259.542 | 0.000 | 0.000% |
| Sony - PlayStation Portable | R3 | 3500 | 3500 | 3,141.323 | 0.000 | 0.000% |
| TAB-Austria - Quizard | R2 | 15 | 20 | 5.854 | 0.011 | 0.187% |
| Tomy - Kiss-Site | R2 | 30 | 142 | 3.467 | 0.056 | 1.609% |
| VM Labs - NUON | R3 | 11 | 11 | 15.840 | 0.000 | 0.000% |
| VTech - V.Flash & V.Smile Pro | R3 | 51 | 51 | 22.615 | 0.000 | 0.000% |
| ZAPiT Games - Game Wave Family Entertainment System | R3 | 16 | 16 | 52.584 | 0.000 | 0.000% |
| funworld - Photo Play | R4 | 17 | 17 | 10.240 | 0.000 | 0.000% |


## Visual Pinball and multimedia collections

The 132 DAT members contain 13,670 set records and 298,098 file occurrences. Eligible bytes total **1,635.854 GiB**, unique declared identities **1,495.981 GiB**, and repeated bytes **139.873 GiB**. Much of the content is MP4/OGG/MP3/PNG/JPG plus VPT/VPX tables and companion resources. Exact whole-file asset reuse is attractive; recompressing already encoded media may yield little and must never be lossy.

Model tables, PinMAME ROM dependencies, PuP packs, B2S backglasses, scripts, relative paths and media roles independently. Shared artwork can serve multiple games without merging their game identities. A VPX edit or repack is not automatically byte-identical restoration. Batocera/ScreenScraper descriptions, artwork and video slots should refer to reusable content objects, retain provider IDs/language/region/provenance and have separate availability states. This extends the existing frontend placeholder concept; it does not mean these assets have been imported. [Visual Pinball project](https://github.com/vpinball/vpinball).

## Which DATs and supporting metadata to keep

Use the latest applicable full-content DAT as the validation target, and retain historical DAT snapshots for old-to-new identity mapping. Parent/clone XML is useful for game relationships and candidate grouping, but relationships are not proof of identical bytes. The directory provides No-Intro Parent-Clone lists plus NES DB Export and Dumplog; no claim is made to have inspected absent Standard/Scene/Daily variants here. Treat update-only or release-oriented lists as additional views with explicit scope, not silent replacements for the complete target catalog.

NES DB Export and Dumplog are valuable for source/revision/hardware/dump provenance, and were already integrated in the NES work. Hardware annotations may be partial or conflicting: retain source, version and confidence rather than presenting inferred values as universal truth. Redump layout bundles, matching-build emulator XML, and both CHD logical and physical catalogs add information that a plain checksum list cannot supply. Never delete an old DAT merely because a new one exists.

| Auxiliary archive / 辅助压缩包 | Role / 类型 | Members |
| --- | --- | --- |
| NEC - PC Engine CD & TurboGrafx CD - Cuesheets (551) (2026-06-14 14-24-19).zip | disc-layout-bundle | 551 |
| Nintendo - Nintendo Entertainment System (DB Export) (20261002-002752).zip | provenance-db-export | 1 |
| Nintendo - Nintendo Entertainment System (Headered) (Dump Log) (20261002-002752).zip | provenance-dumplog | 1 |
| Panasonic - 3DO Interactive Multiplayer - Cuesheets (672) (2026-06-09 14-48-47).zip | disc-layout-bundle | 672 |
| SNK - Neo Geo CD - Cuesheets (111) (2026-05-06 12-21-03).zip | disc-layout-bundle | 111 |
| Sega - Dreamcast - Cuesheets (1516) (2026-06-14 18-25-41).zip | disc-layout-bundle | 1516 |
| Sega - Dreamcast - GDI Files (1427) (2026-06-14 13-24-27).zip | disc-layout-bundle | 1427 |
| Sega - Mega CD & Sega CD - Cuesheets (549) (2026-05-28 18-06-58).zip | disc-layout-bundle | 549 |
| Sega - Saturn - Cuesheets (2457) (2026-06-14 12-36-08).zip | disc-layout-bundle | 2457 |


## Proposed storage and implementation gates

1. Keep a single SQLite artifact with content-addressed objects, exact file identities, independently versioned source catalogs and platform adapters. Names, paths and case belong to memberships/export plans, not to physical deduplication keys. Identical bytes may share storage across emulator families without merging their catalog identities.
2. Preserve original objects and logical decoded content as separate identities. Record ordered segments, exact external headers, transforms, parameters, exceptions, hardware metadata and lineage. Do not deduplicate solely on titles or parent/clone labels.
3. Keep lossless block compression and bounded delta chains; benchmark fixed, aligned and content-defined chunks against real data. Count indexes/recipes/groups and random-export cost. Already compressed containers can remain opaque when decoding gives no worthwhile net gain.
4. Store expected CRC32/MD5/SHA1/SHA256 for every relevant identity when available, including raw/headered/headerless bytes, tracks, source archives and generated exports. Expected and computed values have separate provenance and availability. Canonical TorrentZip output is generated at export time and has its own checksums; it need not reproduce the original source ZIP byte stream.
5. Build streaming large-object and archive support before large-platform imports. The current NES path has a 256 MiB ROM limit, a 2 GiB expanded ZIP import limit and classic ZIP export without ZIP64. Some FBNeo files already exceed these bounds; generic asset support does not establish a working large-disc importer.
6. Pilot representative revisions, regions, multi-track discs, protected sectors, encrypted examples, large files and already compressed media. Verify **every preserved object** by reassembly and available original hashes, plus internal SHA256; test exported packages independently. Record actual original ZIP/CHD/RVZ bytes, final compacted SQLite bytes, temporary space, import time and cold/warm export time.
7. Adopt a new adapter only after full round-trip correctness and a worthwhile measured storage/performance tradeoff. Keep migrations transactional and retain a rollback copy. Publish payload-free research/catalogs; keep ROM, original DAT and media data local.

## Reproduce the DAT analysis

Python 3.10+ standard library; read-only access to the source directory. The script understands this inventory's ZIP/XML naming and schemas, rejects unhandled files and oversized XML members, and does not download or extract original DATs onto disk. The NES DB Export is inventoried by source hash because its provenance structure is handled by the existing NES-specific importer.

```sh
python3 -B assessment/tools/survey_datfiles.py /path/to/Datfiles /tmp/retroboxdb-survey
python3 -B -m unittest discover -s assessment/tools -p 'test_*.py' -v
```

The directory-size JSON is a separate point-in-time file-size observation; it is not produced by the DAT parser. Updated source archives naturally produce different survey results. Source archive and member SHA256 hashes identify exactly which inputs were assessed. Nine synthetic tests cover identity eligibility, duplicate accounting, CHD hash separation, sidecar exclusion, relationship counting, entity rejection, timestamp selection and multi-member aggregation.

### Complete selected FBNeo member table

| FBNeo DAT member | Sets | Files | Raw GiB | Repeated GiB |
| --- | --- | --- | --- | --- |
| arcade.dat | 8457 | 71897 | 51.531 | 13.490 |
| channelf.dat | 50 | 52 | 0.001 | 0.000 |
| coleco.dat | 656 | 659 | 0.025 | 0.000 |
| fds.dat | 207 | 207 | 0.023 | 0.000 |
| gamegear.dat | 635 | 635 | 0.205 | 0.000 |
| hdd.dat | 2 | 2 | 0.548 | 0.000 |
| megadrive.dat | 2921 | 2928 | 4.151 | 0.009 |
| msx.dat | 1797 | 1822 | 0.120 | 0.000 |
| nes.dat | 2905 | 2905 | 0.735 | 0.000 |
| ngp.dat | 174 | 175 | 0.214 | 0.000 |
| pce.dat | 376 | 376 | 0.155 | 0.000 |
| samples.dat | 65 | 596 | 6.918 | 0.008 |
| sg1000.dat | 255 | 255 | 0.007 | 0.000 |
| sgx.dat | 10 | 10 | 0.007 | 0.000 |
| sms.dat | 858 | 858 | 0.199 | 0.000 |
| snes.dat | 2625 | 2625 | 4.242 | 0.000 |
| spectrum.dat | 3349 | 3517 | 0.181 | 0.003 |
| tg16.dat | 102 | 102 | 0.040 | 0.000 |
