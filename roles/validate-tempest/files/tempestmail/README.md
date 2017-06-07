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
