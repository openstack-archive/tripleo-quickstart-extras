Role Name
=========

An Ansible role to copy configuration files to the undercloud prior to deployment.

Requirements
------------

This  playbook expects that the undercloud has been installed and setup using one of the roles relevant to baremetal overcloud deployments.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/sect-Scaling_the_Overcloud.html).

- working_dir: <'/home/stack'> -- working directory for the role. Assumes stackrc file is present at this location
- baremetal_instackenv: <"{{ working_dir }}/instackenv.json"> -- location of instackenv.json to copy over
- baremetal_network_environment: <"{{ working_dir }}/network-isolation.yml"> -- location of network-environment file to copy over
- undercloud_type: <virtual> -- can be overwritten with values like 'baremetal' or 'ovb'

Dependencies
------------

This playbook does not deploy the overcloud. After this playbook runs, call https://github.com/redhat-openstack/ansible-role-tripleo-overcloud.

Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Copy configuration files
      hosts: virthost
      gather_facts: false
      roles:
        - ansible-role-tripleo-overcloud-prep-config

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team

