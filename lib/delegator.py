#!/usr/bin/env python

from http import http
from ftp import ftp
from nbt import nbt

def receive_service_data(sender=None, **kw):
    """Receive data either directly (not implemented) or via signal. Delegate 
    service enumeration depending on reported services.

    Keyword arguments:
    sender -- Name value of where the signal was sent from (default: None)
    kw -- Keyword argument. IP scan results are passed as a dict.
    """

    results = kw.get('scan_results')
    working_directory = kw.get('directory')
    ip = results.keys()[0]

    tcp_services = results[ip]['tcp']
    udp_services = results[ip]['udp']

    for tcp_service in tcp_services:
        service, port, state = tcp_service.get('service'), tcp_service.get('port'), tcp_service.get('state')

        # ruleset for initiating http enumeration.
        if (
            'http' in service and 'proxy' not in service \
            or port in ['8081']
        ) and state == 'open':
            http.scan(ip, port, working_directory)

        if 'ftp' in service and state == 'open':
            ftp.scan(ip, port, working_directory)

        if port == '445' and state == 'open':
            nbt.scan(ip, working_directory)

    # TODO: When UDP service enumeration tools are available, do as I'm doing above.


if __name__ == '__main__':
    # TODO: Possibly set up delegator module to accept a json file of
    # results if called directly.
    pass
