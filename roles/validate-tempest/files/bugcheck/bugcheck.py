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
#
# flake8: noqa

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import argparse
import bugzilla
import logging
import sys
import xmlrpclib
import yaml

from launchpadlib.launchpad import Launchpad

LOG = logging.getLogger(__name__)
OPEN = 1
CLOSED = 2
INVALID = 3


class LaunchpadConnector(object):
    def __init__(self, cachedir='/tmp/.launchpadlib/cache/'):
        self.cachedir = cachedir
        self.lp = Launchpad.login_anonymously('Bugs', 'production', cachedir,
                                              version='devel')

    def get_bug_status(self, bug_id):
        try:
            bug = self.lp.bugs[bug_id]
            # We are assuming that last task have the final status
            # And we cannot slice from the last
            task = bug.bug_tasks[len(bug.bug_tasks) - 1]
            if task:
                if task.status in ['Fix Released', 'Fix Committed', 'Invalid']:
                    return CLOSED
                else:
                    return OPEN
        except KeyError:
            LOG.error('Bug {} does not exist in launchpad'.format(bug_id))
            return INVALID


class BugzillaConnector(object):
    def __init__(self, url='https://bugzilla.redhat.com/xmlrpc.cgi'):
        self.bugzilla = bugzilla.Bugzilla(url=url)

    def get_bug_status(self, bug_id):
        try:
            bug = self.bugzilla.getbug(bug_id)
            if bug.status == 'CLOSED':
                return CLOSED
            else:
                return OPEN
        except xmlrpclib.Fault as err:
            # Fault code 102 means it's a private bug and we don't have
            # permission to see, so we can't confirm if it's closed
            if err.faultCode == 102:
                return OPEN
            LOG.error('Bug {} failed with fault code {}'.format(bug_id,
                                                                err.faultCode))
            return INVALID


class VerifyBug(object):
    def __init__(self):
        self.bugzilla = BugzillaConnector()
        self.launchpad = LaunchpadConnector()

    def check_bug_status(self, url):
        connector = self._get_connector(url)
        bug_id = self._get_id_from_url(url)
        return connector.get_bug_status(bug_id)

    def is_bug_open(self, url):
        status = self.check_bug_status(url)
        if status in [CLOSED, INVALID]:
            return False
        else:
            return True

    def _get_id_from_url(self, url):
        if 'launchpad' in url:
            # The format is https://bugs.launchpad.net/tripleo/+bug/1577769
            return int(url.split('/')[-1])
        elif 'bugzilla' in url:
            return int(url.split('=')[-1])

    def _get_connector(self, url):
        if 'launchpad' in url:
            return self.launchpad
        elif 'bugzilla' in url:
            return self.bugzilla
        else:
            raise ValueError('Cannot find a connector for {}'.format(url))


class BugVerifyCmd(object):
    def __init__(self):
        self.skipped_failures = []

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(description='Bug verify')
        parser.add_argument('--skip-file', dest='skip_file',
                            help='Load skip file', required=True)
        parser.add_argument('--output', action='store_true',
                            help='Print the output')
        parser.add_argument('--format', dest='output_format',
                            default='yaml', help='Output format',
                            choices=['yaml', 'txt'])
        parser.add_argument('--to-file', dest='to_file',
                            help='Save the skip list to a file')
        parser.add_argument('--report', dest='report', action='store_true',
                            help='Shows report at the end')
        parser.add_argument('--debug', dest='debug', action='store_true',
                            help='Enable debug')
        self.args = parser.parse_args(args)

    def setup_logging(self):
        level = logging.DEBUG if self.args.debug else logging.INFO
        logging.basicConfig(level=level,
                            format='%(asctime)s %(levelname)s %(name)s: '
                                   '%(message)s')

    def load_skip_file(self):
        known_failures = []
        try:
            with open(self.args.skip_file) as f:
                skip = yaml.safe_load(f)
            for t in skip.get('known_failures'):
                bug = {'test': t.get('test'), 'reason': t.get('reason')}
                if t.get('lp'):
                    bug['lp'] = t.get('lp')
                if t.get('bz'):
                    bug['bz'] = t.get('bz')
                known_failures.append(bug)
        except yaml.constructor.ConstructorError:
            LOG.error('Invalid yaml file {}'.format(self.args.skip_file))
        except IOError:
            LOG.error('File not found {}'.format(self.args.skip_file))
        finally:
            return known_failures

    def _print_yaml(self, known_failures):
        return yaml.dump({'known_failures': known_failures},
                         default_flow_style=False,
                         explicit_start=True)

    def _print_txt(self, known_failures):
        output = ''
        for bug in known_failures:
            output += '# {}\n'.format(bug.get('reason'))
            output += '{}\n'.format(bug.get('test'))
        return output

    def get_output(self, known_failures, output_format):
        output = ''
        if output_format == 'txt':
            output = self._print_txt(known_failures)
        elif output_format == 'yaml':
            output = self._print_yaml(known_failures)
        else:
            raise ValueError(
                'Output format not supported: {}'.format(output_format))
        return output

    def print_output(self, known_failures, output_format):
        print(self.get_output(known_failures, output_format))

    def show_report(self):
        print('Here\'s the original list:')
        self.print_output(self.original_failures, self.args.output_format)
        print('\n\n')
        print('Here\'s the skipped list:')
        self.print_output(self.skipped_failures, self.args.output_format)

    def save_output(self, known_failures, output_format):
        output = self.get_output(known_failures, output_format)
        f = open(self.args.to_file, 'w')
        f.write(output)
        f.close()

    def run(self):
        known_failures = self.load_skip_file()
        self.original_failures = known_failures
        open_failures = []

        v_bug = VerifyBug()
        for bug in known_failures:
            LOG.debug('Checking bug: {}'.format(bug))
            if not bug.get('lp') and not bug.get('bz'):
                open_failures.append(bug)
                continue
            bug_url = bug.get('lp') or bug.get('bz')
            if not v_bug.is_bug_open(bug_url):
                self.skipped_failures.append(bug)
            else:
                open_failures.append(bug)
        if self.args.output:
            self.print_output(open_failures, self.args.output_format)
        if self.args.to_file:
            self.save_output(open_failures, self.args.output_format)
        if self.args.report:
            self.show_report()


def main():
    bvc = BugVerifyCmd()
    bvc.parse_arguments(sys.argv[1:])
    bvc.setup_logging()
    bvc.run()


if __name__ == '__main__':
    sys.exit(main())
