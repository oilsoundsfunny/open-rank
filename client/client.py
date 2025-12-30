#!/usr/bin/env python3

import argparse
import json
import os
import requests

from exceptions import *
from hardware import HardwareConfig

def url_join(*parts):
    return '/'.join(p.strip('/') for p in parts if p) + '/'

def parse_arguments():

    # We can use ENV variables for the Username, Passwords, and Servers
    req_user   = 'OPENRANK_USERNAME' not in os.environ
    req_pass   = 'OPENRANK_PASSWORD' not in os.environ
    req_server = 'OPENRANK_SERVER'   not in os.environ

    help_user   = 'Username. May also be provided via OPENRANK_USERNAME environment variable'
    help_pass   = 'Password. May also be provided via OPENRANK_PASSWORD environment variable'
    help_server = 'Server URL. May also be provided via OPENRANK_SERVER environment variable'

    # Pretty formatting
    p = argparse.ArgumentParser(
        formatter_class=lambda prog:
            argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=10)
    )

    # Create and parse all arguments into a raw format
    p.add_argument('-U', '--username', help=help_user  , required=req_user  )
    p.add_argument('-P', '--password', help=help_pass  , required=req_pass  )
    p.add_argument('-S', '--server'  , help=help_server, required=req_server)

    # Replace with ENV variables if needed
    args, unknown = p.parse_known_args()
    args.username = args.username if args.username else os.environ['OPENRANK_USERNAME']
    args.password = args.password if args.password else os.environ['OPENRANK_PASSWORD']
    args.server   = args.server   if args.server   else os.environ['OPENRANK_SERVER'  ]

    return args

def client_connect(args, hwinfo):

    secret = worker_id = None

    if os.path.exists('worker.info'):
        with open('worker.info', 'r') as f:
            secret, worker_id = f.read().strip().split()

    payload = {
        'username' : args.username,
        'password' : args.password,
        'hardware' : json.dumps(vars(hwinfo)),
    }

    if secret and worker_id:
        payload.update({ 'secret': secret, 'worker_id': worker_id })

    if 'error' in (resp := requests.post(url_join(args.server, 'client/connect/'), data=payload).json()):
        raise OpenRankAuthenticationError(resp['error'])

    with open('worker.info', 'w') as f:
        f.write('%s %s' % (resp['secret'], resp['worker_id']))

    return resp

def client_request_work(args, auth_data):

    if 'error' in (resp := requests.post(url_join(args.server, 'client/request_work/'), data=auth_data).json()):
        raise OpenRankAuthenticationError(resp['error'])

    return resp

if __name__ == '__main__':

    # Use client.py's path as the base pathway always
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Grab the hardware info first, in case this machine is not allowed
    hwinfo = HardwareConfig()

    # Username, Password, Server
    args = parse_arguments()

    # Going forward, all requests contain secret and worker_id
    auth_data = client_connect(args, hwinfo)

    # Could be { 'warning' : ... }
    workload = client_request_work(args, auth_data)

    print (workload)
