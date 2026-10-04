"""Build a public name-update Catalog from a checksum-pinned, payload-free release."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import urllib.request

from import_game_names import import_names, resource

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_TABLES = ('compression_groups', 'chunks', 'object_chunks')


def digest_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def table_digest(c, table):
    columns = sorted(row[1] for row in c.execute(f'PRAGMA table_info("{table}")'))
    selection = ','.join('"' + column + '"' for column in columns)
    rows = c.execute(f'SELECT {selection} FROM "{table}" ORDER BY {selection}').fetchall()
    data = json.dumps({'columns': columns, 'rows': rows}, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(data.encode()).hexdigest()


def require_catalog(c):
    meta = dict(c.execute('SELECT key,value FROM meta'))
    if meta.get('edition') != 'catalog-only' or meta.get('payload_available') != 'false':
        raise ValueError('Input must be the metadata-only Catalog edition')
    for table in PAYLOAD_TABLES:
        if c.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]:
            raise ValueError(f'Refusing input with data in {table}')


def verify_original_tables(c, expected):
    for table, checks in expected.items():
        digest, count = hashlib.sha256(), 0
        for row in c.execute(f'SELECT * FROM "{table}"'):
            for value in row:
                encoded = value if isinstance(value, bytes) else repr(value).encode()
                digest.update(str(len(encoded)).encode() + b':' + encoded)
            count += 1
        if {'count': count, 'sha256': digest.hexdigest()} != checks:
            raise ValueError(f'Original Catalog table changed: {table}')


def run_embedded_tests(c):
    with tempfile.TemporaryDirectory(prefix='catalog-release-tests-') as folder:
        output = Path(folder)
        names = ['schema.sql', 'build_v3.py', 'build_v2.py', 'seed.json', 'group_schema.sql',
                 'migrate_v3.py', 'build_catalog.py', 'nointro.py', 'nointro_schema.sql',
                 'tests.py', 'tests_storage.py', 'tests_frontend.py', 'tests_nointro.py',
                 'tests_groups.py', 'import_game_names.py', 'game_names_schema.sql', 'tests_game_names.py']
        resources = {name: name for name in names}
        resources.update({'engine.py': 'engine.full.py', 'catalog_engine.py': 'engine.py'})
        for filename, name in resources.items():
            content = c.execute('SELECT content FROM resources WHERE name=?', (name,)).fetchone()[0]
            (output / filename).write_text(content, encoding='utf-8')
        test = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'tests', 'tests_storage',
                               'tests_frontend', 'tests_nointro', 'tests_groups', 'tests_game_names'],
                              cwd=output, capture_output=True, text=True)
        print(test.stdout + test.stderr, flush=True)
        if test.returncode:
            raise RuntimeError('Embedded Catalog tests failed')
        return test.stdout + test.stderr


def build(manifest_path, output, base=None):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    output = Path(output)
    if output.exists():
        raise ValueError('Refusing to replace an existing output Catalog')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='name-catalog-base-') as folder:
        if base is None:
            base = Path(folder) / 'base.sqlite'
            request = urllib.request.Request(manifest['base_url'], headers={'User-Agent': 'RetroBoxDB-release'})
            with urllib.request.urlopen(request, timeout=120) as response, base.open('wb') as target:
                shutil.copyfileobj(response, target)
        if digest_file(base) != manifest['base_sha256']:
            raise ValueError('Base Catalog SHA256 mismatch')
        source = sqlite3.connect(Path(base).resolve().as_uri() + '?mode=ro', uri=True)
        try:
            require_catalog(source)
            c = sqlite3.connect(output)
            source.backup(c)
        finally:
            source.close()
        try:
            c.execute('PRAGMA foreign_keys=ON')
            c.execute('PRAGMA synchronous=FULL')
            c.execute('BEGIN IMMEDIATE')
            csv_path = ROOT / manifest['source_csv']
            if digest_file(csv_path) != manifest['source_csv_sha256']:
                raise ValueError('Name CSV SHA256 mismatch')
            import_names(c, csv_path.read_bytes(), csv_path.name)
            # Preserve the local Catalog source-import timestamp and therefore row identities.
            c.execute('UPDATE game_name_imports SET imported_at=? WHERE source_sha256=?',
                      (manifest['source_imported_at'], manifest['source_csv_sha256']))
            for name, info in manifest['resources'].items():
                content = (ROOT / info['path']).read_bytes().decode('utf-8')
                resource(c, name, info['kind'], content)
            original = json.loads((ROOT / 'reports/game-names-matching-verification-report.json').read_text())
            fingerprints = original['databases']['RetroBoxDB.NES.Catalog.sqlite']['original_data_fingerprints']
            verify_original_tables(c, fingerprints)
            for table, expected in manifest['name_table_sha256'].items():
                if table_digest(c, table) != expected:
                    raise ValueError(f'Published name data differs from the local Catalog: {table}')
            require_catalog(c)
            if c.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Foreign key check failed')
            if c.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                raise ValueError('Integrity check failed')
            for name, content, sha256 in c.execute('SELECT name,content,sha256 FROM resources'):
                if hashlib.sha256(content.encode()).hexdigest() != sha256:
                    raise ValueError(f'Resource checksum mismatch: {name}')
            run_embedded_tests(c)
            resource(c, 'name-release-manifest', 'json', json.dumps(manifest, ensure_ascii=False, indent=2))
            c.commit()
            c.execute('VACUUM')
            report = json.loads(c.execute("SELECT content FROM resources WHERE name='catalog-report'").fetchone()[0])
            report.update({'metadata_update': 'game names extension v4; published from a pinned Catalog',
                           'release_tag': manifest['tag'], 'integrity_check': 'ok', 'foreign_key_errors': [],
                           'name_tables_equal_local_catalog': True, 'synthetic_tests': 94})
            for _ in range(3):
                report['counts'] = {table: c.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]
                                    for (table,) in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
                report['size_bytes'] = output.stat().st_size
                resource(c, 'catalog-report', 'json', json.dumps(report, ensure_ascii=False, indent=2))
                c.commit()
        except BaseException:
            c.rollback()
            raise
        finally:
            c.close()
    checksum = digest_file(output)
    (output.parent / 'SHA256SUMS').write_text(f'{checksum}  {output.name}\n', encoding='utf-8')
    notes = (ROOT / 'release/notes.md').read_text(encoding='utf-8')
    notes += f'\nCatalog size: **{output.stat().st_size:,} bytes**.\n\nSHA256: `{checksum}`\n'
    (output.parent / 'release-notes.md').write_text(notes, encoding='utf-8')
    print(json.dumps({'catalog': str(output), 'sha256': checksum, 'size': output.stat().st_size,
                      'tag': manifest['tag'], 'name_tables_equal_local_catalog': True}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'release/catalog-release.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/RetroBoxDB.NES.Catalog.sqlite')
    parser.add_argument('--base', type=Path, help='Use a local base with the same required checksum')
    args = parser.parse_args()
    build(args.manifest, args.output, args.base)
