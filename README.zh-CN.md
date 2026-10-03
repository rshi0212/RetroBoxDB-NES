# RetroBoxDB NES

[English](README.md) | 中文

RetroBoxDB 将 ROM 正文、DAT 原始内容、校验信息、硬件来源、可逆头部版本和处理代码集中保存在本地单个 SQLite 文件中。存储格式 v3 在分块去重、独立头部和差异编码之上，加入了共享压缩组。

**GitHub 公开的是无载荷 Catalog，不包含 ROM 正文、DAT／DB／Dumplog 原始文件、压缩后的游戏数据或媒体实体。** 含实际内容的 `RetroBoxDB.sqlite` 只保留在本地。公开 Catalog 有元数据、预期校验值、小型头部字段、重建配方和程序代码，不能独立恢复 ROM。

| 文件 | 用途 |
| --- | --- |
| [RetroBoxDB.NES.Catalog.sqlite](https://github.com/rshi0212/RetroBoxDB-NES/releases/latest/download/RetroBoxDB.NES.Catalog.sqlite) | 当前公开目录库，作为 GitHub Release 附件下载 |
| [英文技术说明](RetroBoxDB.NES.Technical-Design.en.md) | 存储格式、约束、迁移和验证细节 |
| [英文首页](README.md) | 项目首页与使用说明 |

Catalog 超过普通 Git 文件的 100 MiB 限制，因此通过 Release 发布。下载后仍是一个普通 SQLite 文件；GitHub 自动生成的源码 ZIP 只含仓库文档，不包含数据库附件。

## 分组压缩已经实施

独立 LZMA 块按最多 **2 MiB 未压缩内容**组成一组，使用 4 MiB 字典的 LZMA2 压缩。每个原有块的编号、大小和 SHA256 保留；对象按原块映射恢复正文，Headered ROM 再拼接独立保存的准确 16 字节头部。

此次迁移将 **125,016 个块**收入 **489 个压缩组**。这些块的压缩数据从 435,766,697 字节变成 342,419,600 字节，减少 **89.02 MiB**。迁移、整理 SQLite 页并完成文档和报告更新后，完整库从 **629.88 MiB 降至 534.50 MiB**，减少 **95.38 MiB，约 15.14%**（660,471,808 → 560,463,872 字节）。准确大小同时记录在 Release 说明与内嵌 `release-manifest` 中。其他收藏的收益需要另行实测。

导出时按需解压所需分组，核验分组和块的 SHA256，组装正文、头部及尾部数据，最后核对文件的大小、CRC32、MD5、SHA1、SHA256。TorrentZip 仍然按既有配方生成，并核对已经保存的导出校验值。迁移不会改变 ROM、DAT 或 ZIP 的逻辑字节身份。

分组解码缓存限制为 16 MiB，原块缓存限制为 64 MiB；读取一个小块有时需要解压整个组。编码最多使用四个工作线程，还需要额外临时内存。原有 raw、fill、zlib、独立 LZMA 和最多两层 XOR 差异编码继续有效。

新导入的数据先使用原有分块去重和压缩流程；批量导入完成后运行 `compact`，把符合条件的新块归组并回收 SQLite 空闲页。已有压缩组不会被反复重写。只有扣除一部分映射／元数据开销后仍节省空间的分组才会采用；失败时事务回滚。v3 引擎可以读取 v2 库，但分组维护需要先迁移到 v3，旧 v2 引擎不能读取 v3 格式。

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

## Batocera／ScreenScraper 占位

全部 7,385 个现有发行版本具有 17 项游戏信息、8 项本地运行状态和 15 类媒体的虚拟占位。未知简介、日期、评分、提供者 ID、URL、路径和校验值仍为空；未执行联网刮削，没有下载实际图片／视频，没有保存 API 凭据。

媒体包括截图、盒图、Logo、视频、背景图、标题图、说明书、杂志、地图、边框、卡带图、备用盒图、盒背、Wheel 和混合图。`frontend_game_values` 支持语言／地区，`scraper_game_links` 保留经确认的提供者身份，`frontend_media_slots` 可关联未来存入完整库的媒体实体。此扩展不包含联网 ScreenScraper 客户端或 Batocera `gamelist.xml` 导出器。

```sql
SELECT * FROM v_screenscraper_games WHERE release_id = 1;
SELECT * FROM v_batocera_game_fields WHERE release_id = 1;
SELECT * FROM v_batocera_media_slots WHERE release_id = 1;
```

映射参考 [Batocera 字段定义](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/MetaData.cpp)、[ScreenScraper API](https://www.screenscraper.fr/webapi2.php) 和 [Batocera 适配器](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/scrapers/ScreenScraper.cpp)。

## 内嵌程序与复现

需要 Python 3.10+、SQLite 3.37+ 和 Python 标准库 `lzma`；SQLite 本身不会执行 Python。无需提取文件即可查询公开库：

```bash
python3 -B -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); s=c.execute("SELECT content FROM resources WHERE name=?",("engine.py",)).fetchone()[0]; c.close(); exec(compile(s,"RetroBoxDB:engine.py","exec"))' ./RetroBoxDB.NES.Catalog.sqlite stats
```

可将 `stats` 换成 `checksums FILE_ID`、`audit` 或 `help`。目录引擎启用 `query_only`，拒绝导入、压缩维护和导出；审计明确返回 `payloads_verified=false`。

下面从 Catalog 提取程序到临时目录并运行全部测试。**测试使用的 `engine.py` 必须来自生产资源 `engine.full.py`。**

```bash
python3 -B - <<'PY'
import pathlib, sqlite3, subprocess, sys, tempfile
c = sqlite3.connect('file:RetroBoxDB.NES.Catalog.sqlite?mode=ro', uri=True)
out = pathlib.Path(tempfile.mkdtemp(prefix='retroboxdb-nes-v3-'))
names = ['schema.sql', 'build_v3.py', 'build_v2.py', 'seed.json',
         'group_schema.sql', 'migrate_v3.py', 'build_catalog.py',
         'nointro.py', 'nointro_schema.sql',
         'tests.py', 'tests_storage.py', 'tests_frontend.py',
         'tests_nointro.py', 'tests_groups.py']
resources = {name: name for name in names}
resources.update({'engine.py': 'engine.full.py', 'catalog_engine.py': 'engine.py'})
for filename, resource in resources.items():
    text = c.execute('SELECT content FROM resources WHERE name=?', (resource,)).fetchone()[0]
    (out / filename).write_text(text, encoding='utf-8')
c.close()
print('Extracted source:', out, flush=True)
subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v',
                'tests', 'tests_storage', 'tests_frontend', 'tests_nointro', 'tests_groups'],
               cwd=out, check=True)
PY
```

**70 项人工数据测试通过**。本次真实收藏迁移还校验全部 165,019 个块、17,734 个可读取对象和 24,487 个导出打包配方。分组有压缩前／后的 SHA256，块继续独立校验，文件和 ZIP 继续核对原有完整校验集合。测试覆盖损坏检测、跨组读取、差异块基础归组、事务回滚、重复导入、来源异常和公开库排除载荷。

提取程序后，可对自己持有的完整库执行：

```bash
# 只读旧库，生成另一个 v3 文件；不会覆盖已有输出路径。
python3 -B migrate_v3.py OLD.sqlite NEW.sqlite
python3 -B engine.py NEW.sqlite audit-all

# 导入自己的 DB／Dumplog 后，将符合条件的新块归组。
python3 -B nointro.py RetroBoxDB.sqlite '/路径/NES DB Export.zip' '/路径/NES Dump Log.zip'
python3 -B engine.py RetroBoxDB.sqlite compact

# 按文件 ID 导出裸 ROM，或生成该文件对应的 TorrentZip。
python3 -B engine.py RetroBoxDB.sqlite export FILE_ID '/路径/output.nes'

# 从完整库生成另一个不含载荷的 Catalog。
python3 -B build_catalog.py RetroBoxDB.sqlite Catalog.sqlite catalog_engine.py
```

文件 ID 决定导出内容，扩展名不会自动把裸 ROM 转成 ZIP；需要 ZIP 时，应选择已有归档文件 ID 或先建立相应 DAT 游戏的打包配方。只包含 DAT 摘要、没有正文的缺失游戏不能恢复。

迁移期间需要旧库与新库两份空间；正常写事务也可能短暂创建回滚日志。提交、关闭之后，每个数据库只有一个持久 SQLite 文件。内嵌 `documentation-index` 区分当前说明与历史报告；`legacy/` 下的原始代码、旧测试报告和历史体积数据保留为来源证据。
