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
'''
import ast
import datetime
import os
import requests

from requests.auth import HTTPBasicAuth


SCHEME = (
    # measurement
    '{measure},'
    # tags
    'branch={branch},'
    'cloud={cloud},'
    'pipeline={pipeline},'
    'toci_jobtype={toci_jobtype} '
    # fields
    'job_duration={job_duration},'
    'logs_size={logs_size},'
    'testenv_prepare={testenv_prepare},'
    'zuul_host_prepare={zuul_host_prepare},'
    'quickstart_prepare={quickstart_prepare},'
    'undercloud_install={undercloud_install},'
    'prepare_images={prepare_images},'
    'images_update={images_update},'
    'images_build={images_build},'
    'containers_prepare={containers_prepare},'
    'overcloud_deploy={overcloud_deploy},'
    'pingtest={pingtest},'
    'tempest_run={tempest_run},'
    'undercloud_reinstall={undercloud_reinstall},'
    'overcloud_delete={overcloud_delete},'
    'undercloud_upgrade={undercloud_upgrade},'
    'overcloud_upgrade={overcloud_upgrade} '
    '{timestamp}'
)

DATA = {
    'measure': '',
    # tags
    'branch': os.environ.get('STABLE_RELEASE') or 'master',
    'cloud': os.environ.get('NODEPOOL_PROVIDER', 'N/A'),
    'pipeline': 'N/A',  # implemented in function
    'toci_jobtype': os.environ.get('TOCI_JOBTYPE', 'N/A'),
    # fields
    'job_duration': 0,  # implemented in function
    'logs_size': 0,  # not implemented
    'testenv_prepare': os.environ.get('STATS_TESTENV', 0),
    'zuul_host_prepare': 0,  # implemented in function
    'quickstart_prepare': os.environ.get('STATS_OOOQ', 0),
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
    'overcloud_upgrade': ["overcloud-upgrade : Upgrade the overcloud"],
    'undercloud_upgrade': ["overcloud-upgrade : Upgrade the undercloud"],
    'timestamp': int(datetime.datetime.utcnow().strftime("%s")),
}


def task_length(x):
    '''Calculate task length in seconds from "%H:%M:%S" format

    :param x: datetime string
    :return: number of seconds spent for task
    '''
    t = datetime.datetime.strptime(x, "%H:%M:%S")
    return datetime.timedelta(hours=t.hour, minutes=t.minute,
                              seconds=t.second).total_seconds()


def translate(measure, json_data, only_ok):
    '''Create data to send to InfluxDB server in format SCHEME

    Fields keys are taken from ARA data according to task names.

    :param measure: name of InfluxDB measurement
    :param json_data: JSON data with tasks and times
    :param: only_ok: boolean, where to count only successful tasks
    :return: full InfluxDB scheme
    '''

    DATA['measure'] = measure
    if os.environ.get('START_JOB_TIME'):
        DATA['job_duration'] = int(
            datetime.datetime.utcnow().strftime("%s")) - int(
            os.environ.get('START_JOB_TIME'))
    if os.environ.get('ZUUL_PIPELINE'):
        if 'check' in os.environ['ZUUL_PIPELINE']:
            DATA['pipeline'] = 'check'
        elif 'gate' in os.environ['ZUUL_PIPELINE']:
            DATA['pipeline'] = 'gate'
        elif 'periodic' in os.environ['ZUUL_PIPELINE']:
            DATA['pipeline'] = 'periodic'
    if (os.environ.get('DEVSTACK_GATE_TIMEOUT') and
            os.environ.get('REMAINING_TIME')):
        DATA['zuul_host_prepare'] = (int(
            os.environ['DEVSTACK_GATE_TIMEOUT']) - int(
            os.environ['REMAINING_TIME'])) * 60

    data = ast.literal_eval(json_data)
    # create a dictionary with durations for each task
    # every task could run multiple times
    times_dict = {}
    for task in data:
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
    # replace tasks lists in DATA with tasks durations
    for i in DATA:
        if isinstance(DATA[i], list):
            DATA[i] = sum([int(times_dict.get(k, 0)) for k in DATA[i]])
    return SCHEME.format(**DATA)


def create_file_with_data(data, path):
    '''Create a file with InfluxDB data to send

    :param data: data to write
    :param path: path of the file
    :return:
    '''
    with open(path, "w") as f:
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
               measure, data_file, only_ok):
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
    :return: JSON ansible result
    '''
    data2send = translate(measure, json_data, only_ok)
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
                        )
    module.exit_json(**result)


from ansible.module_utils.basic import *  # noqa

if __name__ == "__main__":
    main()
