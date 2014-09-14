#!/usr/bin/env python
"""GenericService encapsulates any 
methods which are common across all
service modules.

@author: Steve Coward (steve<at>sugarstack.io)
@version 1.0
"""
import re


class GenericService(object):
    compiled_service_definition = None

    def __init__(self):
        self.compiled_service_definition = self.compile_service_definition(
            self.SERVICE_DEFINITION)

    def compile_service_definition(self, definition):
        """Take a string of key:values and parse
        the values into a python interpretable
        conditional statement.

        @param definition: String used to classify
        a service.
        """
        rule_parser_pattern = re.compile('([^\s]+\s)?(\w+):([^\s]+)')
        rule = []
        for rule_set in rule_parser_pattern.findall(definition):
            conditional, key, values = map(str.strip, rule_set)

            # Determine if values need to be split apart.
            # Rule: If there are no '-' values at the beginning of each value, we can use a list.
            # Rule: If there are '-' values at the beginning of each value,
            # split apart.
            if len([val for val in values.split(',') if val[0] == '-']):
                values_set = values.split(',')
                for value in values_set:
                    if value[0] == '-':
                        rule.append('"%s" not in %s' % (value[1:], key))
                    else:
                        rule.append('"%s" in %s' % (value, key))
            else:
                values_set = values.split(',')
                rule.append('%s %s in %s' % (conditional, key, values_set))

        return ' and '.join(rule).replace('and or', 'or')

    def is_valid_service(self, attributes):
        """Returns True or False if the attributes
        of a service record match the definition of
        a service.

        @param attributes: Dict value of a scanned service
        (service,port,state).
        """
        service = attributes.get('service')
        port = attributes.get('port')
        state = attributes.get('state')

        if state != 'open':
            return False

        # The keys in rule will map to service, port and status set above.
        return eval(self.compiled_service_definition)
