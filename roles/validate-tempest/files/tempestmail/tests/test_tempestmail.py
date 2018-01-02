import datetime
import mock
import tempfile
import unittest

from tempestmail import Config
from tempestmail import Mail
from tempestmail import TempestMailCmd


class MailTest(unittest.TestCase):
    def setUp(self):
        self.config = self._generate_config()
        self.data = self._generate_data()
        self.render_output = self._get_render_template_output()
        self.maxDiff = None

    def _generate_config(self):
        config = Config()
        config.mail_from = 'tripleoresults@gmail.com'
        config.templates_path = 'tests/fixtures/'
        config.log_url = 'http://logs.openstack.org/periodic/'
        config.api_server = 'http://tempest-tripleoci.rhcloud.com/api/v1.0/sendmail'
        config.use_api_server = True
        config.default_log_url = 'http://logs.openstack.org'
        config.username = ''
        config.password = ''
        config.smtp = ''
        config.require_auth = True
        config.emails = [
            {'mail': 'email1@example.com', 'name': 'name 1',
             'jobs': [], 'regex': []},
            {'mail': 'email2@example.com', 'name': 'name 2',
             'jobs': [], 'regex': []}
            ]
        config.template = 'template.html'
        return config

    def _get_render_template_output(self):
        output = (u'<html>\n    <head></head>\n    <body>\n        '
                  '<p>Hello,</p>\n        <p>Here\'s the result of the latest '
                  'tempest run for job '
                  'periodic-tripleo-ci-centos-7-ovb-ha-tempest.</p>\n        '
                  '<p>The job ran on 2017-01-19 08:27:00.</p>\n        '
                  '<p>For more details, you can check the URL: '
                  'http://logs.openstack.org/periodic/periodic-tripleo-ci-'
                  'centos-7-ovb-ha-tempest/1ce5e95/console.html (It might take '
                  'a few minutes to upload the logs).</p>\n    \n    '
                  '<h2>New failures</h2>\n    <ul>\n    \n        <li>'
                  'tempest.api.object_storage.test_container_quotas.'
                  'ContainerQuotasTest.test_upload_too_many_objects</li>'
                  '\n    \n        <li>tempest.api.object_storage.test_'
                  'container_quotas.ContainerQuotasTest.'
                  'test_upload_valid_object</li>\n    \n    </ul>\n    \n\n    '
                  '\n    \n    \n    <p></p>\n    <p>You are receiving this '
                  'email because someone from TripleO team though you were '
                  'interested in these results.</p>\n    <p>\n    '
                  '</body>\n</html>\n')
        return output

    def _generate_data(self):
        data = {
            'errors': [],
            'run': True,
            'failed': [
                u'tempest.api.object_storage.test_container_quotas.ContainerQuotasTest.test_upload_too_many_objects',
                u'tempest.api.object_storage.test_container_quotas.ContainerQuotasTest.test_upload_valid_object'
            ],
            'job': 'periodic-tripleo-ci-centos-7-ovb-ha-tempest',
            'link': u'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ovb-ha-tempest/1ce5e95/console.html',
            'covered': [],
            'date': datetime.datetime(2017, 1, 19, 8, 27),
            'new': [
                u'tempest.api.object_storage.test_container_quotas.ContainerQuotasTest.test_upload_too_many_objects',
                u'tempest.api.object_storage.test_container_quotas.ContainerQuotasTest.test_upload_valid_object'
            ]
        }
        return data

    def test_render_template(self):
        mail = Mail(self.config)
        content = mail.render_template(self.data)
        self.assertEquals(self.render_output, content)

    def test_filter_emails(self):
        mail = Mail(self.config)
        self.assertEquals(self.data.get('has_errors'), None)
        addresses = mail.filter_emails(
            'periodic-tripleo-ci-centos-7-ovb-ha-tempest', self.data)
        self.assertEquals(['email1@example.com', 'email2@example.com'],
                          addresses)
        mail.config.emails[0]['jobs'].append('another-job')
        addresses = mail.filter_emails(
            'periodic-tripleo-ci-centos-7-ovb-ha-tempest', self.data)
        self.assertEquals(['email2@example.com'], addresses)
        self.assertEquals(self.data['has_errors'], True)
        mail.config.emails[0]['jobs'] = []
        mail.config.emails[0]['regex'].append('tempest.some.regex')
        self.assertEquals(['email2@example.com'], addresses)

    @mock.patch('tempestmail.Mail._send_mail_api')
    @mock.patch('tempestmail.Mail._send_mail_local')
    def test_send_mail(self, mock_local, mock_api):
        mail = Mail(self.config)
        mail.send_mail('periodic-tripleo-ci-centos-7-ovb-ha-tempest',
                       self.data, False)
        mock_api.assert_called_with(['email1@example.com',
                                     'email2@example.com'],
                                    self.render_output,
                                    'Job periodic-tripleo-ci-centos-7-ovb-ha-'
                                    'tempest results')
        mock_local.assert_not_called()
        mock_api.reset_mock()
        self.config.use_api_server = False
        mail = Mail(self.config)
        mail.send_mail('periodic-tripleo-ci-centos-7-ovb-ha-tempest',
                       self.data, False)
        mock_local.assert_called_with(['email1@example.com',
                                       'email2@example.com'],
                                      self.render_output,
                                      'Job periodic-tripleo-ci-centos-7-ovb-ha-'
                                      'tempest results', False)


class TestTempestMailCmd(unittest.TestCase):
    def setUp(self):
        self.content_job = self._get_content_file(
            'tests/fixtures/content_job.html')
        self.console_ok = self._get_content_file(
            'tests/fixtures/console_ok.log')
        self.console_fail = self._get_content_file(
            'tests/fixtures/console_fail.log')
        self.fd_file, self.tmp_file = tempfile.mkstemp()
        self._populate_skip_file()

    def _get_content_file(self, filename):
        with open(filename) as f:
            content = f.read()

        return content

    def _populate_skip_file(self):
        content = '''
        known_failures:
        - test: '.*test_external_network_visibility'
          reason: 'Tempest test "external network visibility" fails'
          lp: 'https://bugs.launchpad.net/tripleo/+bug/1577769'
        - test: 'tempest.api.data_processing'
          reason: 'tempest.api.data_processing tests failing on newton'
          bz: 'https://bugzilla.redhat.com/show_bug.cgi?id=1357667'
        - test: 'neutron.tests.tempest.api.test_revisions.TestRevisions'
          reason: 'New test, need investigation'
        '''
        self.skip_file = open(self.tmp_file, 'w')
        self.skip_file.write(content)
        self.skip_file.close()

    @mock.patch('tempestmail.get_html')
    def test_get_index(self, html_mock):
        tmc = TempestMailCmd()
        tmc.parse_arguments(['-c', 'tests/fixtures/config.yaml', '--job',
                             'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                             'oooq-master'])
        tmc.setup_logging()
        tmc.setupConfig()

        html_mock.return_value.content.decode.return_value = self.content_job.decode()
        index = tmc.get_index()
        self.assertEquals(index, [(u'http://logs.openstack.org/periodic/perio'
                                   'dic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                                   'oooq-master/613de4e/')])

        html_mock.return_value.content.decode.return_value = 'No links'
        index = tmc.get_index()
        self.assertEquals(index, [])

        html_mock.return_value = None
        index = tmc.get_index()
        self.assertEquals(index, [])

        html_mock.ok.return_value = None
        index = tmc.get_index()
        self.assertEquals(index, [])

        html_mock.ok.return_value = True
        html_mock.content.return_value = None
        index = tmc.get_index()
        self.assertEquals(index, [])

    @mock.patch('tempestmail.get_html')
    def test_get_console(self, html_mock):
        tmc = TempestMailCmd()
        tmc.parse_arguments(['-c', 'tests/fixtures/config.yaml', '--job',
                             'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                             'oooq-master', '--file',
                             'tests/fixtures/console_ok.log'])
        tmc.setup_logging()
        tmc.setupConfig()

        console, date, log_path = tmc.get_console()
        self.assertEquals(console, self.console_ok)
        self.assertEquals(log_path, None)

        tmc.parse_arguments(['-c', 'tests/fixtures/config.yaml', '--job',
                             'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                             'oooq-master', '--file',
                             'tests/fixtures/not_found.log'])
        self.assertEquals(tmc.get_console(), (None, None, None))

        html_mock.return_value.status_code = '300'
        result = tmc.get_console(job_url='http://logs.openstack.org')
        self.assertEquals(result, (None, None, None))

        html_mock.return_value.status_code = '200'
        html_mock.return_value.content = self.console_ok
        console, date, url = tmc.get_console(
            job_url='http://logs.openstack.org')

        self.assertEquals(console, self.console_ok.decode('utf-8'))
        self.assertEquals(url, 'http://logs.openstack.org/console.html.gz')

        html_mock.return_value = None
        result = tmc.get_console(job_url='http://logs.openstack.org')
        self.assertEquals(result, (None, None, None))

    def test_get_data(self):
        tmc = TempestMailCmd()
        tmc.parse_arguments(['-c', 'tests/fixtures/config.yaml', '--job',
                             'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                             'oooq-master', '--file',
                             'tests/fixtures/not_found.log'])
        tmc.setup_logging()
        tmc.setupConfig()

        data = tmc.get_data(self.console_ok, None, 'http://logs.openstack.org')

        self.assertEquals(
            data['job'],
            'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq-master')
        self.assertEquals(data['date'], None)
        self.assertEquals(data['run'], True)
        self.assertEquals(data['link'], 'http://logs.openstack.org')
        self.assertEquals(len(data['ok']), 2)
        self.assertEquals(data.get('failed'), None)
        self.assertEquals(data.get('covered'), None)
        self.assertEquals(data.get('new'), None)
        self.assertEquals(data.get('errors'), None)

        data = tmc.get_data('some content', None, 'http://logs.openstack.org')
        self.assertEquals(data['run'], False)

        data = tmc.get_data(self.console_fail, None,
                            'http://logs.openstack.org')
        self.assertNotEquals(data['failed'], None)

    def test_load_skip_file(self):
        tmc = TempestMailCmd()
        tmc.parse_arguments(['-c', 'tests/fixtures/config.yaml', '--job',
                             'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                             'oooq-master', '--file',
                             'tests/fixtures/not_found.log', '--skip-file',
                             self.tmp_file])
        tmc.setup_logging()
        tmc.setupConfig()

        result = tmc.load_skip_file(self.tmp_file)

        expected = [
            {'test': '.*test_external_network_visibility',
             'reason': 'Tempest test "external network visibility" fails'},
            {'test': 'tempest.api.data_processing',
             'reason': 'tempest.api.data_processing tests failing on newton'},
            {'test': 'neutron.tests.tempest.api.test_revisions.TestRevisions',
             'reason': 'New test, need investigation'}
        ]
        self.assertEquals(result, expected)
        tmc.parse_arguments(['-c', 'tests/fixtures/config.yaml', '--job',
                             'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                             'oooq-master', '--file',
                             'tests/fixtures/not_found.log', '--skip-file',
                             'non_exist_file.txt'])
        result = tmc.load_skip_file(self.tmp_file)
        self.assertEquals(result, [])

    def test_setup_config(self):
        tmc = TempestMailCmd()
        tmc.parse_arguments(['-c', 'tests/fixtures/config.yaml', '--job',
                             'periodic-tripleo-ci-centos-7-ovb-nonha-tempest-'
                             'oooq-master', '--file',
                             'tests/fixtures/not_found.log', '--skip-file',
                             self.tmp_file])
        tmc.setup_logging()
        tmc.setupConfig()
        config = tmc.config

        self.assertEquals(config.require_auth, True)
        self.assertEquals(config.mail_from, 'tripleoresults@gmail.com')
        self.assertEquals(config.templates_path, 'template/')
        self.assertEquals(
            config.log_url,
            'http://logs.openstack.org/periodic/')
        self.assertEquals(
            config.api_server,
            'http://tempest-tripleoci.rhcloud.com/api/v1.0/sendmail')
        self.assertEquals(config.use_api_server, True)
        self.assertEquals(config.default_log_url, 'http://logs.openstack.org')
