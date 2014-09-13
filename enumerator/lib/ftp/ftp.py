#!/usr/bin/env python
""" 
The FTP module performs ftp-related 
enumeration tasks.

@author: Steve Coward (steve<at>sugarstack.io)
@version: 1.0
"""
import os
import sys
from ..process_manager import ProcessManager
from ..generic_service import GenericService


class FtpEnumeration(GenericService, ProcessManager):
    LIB_PATH = os.path.dirname(os.path.realpath(__file__))
    SERVICE_DEFINITION = 'service:ftp'
    PROCESSES = [
        'nmap -Pn -p %(port)s \
            --script=ftp-anon,ftp-bounce,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221 \
            -oN %(output_dir)s/%(host)s-ftp-%(port)s-standard.txt %(host)s',
        'hydra -L %(lib_path)s/user-password-micro.txt -P %(lib_path)s/user-password-micro.txt \
            -o %(output_dir)s/%(host)s-ftp-%(port)s-hydra.txt ftp://%(host)s:%(port)s',
    ]

    def scan(self, directory, service_parameters):
        """Iterates over PROCESSES and builds
        the specific parameters required for 
        command line execution of each process.

        @param directory: Directory path where 
        final command output will go.

        @param service_parameters: Dictionary with
        key:value pairs of service-related data.
        """

        for process in self.PROCESSES:
            self.start_processes(process, params={
                'host': service_parameters.get('ip'),
                'port': service_parameters.get('port'),
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
    ftp.scan(sys.argv[3], dict(ip=sys.argv[1], port=sys.argv[2]))
