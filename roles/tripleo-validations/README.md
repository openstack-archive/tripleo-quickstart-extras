Tripleo-validations
===================

An Ansible role to setup [tripleo-validations](https://github.com/openstack/tripleo-validations)

Requirements
------------

This playbook expects that the undercloud has been installed.

Role Variables
--------------

- working_dir: <'/home/stack'> -- working directory for the role.
- run_tripleo_validations: <False> -- to setup and run tripleo-validations tests
- run_tripleo_validations_negative_tests: <False> to run negative tests
- run_tripleo_validations_setup: <False> -- to setup or not tripleo-validations
- exit_on_validations_failure: <False> -- Exit tripleo-quickstart on validations failure
- validations_group: <[]> -- The validation group name which should be
  'pre-introspection', 'pre-deployment' or 'post-deployment'

Dependencies
------------

No dependencies.

Example Playbook
----------------

Run the tripleo-validations setup only:

    - hosts: undercloud
      vars:
        run_tripleo_validations_setup: True
      roles:
         - { role: tripleo-validations, when: run_tripleo_validations|bool }

Run the tripleo-validations tests belonging to the pre-introspection group:

    - hosts: undercloud
      vars:
        validations_group: ['pre-introspection']
      roles:
         - { role: tripleo-validations, when: run_tripleo_validations|bool }

Run pre-introspection negative tests

    - hosts: undercloud
      vars:
        validations_group: ['pre-introspection']
      roles:
         - { role: tripleo-validations, when: run_tripleo_validations_negative_tests|bool }

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
