#!/usr/bin/env python

import os
import sys
import subprocess

lib_path = os.path.dirname(os.path.realpath(__file__))

PROCESS_NMAP_FTP = 'nmap -Pn -p %(port)s \
    --script=ftp-anon,ftp-bounce,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221 \
    -oN %(output_dir)s/%(host)s-ftp-%(port)s-standard.txt %(host)s'

PROCESS_HYDRA_FTP = 'hydra -L %(lib_path)s/user-password-micro.txt -P %(lib_path)s/user-password-micro.txt \
    -o %(output_dir)s/%(host)s-ftp-%(port)s-hydra.txt ftp://%(host)s:%(port)s'

def start_processes(process, ip, port, directory):
    try:
        subprocess.check_output(process % {
            'output_dir': directory,
            'host': ip,
            'port': port,
            'lib_path': lib_path,
        }, shell=True)
    except Exception as exception:
        print '   [!] Error running process %s' % process.split(' ')[0]
        print '   [!] Exception: %s' % exception

def scan(ip, port, directory):
    for process in [PROCESS_NMAP_FTP, PROCESS_HYDRA_FTP]:
        start_processes(process, ip, port, directory)

if __name__ == '__main__':
    scan(sys.argv[1], sys.argv[2], sys.argv[3])