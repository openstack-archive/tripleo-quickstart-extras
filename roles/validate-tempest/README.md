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
* `tempest_source`: rdo/upstream - Where to take tempest sources from - RDO package or upstream git repo
* `tempest_format`: venv/packages - Which tempest installation to use - either install python virtual environment
                    with installed there python modules from requirements file, or to use installed with RDO RPM packages
* `tempest_log_file` - name of log file for tempest run
* `test_regex` - tests regular expression for testr run, i.e. ".*smoke"
* `run_tempest`: false/true - to run tempest or not
* `skip_file_src`: path to skip tests file, set it empty if running without skip list: `skip_file_src=''`
* `tempest_workers`: int - how many parallel workers to run (default is number of cores)
* `tempest_isolated`: false/true - if to run every test id in separate test runner (default is false)
* `tempest_tests_file`: path to file - path to file with tests to run
* `tempest_until_failure`: false/true - default is false, repeat the run again and again until failure occurs
* `tempest_failing`: false/true - default is false, run only tests known to be failing

Dependencies
------------

No dependencies

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

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
