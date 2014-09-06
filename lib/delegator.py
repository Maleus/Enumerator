#!/usr/bin/env python

from http import http
from ftp import ftp

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
        if 'http' in tcp_service.get('service') and tcp_service.get('state') == 'open':
            http.scan(ip, tcp_service.get('port'), directory)

    # TODO: When UDP service enumeration tools are available, do as I'm doing above.


if __name__ == '__main__':
    # TODO: Possibly set up delegator module to accept a json file of
    # results if called directly.
    pass
