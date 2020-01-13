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
import datetime
import logging
import os
import re
import requests
import smtplib
import sys
import yaml

from email.mime.text import MIMEText
from jinja2 import Environment
from jinja2 import FileSystemLoader
from six.moves.urllib.parse import urljoin

HREF = re.compile('href="([^"]+)"')
JOBRE = re.compile('[a-z0-9]{7}/')
TESTRE = re.compile(r'(tempest[^ \(\)]+|\w+\.tests\.[^ \(\)]+)')
TIMEST = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}):\d{2}\.\d+ \|')
TITLE = re.compile('<title>(.*?)</title>')

FAILED = "... FAILED"
OK = "... ok"
ERROR = "... ERROR"
SKIPPED = "... SKIPPED"

NLINKS = 1


def compare_tests(failures, config):
    '''Detect fails covered by bugs and new'''
    covered, new = [], []
    for fail in failures:
        for test in config.known_failures:
            if re.search(test.get('test'), fail):
                covered.append({'failure': fail, 'reason': test.get('reason')})
    new = [fail for fail in failures if not any(
        c['failure'] == fail for c in covered)]
    return covered, new


def get_html(url):
    try:
        resp = requests.get(url)
        if resp is None:
            raise TypeError
    except TypeError as e:
        print("Exception %s" % str(e))
        return
    return resp


def get_tests_results(console):
    '''Get results of tests from console'''
    failed = [TESTRE.search(l).group(1)
              for l in console.splitlines() if FAILED in l]
    ok = [TESTRE.search(l).group(1)
          for l in console.splitlines() if OK in l]
    errors = [TESTRE.search(l).group(1)
              for l in console.splitlines() if ERROR in l]

    # all_skipped = [TESTRE.search(l).group(1)
    #               for l in console.splitlines() if SKIPPED in l]
    return failed, ok, errors


class Config(object):
    pass


class Mail(object):
    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger('Mail')
        self.mail_from = config.mail_from
        self.username = config.username
        self.password = config.password
        self.smtp = config.smtp
        self.require_auth = config.require_auth
        self.templates_path = os.path.join(os.path.dirname(__file__),
                                           config.templates_path)
        self.template = config.template

    def render_template(self, data):
        self.log.debug('Rendering template')
        env = Environment(loader=FileSystemLoader(self.templates_path))
        env.filters['datetimeformat'] = self.datetimeformat
        template = env.get_template(self.template)
        return template.render(data=data)

    def datetimeformat(self, value, format="%d-%m-%Y %H:%M"):
        return value.strftime(format)

    def filter_emails(self, job, data):
        has_errors = False
        bookaddr = {}

        for error in [data.get(x, []) for x in ('new', 'failed', 'errors')]:
            if error:
                self.log.debug('There are tests with failed result')
                has_errors = True
                break

        if has_errors:
            # Check if the user is assigned for the job
            # If there's no job assigned, we add the user anyway
            emails = [m for m in self.config.emails if job in
                      m.get('jobs') or not
                      m.get('jobs')]

            # Add all addresses except those that regex don't match
            for email in emails:
                add = True
                if email.get('regex'):
                    for r in email.get('regex'):
                        if len(filter(r.search, data.get('new'))):
                            break
                        add = False
                if add:
                    topics = ''
                    if email.get('topics'):
                        # Parse topics and format it between brackets
                        t = email.get('topics').split(',')
                        topics = ''.join('[{}]'.format(s) for s in t)
                    # Add the address to the bookaddr dict
                    # {'[foo][bar]' : ['john@redhat.com', 'mary@redhat.com']}
                    bookaddr.setdefault(topics, []).append(email.get('mail'))
        else:
            self.log.debug('No failures send email to everybody')
            addresses = [m.get('mail') for m in self.config.emails
                         if not m.get('fail_only')]
            # Single group with empty topic is added to the bookaddr
            bookaddr.setdefault('', []).append(addresses)

        data['has_errors'] = has_errors

        return bookaddr

    def _send_mail_local(self, addresses, message, subject, output):
        msg = MIMEText(message, 'html')
        msg['Subject'] = subject
        msg['From'] = self.mail_from
        msg['To'] = ",".join(addresses)
        s = smtplib.SMTP(self.smtp)
        if self.require_auth:
            s.ehlo()
            s.starttls()
            s.login(self.username, self.password)
        s.sendmail(self.mail_from, addresses, msg.as_string())
        self.log.debug('Sending mail')
        s.quit()

        if output:
            self.log.debug('Writing email in {}'.format(output))
            with open(output, 'w') as f:
                f.write(msg.as_string())

    def _send_mail_api(self, addresses, message, subject):
        data = {'addresses': addresses, 'message': message, 'subject': subject,
                'mime_type': 'html'}
        requests.post(self.config.api_server, data=data)

    def send_mail(self, job, data, output):
        bookaddr = self.filter_emails(job, data)
        message = self.render_template(data)

        # Send a separate email to the addresses grouped by topics
        for topics, addresses in bookaddr.items():
            subject = '{} Job {} results'.format(topics, job).lstrip()
            if self.config.use_api_server:
                self._send_mail_api(addresses, message, subject)
            else:
                self._send_mail_local(addresses, message, subject, output)


class TempestMailCmd(object):
    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(description='tempest-mail')
        parser.add_argument('-c', dest='config',
                            default='/etc/tempest-mail/tempest-mail.yaml',
                            help='Path to config file')
        parser.add_argument('-l', dest='logconfig',
                            help='Path to log config file')
        parser.add_argument('--version', dest='version',
                            help='Show version')
        parser.add_argument('--job', dest='job',
                            help='Job name', required=True)
        parser.add_argument('--file', dest='file',
                            help='File containing tempest output')
        parser.add_argument('--skip-file', dest='skip_file',
                            help='List of skip files')
        parser.add_argument('--output', dest='output',
                            help='Save the email content in a file')
        parser.add_argument('--log-url', dest='log_url',
                            help='Set log url')
        self.args = parser.parse_args(args)

    def setup_logging(self):
        self.log = logging.getLogger('tempestmail.TempestMail')
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s: '
                                   '%(message)s')

    def get_index(self):
        '''Get index page of periodic job and returns all links to jobs'''
        url = urljoin(self.config.log_url, self.args.job)
        res = get_html(url)
        if res is None or not res.ok:
            return []

        body = res.content.decode() if res.content else ''
        hrefs = [HREF.search(l).group(1)
                 for l in body.splitlines() if HREF.search(l)]
        links = ["/".join((url, link))
                 for link in hrefs if JOBRE.match(link)]
        if links:
            # Number of links to return
            return links[:NLINKS]
        else:
            return []

    def get_console(self, job_url=None):
        '''Get console page of job'''

        if self.args.file and not job_url:
            try:
                with open(self.args.file) as f:
                    console = f.read()
            except IOError:
                return (None, None, None)

        log_path = os.environ.get('LOG_PATH', None)
        if log_path:
            log_path = urljoin(getattr(
                self.args, 'log_url', self.config.default_log_url), log_path)

        return (console, datetime.datetime.now(), log_path)

        def _good_result(res):
            if res is None or int(res.status_code) not in (200, 404):
                return False
            else:
                return True

        def _get_date(c):
            text = c.splitlines()
            # find last line with timestamp
            for l in text[::-1]:
                if TIMEST.match(l):
                    return datetime.datetime.strptime(
                        TIMEST.search(l).group(1),
                        "%Y-%m-%d %H:%M")
            return None

        url = urljoin(job_url, "console.html.gz")
        res = get_html(url)
        if not _good_result(res):
            print("Error getting console %s" % url)
            # Try again
            res = get_html(url)
            if not _good_result(res):
                return (None, None, None)
        elif int(res.status_code) == 404:
            url = urljoin(job_url, "console.html")
            res = get_html(url)
            if not _good_result(res):
                # Try again
                res = get_html(url)
                if not _good_result(res):
                    print("Error getting console %s" % url)
                    return (None, None, None)
        console = res.content.decode('utf-8')
        date = _get_date(console)
        return console, date, url

    def get_data(self, console, date, link):
        fails, ok, errors = get_tests_results(console)

        d = {
            'run': True,
            'date': date,
            'link': link,
            'job': self.args.job
        }

        if fails or errors:
            covered, new = compare_tests(fails, self.config)
            d.update({
                'failed': fails,
                'covered': covered,
                'new': new,
                'errors': errors,
            })
        elif ok:
            d['ok'] = ok
        elif not fails and not ok and not errors:
            d['run'] = False

        return d

    def load_skip_file(self, skipfile):
        known_failures = []
        try:
            skip = yaml.safe_load(open(self.args.skip_file))
        except yaml.constructor.ConstructorError:
            self.log.error('Invalid yaml file {}'.format(self.args.skip_file))
        else:
            for t in skip.get('known_failures'):
                known_failures.append({'test': t.get('test'),
                                       'reason': t.get('reason')})

        return known_failures

    def checkJobs(self):
        data = []
        if self.args.file:
            console, date, link = self.get_console()
            link = link or ''
            d = self.get_data(console, date, link)

            data.append(d)
        else:
            index = self.get_index()
            for run in index:
                console, date, link = self.get_console(run)

                if not console or not date:
                    continue

                link = link or ''
                d = self.get_data(console, date, link)

                data.append(d)

        data = sorted(data, key=lambda x: x['date'])
        last = data[-1]
        send_mail = Mail(self.config)
        send_mail.send_mail(self.args.job, last, self.args.output)

    def setupConfig(self):
        self.log.debug("Loading configuration")
        try:
            config = yaml.safe_load(open(self.args.config))
        except yaml.constructor.ConstructorError:
            self.log.error('Invalid yaml file {}'.format(self.args.config))

        newconfig = Config()
        known_failures = []

        newconfig.emails = []
        newconfig.username = config.get('mail_username', '')
        newconfig.password = config.get('mail_password', '')
        newconfig.mail_from = config.get('mail_from', '')
        newconfig.smtp = config.get('smtp_server', '')
        newconfig.templates_path = config.get('templates_path')
        newconfig.template = config.get('template')
        newconfig.log_url = config.get('log_url')
        newconfig.require_auth = config.get('require_auth', False)
        newconfig.default_log_url = config.get('default_log_url',
                                               'http://logs.openstack.org')

        for e in config.get('emails'):
            regex = [re.compile(r) for r in e.get('regex', [])]

            newconfig.emails.append({'name': e.get('name'),
                                     'mail': e.get('mail'),
                                     'jobs': e.get('jobs', []),
                                     'regex': regex,
                                     'topics': e.get('topics'),
                                     'fail_only': e.get('fail_only', False)})
        for t in config.get('known_failures', []):
            known_failures.append({'test': t.get('test'),
                                   'reason': t.get('reason')})

        if self.args.skip_file:
            known_failures = (
                known_failures + self.load_skip_file(self.args.skip_file))

        newconfig.known_failures = known_failures
        newconfig.api_server = config.get('api_server')
        newconfig.use_api_server = config.get('use_api_server', False)
        self.config = newconfig


def main():
    tmc = TempestMailCmd()
    tmc.parse_arguments(sys.argv[1:])
    tmc.setup_logging()
    tmc.setupConfig()
    tmc.checkJobs()


if __name__ == '__main__':
    sys.exit(main())
