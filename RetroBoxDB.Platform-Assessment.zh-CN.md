# RetroBoxDB：平台适合程度与本地 DAT 评估

[English report](RetroBoxDB.Platform-Assessment.en.md) | 中文 | [项目首页](README.md)

> **实施状态（2026-10-05）**：NES、SNES、Mega Drive、Game Boy、Game Boy Color、Game Boy Advance、Famicom Disk System（FDS／QD）七个平台已实现，均使用存储 v4，参数按各平台实测确定，并已导入 RetroAchievements 整理的 ROM 目录，见 [存储 v4 说明](RetroBoxDB.Storage-v4.zh-CN.md)。Satellaview 作为独立平台，计划以后单独建库，不并入 SNES。下文是 2026-10-04 的调查原文，其中的数字和建议未随后续实施更新。

发布日期：2026-10-04；本地盘点日期：2026-10-03，Asia/Shanghai。本报告是研究结论与实施路线。**NES 已实现，其他平台的适配方案仍属于建议，并不表示现在已经支持导入或导出。** 本次文档更新不修改含游戏的 NES 本地数据库，也不更换公开 Catalog 发布附件。

## 结论与推荐顺序

结合实际发现的本地收藏，建议把 **FBNeo → MAME ROM → HBMAME ROM** 作为共享街机内容的实施方向；卡带方向则按 **GBA → SNES → Mega Drive → GB/GBC** 推进。街机有明确的整文件重复证据，卡带更接近现有 NES 架构。具备流式光盘处理能力后，再做 **PlayStation → Saturn → PC Engine CD／Mega CD／Neo Geo CD**。Visual Pinball 共享资源较多，但需要独立的依赖和前端资源模型；大型加密光盘、保留时序的转储应专门处理。

这是工程优先级，不是通用压缩率排行榜。很小的平台即使重复比例高，绝对收益也可能很少。除 NES 外，本次没有其他平台的 SQLite 实测节省比例。

- 本地最新 FBNeo 的 18 份清单，声明的重复文件字节为 **13.511 GiB／19.496%**；只看 arcade 清单则为 **26.179%**。
- 选定的 Demul、FBNeo、HBMAME、MAME ROM 清单，各自去重之后再跨集合共享，额外重合 **67.047 GiB**。其中 FBNeo 包含主机清单、samples 和 HDD 条目。
- Visual Pinball 声明重复文件字节为 **139.873 GiB／8.550%**，但清单本身体量很大。这不是用户现有压缩文件已经实测可以减少的空间。
- MAME merged 与 split 清单的**有效唯一内容集合完全相同**，不能当成两套独立收藏，也不能把两种布局的内部去重收益相加。
- 已完成的 NES v3 迁移实测：**629.875 → 534.500 MiB**，相对上一版已经去重的数据库再减少 **95.375 MiB／15.142%**。这是增量压缩收益，不是相对原始 ZIP 的总节省率。

## 范围与证据

共盘点 **172 个 ZIP 压缩包**，解析 **329 个 DAT XML 成员**，按 **134 个本地系列**选择最新快照，其中有 **274 个选用的 DAT 成员**。另外 38 个历史压缩包也保留在清单中。系列可能代表格式、打包布局或来源角色，并不等于平台。9 个辅助包分别为 NES DB Export、NES Dumplog 和 7 个 Redump 布局包。DB Export 和布局包只作专项盘点，不混入普通 ROM 统计。

| Family / 来源 | ZIPs | Parsed DATs / 已解析 DAT | Latest series / 最新本地系列 | Selected DATs / 选用 DAT |
| --- | --- | --- | --- | --- |
| Demul | 2 | 2 | 2 | 2 |
| FBNeo | 2 | 36 | 1 | 18 |
| HBMAME | 3 | 4 | 3 | 4 |
| MAME | 4 | 4 | 4 | 4 |
| No-Intro | 85 | 83 | 60 | 58 |
| Redump | 75 | 68 | 63 | 56 |
| Visual Pinball | 1 | 132 | 1 | 132 |


证据分为三种：**实测**（已有 NES 验证及本地目录大小）、**DAT 推算**（声明大小和校验值）、**工程判断**（分块、差分、格式适配的预期价值）。文中“最新”均指目录内最新，不代表上游最新。分发包版本与内部 DAT 版本分别记录。

公开资料包括：[172 个压缩包清单](assessment/data/dat-inventory.csv)、[汇总和逐 DAT 成员统计](assessment/data/dat-survey.json)、[本地目录大小统计](assessment/data/local-collection-sizes.json)、[调查程序](assessment/tools/survey_datfiles.py)。其中没有原始 DAT、ROM、光盘、图片或视频数据，只保留 DAT／压缩包名称、来源 SHA256 和汇总结果；本次调查也没有输出逐游戏 ROM 校验列表。

### 数值如何计算

有效身份使用 `(声明大小, SHA1)`：必须不是 `nodump`，具有合法 SHA1 和非负大小。`baddump` 仍作为需要保存的内容；未知或不合法身份不进入估算。重复字节＝所有有效文件出现次数对应的大小之和－有效唯一内容的大小之和。后续必须用实际文件及更强的内部校验确认，DAT 中 SHA1 相同不能代替逐字节验证。缺失校验值仍是未知。

Redump 的媒体统计排除了 `.cue`、`.gdi`、`.sbi`、`.sub`、`.txt`、`.log`、`.mds`、`.ccd`。这只是统计口径，文件实际存在时仍要保存。“媒体条目”是排除辅助文件后的有效条目，不一定就是音轨或完整光盘。CHD 的 `disk` 身份另计，此处没有可直接比较的声明文件大小。

其他平台没有进行压缩实验。这些估算没有包含块级共享、地区／修订差分、SQLite 索引和配方开销、现有 ZIP 压缩、隐含模拟器依赖、CHD／RVZ 压缩或临时空间。不能把 DAT 的未压缩总量直接与压缩数据库相比，并称之为实测去重收益。

## 街机：新增整文件共享最值得优先验证

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


Raw 与 Repeated 列仅统计有效的 `rom` 文件记录。只有 `disk` 的 CHD 行标为 N/A，不表示确定没有收益。MAME CHD dir2dat 统计的是物理 `.chd` 文件。Visual Pinball 放在这里便于比较文件级统计，不代表它属于 MAME ROM 集。

选用的清单中，**`cloneof`、`romof`、`device_ref` 和 ROM `merge` 属性数量全部为零**。这些是展开后的打包清单，可以描述现有包，却不能单独推导任意 merged／split／non-merged 依赖。需要补充对应构建版本的模拟器 `-listxml`、software list 或 FBNeo 原生元数据，保留来源、构建、清单、集合身份以及 BIOS／设备／父子关系。[MAME 集合语义](https://docs.mamedev.org/usingmame/aboutromsets.html)、[命令行说明](https://docs.mamedev.org/commandline/commandline-all.html)、[软件清单](https://docs.mamedev.org/contributing/softlist.html)、[FBNeo 文档](https://github.com/finalburnneo/FBNeo/wiki)。

HBMAME 的修改版和自制内容可以与 MAME、其他修改版共享基础 ROM。整文件共享已有证据，额外的块级／差分收益仍需测试。本地 software-list 外包版本为 **0.288.2**，内部成员头部版本却为 **0.245.31**，应同时保留。266 个软件条目含 265 个 `.neo` 和 1 个 `.7z`；DAT 直接校验的 `.7z` 本身就是待保存文件，不能默认当作可丢弃的外层导入包装。Rollback CHD 仍有历史保存价值。Demul 内部重复率仅 0.834%，但与 MAME 的共有内容使跨集合共享值得做。[HBMAME 项目](https://hbmame.1emulation.com/)。

### 跨集合共有内容

选定集合分别去重后合计 **320.127 GiB**；全局唯一内容为 **253.080 GiB**，差额 **67.047 GiB**。下表两两重合**不能相加**，否则会重复计算三方、四方共享。MAME 只使用 split ROM；HBMAME 只使用 merged ROM；FBNeo 使用当前全部 18 份清单；Demul 只使用 ROM。CHD 不参与此项统计。

| Collection A | Collection B | Shared identities | Shared GiB |
| --- | --- | --- | --- |
| Demul ROMs | FBNeo | 73 | 2.746 |
| Demul ROMs | HBMAME ROMs merged | 22 | 0.826 |
| Demul ROMs | MAME ROMs split | 1994 | 23.424 |
| FBNeo | HBMAME ROMs merged | 10322 | 16.042 |
| FBNeo | MAME ROMs split | 55569 | 26.982 |
| HBMAME ROMs merged | MAME ROMs split | 8290 | 9.587 |


### CHD 有两个不同的校验对象

MAME 的 `disk sha1` 按 CHD 格式／版本标识内部逻辑内容；CHD v5 还区分原始数据与包含元数据的整体校验。dir2dat SHA1 校验的是编码后的 `.chd` 文件字节。重新压缩可以保留逻辑内容，却改变物理文件校验值。应分别保存两种身份、编码器／版本、元数据、父依赖和源文件身份，不能互相替代。[chdman 文档](https://docs.mamedev.org/tools/chdman.html)。

本地示例 `dvp-0027a` 的 disk SHA1 是 `da1aacee9e32e813844f4d434981e69cc5c80682`；dir2dat 的文件 SHA1 是 `d3ec0dd0532b4c362957c116dfcf39ff0293c855`，大小 3,317,217,136 字节。MAME 逻辑清单有 1,042 个不带大小的 disk 引用；物理清单有 1,042 个 `.chd` 文件条目，整文件重复仅 **0.268%**。这不能说明解码后的块重合程度。

把现有 CHD 作为不解析内部结构的对象保存，容易保证原编码文件完整恢复。解码分块可能提高跨游戏共享，但需要新适配器；除非保留原编码或能精确复现，否则不能承诺恢复原 CHD 文件的逐字节身份。父盘／差分 CHD 的所有依赖都必须保留。

## No-Intro：卡带顺序与格式边界

| 类型 | 适合程度与处理方式 |
| --- | --- |
| N0 | NES 已实现：完整主体共享、精确保留新旧头部、块级去重、无损压缩。 |
| N1 | 下一批卡带：GBA、SNES、Mega Drive、GB/GBC；本地收藏较大，原始字节复原相对直接。 |
| N2 | 普通卡带适合处理，但绝对收益通常较小；保留内部头部、mapper、bank、镜像映射及芯片顺序。 |
| N2B | N64：只有实际存在多种字节序版本时，统一内容表示才有额外共享收益；记录可逆变换。 |
| N3 | 先做格式适配：多芯片卡带、FDS/QD、64DD、混合容器或必要配套资源。 |
| N4 | DS/DSi、解密 3DS/New 3DS：值得研究大文件分块，但流式处理、文件系统、加密边界增加成本。 |
| N5 | IPF、磁通、波形：优先精确保留原始数据，不能用逻辑镜像规范化代替时序保存。 |

本地现有压缩收藏大小：

| Measured directory group / 已测量目录组 | Files | Stored GiB |
| --- | --- | --- |
| No-Intro | 48115 | 29.347 |
| FBNeo 1.0.0.3 260723 GIT7a28a7d debug ROMs (split) | 25446 | 33.617 |


这是目录文件大小之和，不是按 DAT 验证后的完整率。No-Intro 有 48,115 个文件（48,111 个 ZIP、4 个文本文件），Aftermarket／Private 目录归入对应平台。GBA 约 **14.422 GiB**、SNES **3.994**、Mega Drive **3.928**、GBC **1.056**、GB **0.289**，支持上述卡带顺序。FBNeo 有 25,446 个文件，约 **33.617 GiB**，也是现成的下一步试验来源。目录存在不代表 DAT 中所有条目都已具备。

关键限制：

- **GBA／GB／GBC：**卡带内部头部属于 ROM 字节，可拆成段建模，但不能作为外部包装丢弃。存档类型、mapper、硬件注释需要记录来源和可信度。[GB 头部规范](https://github.com/gbdev/pandocs/blob/master/src/The_Cartridge_Header.md)。
- **SNES：**区分外部 512 字节 copier header 与内部 ROM header。LoROM／HiROM、增强芯片、SRAM、区域信息写入元数据；修正头部或内部校验不能覆盖保存的原文件。[SNES 文件格式](https://snes.nesdev.org/wiki/ROM_file_formats)。
- **Mega Drive／32X：**普通 ROM 可直接分块；交错或交换字节序的格式需检测后做可逆变换。不能仅看扩展名，也不能在本地没有这些变体时虚报共享收益。
- **Atari 7800／Lynx：**本地是 BIN、LYX 清单。如果以后导入相应外部头部版本，可共享验证过的主体并保留各自原头部；不能默认本地已经同时存在。
- **N64：**根据实际字节序检测交换规则，保留内部头部与精确长度。本地 No-Intro 是 BigEndian 清单，多字节序共享目前只是可能性。[N64 格式](http://n64dev.org/romformats.html)。
- **FDS／QD：**可选 FDS 包装头部与磁盘数据分开。QD 不是 FDS 简单换头：FDS 通常每面 65,500 字节，QD 每面 65,536 字节并包含 CRC。校验、顺序、填充和异常必须进入可逆配方。[FDS 文件格式](https://www.nesdev.org/wiki/FDS_file_format)、[磁盘格式](https://www.nesdev.org/wiki/FDS_disk_format)。
- **DS／DSi／3DS：**保留文件系统偏移、安全／加密区域、签名、填充和精确裁剪状态。解密不等于所有内容都容易压缩。仅能运行却不符合原 DAT 的镜像不算成功复原。[3DS RomFS](https://www.3dbrew.org/wiki/RomFS)、[AES 寄存器](https://3dbrew.org/wiki/AES_Registers)。
- **混合来源：**Atari 2600 含 WAV；C64 含 CRT／D64／PRG 和芯片数据；VIC-20 可能有按地址划分的芯片；Intellivision 混合 BIN／INT／ROM。GP32 的 `.smc` 不能当成 SNES。Game & Watch ROM 不意味着包含完整美术资源。NES、Satellaview 清单也含辅助文件，必须保留。
- **时序数据：**Atari ST 有 546 个 IPF；Sharp X1 有 8 个 WAV；X68000 Flux 是一个集合中的 336 个 RAW 成员。转换成逻辑扇区可能丢失原时序、保护或信号数据，应先按原字节对象／分块无损保存。[Greaseweazle 镜像格式](https://github.com/keirf/greaseweazle/wiki/Supported-Image-Types/a8b5dc0199b156ef95bd9039277b3e9d4cde28d4)。

### 本地最新 No-Intro 平台完整表

类型表示工程适合程度，不是压缩率。“Sets” 是 DAT 记录数，不是整理后的独立游戏数量。最大文件大小用于识别现有导入限制。

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


## Redump：光盘处理顺序

| 类型 | 优先级与必要工作 |
| --- | --- |
| R1 | 首批：PS1、Saturn、PCE CD、Mega CD、Neo Geo CD；整轨重复、地区和修订共享值得验证。 |
| R2 | 其他以 CD 为主的收藏：复用轨道／布局基础，通常绝对规模或证据较少。 |
| R2D | Dreamcast：GD-ROM 几何布局、GDI／CUE 表示需专门的精确布局适配。 |
| R3 | PS2／PSP 等较大镜像：流式分块；整盘校验不同不能说明内部没有共享。 |
| R3W | GameCube／Wii：研究可逆垃圾／填充重建，保留异常，并与 RVZ 基线比较。 |
| R4 | 混合 PC／街机包、Xbox／Xbox 360、PS3：保护、密钥、特殊布局或媒体格式须逐项适配。 |

PS1 重复媒体字节为 **394.661 GiB／8.410%**；Saturn **140.174 GiB／13.959%**；PCE CD **37.475 GiB／15.762%**；Mega CD **25.139 GiB／10.597%**；Neo Geo CD **6.610 GiB／11.025%**。这些支持轨道共享试验，但不保证比 CHD 节省同样比例。Konami System GV 达到 48.161%，却只有两个集合，不能仅按百分比排第一。

CD 要保存各原始轨道身份、扇区模式、轨道顺序、index／pregap 及现有 CUE／GDI／SUB／SBI／MDS／CCD 等配套文件。重新生成 EDC／ECC、零区域或音频表示时必须验证精确性，并保存非标准扇区异常。符合 Redump 的 BIN／ISO 不自动等于保留了所有物理防拷信息。[Redump MDF/MDS 指南](https://wiki.redump.info/MDF/MDS_Dumping_Guide)。

GameCube／Wii 应参考 Dolphin RVZ 现有方案，它对可生成的垃圾数据及 Wii 编码细节有专门建模。不能直接删除“未使用”区域后就宣称无损；所有必要种子、参数和异常都要保存，并与同一实际收藏的 RVZ 比较。[WIA/RVZ 规范](https://github.com/dolphin-emu/dolphin/blob/master/docs/WiaAndRvz.md)。

Xbox 与 PS3 应明确区分转储变体、加密／解密字节。精确变换所需密钥应记录来源并遵循本地私有保存策略；DAT 存在不代表已具备密钥。[Xbox 光盘结构](https://xboxdevwiki.net/Xbox_Game_Disc)、[Redump PS3 指南](https://wiki.redump.info/Sony_PlayStation_3_Dumping_Guide)。

本地布局包覆盖并不相同：Dreamcast 有 **1,516 个 CUE 成员、1,427 个 GDI 成员**。必须按光盘身份关联，不能假定一一对应且完整。下面的集合数和媒体文件数不能互换。

### 本地最新 Redump 平台完整表

整文件重复为零，不代表没有块共享或压缩价值。显示保留三位小数，JSON 保存整数字节。

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


## Visual Pinball 与媒体资源

132 个 DAT 成员包含 13,670 个集合记录、298,098 次文件出现。有效总量 **1,635.854 GiB**，唯一声明内容 **1,495.981 GiB**，重复 **139.873 GiB**。大量内容是 MP4／OGG／MP3／PNG／JPG，以及 VPT／VPX 桌台和配套资源。完整资源复用很有价值，但再次压缩已编码媒体可能收益很低，而且不能有损处理。

桌台、PinMAME ROM 依赖、PuP 包、B2S 背板、脚本、相对路径和媒体角色应分别建模。多个游戏可共享同一美术对象，而不合并游戏身份。修改或重打包 VPX 不自动保证逐字节一致。Batocera／ScreenScraper 的简介、图片和视频占位应引用可复用内容对象，并保留提供方 ID、语言、区域、来源及独立可用状态。这是现有占位模型的扩展建议，不表示已导入这些资源。[Visual Pinball 项目](https://github.com/vpinball/vpinball)。

## 应保留哪些 DAT 与辅助元数据

用适用的最新完整内容 DAT 作为校验目标，同时保留历史快照以建立新旧身份映射。Parent/Clone XML 有助于游戏关系与候选分组，但父子关系不能证明字节相同。本目录有 No-Intro Parent-Clone、NES DB Export、Dumplog；本报告不声称检查过这里没有的 Standard／Scene／Daily 变体。增量更新或按发布组织的清单应作为范围明确的补充视图，不能悄悄代替完整目标目录。

NES DB Export、Dumplog 对来源、修订、硬件和转储溯源有价值，已有 NES 工作已整合。硬件字段可能缺失或冲突，应保留来源、版本与可信度，不把推断当成完整事实。Redump 布局包、对应模拟器构建的 XML、CHD 逻辑及物理两类清单，都提供普通校验表没有的信息。不能仅因出现新 DAT 就删除旧 DAT。

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


## 建议架构与实施验收

1. 继续使用单 SQLite 文件：按内容寻址的对象、精确文件身份、独立版本化的源目录、平台适配器。名称、路径、大小写属于目录成员和导出计划，不是物理去重键。不同模拟器可共享字节，而保留各自目录身份。
2. 原始对象和解码后的逻辑内容分别建身份。保存有序片段、精确外部头部、变换、参数、异常、硬件信息和来源关系。不能仅凭名称或父子关系去重。
3. 保留无损块压缩和有深度限制的差分链；用真实数据比较固定、对齐、内容定义分块。计入索引、配方、压缩组及随机导出开销。解析已压缩容器没有净收益时，可以继续按完整对象保存。
4. 对可获得的各格式身份保存预期 CRC32／MD5／SHA1／SHA256，包括 raw／headered／headerless、轨道、来源压缩包与生成导出。预期值和实算值分别记录来源、可用状态。TorrentZip 在导出时生成并有独立校验，不要求等于原始来源 ZIP 字节。
5. 大平台导入前先实现流式大对象和归档支持。目前 NES 路径限制为 ROM 256 MiB、ZIP 展开导入 2 GiB、经典 ZIP 导出且无 ZIP64。部分 FBNeo 文件已超过这些限制；通用资源存储不代表已有完整大光盘导入器。
6. 试验需覆盖修订、区域、多轨、保护扇区、加密、大文件、已压缩媒体。对**每个保存对象**重新组装并校验可用原始哈希和内部 SHA256，导出包另行验证。记录真实 ZIP／CHD／RVZ 基线、压实后 SQLite 大小、临时空间、导入时间、冷／热导出时间。
7. 只有完整往返验证通过，且空间与性能收益值得时，才采用新适配器。迁移使用事务并保留回退副本；公开无载荷研究资料和目录，ROM、原始 DAT、媒体继续留在本地。

## 复现 DAT 分析

使用 Python 3.10+ 标准库，以只读方式访问源目录。程序针对本次 ZIP/XML 命名和结构，遇到未支持文件或过大 XML 成员会停止，不下载或解压保存原 DAT。NES DB Export 仅按源文件哈希盘点，其溯源结构由现有 NES 专用导入器处理。

```sh
python3 -B assessment/tools/survey_datfiles.py /path/to/Datfiles /tmp/retroboxdb-survey
python3 -B -m unittest discover -s assessment/tools -p 'test_*.py' -v
```

目录大小 JSON 是单独的时间点文件大小观察，不由 DAT 分析程序生成。源压缩包更新后结果自然会变化。源包与成员 SHA256 标明本次评估输入。9 个合成测试覆盖身份有效性、重复计算、CHD 校验分离、辅助文件排除、关系计数、实体拒绝、日期选择和多成员汇总。

### 选用 FBNeo 成员完整表

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
