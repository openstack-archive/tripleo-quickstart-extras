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
