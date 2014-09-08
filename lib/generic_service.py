#!/usr/bin/env python

import subprocess

class GenericService(object):
    def start_processes(self, process, **kwargs):
        params = kwargs.get('params')
        display_exception = kwargs.get('display_exception')

        try:
            subprocess.check_output(process % params, shell=True)
        except Exception as exception:
            if display_exception:
                print '   [!] Error running process %s' % process.split(' ')[0]
                print '   [!] Exception: %s' % exception
            else:
                pass
