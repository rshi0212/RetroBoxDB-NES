# RetroBoxDB NES

[English](README.md) | 中文

这是 RetroBoxDB 的 NES 游戏目录与校验信息公开版本。数据库保留文件身份、游戏目录、DAT 解析结果、硬件信息和处理程序，**不包含游戏 ROM、DAT 原始文件或其他文件实体的数据块**。

| 文件 | 内容 |
| --- | --- |
| [RetroBoxDB.NES.Catalog.sqlite](RetroBoxDB.NES.Catalog.sqlite) | 96.58 MiB 的 SQLite 目录库，含元数据、校验值和内嵌代码 |
| [RetroBoxDB.NES.Technical-Design.en.md](RetroBoxDB.NES.Technical-Design.en.md) | 英文技术说明 |
| [README.md](README.md) | 英文首页 |
| README.zh-CN.md | 中文使用与复现说明 |

数据库保留 58,747 条文件记录、17,548 条 ROM 记录、22,065 条 DAT ROM 条目和 24,479 个 ZIP 打包配方，以及游戏名称、原始文件名、来源、DAT 匹配结果、头部版本、硬件声明和修复记录。DAT 的解析条目（包括条目 XML）和 NES 的 16 字节头部属于保留的元数据。

实际内容表 `chunks` 与块映射表 `object_chunks` 均为空。本库是在新文件中复制元数据生成的，不是从完整库删除内容后留下空闲页的副本。没有 ROM 正文、DAT 原始文件字节、原始 ZIP 或媒体文件的数据块；含实际内容的完整数据库不在本仓库内。**目录库不能独立恢复游戏文件，也不能替代完整内容备份。**

所有原库已有校验值均已保留并比对一致。逻辑文件保存大小、CRC32、MD5、SHA1、SHA256；Headered 文件与 Headerless 正文各有自己的校验值。原始 ZIP 与导出 TorrentZip 的校验值分别保存。DAT 未提供的摘要字段仍为空，不会编造摘要。目录库中的值是预期文件身份，不代表可以在缺少内容时重新计算或验证这些字节。

使用 SQLite 工具可以直接查询：

```sql
-- 原始文件与导出文件的校验值
SELECT * FROM v_file_checksums WHERE file_id = 1;

-- ROM 本体与去头部正文的校验值
SELECT * FROM v_rom_checksums WHERE rom_id = 1;

-- ZIP 配方和预先计算的导出校验值
SELECT * FROM archive_plans WHERE id = 1;

-- DAT 匹配情况
SELECT dat_set_id, status, COUNT(*)
FROM v_dat_coverage
GROUP BY dat_set_id, status;

-- 查看内嵌资源与目录库生成报告
SELECT name, kind, sha256 FROM resources;
SELECT content FROM resources WHERE name = 'catalog-report';
```

处理逻辑由数据库中保存的 Python 程序执行；SQLite 本身不会执行 Python。运行环境需要 Python 3.10+、SQLite 3.37+ 及支持 `lzma` 的 Python 标准库。在文件所在目录执行：

```bash
python3 -B -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); s=c.execute("SELECT content FROM resources WHERE name=?",("engine.py",)).fetchone()[0]; c.close(); exec(compile(s,"RetroBoxDB:engine.py","exec"))' ./RetroBoxDB.NES.Catalog.sqlite stats
```

将最后的 `stats` 换成 `checksums 1`、`audit` 或 `help`，可查询校验信息、审计元数据或查看帮助。目录引擎启用 `query_only`，拒绝导入、修复、打包和导出。`audit` 会明确返回 `payloads_verified=false`，只检查 SQLite 完整性、外键和校验字段。

`resources` 中保存了可复现的程序代码：

| 资源 | 用途 |
| --- | --- |
| `engine.py` | 目录查询与元数据审计入口 |
| `engine.full.py` | 完整导入、去重、DAT 校验、头部处理和导出引擎 |
| `schema.sql` | 表、索引、视图与约束 |
| `build_v2.py`、`seed.json` | 测试用建库程序与初始化配置 |
| `tests.py`、`tests_storage.py`、`tests_frontend.py` | 使用人工生成数据的功能测试 |
| `frontend_schema.sql` | Batocera／ScreenScraper 占位结构与字段映射 |
| `TECHNICAL-DESIGN.en` | 内嵌英文技术说明 |

以下命令将源码提取到临时目录，并运行测试。**测试所导入的 `engine.py` 必须来自资源 `engine.full.py`，不能使用受限的目录查询入口。**

```bash
python3 -B - <<'PY'
import pathlib
import sqlite3
import subprocess
import sys
import tempfile

db = sqlite3.connect('file:RetroBoxDB.NES.Catalog.sqlite?mode=ro', uri=True)
out = pathlib.Path(tempfile.mkdtemp(prefix='retroboxdb-nes-code-'))
resources = {
    'engine.py': 'engine.full.py',
    'schema.sql': 'schema.sql',
    'build_v2.py': 'build_v2.py',
    'seed.json': 'seed.json',
    'tests.py': 'tests.py',
    'tests_storage.py': 'tests_storage.py',
    'tests_frontend.py': 'tests_frontend.py',
}
for filename, resource in resources.items():
    content = db.execute(
        'SELECT content FROM resources WHERE name=?', (resource,)
    ).fetchone()[0]
    (out / filename).write_text(content, encoding='utf-8')
db.close()
print('Extracted source:', out, flush=True)
subprocess.run(
    [sys.executable, '-B', '-m', 'unittest', '-v', 'tests', 'tests_storage', 'tests_frontend'],
    cwd=out, check=True,
)
PY
```

发布前已从本目录库提取代码运行，47 项测试全部通过（原有 39 项，加上 8 项前端扩展测试）。测试只使用人工生成的数据，不需要游戏或 DAT 文件。若要复现原收藏的处理结果，需要自行提供相同的 ROM/DAT 输入，并在另一个完整工作库中运行处理引擎；目录库本身不能补回缺失的字节。测试建库程序的默认 NES 块大小为 4 KiB，原完整收藏实测选用 8 KiB 块和 64 KiB SQLite 页，两项设置彼此独立。

完整方案通过“正文共享＋独立头部”、跨游戏分块去重、无损压缩及最多两层的差异引用减少占用。ZIP 仅保存配方；注册配方时实际编码一次取得输出校验值，导出时重新编码并复验。压缩器版本改变可能改变 ZIP 字节，此时引擎会报告校验不符。原完整库从 7.95 GiB 缩减到 594.88 MiB 是参考收藏的实测结果，不表示本目录库包含那些内容，也不保证其他收藏取得相同比例。

资源中的原始收藏与迁移报告属于完整库的历史记录，当前目录库的信息以 `catalog-report` 为准。SQLite 写事务可能短暂生成回滚日志；正常提交并关闭后，每个数据库只有一个持久文件。


Batocera／ScreenScraper 占位已经加入数据库，覆盖全部 7,385 个现有发行版本：17 项游戏信息、8 项本地运行状态和 15 类媒体。媒体类型包括截图、封面、Logo、视频、背景图、标题图、说明书、杂志、地图、边框、卡带图、备用盒图、盒背、Wheel 和混合图。字段定义参考 [Batocera 元数据定义](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/MetaData.cpp)；提供者字段与媒体名称参考 [ScreenScraper API](https://www.screenscraper.fr/webapi2.php) 和 [Batocera ScreenScraper 适配器](https://github.com/batocera-linux/batocera-emulationstation/blob/master/es-app/src/scrapers/ScreenScraper.cpp)。

占位由视图按发行版本与共享字段定义生成，不为每项未知数据写入重复空记录。名称可显示有明确标记的目录标题回退值；未知简介、评分、日期、提供者 ID、媒体 URL、文件路径和摘要均为空，状态为 `pending`。未执行在线刮削，没有新增实际图片或视频，没有保存 API 凭据。

```sql
SELECT * FROM v_screenscraper_games WHERE release_id = 1;
SELECT * FROM v_batocera_game_fields WHERE release_id = 1;
SELECT * FROM v_batocera_media_slots WHERE release_id = 1;
SELECT * FROM frontend_fields WHERE category = 'media';
```

`frontend_game_values` 支持语言和地区区分，`scraper_game_links` 保存经确认的提供者游戏 ID 与来源，`frontend_media_slots` 可关联既有 `media` 记录。未来实际资产通过 `media → files → objects → chunks` 存放完整字节和校验值，PDF 可使用 `files.kind=other`。封面、截图、Logo 的初始映射可配置；杂志和卡带图保留占位但不猜测提供者媒体类型。

此扩展提供字段、状态、约束及关联，不包含联网 ScreenScraper 客户端或 Batocera `gamelist.xml` 导出器。后续适配器需要选择语言／地区、转换评分与日期，并选定具体 ROM 版本和导出路径；不能把所有同名版本当成同一个文件。
