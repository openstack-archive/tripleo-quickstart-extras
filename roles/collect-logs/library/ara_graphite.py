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
module: ara_graphite
version_added: "1.0"
short_description: Send ARA stats to graphite
description:
    - Python ansible module to send ARA stats to graphite
options:
  graphite_host:
    description:
      - The hostname of the Graphite server with optional port:
        graphite.example.com:2004. The default port is 2003
    required: True
  ara_mapping:
    description:
      - Mapping task names to Graphite paths
    required: True
  ara_data:
    description:
      - List of ARA results: ara result list --all -f json
    required: True
  ara_only_successful:
    description:
      - Whether to send only successful tasks, ignoring skipped and failed,
        by default True.
    required: True
'''

EXAMPLES = '''
- name: Get ARA json data
  shell: "{{ local_working_dir }}/bin/ara task list --all -f json"
  register: ara_data

- ara_graphite:
    graphite_host: 10.2.2.2
    ara_data: "{{ ara_task_output.stdout }}"
    ara_mapping:
        - "Name of task that deploys overcloud": overcloud.deploy.seconds
'''
import ast
import datetime
import socket


def stamp(x):
    '''Convert ISO timestamp to Unix timestamp

    :param x: string with timestamp
    :return: string with Unix timestamp
    '''
    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime('%s')


def task_length(x):
    '''Calculate task length in seconds from "%H:%M:%S" format

    :param x: datetime string
    :return: number of seconds spent for task
    '''
    t = datetime.datetime.strptime(x, "%H:%M:%S")
    return datetime.timedelta(hours=t.hour, minutes=t.minute,
                              seconds=t.second).total_seconds()


def translate(mapping, json_data, only_ok):
    '''Create data to send to Graphite server in format:

        GraphitePath Timestamp TaskDuration
    GraphitePath is taken from mapping dictionary according to task name.

    :param mapping: dictionary of mapping task names to graphite paths
    :param json_data: JSON data with tasks and times
    :return: list of graphite data
    '''
    items = []
    data = ast.literal_eval(json_data)
    for task in data:
        if not only_ok or (only_ok and task['Status'] in ['changed', 'ok']):
            if task['Name'] in mapping:
                timestamp, duration = stamp(task['Time Start']), task_length(
                    task['Duration'])
                items.append([mapping[task['Name']], timestamp, duration])
    return items


def send(data, gr_host, gr_port, prefix):
    '''Actual sending of data to Graphite server via network

    :param data: list of items to send to Graphite
    :param gr_host: Graphite host (with optional port)
    :param prefix: prefix to append before Graphite path
    :return: True if sent successfully, otherwise False
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect((gr_host, gr_port))
    except Exception as e:
        return False, str(e)
    for content in data:
        s.send(prefix + " ".join([str(i) for i in content]) + "\n")
    s.close()
    return True, ''


def send_stats(gr_host, gr_port, mapping, json_data, prefix, only_ok):
    '''Send ARA statistics to Graphite server

    :param gr_host: Graphite host (with optional port)
    :param mapping: dictionary of mapping task names to graphite paths
    :param json_data: JSON data with tasks and times
    :param prefix: prefix to append before Graphite path
    :return: JSON ansible result
    '''
    data2send = translate(mapping, json_data, only_ok)
    response, reason = send(data2send, gr_host, gr_port, prefix)
    if not response:
        return {
            'changed': False,
            'failed': True,
            'graphite_host': gr_host,
            'msg': "Can't connect to Graphite: %s" % reason
        }
    return {
        'changed': True,
        'graphite_host': gr_host,
        'sent_data': data2send,
    }


def main():
    module = AnsibleModule(  # noqa
        argument_spec=dict(
            graphite_host=dict(required=True, type='str'),
            graphite_port=dict(required=False, type='int', default=2003),
            ara_mapping=dict(required=True, type='dict'),
            ara_data=dict(required=True, type='str'),
            graphite_prefix=dict(required=False, type='str', default=''),
            only_successful_tasks=dict(required=False, type='bool',
                                       default=True)
        )
    )
    result = send_stats(module.params['graphite_host'],
                        module.params['graphite_port'],
                        module.params['ara_mapping'],
                        module.params['ara_data'],
                        module.params['graphite_prefix'],
                        module.params['only_successful_tasks'])
    module.exit_json(**result)


from ansible.module_utils.basic import *  # noqa

if __name__ == "__main__":
    main()
