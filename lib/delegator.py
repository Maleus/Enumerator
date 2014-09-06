#!/usr/bin/env python

def receive_service_data(sender=None, **kw):
    print sender
    print kw


if __name__ == '__main__':
    # TODO: Possibly set up delegator module to accept a json file of
    # results if called directly.
    pass
