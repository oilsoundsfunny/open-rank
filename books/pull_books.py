#!/usr/bin/env python3

import os
import pathlib
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
import zstandard as zstd

BOOKS = [
    'https://github.com/AndyGrant/openbench-books/raw/refs/heads/master/UHO_Lichess_4852_v1.epd.zip'
]

def download(url, dest):
    print('Downloading %s' % url)
    urllib.request.urlretrieve(url, dest)

def compress_zstd(src, dst):
    print('Compressing %s -> %s' % (src.name, dst.name))
    with open(src, 'rb') as fin:
        with open(dst, 'wb') as fout:
            with zstd.ZstdCompressor(level=19).stream_writer(fout) as writer:
                while (chunk := fin.read(1024* 1024)):
                    writer.write(chunk)

def main():

    artifacts_dir = pathlib.Path('artifacts')
    artifacts_dir.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = pathlib.Path(tmpdir)

        for url in BOOKS:
            parsed   = urllib.parse.urlparse(url)
            zip_name = pathlib.Path(parsed.path).name

            if not zip_name.endswith('.zip'):
                raise RuntimeError('URL does not end with .zip: %s' % url)

            base_name   = zip_name[:-4]
            zip_path    = tmpdir / zip_name
            output_path = artifacts_dir / (base_name + '.zst')

            if output_path.exists():
                print ('Found %s locally' % (output_path))
                continue

            download(url, zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zf:
                names = []
                for n in zf.namelist():
                    if not n.endswith('/'):
                        names.append(n)

                if len(names) != 1:
                    raise RuntimeError('%s contains %d files (expected 1)' % (zip_name, len(names)))

                member = names[0]
                zf.extract(member, tmpdir)

            extracted   = tmpdir / member
            compress_zstd(extracted, output_path)

            print('Saved %s' % (output_path))

if __name__ == '__main__':
    main()