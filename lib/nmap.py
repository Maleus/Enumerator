#!/usr/bin/env python

import sys
import os
import subprocess

process_tcp = 'nmap -Pn -T4 -sS -sV -p- -oN %(output_dir)s/%(host)s-tcp-standard.txt -oG %(output_dir)s/%(host)s-tcp-greppable.txt %(host)s'
process_udp = 'nmap -Pn -T4 -sU -sV --top-ports 200 -oN %(output_dir)s/%(host)s-udp-standard.txt -oG %(output_dir)s/%(host)s-udp-greppable.txt %(host)s'

def scan(ip, directory):
    # ensure output directory exists; if it doesn't, create it
    output_dir = '%s/%s' % (directory, ip)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # fire off tcp scan
    print '   [-] nmap: running TCP & UDP scans for host: %s' % ip
    scan_results_tcp = subprocess.check_output(process_tcp % {'output_dir': output_dir, 'host': ip}, shell=True)
    scan_results_udp = subprocess.check_output(process_udp % {'output_dir': output_dir, 'host': ip}, shell=True)

if __name__ == '__main__':
    # for testing purposes
    # 1st arg is IP, 2nd is a directory
    scan(sys.argv[1],sys.argv[2])