ansible-role-tripleo-tempest
=========

Run tempest tests on undercloud or overcloud.

Requirements
------------

This Ansible role allows to run tempest tests against installed undercloud or overcloud.
 It can use both upstream sources with virtualenv and RDO packages for tempest.

Role Variables
--------------

* `tempest_undercloud`: false/true - whether to run tempest on installed undercloud
* `tempest_overcloud`: false/true - whether to run tempest on installed overcloud
* `tempest_format`: venv/packages - Which tempest installation to use - either install python virtual environment
                    with installed there python modules from requirements file, or to use installed with RDO RPM packages
* `tempest_log_file` - name of log file for tempest run
* `test_regex` - tests regular expression for testr run, i.e. smoke or tempest.api.object_storage|keystone_tempest_plugin.
* `run_tempest`: false/true - to run tempest or not
* `tempest_config`: false/true - whether to prepare the script which configures and runs tempest or not
* `skip_file_src`: path to skip tests file, set it empty if running without skip list: `skip_file_src=''`
* `tempest_workers`: int - how many parallel workers to run (default is number of cores)
* `tempest_isolated`: false/true - if to run every test id in separate test runner (default is false)
* `tempest_tests_file`: path to file - path to file with tests to run
* `tempest_until_failure`: false/true - default is false, repeat the run again and again until failure occurs
* `tempest_failing`: false/true - default is false, run only tests known to be failing
* `tempest_exit_on_failure`: true/false - whether to exit from role with tempest exit code (default: true)
* `tempestmail_config`: config.yaml - name of config file for tempestmail script
* `tempest_track_resources`: true/false - whether to save the state of resources after tempest run (default: true)

Skip tests file
---------------

Tempest test can be skipped if they are in a skip file, using the whole test
name or a regular expression.
Since the intention is to use the list of skip tests in other parts of
quickstart-extras, it's easier to have this list of skip tests in yaml format
where you can set the skip test, reason and launchpad or bugzilla. This make
easier later to check whether the test still valid or not to be skipped.
Skip files are under roles/validate-tempest/vars/tempest_skip_VERSION.yaml.
In these files you can add a regex, together with a reason and a bugzilla
or launchpad bug related to that particular test.
Launchpad and/or bugzilla re optional, however you must specify a reason why
you are skipping the test.

Example of skip file:

    ---
    known_failures:
      - test: 'tempest.scenario.test_volume_boot_pattern'
        reason: 'rdo-manager tempest smoke test failing on "floating ip pool not found"'
        bz: 'https://bugzilla.redhat.com/show_bug.cgi?id=1272289'
      - test: 'tempest.api.volume.test_volumes_get'
        reason: 'rdo-manager tempest smoke test failing on "floating ip pool not found"'
      - test: 'tempest.api.identity.*v3'
        reason: 'Tempest Identify tests failed on V3 api on OSP-D puddle'
        bz: 'https://bugzilla.redhat.com/show_bug.cgi?id=1266947'
      - test: 'tempest.api.image.v2.test_images_metadefs_namespace_properties.MetadataNamespacePropertiesTest.test_basic_meta_def_namespace_property'
        reason: 'glance is not calling glance-manage db_load_metadefs'
        lp: 'https://bugs.launchpad.net/tripleo/+bug/1664995'

Dependencies
------------

No dependencies

Example Playbook
----------------

    ---
    - name:  Run tempest
      hosts: undercloud
      gather_facts: no
      roles:
        - tripleo-tempest

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
