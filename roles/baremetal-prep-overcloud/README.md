Role Name
=========

An Ansible role to setup the undercloud for a deployment on baremetal overcloud nodes.

Requirements
------------

This  playbook expects that the undercloud has been installed and setup using one of the roles relevant to baremetal overcloud deployments.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/sect-Scaling_the_Overcloud.html).

- step_root_device_size: <false> -- boolean value that will apply disk size hints and rerun introspection if true
- working_dir: <'/home/stack'> -- working directory for the role. Assumes stackrc file is present at this location
- step_adjust_mtu: <false> -- boolean value that will change MTUS on specified nics
- mtu: <1350> -- numerical value to set MTUs
- mtu_interface: <'eth1'> -- list of NICs
- undercloud_type: <virtual> -- can be overwritten with values like 'baremetal' or 'ovb'
- network_isolation: <true> -- bolean value to test if network isolation wil be used in the deployment
- network_isolation_ipv4_cidr: <"172.16.23.0/24">

Dependencies
------------

This playbook does not deploy the overcloud. After this playbook runs, call https://github.com/redhat-openstack/ansible-role-tripleo-overcloud.

Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Prepare for deployment on baremetal overcloud
      hosts: virthost
      gather_facts: no
      roles:
        - ansible-role-tripleo-overcloud-prep-baremetal

License
-------

Apache

Author Information
------------------

RDO-CI Team

