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

def is_http(service, port, state):
    """ Ruleset for classifying an http service."""
    return (
        'http' in service and 'proxy' not in service \
        or port in ['8081']
    ) and state == 'open'

def is_ftp(service, port, state):
    """ Ruleset for classifying an ftp service."""
    return 'ftp' in service and state == 'open'

def is_nbt(service, port, state):
    """ Ruleset for classifying a netbios service."""
    return port == '445' and state == 'open'

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
        service, port, state = tcp_service.get('service'), tcp_service.get('port'), tcp_service.get('state')

        if is_http(service, port, state):
            http = HttpEnumeration()
            http.scan(ip, port, working_directory)

        if is_ftp(service, port, state):
            ftp = FtpEnumeration()
            ftp.scan(ip, port, working_directory)

        if is_nbt(service, port, state):
            nbt = NbtEnumeration()
            nbt.scan(ip, working_directory)

    # TODO: When UDP service enumeration tools are available, do as I'm doing above.


if __name__ == '__main__':
    # TODO: Possibly set up delegator module to accept a json file of
    # results if called directly.
    pass
