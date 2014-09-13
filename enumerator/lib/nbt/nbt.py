#!/usr/bin/env python
""" 
The Netbios module performs netbios-related 
enumeration tasks.

@author: Steve Coward (steve<at>sugarstack.io)
@version: 1.0
"""
import os
import sys
from ..process_manager import ProcessManager
from ..generic_service import GenericService


class NbtEnumeration(GenericService, ProcessManager):
    LIB_PATH = os.path.dirname(os.path.realpath(__file__))
    SERVICE_DEFINITION = 'port:445'
    PROCESSES = [
        'enum4linux -a %(host)s > %(output_dir)s/%(host)s-nbt-enum4linux.txt', ]

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
                'output_dir': directory,
            }, display_exception=False)

if __name__ == '__main__':
    """For testing purposes, this 
    module can be executed as a script.
    Use the following syntax from the root
    directory of enumerator:

    python -m lib.nbt.nbt <ip> <output directory>
    """
    nbt = NbtEnumeration()
    nbt.scan(sys.argv[2], dict(ip=sys.argv[1]))
