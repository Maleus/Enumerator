#!/usr/bin/env python

import sys
import subprocess
import multiprocessing
from multiprocessing import Process

PROCESS_NIKTO = 'nikto -F txt -o %(output_dir)s/%(host)s-http-nikto.txt -h %(host)s -p %(port)s'
PROCESS_DIRB = 'dirb %(url)s %(wordlist)s -o %(output_dir)s/%(host)s-http-dirb.txt -r -S -w'
DIRB_WORDLISTS = '/usr/share/dirb/wordlists/common.txt,/opt/metasploit/apps/pro/msf3/data/wmap/wmap_dirs.txt'

def start_processes(process, ip, port, url, directory):
    subprocess.check_output(process % {
        'output_dir': directory,
        'host': ip,
        'port': port,
        'url': url,
        'wordlist': DIRB_WORDLISTS,
    })

def scan(ip, port, directory):
    url = 'https://%s/' % ip if port == '443' else 'http://%s/' % ip
    for process in [PROCESS_NIKTO, PROCESS_DIRB]:
        jobs = []
        p = multiprocessing.Process(target=start_processes, args=(process, ip, port, url, directory))
        jobs.append(p)
        p.start()

if __name__ == '__main__':
    scan(sys.argv[1], sys.argv[2], sys.argv[3])
