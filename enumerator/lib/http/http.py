#!/usr/bin/env python
""" 
The HTTP module performs http-related 
enumeration tasks.

@author: Steve Coward (steve<at>sugarstack.io)
@version: 1.0
"""
import os, sys
from ..generic_service import GenericService

class HttpEnumeration(GenericService):
    LIB_PATH = os.path.dirname(os.path.realpath(__file__))
    PROCESSES = [
        'nikto -F txt -o %(output_dir)s/%(host)s-http-%(port)s-nikto.txt -h %(host)s -p %(port)s',
        'dirb %(url)s %(wordlist)s -o %(output_dir)s/%(host)s-http-%(port)s-dirb.txt -r -S -w',
    ]

    # TODO: Make these configurable either at runtime or via config file.
    # On the Kali distro, both of these files/paths exist.
    DIRB_WORDLISTS = '/usr/share/dirb/wordlists/common.txt,/opt/metasploit/apps/pro/msf3/data/wmap/wmap_dirs.txt'

    def scan(self, ip, port, directory):
        """Iterates over PROCESSES and builds
        the specific parameters required for 
        command line execution of each process.

        @param ip: IP address being processed.
        
        @param port: Port which the HTTP process 
        is running on.

        @param directory: Directory path where 
        final command output will go.
        """
        for process in self.PROCESSES:
            self.start_processes(process, params={
                'host': ip,
                'port': port,
                'url': 'https://%s/' % ip if port == '443' else 'http://%s:%s/' % (ip, port),
                'output_dir': directory,
                'wordlist': self.DIRB_WORDLISTS,
            }, display_exception=False)

if __name__ == '__main__':
    """For testing purposes, this 
    module can be executed as a script.
    Use the following syntax from the root
    directory of enumerator:

    python -m lib.http.http <ip> <port> <output directory>
    """
    http = HttpEnumeration()
    http.scan(sys.argv[1], sys.argv[2], sys.argv[3])
