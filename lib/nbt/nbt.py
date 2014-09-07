#!/usr/bin/env python

import os
import sys
import subprocess

lib_path = os.path.dirname(os.path.realpath(__file__))

PROCESS_ENUM4LINUX = 'enum4linux -a %(host)s > %(output_dir)s/%(host)s-nbt-enum4linux.txt'

def start_processes(process, ip, directory):
    try:
        subprocess.check_output(process % {
            'output_dir': directory,
            'host': ip,
            'lib_path': lib_path,
        }, shell=True)
    except Exception as exception:
        # Suppress exceptions for enum4linux, pipe to file works properly.
        pass

def scan(ip, directory):
    for process in [PROCESS_ENUM4LINUX]:
        start_processes(process, ip, directory)

if __name__ == '__main__':
    scan(sys.argv[1], sys.argv[2])