#!/usr/bin/env python
#
# Author: Maleus
# Date: 7.28.14
# Notes: Made for Kali Linux, not tested on other distros.
#
# import ipdb; ipdb.set_trace()

import argparse
import sys
import os
import subprocess
import multiprocessing
from multiprocessing import Process

from lib import nmap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is intended to simplify the common enumeration \
        actions taken during a pentest engagement. The only parameter required is a path to a list of \
        host IP addresses. nmap processes are then kicked off which in turn intelligently kick off ftp \
        scanning (anonymous & hydra), enum4linux, dirb or nikto processes depending on nmap service \
        enumeration output. All output is organized and saved to local folders named by IP address.')

    parser.add_argument('filepath', metavar='file path', type=argparse.FileType('r'), help='path to file of IP addresses')
    args = parser.parse_args()
    
    file_contents = args.filepath.read()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    ip_list = []

    # handle empty file
    if file_contents == '':
        print '[!] The contents of the provided file are empty.'
        sys.exit(0)
    else:
        # turn the file contents into a list of ip addresses
        # trim blank lines out of list
        ip_list = file_contents.split('\n')
        ip_list = [ip for ip in ip_list if ip != '']


    print '[+] IP list parsed, sending hosts to nmap...'
    for ip in ip_list:
        jobs = []
        p = multiprocessing.Process(target=nmap.scan, args=(ip,current_dir))
        jobs.append(p)
        p.start()
