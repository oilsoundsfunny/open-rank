#!/usr/bin/env python3

import argparse
import os
from bench_engine import bench_engine

def main(seconds, threads, debug):

    for name in sorted(os.listdir('tarballs')):

        engine = name.removesuffix('.tar.zst').replace('openrank-', '')
        values = bench_engine(engine, seconds, threads, debug)
        avg    = sum(values) / len(values)

        print ('%32s %10d' % (engine, avg))

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('--seconds', type=int, default=5)
    p.add_argument('--threads', type=int, default=1)
    p.add_argument('--debug', default=False, action='store_true')
    args = p.parse_args()

    main(args.seconds, args.threads, args.debug)
