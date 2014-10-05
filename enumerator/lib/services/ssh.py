#!/usr/bin/env python
""" 
The SSH module performs ssh-related 
enumeration tasks.

@author: Steve Coward (steve<at>sugarstack.io)
@author: Erik Dominguez (maleus<at>overflowsecurity.com)
@version: 1.0
"""
import sys
from .. import config
from ..process_manager import ProcessManager
from ..generic_service import GenericService


class SshEnumeration(GenericService, ProcessManager):
    SERVICE_DEFINITION = 'service:ssh'
    PROCESSES = [{
        'command': 'nmap -Pn -p %(port)s %(scan_mode)s \
            -oN %(output_dir)s/%(host)s-ssh-%(port)s-standard.txt %(host)s',
        'normal': '-T4 --script=ssh-hostkey',
        'stealth': '-T2'
    }, {
        'command': 'hydra -L %(static_path)s/user-password-%(scan_mode)s.txt -P %(static_path)s/user-password-%(scan_mode)s.txt \
            -o %(output_dir)s/%(host)s-ssh-%(port)s-hydra.txt -t 4 %(host)s ssh',
        'normal': 'tiny',
        'stealth': 'micro',
    }]

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
            self.start_processes(process.get('command'), params={
                'host': service_parameters.get('ip'),
                'port': service_parameters.get('port'),
                'output_dir': directory,
                'static_path': self.static_path,
                'scan_mode': process.get(config.mode),
            }, display_exception=False)

if __name__ == '__main__':
    """For testing purposes, this 
    module can be executed as a script.
    Use the following syntax from the root
    directory of enumerator:

    python -m lib.ssh.ssh <ip> <port> <output directory>
    """
    ssh = SshEnumeration()
    ssh.scan(sys.argv[3], dict(ip=sys.argv[1], port=sys.argv[2]))
