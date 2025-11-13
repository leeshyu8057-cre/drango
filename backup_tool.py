#!/usr/bin/env python3
"""
Backup tool for django_docker_app.

Creates a ZIP archive of the project (excluding virtualenvs, backups, __pycache__, etc.)
and names the archive using the CRC-32 hash of the timestamp (FIPS-unrelated but
fulfills the requirement of CRC output). Usage:

    python backup_tool.py            # backup current directory
    python backup_tool.py --root chem_site/bioweb --dest backups
"""

import argparse
import datetime as dt
import os
from pathlib import Path
import sys
import zipfile
import zlib

DEFAULT_EXCLUDES = {
    '.git',
    '.mypy_cache',
    '.pytest_cache',
    '__pycache__',
    'backups',
    'venv',
    'env',
    '.venv',
    'node_modules',
}


def crc32_of(text: str) -> str:
    """Return 8-char lowercase CRC32 string for the given text."""
    return format(zlib.crc32(text.encode('utf-8')) & 0xFFFFFFFF, '08x')


def should_skip(path: Path, root: Path, excludes) -> bool:
    rel_parts = path.relative_to(root).parts
    for part in rel_parts:
        if part in excludes:
            return True
    return False


def build_backup(root: Path, dest: Path, excludes):
    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    crc_name = crc32_of(timestamp)
    dest.mkdir(parents=True, exist_ok=True)
    backup_path = dest / f'{crc_name}.zip'

    with zipfile.ZipFile(backup_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for path in root.rglob('*'):
            if should_skip(path, root, excludes):
                continue
            if path.is_file() and path.suffix == '.pyc':
                continue
            arcname = path.relative_to(root)
            zf.write(path, arcname)

    return backup_path, timestamp


def main():
    parser = argparse.ArgumentParser(description='Create CRC32-named backup archive.')
    parser.add_argument('--root', default='.', help='Root directory to backup (default: current dir)')
    parser.add_argument('--dest', default='backups', help='Destination directory for archives')
    parser.add_argument('--exclude', action='append', default=[], help='Extra directories to exclude')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        sys.exit(f'Root directory not found: {root}')

    excludes = DEFAULT_EXCLUDES.union(set(args.exclude))

    backup_path, timestamp = build_backup(root, Path(args.dest).resolve(), excludes)
    print(f'✅ Backup created: {backup_path}')
    print(f'   Timestamp: {timestamp} (CRC32 -> {backup_path.stem})')
    print(f'   Source root: {root}')


if __name__ == '__main__':
    main()
