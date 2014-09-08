#!/usr/bin/env python

import os, sys
from ..generic_service import GenericService

class FtpEnumeration(GenericService):
    LIB_PATH = os.path.dirname(os.path.realpath(__file__))
    PROCESSES = [
        'nmap -Pn -p %(port)s \
            --script=ftp-anon,ftp-bounce,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221 \
            -oN %(output_dir)s/%(host)s-ftp-%(port)s-standard.txt %(host)s',
        'hydra -L %(lib_path)s/user-password-micro.txt -P %(lib_path)s/user-password-micro.txt \
            -o %(output_dir)s/%(host)s-ftp-%(port)s-hydra.txt ftp://%(host)s:%(port)s',
    ]

    def scan(self, ip, port, directory):
        for process in self.PROCESSES:
            self.start_processes(process, params={
                'host': ip,
                'port': port,
                'output_dir': directory,
                'lib_path': self.LIB_PATH,
            }, display_exception=False)

if __name__ == '__main__':
    ftp = FtpEnumeration()
    ftp.scan(sys.argv[1], sys.argv[2], sys.argv[3])
