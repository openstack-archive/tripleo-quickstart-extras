#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---
module: jenkins_deps
version_added: "2.0"
short_description: Parses the Gerrit commit message and identifies cross repo dependency changes
description:
    - Parses the Gerrit commit message and identifies cross repo dependency changes.
      The expected format in the commit message is:
      Depends-On: <change-id>[@<gerrit-instance-shorthand>]
      Where <change-id> is the gerrit Change-Id of the dependent change,
      <gerrit-instance> should be a part of a hostname in ALLOWED_HOSTS.
options:
  host:
    description:
      - The hostname of the Gerrit server.
    required: True
  change_id:
    description:
      - The change-id of the Gerrit change, starting with I...
    required: True
  branch:
    description:
      - The branch of the change.
    required: True
  patchset_rev:
    description:
      - The sha hash of the patchset to be tested. Latest will be used if omitted.
    required: False
'''

EXAMPLES = '''
- jenkins-deps:
    host: review.opendev.org
    change_id: I387b6bfd763d2d86cad68a3119b0edd0caa237b0
    patchset_rev: d18f21853e2f3be7382a20d0f42232ff3a78b348
'''

import json
import logging
import re
import requests

# we ignore any other host reference
ALLOWED_HOSTS = ['review.opendev.org',
                 'review.gerrithub.io',
                 'review.rdoproject.org']


def parse_commit_msg(current_host, msg):
    '''Look for dependency links in the commit message.'''
    tags = []
    for line in iter(msg.splitlines()):
        # note: this regexp takes care of sanitizing the input
        tag = re.search(r'Depends-On: *(I[0-9a-f]+)@?([0-9a-z\.\-:]*)',
                        line, re.IGNORECASE)
        if tag:
            change_id = tag.group(1)
            target = tag.group(2)
            if target == '':
                host = current_host
            else:
                # match a shorthand hostname for our allowed list
                for hostname in ALLOWED_HOSTS:
                    if target in hostname:
                        host = hostname
                        break
                else:
                    logging.warning('Cannot resolve "%s" to a host from the '
                                    'ALLOWED HOSTS list', target)
                    continue
            tags.append({'host': host,
                         'change_id': change_id,
                         'branch': None,
                         'revision': None})
    return tags


def get_details(host, change_id, branch, revision):
    '''Get the details of a specific change'''
    url = ''.join(['https://', host, '/changes/?q=change:', change_id])
    try:
        req = requests.get(url)
        req.raise_for_status()
    except requests.exceptions.HTTPError:
        return {'fail_msg': ''.join(['warning: failed to query change '
                                     'details from ', url])}
    # strip XSSI attack prevention prefix
    data = json.loads(req.text[4:])
    if len(data) == 0:
        return {'fail_msg': ''.join(['warning: no change found with id ',
                                     change_id, ' at ', url])}
    elif len(data) == 1:
        # not filtering by branch if not necessary
        full_id = data[0]['id']
    else:
        # there are more than one change with the same ID
        try:
            full_id = [change['id'] for change
                       in data if change['branch'] == branch][0]
        except IndexError:
            return {'fail_msg': ''.join(['warning: no change found with id ',
                                         change_id, ' for branch ', branch,
                                         ' at ', url])}
    url = ''.join(['https://', host, '/changes/', full_id,
                   '?o=ALL_REVISIONS&o=ALL_COMMITS'])
    try:
        req = requests.get(url)
        req.raise_for_status()
    except requests.exceptions.HTTPError:
        return {'fail_msg': ''.join(['warning: failed to fetch details of ',
                                     change_id, ' from ', url])}
    # strip XSSI attack prevention prefix
    data = json.loads(req.text[4:])
    if revision is None:
        revision = data['current_revision']
    if revision not in data['revisions']:
        return {'fail_msg': ''.join(['warning: cannot find revision ',
                                     revision, ' of change ', change_id,
                                     ' at ', url])}
    return {'host': host,
            'change_id': str(data['change_id']),
            'project': str(data['project']),
            'branch': str(data['branch']),
            'refspec': str(data['revisions'][revision]['ref']),
            'commit_msg':
                str(data['revisions'][revision]['commit']['message'])}


def resolve_dep(host, change_id, branch, revision):
    '''Dependency resolution.

    Resolve the dependencies in the target commits until there are no more
    dependent changes. If the branch or revision is None, it can still resolve
    the dependencies. It only uses the branch when the change_id is ambiguous
    and by default uses the latest patchset's revision.

    The function avoids circular dependencies and only allows one change per
    project to be added to the output list.

    Returns a list of dictionaries with the dependent changes.
    '''

    resolved_ids = []
    deps = []
    to_resolve = [{'host': host,
                   'change_id': change_id,
                   'branch': branch,
                   'revision': revision}]
    output_msg = []
    while len(to_resolve) > 0:
        change = to_resolve.pop()
        # use the original branch as default
        if change['branch'] is None:
            change['branch'] = branch

        # avoid circular dependencies
        if change['change_id'] in resolved_ids:
            continue

        details = get_details(**change)
        if 'fail_msg' in details:
            output_msg.append(details['fail_msg'])
            continue
        resolved_ids.append(details['change_id'])

        # allow only one of each project as a dependency
        if details['project'] not in (d['project'] for d in deps):
            deps.append({'host': change['host'],
                         'project': details['project'],
                         'branch': details['branch'],
                         'refspec': details['refspec']})
        else:
            output_msg.append(
                ''.join(['warning: skipping ', change['change_id'], ' on ',
                         change['host'], ' because project "',
                         details['project'], '" is already a dependency']))
            continue
        new_deps = parse_commit_msg(change['host'], details['commit_msg'])
        to_resolve.extend(new_deps)
    if len(deps) == 0:
        output_msg.append('error: failed to resolve the target change')
        return {'failed': True,
                'msg': ', '.join(output_msg)}
    else:
        return {'changed': True,
                'ansible_facts': {'artg_change_list': deps},
                'msg': ', '.join(output_msg)}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True, type='str'),
            change_id=dict(required=True, type='str'),
            branch=dict(required=False, default=None, type='str'),
            patchset_rev=dict(required=False, default=None, type='str')
        )
    )
    result = resolve_dep(module.params['host'],
                         module.params['change_id'],
                         module.params['branch'],
                         module.params['patchset_rev'])
    module.exit_json(**result)


# see http://docs.ansible.com/developing_modules.html#common-module-boilerplate
from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
