#!/usr/bin/env python
""" 
The FTP module performs ftp-related 
enumeration tasks.

@author: Steve Coward (steve<at>sugarstack.io)
@version: 1.0
"""
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
        """Iterates over PROCESSES and builds
        the specific parameters required for 
        command line execution of each process.

        @param ip: IP address being processed.
        
        @param port: Port which the FTP process 
        is running on.

        @param directory: Directory path where 
        final command output will go.
        """
        for process in self.PROCESSES:
            self.start_processes(process, params={
                'host': ip,
                'port': port,
                'output_dir': directory,
                'lib_path': self.LIB_PATH,
            }, display_exception=False)

if __name__ == '__main__':
    """For testing purposes, this 
    module can be executed as a script.
    Use the following syntax from the root
    directory of enumerator:

    python -m lib.ftp.ftp <ip> <port> <output directory>
    """
    ftp = FtpEnumeration()
    ftp.scan(sys.argv[1], sys.argv[2], sys.argv[3])
