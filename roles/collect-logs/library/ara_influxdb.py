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
module: ara_influxdb
version_added: "1.0"
short_description: Send ARA stats to InfluxDB
description:
    - Python ansible module to send ARA stats to InfluxDB timeseries database
options:
  influxdb_url:
    description:
      - The URL of HTTP API of InfluxDB server:
        for example https://influxdb.example.com
    required: True
  influxdb_port:
    description:
      - The port of HTTP API of InfluxDB server, by default is 8086
    required: True
  influxdb_user:
    description:
      - User for authentication to InfluxDB server
    required: False
  influxdb_password:
    description:
      - Password for authentication to InfluxDB server
    required: False
  influxdb_db:
    description:
      - Database name in InfluxDB server for sending data to it
    required: True
  measurement:
    description:
      - Name of Influx measurement in database
    required: True
  data_file:
    description:
      - Path to file to save InfluxDB data in it
    required: True
  ara_data:
    description:
      - List of ARA results: ara result list --all -f json
    required: True
  only_successful_tasks:
    description:
      - Whether to send only successful tasks, ignoring skipped and failed,
        by default True.
    required: True
  mapped_fields:
    description:
      - Whether to use configured static map of fields and tasks,
        by default True.
    required: False
  standard_fields:
    description:
      - Whether to send standard fields of each job, i.e. times,
        by default True.
    required: False
  longest_tasks:
    description:
      - Whether to to print only longest tasks and how many,
        by default 0.
    required: False
'''

EXAMPLES = '''
- name: Get ARA json data
  shell: "{{ local_working_dir }}/bin/ara result list --all -f json"
  register: ara_data

- name: Collect and send data to InfluxDB
  ara_influxdb:
    influxdb_url: https://influxdb.example.com
    influxdb_port: 8086
    influxdb_user: db_user
    influxdb_password: db_password
    influxdb_db: db_name
    ara_data: "{{ ara_data.stdout }}"
    measurement: test
    data_file: /tmp/test_data
    only_successful_tasks: true
    mapped_fields: false
    standard_fields: false
    longest_tasks: 15
  when: ara_data.stdout != "[]"
'''

import ast  # noqa pylint: disable=C0413
import datetime  # noqa pylint: disable=C0413
import os  # noqa pylint: disable=C0413
import re  # noqa pylint: disable=C0413
import requests  # noqa pylint: disable=C0413

from requests.auth import HTTPBasicAuth  # noqa pylint: disable=C0413


SCHEME = '{measure},{tags} {fields} {timestamp}'

CUSTOM_MAP = {
    'undercloud_install': ["undercloud-deploy : Install the undercloud"],
    'prepare_images': [
        "overcloud-prep-images : Prepare the overcloud images for deploy"],
    'images_update': [
        "modify-image : Convert image",
        "modify-image : Run script on image",
        "modify-image : Close qcow2 image"
    ],
    'images_build': ["build-images : run the image build script (direct)"],
    'containers_prepare': [
        "overcloud-prep-containers : "
        "Prepare for the containerized deployment"],
    'overcloud_deploy': ["overcloud-deploy : Deploy the overcloud"],
    'pingtest': ["validate-simple : Validate the overcloud"],
    'tempest_run': ["validate-tempest : Execute tempest"],
    'undercloud_reinstall': [
        "validate-undercloud : Reinstall the undercloud to check idempotency"],
    'overcloud_delete': [
        "overcloud-delete : check for delete command to complete or fail"],
    'overcloud_upgrade': ["overcloud-upgrade : Upgrade the overcloud",
                          "tripleo-upgrade : run docker upgrade converge step",
                          "tripleo-upgrade : run docker upgrade composable "
                          "step"],
    'undercloud_upgrade': ["tripleo-upgrade : upgrade undercloud"],
}


class InfluxStandardTags(object):

    '''InfluxStandardTags contains:

        calculation of standard job describing parameters as:
         * release
         * nodepool provider cloud
         * zuul pipeline name
         * toci_jobtype
       and rendering them in tags template

    '''

    def branch(self):
        return os.environ.get('STABLE_RELEASE') or 'master'

    def cloud(self):
        return os.environ.get('NODEPOOL_PROVIDER', 'null')

    def pipeline(self):
        if os.environ.get('ZUUL_PIPELINE'):
            if 'check' in os.environ['ZUUL_PIPELINE']:
                return 'check'
            elif 'gate' in os.environ['ZUUL_PIPELINE']:
                return 'gate'
            elif 'periodic' in os.environ['ZUUL_PIPELINE']:
                return 'periodic'
        return 'null'

    def toci_jobtype(self):
        return os.environ.get('TOCI_JOBTYPE', 'null')

    def render(self):
        return ('branch=%s,'
                'cloud=%s,'
                'pipeline=%s,'
                'toci_jobtype=%s') % (
                    self.branch(),
                    self.cloud(),
                    self.pipeline(),
                    self.toci_jobtype(),
        )


class InfluxStandardFields(object):
    '''InfluxStandardFields contains:

        calculation of time of job steps as:
         * whole job duration
         * testing environment preparement
         * quickstart files and environment preparement
         * zuul host preparement
       and rendering them in template

    '''

    def job_duration(self):
        if os.environ.get('START_JOB_TIME'):
            return int(
                datetime.datetime.utcnow().strftime("%s")) - int(
                os.environ.get('START_JOB_TIME'))
        return 0

    def logs_size(self):
        # not implemented
        return 0

    def timestamp(self):
        return datetime.datetime.utcnow().strftime("%s")

    def testenv_prepare(self):
        return os.environ.get('STATS_TESTENV', 0)

    def quickstart_prepare(self):
        return os.environ.get('STATS_OOOQ', 0)

    def zuul_host_prepare(self):
        if (os.environ.get('DEVSTACK_GATE_TIMEOUT') and
                os.environ.get('REMAINING_TIME')):
            return (int(
                os.environ['DEVSTACK_GATE_TIMEOUT']) - int(
                os.environ['REMAINING_TIME'])) * 60
        return 0

    def render(self):
        return ('job_duration=%d,'
                'logs_size=%d,'
                'testenv_prepare=%s,'
                'quickstart_prepare=%s,'
                'zuul_host_prepare=%d,'
                ) % (
                    self.job_duration(),
                    self.logs_size(),
                    self.testenv_prepare(),
                    self.quickstart_prepare(),
                    self.zuul_host_prepare()
        )


class InfluxConfiguredFields(object):
    '''InfluxConfiguredFields contains calculation:

         * whole job duration
         * testing environment preparement
         * quickstart files and environment preparement
         * zuul host preparement
       and rendering them in template
    '''
    def __init__(self, match_map, json_data, only_ok=True):
        """Set up data for configured field

            :param match_map {dict} -- Map of tasks from ansible playbook to
                                        names of data fields in influxDB.
            :param json_data: {dict} -- JSON data generated by ARA
            :param only_ok=True: {bool} -- to count only passed tasks
        """
        self.map = match_map
        self.only_ok = only_ok
        self.data = json_data

    def task_maps(self):
        times_dict = tasks_times_dict(self.data, self.only_ok)
        tasks = {}
        for i in self.map:
            tasks[i] = sum([int(times_dict.get(k, 0)) for k in self.map[i]])
        return tasks

    def render(self):
        tasks = self.task_maps()
        result = ''
        for task, timest in tasks.items():
            result += "%s=%d," % (task, timest)
        return result


class InfluxLongestFields(object):
    '''InfluxLongestFields runs calculation of:

        tasks that took the longest time.
        The tasks could be from undercloud or overcloud playbooks.

    '''

    def __init__(self, json_data, only_ok=True, top=15):
        """Constructor for InfluxLongestFields

            :param json_data: {dict} -- JSON data generated by ARA
            :param only_ok=True: {bool} -- to count only passed tasks
            :param top=15: {int} -- how many tasks to send to DB
        """
        self.top = top
        self.only_ok = only_ok
        self.data = json_data

    def collect_tasks(self):
        tasks_dict = tasks_times_dict(self.data, self.only_ok)
        return sorted(
            [[k, v] for k, v in tasks_dict.items()],
            key=lambda x: x[1],
            reverse=True
        )[:self.top]

    def translate_names(self, names):
        for i in names:
            i[0] = re.sub(
                r'[^0-9A-z\-_]+',
                '',
                i[0].replace(":", "__").replace(" ", "_"))
            i[1] = int(i[1])
        return names

    def render(self):
        result = ''
        for i in self.translate_names(self.collect_tasks()):
            result += "{0}={1},".format(*i)
        return result


def tasks_times_dict(tasks, only_ok=True):
    times_dict = {}
    for task in tasks:
        if not only_ok or task['Status'] in ['changed', 'ok']:
            name = task['Name']
            if name in times_dict:
                times_dict[name].append(task['Duration'])
            else:
                times_dict[name] = [task['Duration']]
    # because of some tasks are executed multiple times we need to count
    # all of them and make summary of all durations
    for i in times_dict:
        times_dict[i] = sum([task_length(t) for t in times_dict[i]])
    return times_dict


def task_length(x):
    '''Calculate task length in seconds from "%H:%M:%S" format

    Arguments:
        x {string} -- a timestamp

    Returns:
        int -- total seconds for the task
    '''

    t = datetime.datetime.strptime(x, "%H:%M:%S")
    return datetime.timedelta(hours=t.hour, minutes=t.minute,
                              seconds=t.second).total_seconds()


def translate(measure, json_data, only_ok,
              mapped_fields=True,
              standard_fields=True,
              longest_tasks=0):
    '''Create data to send to InfluxDB server in format SCHEME

    Fields keys are taken from ARA data according to task names.

    :param measure: name of InfluxDB measurement
    :param json_data: JSON data with tasks and times
    :param: only_ok: boolean, where to count only successful tasks
    :return: full InfluxDB scheme
    '''
    data = ast.literal_eval(json_data)
    tags = InfluxStandardTags()
    std_fields = InfluxStandardFields()
    map_fields = InfluxConfiguredFields(
        match_map=CUSTOM_MAP, json_data=data, only_ok=only_ok)
    longest_fields = InfluxLongestFields(json_data=data,
                                         top=longest_tasks,
                                         only_ok=only_ok)
    fields = ''
    if standard_fields:
        fields += std_fields.render()
    if mapped_fields:
        fields += map_fields.render()
    if longest_tasks:
        fields += longest_fields.render()
    fields = fields.rstrip(",")
    result = SCHEME.format(
        measure=measure,
        tags=tags.render(),
        fields=fields,
        timestamp=std_fields.timestamp()
    )

    return result


def create_file_with_data(data, path):
    '''Create a file with InfluxDB data to send

    :param data: data to write
    :param path: path of the file
    :return:
    '''
    with open(path, "a") as f:
        f.write(data + "\n")


def send(file_path, in_url, in_port, in_user, in_pass, in_db):
    '''Actual sending of data to InfluxDB server via network

    :param file_path: path to file with data to send
    :param in_url: InfluxDB URL
    :param in_port: InfluxDB port
    :param in_user: InfluxDB user
    :param in_pass: InfluxDB password
    :param in_db: InfluxDB database name
    :return: True if sent successfully, otherwise False
    '''
    url = in_url.rstrip("/")
    if in_port != 80:
        url += ":%d" % in_port
    url += "/write"
    params = {"db": in_db, "precision": "s"}
    if in_user:
        if not in_pass:
            if os.environ.get('INFLUXDB_PASSWORD'):
                with open(os.environ['INFLUXDB_PASSWORD']) as f:
                    in_pass = f.read().strip()
            else:
                return False, 'InfluxDB password was not provided!'
        auth = HTTPBasicAuth(in_user, in_pass)
    else:
        auth = None
    with open(file_path, "rb") as payload:
        req = requests.post(url, params=params, data=payload, auth=auth,
                            verify=False)
    if not req or req.status_code != 204:
        return False, "HTTP: %s\nResponse: %s" % (req.status_code, req.content)
    return True, ''


def send_stats(in_url, in_port, in_user, in_pass, in_db, json_data,
               measure, data_file, only_ok, mapped_fields=True,
               standard_fields=True, longest_tasks=0):
    '''Send ARA statistics to InfluxDB server

    :param in_url: InfluxDB URL
    :param in_port: InfluxDB port
    :param in_user: InfluxDB user
    :param in_pass: InfluxDB password
    :param in_db: InfluxDB database name
    :param json_data: JSON data with tasks and times from ARA
    :param measure: InfluxDB measurement name
    :param data_file: path to file with data to send
    :param: only_ok: boolean, where to count only successful tasks
    :param: mapped_fields: if to use configured map of fields and tasks
    :param: standard_fields: if to send standard fields of each job, i.e. times
    :param: longest_tasks: if to print only longest tasks and how many
    :return: JSON ansible result
    '''
    data2send = translate(measure, json_data, only_ok, mapped_fields,
                          standard_fields, longest_tasks)
    create_file_with_data(data2send, data_file)
    if in_url:
        response, reason = send(data_file, in_url, in_port, in_user, in_pass,
                                in_db)
        if not response:
            return {
                'changed': False,
                'failed': True,
                'influxdb_url': in_url,
                'msg': reason
            }
        return {
            'changed': True,
            'influxdb_url': in_url,
            'sent_data': data2send,
        }
    else:
        return {
            'changed': True,
            'data_file': data_file,
            'sent_data': data2send,
        }


def main():
    module = AnsibleModule(  # noqa
        argument_spec=dict(
            influxdb_url=dict(required=True, type='str'),
            influxdb_port=dict(required=True, type='int'),
            influxdb_user=dict(required=False, type='str', default=None),
            influxdb_password=dict(required=False, type='str', default=None),
            influxdb_db=dict(required=True, type='str'),
            ara_data=dict(required=True, type='str'),
            measurement=dict(required=True, type='str'),
            data_file=dict(required=True, type='str'),
            only_successful_tasks=dict(required=True, type='bool'),
            mapped_fields=dict(default=True, type='bool'),
            standard_fields=dict(default=True, type='bool'),
            longest_tasks=dict(default=0, type='int'),
        )
    )
    result = send_stats(module.params['influxdb_url'],
                        module.params['influxdb_port'],
                        module.params['influxdb_user'],
                        module.params['influxdb_password'],
                        module.params['influxdb_db'],
                        module.params['ara_data'],
                        module.params['measurement'],
                        module.params['data_file'],
                        module.params['only_successful_tasks'],
                        module.params['mapped_fields'],
                        module.params['standard_fields'],
                        module.params['longest_tasks'],
                        )
    module.exit_json(**result)


# pylint: disable=W0621,W0622,W0614,W0401,C0413
from ansible.module_utils.basic import *  # noqa

if __name__ == "__main__":
    main()
