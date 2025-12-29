#!/usr/bin/env python3

import argparse
import os
import subprocess

def image_exists(name):
    return subprocess.run(
        ['docker', 'image', 'inspect', name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0

def main():

    DOCKER_DIR    = './dockers'
    TARBALL_DIR   = './tarballs'
    LOG_FILE_PATH = os.path.join('docker_build.log')

    p = argparse.ArgumentParser()
    p.add_argument('--rebuild', action='store_true', help='Rebuild existing images')
    p.add_argument('--dry', action='store_true', help='Do not actually do anything')
    args = p.parse_args()

    # Ensure tarball dir exists
    os.makedirs(TARBALL_DIR, exist_ok=True)

    # Ensure logfile exists, to later append to
    with open(LOG_FILE_PATH, 'w') as f:
        f.write('Docker build log begin...\n\n')

    for filename in sorted(os.listdir(DOCKER_DIR)):

        dockerfile_path = os.path.join(DOCKER_DIR, filename)
        base_name       = filename.rsplit('.Dockerfile', 1)[0]
        image_name      = 'openrank-%s' % (base_name.lower())

        if not args.rebuild and image_exists(image_name):
            print ('Found image %s for %s' % (image_name, dockerfile_path))
            continue

        print('Building image %s from %s...' % (image_name, dockerfile_path))

        if args.dry:
            continue

        try:
            # Build the Docker Image
            build_cmd = ['docker', 'build', '-t', image_name, '-f', dockerfile_path, DOCKER_DIR]
            subprocess.run(build_cmd, check=True, capture_output=True, text=True)

            # Export the Image
            tar_path = os.path.join(TARBALL_DIR, f'{image_name}.tar')
            save_cmd = ['docker', 'save', '-o', tar_path, image_name]
            subprocess.run(save_cmd, check=True, capture_output=True, text=True)

            # Compress with zstd
            compressed_path = tar_path + '.zst'
            compress_cmd = ['zstd', '-f', tar_path, '-o', compressed_path]
            subprocess.run(compress_cmd, check=True, capture_output=True, text=True)

            # Remove the uncompressed tar
            os.remove(tar_path)

        except subprocess.CalledProcessError as e:
            # Dump all output to log file
            with open(LOG_FILE_PATH, 'a') as f:
                f.write(f'Error building {filename}:\n')
                f.write(e.stdout or '')
                f.write('\n')
                f.write(e.stderr or '')
                f.write('\n' + '=' * 60 + '\n')
            print('Failed building %s. Check %s for details.' % (filename, LOG_FILE_PATH))

if __name__ == '__main__':
    main()