#!/usr/bin/env python3

import argparse
import re
import subprocess
import threading

def run_engine(engine, seconds, result, debug):

    proc = subprocess.Popen(
        ['docker', 'run', '-i', '--rm', 'openrank-' + engine],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    proc.stdin.write('uci\n')
    proc.stdin.write('isready\n')
    proc.stdin.flush()

    while proc.stdout.readline().rstrip() != 'readyok':
        pass

    proc.stdin.write('position startpos\n')
    proc.stdin.write('go movetime %d\n' % (seconds * 1000))
    proc.stdin.flush()

    nps = None
    while 'bestmove' not in (line := proc.stdout.readline()):
        if debug:
            print (line)
        if (m := re.search(r'nps\s+(\d+)', line)):
            nps = int(m.group(1))

    proc.stdin.write('quit\n')
    proc.stdin.flush()
    proc.wait()

    result['nps'] = nps

def bench_engine(engine, seconds, threads, debug):

    results = [
        { 'nps' : None } for f in range(threads)
    ]

    workers = [
        threading.Thread(
            target=run_engine,
            args=(engine, seconds, results[f], debug)
        ) for f in range(threads)
    ]

    for t in workers:
        t.start()

    for t in workers:
        t.join()

    return [result['nps'] for result in results]

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('--engine', required=True)
    p.add_argument('--seconds', type=int, default=10)
    p.add_argument('--threads', type=int, default=1)
    p.add_argument('--debug', default=False, action='store_true')
    args = p.parse_args()

    values = bench_engine(args.engine, args.seconds, args.threads, args.debug)

    print('min:', min(values))
    print('max:', max(values))
    print('avg:', sum(values) / len(values))
    print('raw:', values)
