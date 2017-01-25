#!/usr/bin/env python

DOCUMENTATION = '''
---
module: zuul_deps
version_added: "2.0"
short_description: Transforms the dependent changes variable from Zuul format into a dictionary
description:
    - Transforms the dependent changes variable from Zuul format into a dictionary
options:
  host:
    description:
      - The content of the ZUUL_HOST variable
    required: True
  changes:
    description:
      - The content of the ZUUL_CHANGES variable
    required: True
'''

EXAMPLES = '''
- zuul_deps:
    host: review.openstack.org
    changes: "openstack/tripleo-heat-templates:master:refs/changes/88/296488/1^openstack/instack-undercloud:master:refs/changes/84/315184/5"
'''

import sys

def process(host, changes):
    """Process the changes from Zuul format"""
    output = []

    for item in changes.split("^"):
        params = item.split(":")
        if params[0] in [i['project'] for i in output]:
            continue
        output.append({"host": host,
                       "project": params[0],
                       "branch": params[1],
                       "refspec": params[2]})
    return {'changed': True,
            'ansible_facts': {'zuul_change_list': output}}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            changes=dict(required=True, type='str')
        )
    )
    result = process(module.params['host'],
                     module.params['changes'])
    module.exit_json(**result)


# see http://docs.ansible.com/developing_modules.html#common-module-boilerplate
from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
