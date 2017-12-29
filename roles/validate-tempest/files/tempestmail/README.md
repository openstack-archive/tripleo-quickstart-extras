Tempest mail tool
=================

Description
-----------

This is a tool to send mails to people interested in TripleO periodic jobs
status.

Usage
-----

```bash
tempestmail.py -c config.yaml --jobs periodic-tripleo-ci-centos-7-ovb-ha-tempest
```

Config file example
-------------------

```yaml
mail_username: username
mail_password: password
smtp_server: smtp.gmail.com:587
mail_from: username@gmail.com
template_path: template/
log_url: 'http://logs.openstack.org/periodic'
emails:
  - mail: 'arxcruz@gmail.com'
    name: 'Arx Cruz'
template: template.html
known_failures:
    - test: 'tempest.scenario.test_volume_boot_pattern.*'
      reason: 'http://bugzilla.redhat.com/1272289'
    - test: 'tempest.api.identity.*v3.*'
      reason: 'https://bugzilla.redhat.com/1266947'
    - test: '.*test_external_network_visibility'
      reason: 'https://bugs.launchpad.net/tripleo/+bug/1577769'
```

With this config file, the user will always get an email independent of the
failed tempest test.
You can also filter to receive the notification, only for a specific set of
jobs. Doing so, the user will only receive an email when the job being
executed matches with one in the jobs list:

```yaml
mail_username: username
mail_password: password
smtp_server: smtp.gmail.com:587
mail_from: username@gmail.com
template_path: template/
log_url: 'http://logs.openstack.org/periodic'
emails:
  - mail: 'arxcruz@gmail.com'
    name: 'Arx Cruz'
    jobs:
      - gate-tripleo-ci-centos-7-ovb-ha-oooq
      - gate-tripleo-ci-centos-7-ovb-containers-oooq
template: template.html
known_failures:
    - test: 'tempest.scenario.test_volume_boot_pattern.*'
      reason: 'http://bugzilla.redhat.com/1272289'
```

In this case, the user will not receive the email if the job name is not
gate-tripleo-ci-centos-7-ovb-ha-oooq or
gate-tripleo-ci-centos-7-ovb-containers-oooq.
You can also set a regular expression with the failure test you are interested.
In this case, you will only receive the email, if the regex matches a test that
fails for that particular job:

```yaml
mail_username: username
mail_password: password
smtp_server: smtp.gmail.com:587
mail_from: username@gmail.com
template_path: template/
log_url: 'http://logs.openstack.org/periodic'
emails:
  - mail: 'arxcruz@gmail.com'
    name: 'Arx Cruz'
    jobs:
      - gate-tripleo-ci-centos-7-ovb-ha-oooq
      - gate-tripleo-ci-centos-7-ovb-containers-oooq
    regex:
      - 'tempest.api.object_storage.test_container_quotas.ContainerQuotasTest'
      - 'tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_mtu_sized_frames'
template: template.html
known_failures:
    - test: 'tempest.scenario.test_volume_boot_pattern.*'
      reason: 'http://bugzilla.redhat.com/1272289'
```

In this example, the user will only receive an email if the job
gate-tripleo-ci-centos-7-ovb-ha-oooq or
gate-tripleo-ci-centos-7-ovb-containers-oooq has a test failure that matches
the regex.

```yaml
...
emails:
 - mail: fail1@example.com
   regex: '.*foo.*'
   topics: foo1
 - mail: fail1@example.com
   regex: '.*bar.*'
   topics: bar1
 - mail: fail2@example.com
   regex: '.*bar.*'
   topics: bar2,extra
...
```

if a jobs contains tests matching both 'foo' and 'bar', then:
* fail1@ will receive an email '[foo1]...' and an email '[bar1]...'
* fail2@ will receive an email '[bar2][extra]...'


So, the order is:

1. If there's no jobs list the user will receive all the emails.
1. If there's a jobs list the user will receive emails only for that jobs.
1. If there's a regex the user will only receive emails when a regex matches.
1. If there's a job list and a regex list the user will only receive an email
   when both matches.

HTML template example
---------------------

Tempest mail uses Jinja2 to create templates in html, and it parses the
following data to HTML (stored in the data dictionary)

* run - Bool - Whether the job runs or not
* date - String - In the format %Y-%m-%d %H:%M
* link - String - Contain the log url
* job - String - The job name
* failed - List - List of tests that fails in string format
* covered - List - List of tests covered in dictionary format, containing:
    * failure - String - Test name
    * reason - String - Reason of the failure
* new - List - List of new failures
* errors - List - Errors found in the log

An example of output of the data is showed below:

```python
[
    {
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
]
```

And here's an example you can use as email template:

```html
<html>
    <head></head>
    <body>
        <p>Hello,</p>
        <p>Here's the result of the latest tempest run for job {{ data.get('job') }}.</p>
        <p>The job ran on {{ data.get('date') }}.</p>
        <p>For more details, you can check the URL: {{ data.get('link') }}
        {% if data.get('new') %}</p>
    <h2>New failures</h2>
    <ul>
    {% for fail in data.get('new') %}
        <li>{{ fail }}</li>
    {% endfor %}
    </ul>
    {% endif %}

    {% if data.get('covered') %}
    <h2>Known failures</h2>
    <ul>
    {% for fail in data.get('covered') %}
    <li>{{ fail.get('failure') }} - {{ fail.get('reason') }}</li>
    {% endfor %}
    </ul>
    {% endif %}
    </body>
</html>
```

Tests
-----

[user@localhost tempestmail]$ python -m unittest discover -v

