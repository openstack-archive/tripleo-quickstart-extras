Role Name
=========

An Ansible role to validate the instackenv.json and IPMI overcloud connections.

Requirements
------------

This role should be executed before deploying an overcloud on baremetal nodes to ensure that introspection and PXE boot will be able to access the nodes required for deployment.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/).

- validate_ipmi_step: <true> -- boolean value that will validate IPMI if true
- working_dir: <'/home/stack'> -- working directory for the role.


Dependencies
------------



Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Validate IPMI connection to overcloud nodes
      hosts: undercloud
      roles:
        - ansible-role-triple-validate-ipmi

License
-------

Apache

Author Information
------------------

RDO-CI Team
