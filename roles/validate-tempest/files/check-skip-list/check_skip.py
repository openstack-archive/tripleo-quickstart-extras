#! /usr/bin/env python

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

import argparse
import json
import logging
import re
import requests
import sys
import yaml


TESTRE = re.compile(r'(tempest[^ \(\)]+|\w+\.tests\.[^ \(\)]+)')
OK = "... ok"


class CheckSkipCmd(object):
    def __init__(self):
        self.parse_arguments(sys.argv[1:])
        if self.args.debug:
            self.setup_logging()

    def run(self):
        console = self.download_console_log()
        ok_results = self.get_test_results(console)
        skip_file = self.load_skip_file()

        regex_removed = self.compare_results(skip_file, ok_results)
        print(json.dumps(regex_removed, indent=4, sort_keys=True))

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(description='Check skip list content')
        parser.add_argument('--log-url', dest='console_log', required=True,
                            help='Url for the console log result')
        parser.add_argument('--skip-file', dest='skip_file',
                            required=True, help='Skip file to compare')
        parser.add_argument('--undercloud', dest='undercloud',
                            action='store_true',
                            help='Load undercloud skip list',
                            default=False)
        parser.add_argument('--debug', dest='debug', action='store_true',
                            help='Enable debug')

        self.args = parser.parse_args(args)

    def setup_logging(self):
        self.log = logging.getLogger(self.__class__)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s: '
                                   '%(message)s')

    def download_console_log(self):
        resp = requests.get(self.args.console_log)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.log.error('An error ocurred when trying to download '
                           'console log: {}'.format(e))
            return None
        return resp.content.decode('utf-8')

    def load_skip_file(self):
        known_failures = []
        try:
            skip = yaml.safe_load(open(self.args.skip_file))
            for t in skip.get('known_failures'):
                if self.args.undercloud == t.get('undercloud', False):
                    known_failures.append(t.get('test'))
        except yaml.constructor.ConstructorError:
            self.log.error('Invalid yaml file {}'.format(self.args.skip_file))
        finally:
            return known_failures

    def get_test_results(self, console):
        ok = [TESTRE.search(l).group(1)
              for l in console.splitlines() if OK in l]
        return ok

    def compare_results(self, known_failures, ok_results):
        regex_to_be_removed = {}

        for kf in known_failures:
            for o_r in ok_results:
                if re.match(kf, o_r):
                    if not regex_to_be_removed.get(kf):
                        regex_to_be_removed[kf] = []
                    regex_to_be_removed[kf].append(o_r)
        return regex_to_be_removed


def main():
    cmd = CheckSkipCmd()
    cmd.run()


if __name__ == '__main__':
    main()
