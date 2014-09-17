#!/usr/bin/env python
"""ProcessManager encapsulates any process-
related methods required by enumerator.

@author: Steve Coward (steve<at>sugarstack.io)
@version 1.0
"""
import subprocess


class ProcessManager(object):

    def start_processes(self, process, **flags):
        """Initiates command line processes.

        @param process: String value of the command 
        to be run.

        @param flags: Extra values which serve to 
        replace named parameters in the command line process
        as well as a flag to toggle the display of 
        any exceptions during execution (used for debugging). 
        """
        params = flags.get('params')
        display_exception = flags.get('display_exception')

        try:
            subprocess.check_output(process % params, shell=True)
	    print process % params
        except Exception as exception:
            if display_exception:
                print '   [!] Error running process %s' % process.split(' ')[0]
                print '   [!] Exception: %s' % exception
            else:
                pass
