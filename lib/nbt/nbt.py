#!/usr/bin/env python

import os, sys
from ..generic_service import GenericService

class NbtEnumeration(GenericService):
    LIB_PATH = os.path.dirname(os.path.realpath(__file__))
    PROCESSES = ['enum4linux -a %(host)s > %(output_dir)s/%(host)s-nbt-enum4linux.txt',]

    def scan(self, ip, directory):
        for process in self.PROCESSES:
            self.start_processes(process, params={
                'host': ip,
                'output_dir': directory,
            }, display_exception=False)

if __name__ == '__main__':
    nbt = NbtEnumeration()
    nbt.scan(sys.argv[1], sys.argv[2])
