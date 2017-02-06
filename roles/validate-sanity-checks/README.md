Validate-Sanity-Checks
======================

This role provides a script for executing sanity checks on an overcloud
deployment. The role creates basic checks using openstack CLI depending
on the services enabled on the overcloud deployment. These sanity checks
are useful when a full overcloud is not deployed and the overcloud
validation roles cannot be run.

Requirements
------------

This role requires that the overcloud is deployed and the services of interest
are available for testing.

Role Variables
--------------

* `sanity_content_name`: <sanity_test> - The sanity tests to be run in checks
* `sanity_scripts`: <validate-sanity-checks.sh.j2> - Script to create the sanity checks tests
* `sanity_checks_log`: <validate_sanity_test.log> - Log file to store the output of the sanity checks
* `sanitytest_create`: <true> - Boolean variable whether to create the artifacts to test enabled services
* `sanitytest_cleanup`: <true> - Boolean variable whether to clean up the artifacts created by the sanity checks
* `sanity_step_sanity_checks`: <true> - Boolean variable whether to execute the sanity checks test

Dependencies
------------

No dependencies.

Example Playbook
----------------

    # Execute sanity checks against the overcloud deployment
    - name: Sanity check the overcloud services
      hosts: undercloud
      roles:
        - { role: validate-sanity-checks,  when: run_sanity_checks|bool}

License
-------

Apache 2.0

Author Information
------------------

TripleO CI Team


