#!/usr/bin/env python
"""The delegator module
receives nmap scan result data
and, based on a set of rules, will
delegate more service-specific 
enumeration.

@author: Steve Coward (steve<at>sugarstack.io)
@version: 1.0
"""
from .http.http import HttpEnumeration
from .ftp.ftp import FtpEnumeration
from .nbt.nbt import NbtEnumeration

http = HttpEnumeration()
ftp = FtpEnumeration()
nbt = NbtEnumeration()
service_modules = [http, ftp, nbt]


def receive_service_data(sender=None, **flags):
    """Receive data either directly (not implemented) or via signal. Delegate 
    service enumeration depending on reported services.

    @param sender: Name value of where the signal was sent from (default: None)
    @param flags: IP scan results are passed as a dict.
    """

    results = flags.get('scan_results')
    working_directory = flags.get('directory')
    ip = results.keys()[0]

    tcp_services = results[ip]['tcp']
    udp_services = results[ip]['udp']

    for tcp_service in tcp_services:
        service, port = tcp_service.get('service'), tcp_service.get('port')
        for module in service_modules:
            if module.is_valid_service(tcp_service):
                module.scan(working_directory, dict(ip=ip, port=port))

if __name__ == '__main__':
    # TODO: Possibly set up delegator module to accept a json file of
    # results if called directly.
    pass
