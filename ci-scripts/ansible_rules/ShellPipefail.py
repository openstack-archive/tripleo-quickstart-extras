#   Copyright Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from ansiblelint import AnsibleLintRule


def incorrect_task(task, cmd):
    if 'shell' not in task:
        return False
    if 'register' in task:
        return False
    if task.get('ignore_errors'):
        return False

    if isinstance(task['shell'], dict):
        args = task['shell']['cmd'].split()
    else:
        args = task['shell'].split()
    if not set(args).isdisjoint(cmd) and 'pipefail' not in args:
        return True

    return False


class ShellPipefail(AnsibleLintRule):
    id = 'OOOQ0001'
    shortdesc = 'Shell should have a pipefail'
    description = 'Shell commands should have "set -o pipefail" if using PIPE'
    tags = ['shell']
    cmd = ["|", "timestamper_cmd"]

    def matchplay(self, file, play):
        ret = []
        if play.get('block') and not play.get('ignore_errors'):
            block = play['block']
            for task in block:
                if incorrect_task(task, self.cmd):
                    ret.append((file, self.shortdesc))
        else:
            if incorrect_task(play, self.cmd):
                ret.append((file, self.shortdesc))
        return ret
