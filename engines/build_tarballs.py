#!/usr/bin/env python3

import subprocess
import os

DOCKER_DIR  = './dockers'
TARBALL_DIR = './tarballs'

os.makedirs(TARBALL_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(DOCKER_DIR, 'docker_build.log')

with open(LOG_FILE_PATH, 'w') as f:
    f.write('Docker build log begin...\n\n')

for filename in os.listdir(DOCKER_DIR):

    dockerfile_path = os.path.join(DOCKER_DIR, filename)
    base_name       = filename.rsplit('.Dockerfile', 1)[0]
    image_name      = 'openrank-%s' % (base_name.lower())

    print('Building image %s from %s...' % (image_name, dockerfile_path))

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

        print('%s saved and compressed as %s' % (image_name, compressed_path))

    except subprocess.CalledProcessError as e:
        # Dump all output to log file
        with open(LOG_FILE_PATH, 'a') as f:
            f.write(f'Error building {filename}:\n')
            f.write(e.stdout or '')
            f.write('\n')
            f.write(e.stderr or '')
            f.write('\n' + '=' * 60 + '\n')
        print('Failed building %s. Check %s for details.' % (filename, LOG_FILE_PATH))
