#!/usr/bin/env python
""" 
The Netbios module performs netbios-related 
enumeration tasks.

@author: Steve Coward (steve<at>sugarstack.io)
@version: 1.0
"""
import os, sys
from ..generic_service import GenericService

class NbtEnumeration(GenericService):
    LIB_PATH = os.path.dirname(os.path.realpath(__file__))
    PROCESSES = ['enum4linux -a %(host)s > %(output_dir)s/%(host)s-nbt-enum4linux.txt',]

    def scan(self, ip, directory):
        """Iterates over PROCESSES and builds
        the specific parameters required for 
        command line execution of each process.

        @param ip: IP address being processed.

        @param directory: Directory path where 
        final command output will go.
        """
        for process in self.PROCESSES:
            self.start_processes(process, params={
                'host': ip,
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
    nbt.scan(sys.argv[1], sys.argv[2])
