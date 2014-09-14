#!/usr/bin/env python
""" 
The Telnet module performs ftp-related 
enumeration tasks.

@author: Erik Dominguez (maleus<at>overflowsecurity.com)
@version: 1.0
"""
import os
import sys
from ..process_manager import ProcessManager
from ..generic_service import GenericService


class TelnetEnumeration(GenericService, ProcessManager):
    LIB_PATH = os.path.dirname(os.path.realpath(__file__))
    SERVICE_DEFINITION = 'service:telnet'
    PROCESSES = [
        'nmap -Pn -p %(port)s \
            --script=telnet-encryption \
            -oN %(output_dir)s/%(host)s-telnet-%(port)s-standard.txt %(host)s',
        'hydra -L %(lib_path)s/user-password-micro.txt -P %(lib_path)s/user-password-micro.txt \
            -o %(output_dir)s/%(host)s-telnet-%(port)s-hydra.txt %(host) telnet',
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

    python -m lib.telnet.telnet <ip> <port> <output directory>
    """
    telnet = TelnetEnumeration()
    telnet.scan(sys.argv[3], dict(ip=sys.argv[1], port=sys.argv[2]))
