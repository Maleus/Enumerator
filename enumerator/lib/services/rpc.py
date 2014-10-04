#!/usr/bin/env python
""" 
The Rpc Bind module performs rpcbind-related 
enumeration tasks.

@author: Erik Dominguez(maleus<at>overflowsecurity.com)
@author: Steve Coward (steve<at>sugarstack.io)
@version: 1.0
"""
import sys
from ..process_manager import ProcessManager
from ..generic_service import GenericService


class RpcEnumeration(GenericService, ProcessManager):
    SERVICE_DEFINITION = 'port:111'
    PROCESSES = [
        'showmount -e %(host)s > %(output_dir)s/%(host)s-rpc-showmount.txt', ]

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

    python -m lib.rpc.rpc <ip> <output directory>
    """
    rpc = RpcEnumeration()
    rpc.scan(sys.argv[2], dict(ip=sys.argv[1]))
