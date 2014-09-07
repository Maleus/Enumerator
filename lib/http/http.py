#!/usr/bin/env python

import sys
import subprocess

PROCESS_NIKTO = 'nikto -F txt -o %(output_dir)s/%(host)s-http-%(port)s-nikto.txt -h %(host)s -p %(port)s'
PROCESS_DIRB = 'dirb %(url)s %(wordlist)s -o %(output_dir)s/%(host)s-http-%(port)s-dirb.txt -r -S -w'

# TODO: Make these configurable either at runtime or via config file.
# On the Kali distro, both of these files/paths exist.
DIRB_WORDLISTS = '/usr/share/dirb/wordlists/common.txt,/opt/metasploit/apps/pro/msf3/data/wmap/wmap_dirs.txt'

def start_processes(process, ip, port, url, directory):
    try:
        subprocess.check_output(process % {
            'output_dir': directory,
            'host': ip,
            'port': port,
            'url': url,
            'wordlist': DIRB_WORDLISTS,
        }, shell=True)
    except Exception as exception:
        print '   [!] Error running process %s' % process.split(' ')[0]
        print '   [!] Exception: %s' % exception

def scan(ip, port, directory):
    url = 'https://%s/' % ip if port == '443' else 'http://%s:%s/' % (ip, port)
    for process in [PROCESS_NIKTO, PROCESS_DIRB]:
        # TODO: multiprocessing multiple http scanning scripts may flood the victim, research this.
        # Until then, execute scanning scripts synchronously.
        start_processes(process, ip, port, url, directory)

if __name__ == '__main__':
    scan(sys.argv[1], sys.argv[2], sys.argv[3])
