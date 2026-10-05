# RetroBoxDB NES

[English](README.md) | 中文

NES（Famicom）的单文件 SQLite 保存库：ROM 数据、DAT 原始内容、校验信息、硬件来源、可逆的头部变体和处理程序都在一个 SQLite 文件中。公开的 Catalog 只含元数据（校验值、DAT 与来源记录、16 字节头部、打包配方和程序），不含 ROM 数据，不能独立恢复文件；完整库 `RetroBoxDB.sqlite` 保留在本地。

| 项目 | 数值 |
| --- | --- |
| 原始大小 | No-Intro ZIP 21,792 个（有头、无头目录及各自的 Aftermarket／Private），4.12 GiB；解压后 ROM 21,793 个，10.69 GiB |
| 入库后大小 | 完整库 `RetroBoxDB.sqlite` 506.2 MiB；公开 Catalog 138.7 MiB（不含 ROM 数据） |
| 比例 | 完整库为原 ZIP 的 12.0%，为解压后 ROM 总量的 4.6% |
| 使用的技术 | 存储 v4：16 字节头部与正文分开存储，有头、无头版本共用正文；正文按头部／PRG／CHR 边界切成 8 KiB 块，按 SHA256 去重，按 No-Intro 游戏族顺序装入最大 256 MiB 的 LZMA2 实体组（字典 256 MiB）；逐块、逐对象完整校验；源 ZIP 由 TorrentZip 配方逐字节重建 |
| 导出性能 | Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz，空闲负载，Python 3.14.4，含全部校验。全集合顺序导出（22,943 个 ROM 文件，每组解压一次）：54.1 MiB/s，平均 9 毫秒／个；单个文件冷缓存（每次清空缓存，需解压所在组的前段）：ROM 平均 2.339 秒，TorrentZip 平均 2.216 秒 |

## 下载与文档

| 文件／文档 | 内容 |
| --- | --- |
| [RetroBoxDB.NES.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-NES/releases/latest/download/RetroBoxDB.NES.Catalog.sqlite) | 公开 Catalog（Release 附件，附 `SHA256SUMS`） |
| [存储 v4 说明](RetroBoxDB.Storage-v4.zh-CN.md)／[English](RetroBoxDB.Storage-v4.en.md)、[Technical design](RetroBoxDB.Storage-v4.Technical-Design.en.md) | 六个平台共用的存储格式、评估与维护 |
| [NES v3 技术设计（历史）](RetroBoxDB.NES.Technical-Design.en.md) | 2026-10-05 之前的存储 v3 |
| [平台评估](RetroBoxDB.Platform-Assessment.zh-CN.md)／[English](RetroBoxDB.Platform-Assessment.en.md) | 本地 172 个 DAT 压缩包的调查 |

## 其他平台

| 平台 | 仓库与 Catalog |
| --- | --- |
| SNES | [RetroBoxDB-SNES](https://github.com/rshi0212/RetroBoxDB-SNES) · [RetroBoxDB.SNES.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-SNES/releases/latest/download/RetroBoxDB.SNES.Catalog.sqlite) |
| Mega Drive | [RetroBoxDB-MegaDrive](https://github.com/rshi0212/RetroBoxDB-MegaDrive) · [RetroBoxDB.MegaDrive.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-MegaDrive/releases/latest/download/RetroBoxDB.MegaDrive.Catalog.sqlite) |
| Game Boy | [RetroBoxDB-GB](https://github.com/rshi0212/RetroBoxDB-GB) · [RetroBoxDB.GB.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-GB/releases/latest/download/RetroBoxDB.GB.Catalog.sqlite) |
| Game Boy Color | [RetroBoxDB-GBC](https://github.com/rshi0212/RetroBoxDB-GBC) · [RetroBoxDB.GBC.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-GBC/releases/latest/download/RetroBoxDB.GBC.Catalog.sqlite) |
| Game Boy Advance | [RetroBoxDB-GBA](https://github.com/rshi0212/RetroBoxDB-GBA) · [RetroBoxDB.GBA.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-GBA/releases/latest/download/RetroBoxDB.GBA.Catalog.sqlite) |

## 存储：从 v3 迁移到 v4

2026-10-05 起 NES 库改用与其他五个平台相同的存储 v4。依据：

- **抽样**（600 个游戏族，652.6 MiB ZIP）：NES v3 引擎原样导入为 91.8 MiB；v4 的 8 KiB 块 + 128 MiB 族排序组为 81.9 MiB（含块元数据估算）。4 KiB 块的元数据开销抵消了去重收益，64 KiB 块不能对齐 PRG／CHR 边界，二者都更大。
- **真实全量数据**：迁移到 32 MiB 组后，把相邻组合并测量（相对 32 MiB）：64 MiB −1.40%、128 MiB −2.59%、256 MiB −5.66%。较小的组都比 256 MiB 组大 0.5% 以上，按规则采用 256 MiB 组。
- **全库结果**：ROM 数据从 v3 的 364.4 MiB（489 个 lzma2-4m 组加 XOR 差分散块）降到 328.3 MiB（−9.91%，6 个组）。格式迁移要求收益不少于 2%。
- **代价**：单个文件冷读取需解压所在组的前段（平均约 2.3 秒）；按集合导出时每个组只解压一次。

迁移（`tools/migrate_v4.py`）复制原库后在新文件上进行：放宽 `compression_groups` 的约束以接受实体组，补齐 v4 的表与视图，为每个正文对象记录游戏族和 RA 哈希，按块编号顺序解码全部正文块（164,951 个），按游戏族顺序重新装入实体组，逐块核对后删除不再使用的 v3 组（489 个）。块编号、SHA256、大小、对象拼接、16 字节头部配方及全部元数据不变。迁移后全量审计通过：17,734 个对象、6 个组、24,487 个 ZIP 配方。

存储格式与各平台的评估详见 [存储 v4 说明](RetroBoxDB.Storage-v4.zh-CN.md) 与 [Technical design](RetroBoxDB.Storage-v4.Technical-Design.en.md)。

## 保留的目录与校验信息

库中保留 **58,935 条文件记录、17,726 条 ROM 记录、22,065 条 DAT ROM 条目和 24,487 个打包配方**。原文件名、目录、游戏发行关联、DAT 条目、命名更正、旧新头部、硬件资料、修复记录和前端占位均保留。

完整文件、Headerless 正文、原始 ZIP 和导出 TorrentZip 分别有自己的身份与校验值。DAT 没提供的摘要字段仍为空；不能凭一个预期哈希恢复缺失的游戏正文。

公开库从新 SQLite 文件建立，排除 **`compression_groups`、`chunks`、`object_chunks`** 三张表的全部内容。这三张表均为空；不是从含 ROM 的数据库删除数据后留下空闲页的副本。解析后的 DAT 条目 XML 和 16 字节 NES 头部属于保留的元数据，压缩的 ROM／DAT 数据不属于允许公开的元数据。

```sql
SELECT * FROM v_file_checksums WHERE file_id = 1;
SELECT * FROM v_rom_checksums WHERE rom_id = 1;
SELECT * FROM archive_plans WHERE id = 1;
SELECT dat_set_id, status, COUNT(*) FROM v_dat_coverage GROUP BY dat_set_id, status;
SELECT content FROM resources WHERE name = 'catalog-report';
SELECT content FROM resources WHERE name = 'group-migration-report';
SELECT content FROM resources WHERE name = 'group-verification-report';
```

## CSV 中英文游戏名

本地完整库和 Catalog 保留 `Nintendo - Nintendo Entertainment System.csv` 的 **4,453 条**原始记录，其中 **3,703 条**提供中文名。名称扩展 v4 按游戏身份消歧后，**4,420 条**确认关联到 **4,429 个发行版本、2,023 个游戏和 8,896 条 ROM 记录**；其中 **3,698 个发行版本**有直接匹配的中文名称。**22 条**保留为待消歧候选，**11 条**尚无同名候选。这里是名称匹配，不代表新增哈希验证或 ROM 正文。

**3,703 条中文名去重为 1,875 个唯一名称**，集中保存在 `game_chinese_names`，通过 `game_name_entries.name_cn_id` 引用。同名中文不会按英文名、地区或版本重复存储；`v_release_chinese_names` 提供每个发行版本去重后的中文名称。`game_name_entries`／`game_name_imports` 保留原始英文、去括号英文、CSV 记录序号和来源 SHA256，`release_name_links` 保留匹配依据；原始 CSV 文本（含原始中文和换行）保存在 `resources`，可追溯每条来源。

去括号英文名现在仅用于候选检索和简洁显示，不作为跨游戏自动关联的充分依据。匹配依次使用完整标题、括号字段等价匹配、身份限定字段匹配，每条已确认来源只能对应一个 `game_id`。解析结果保留地区、语言、版本和身份标识；未知括号按身份标识保留。册别、厂商、卡带编号参与识别，`Bulletproof`／`Bullet-Proof` 支持已知别名归一化，括号顺序不影响结构化匹配。地区以及 Beta／Proto 等标记在同名跨组时参与消歧；无法消歧的候选不进入标准名或继承依据。

NHK 六年级 `(Jou)`／`(Ge)` 已分别关联“上”／“下”，两个独立游戏不再共享错配名称。`Baseball (USA) (Intellivision)` 不再从另一个同名游戏组获得“任天堂棒球”。本次移除了 **488 条跨游戏组的旧来源关联**；其余部分旧的版本名称匹配改为明确的组内继承。原始 CSV、中文名去重记录和游戏分组均保留。决策及解析字段见 `game_name_match_decisions`，候选清单见 [game-names-match-review.csv](reports/game-names-match-review.csv)，变更明细见 [game-names-matching-changes.json](reports/game-names-matching-changes.json)。

Parent／Clone 通过现有 `game_id` 共享游戏组名称。**1,556 个组**只有一个已确认中文译名，该名称自动作为组内标准名，为 **14 个 Parent 和 375 个 Clone**提供继承名称。计入继承后，**4,087 个发行版本、8,100 条本地 ROM 记录**有可用中文名。按发行条目统计，Parent 中文覆盖率为 **49.50%**（1,721／3,477），Clone 为 **60.54%**（2,366／3,908）。这是中文覆盖率，区别于英文名称直接匹配率。消歧前的 4,112 个发行版本包含部分依据不足的关联，不再作为当前覆盖数。

另有 **167 个已确认多译名组**标记为 `needs_review`，标准名保持空，已确认的别名保留；**1,754 个组**尚无已确认中文名。待选标准名清单见 [game-names-review.csv](reports/game-names-review.csv)，与尚未确认游戏身份的 22 条来源候选分别统计。标准名及继承关系通过数据库视图实时推导，不复制中文字符串，也不把继承伪装成 CSV 直接匹配。新增来源若令唯一译名变为多译名，继承会自动停止。`v_game_chinese_name_evidence` 可追溯组内名称的原始发行版本和 CSV 来源。

**11 条未匹配记录仍保存在库中**，其中有中文名的是 `EarthBound Beginnings`（地球冒险）和 `Baoxiao Sanguo`（爆笑三国）。空白中文名保持为空，不生成译名。既有游戏标题、ROM、校验值和前端字段不变。GitHub Release 提供无载荷 Catalog，完整数据库保留在本地。

```sql
-- 按游戏或 ROM 查询；发行级视图还包含原始英文名和来源。
SELECT * FROM v_game_names WHERE name_cn LIKE '%魂斗罗%';
SELECT * FROM v_release_chinese_names WHERE name_cn LIKE '%魂斗罗%';
-- 推荐用于展示：同时返回 direct / group_inherited，保留多译名。
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

可重复运行导入，相同平台和 CSV SHA256 不会重复建源或记录；所有已存来源的关联会按当前目录及规则刷新，避免旧来源保留已失效的跨组匹配。导入采用事务，`--dry-run` 会回滚全部更改，包括扩展升级。独立脚本与 SQL 同时内嵌于 `resources`（`import_game_names.py`、`game_names_schema.sql`），提取到同一目录即可使用。

```bash
python3 -B tools/import_game_names.py "$HOME/下载/Nintendo - Nintendo Entertainment System.csv" RetroBoxDB.sqlite RetroBoxDB.NES.Catalog.sqlite
python3 -B -m unittest discover -s tests -v
```

## No-Intro DB 与 Dumplog

`20261002-002752` 快照保留 7,704 个档案、16,154 条独立文件身份、13,930 条 Dump 来源、898 条 Scene 来源和 7,674 条 Dumplog 状态。来源 ID 按类型与快照隔离；同一文件被多个 Dump 引用时，不重复保存正文。

头部资料包括 8,026 条声明头部和 245 条完整历史头部；另有一条不完整历史头部备注保留为异常，不猜补缺失位。存在一条 Headerless 分类记录附带 header 字段，因此不能只凭字段判断文件含头部。头部解析结果与实物硬件声明分别保存。

6,414 条带卡带／硬件编号的来源记录全部保留，其中 6,412 条关联到现有 ROM 或发行版本。PCB、芯片、Lockout、SaveChip、卡带编号、印章和包装信息按来源保存，可信级别为 `documented`，不会把不同实物修订版合并成唯一硬件。

完整库保留 178 个经过全部校验值验证的新增 Headered 重建版本，其中 30 个保留 Bad 标记。旧版 Headered DAT 匹配 **7,100 / 7,288**；新版 Headered **7,091 / 7,387**；新版 Headerless **7,094 / 7,390**。此前补齐的 6 个旧 DAT 游戏均保留 TorrentZip 配方和导出校验值。

15 个未通过校验的候选配对、11 个 Dumplog 硬件待核查档案、一条 Headerless 头部字段异常和一条不完整历史头部备注均保留。Steel Legion 两个 Demo 的交叉重建关系有完整校验证据，原来源关系仍然存在。Pressing Buttons 多出的 Headerless 数据没有丢弃。Dumplog 官方 Verified 状态与本地 DAT 匹配状态分开保存；硬件采用 DB 逐来源信息，CSV 冲突不覆盖实物声明。

```sql
SELECT * FROM ni_snapshots;
SELECT status, COUNT(*) FROM v_nointro_status GROUP BY status;
SELECT * FROM v_nointro_headers WHERE file_id = '12868';
SELECT * FROM v_nointro_hardware WHERE archive_id = '1214';
SELECT * FROM ni_reconstructions;
SELECT category, COUNT(*) FROM ni_anomalies GROUP BY category;
```

## RetroAchievements 成就匹配

迁移时为每个 NES ROM 计算 RA 哈希（去掉 16 字节头后的正文 MD5，与 rcheevos 一致），并导入 RA 公开 API 的 console 7 快照。有成就的 RA 游戏 1,123 个：本地有匹配 ROM 的 933 个（2,708 个 ROM），仅 DAT 有 1 个，仅对应 DB Export 文件 2 个，无 No-Intro 对应 187 个（其中 Hack 133 个）。逐游戏清单见 [reports/ra-nes-games.csv](reports/ra-nes-games.csv)。

## Batocera／ScreenScraper 占位

全部 7,385 个现有发行版本具有 17 项游戏信息、8 项本地运行状态和 15 类媒体的虚拟占位。未知简介、日期、评分、提供者 ID、URL、路径和校验值仍为空；未执行联网刮削，没有下载实际图片／视频，没有保存 API 凭据。

媒体包括截图、盒图、Logo、视频、背景图、标题图、说明书、杂志、地图、边框、卡带图、备用盒图、盒背、Wheel 和混合图。`frontend_game_values` 支持语言／地区，`scraper_game_links` 保留经确认的提供者身份，`frontend_media_slots` 可关联未来存入完整库的媒体实体。此扩展不包含联网 ScreenScraper 客户端或 Batocera `gamelist.xml` 导出器。

```sql
SELECT * FROM v_screenscraper_games WHERE release_id = 1;
SELECT * FROM v_batocera_game_fields WHERE release_id = 1;
SELECT * FROM v_batocera_media_slots WHERE release_id = 1;
```

映射参考 [Batocera 字段定义](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/MetaData.cpp)、[ScreenScraper API](https://www.screenscraper.fr/webapi2.php) 和 [Batocera 适配器](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/scrapers/ScreenScraper.cpp)。

## 导出、维护与发布

```bash
# 按 DAT（有头／无头）、1G1R、RA 成就、TorrentZip／裸 ROM 组合导出
python3 -B tools/export_set.py RetroBoxDB.sqlite OUT --dat-mode headered --set 1g1r --ra achievements --container torrentzip
# 增量加入新的 DAT、DB Export／Dump Log、ROM 与 RA 快照（NES 使用其有头／无头导入路径与 NES 专用 DB 导入器）
python3 -B tools/update_db.py RetroBoxDB.sqlite --discover --ra
# Catalog 内嵌引擎只读审计（stats、checksums FILE_ID、help 同理）
python3 -B -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); s=c.execute("SELECT content FROM resources WHERE name=?",("engine.py",)).fetchone()[0]; c.close(); exec(compile(s,"RetroBoxDB:engine.py","exec"))' ./RetroBoxDB.NES.Catalog.sqlite audit
```

发布流程：推送 `release/catalog-release.json` 后，`.github/workflows/publish-catalog.yml` 从清单中按 SHA256 固定的基础 Catalog 出发，注入本次提交的统一引擎和文档，核对全部数据表摘要、完整性、外键、Catalog 审计、仓库测试和 NES 内嵌测试套件，确认无空闲页后发布 Release 与 `SHA256SUMS`。`resources` 中的程序是可执行代码，只应从自己构建或 SHA256 已核对的 Release 附件中执行。

## 历史

NES 库先后使用过 v1（1 MiB 原始块）、v2（8 KiB 块、XOR 差分）和 v3（2 MiB LZMA2 分组）格式，相关程序、报告和设计文档保存在 `resources` 的 `legacy/` 名下及 [NES v3 技术设计](RetroBoxDB.NES.Technical-Design.en.md) 中。v3 分组时的实测记录如下（原文保留）：

独立 LZMA 块按最多 **2 MiB 未压缩内容**组成一组，使用 4 MiB 字典的 LZMA2 压缩。每个原有块的编号、大小和 SHA256 保留；对象按原块映射恢复正文，Headered ROM 再拼接独立保存的准确 16 字节头部。

此次迁移将 **125,016 个块**收入 **489 个压缩组**。这些块的压缩数据从 435,766,697 字节变成 342,419,600 字节，减少 **89.02 MiB**。迁移、整理 SQLite 页并完成文档和报告更新后，完整库从 **629.88 MiB 降至 534.50 MiB**，减少 **95.38 MiB，约 15.14%**（660,471,808 → 560,463,872 字节）。准确大小同时记录在 Release 说明与内嵌 `release-manifest` 中。其他收藏的收益需要另行实测。

导出时按需解压所需分组，核验分组和块的 SHA256，组装正文、头部及尾部数据，最后核对文件的大小、CRC32、MD5、SHA1、SHA256。TorrentZip 仍然按既有配方生成，并核对已经保存的导出校验值。迁移不会改变 ROM、DAT 或 ZIP 的逻辑字节身份。

分组解码缓存限制为 16 MiB，原块缓存限制为 64 MiB；读取一个小块有时需要解压整个组。编码最多使用四个工作线程，还需要额外临时内存。原有 raw、fill、zlib、独立 LZMA 和最多两层 XOR 差异编码继续有效。

新导入的数据先使用原有分块去重和压缩流程；批量导入完成后运行 `compact`，把符合条件的新块归组并回收 SQLite 空闲页。已有压缩组不会被反复重写。只有扣除一部分映射／元数据开销后仍节省空间的分组才会采用；失败时事务回滚。v3 引擎可以读取 v2 库，但分组维护需要先迁移到 v3，旧 v2 引擎不能读取 v3 格式。

## 平台研究

[中文评估](RetroBoxDB.Platform-Assessment.zh-CN.md)与[英文评估](RetroBoxDB.Platform-Assessment.en.md)覆盖 329 个 DAT 成员，区分 NES 实测、DAT 推算与平台实施建议。`assessment/` 提供可复现汇总证据和只读调查程序，不包含原始 DAT、ROM 或媒体文件。目前实际实现的平台仍为 NES；这次研究更新不更换 Catalog 发布附件。

