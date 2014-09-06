#!/usr/bin/env python

import sys
import os
import re
import glob
import time
import subprocess
import multiprocessing
from multiprocessing import Process
# from blinker import signal

PROCESS_TCP = 'nmap -Pn -T4 -sS -sV -p- -oN %(output_dir)s/%(host)s-tcp-standard.txt -oG %(output_dir)s/%(host)s-tcp-greppable.txt %(host)s'
PROCESS_UDP = 'nmap -Pn -T4 -sU -sV --top-ports 100 -oN %(output_dir)s/%(host)s-udp-standard.txt -oG %(output_dir)s/%(host)s-udp-greppable.txt %(host)s'

# Very broad match for greppable nmap output.
# e.g. will match: 22/open/tcp//tcpwrapped///, 8081/open/tcp//http//Node.js (Express middleware)/
SERVICE_PATTERN = re.compile(r'Ports: (\d+\/.+\/)')

def parse_results(ip, directory):
    """Find greppable nmap scan output, extract service data

    Keyword arguments:
    ip -- IP address
    directory -- directory to search for scan output
    """

    # output structure to store results
    results = {
        ip: {
            'tcp': [],
            'udp': [],
        },
    }

    # find greppable nmap output files
    scan_output = glob.glob('%s/*greppable*' % directory)
    for output_file in scan_output:
        contents = ''
        with open(output_file, 'r') as fh:
            contents = fh.read()

        # locate service-related output from file contents
        match = SERVICE_PATTERN.search(contents)

        # store regex matched string, if it fails, match is an empty string.
        try:
            match = match.groups()[0]
        except:
            match = ''

        # services are separated by a comma and strip any whitespace.
        services = match.split(',')
        services = [service_entry.strip() for service_entry in services]

        for service_entry in services:
            # split apart the service data, excluding the last list element (end of string).
            try:
                port, state, protocol, owner, service, rpc_info, version = service_entry.split('/')[:-1]
                results[ip][protocol].append({
                    'port': port,
                    'state': state,
                    'owner': owner,
                    'service': service,
                    'version': version,
                })
            except:
                # TODO: debug exceptions
                pass

    return results

def start_processes(process, ip, directory):
    """Receive a shell command statement and execute it.

    Keyword arguments:
    process -- shell command
    output_dir -- directory to store command output
    ip -- IP address being scanned
    """

    subprocess.check_output(process % {'output_dir': directory, 'host': ip}, shell=True)

def scan(ip, directory):
    """Build output folder structure and initiate multiprocessing threads

    Keyword arguments:
    ip -- IP address being scanned
    directory -- directory to store command output
    """
    
    # ensure output directory exists; if it doesn't, create it
    output_dir = '%s/%s' % (directory, ip)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # fire off tcp scan
    print '   [-] nmap: running TCP & UDP scans for host: %s' % ip
    jobs = []
    for process in [PROCESS_TCP, PROCESS_UDP]:
        p = multiprocessing.Process(target=start_processes, args=(process, ip, output_dir))
        jobs.append(p)
        p.start()
    p.join()

    time.sleep(5)

    # nmap scans have completed at this point, parse file output
    print parse_results(ip, output_dir)

if __name__ == '__main__':
    scan(sys.argv[1],sys.argv[2])
