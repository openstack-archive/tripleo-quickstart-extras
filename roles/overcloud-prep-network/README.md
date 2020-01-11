Role Name
=========

An Ansible role to copy configuration files to the undercloud prior to
deployment.

Requirements
------------

This  playbook expects that the undercloud has been installed and setup using
one of the roles relevant to baremetal overcloud deployments.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/sect-Scaling_the_Overcloud.html).

- working_dir: <'/home/stack'> -- working directory for the role. Assumes
stackrc file is present at this location
- baremetal_instackenv: <"{{ working_dir }}/instackenv.json"> -- location of
instackenv.json to copy over
- baremetal_network_environment: <"{{ working_dir }}/network-isolation.yml">
-- location of network-environment file to copy over
- undercloud_type: <virtual> -- can be overwritten with values like 'baremetal'
 or 'ovb'
- undercloud_networks: by default an external network is defined by
  tripleo-quickstart, as follows:

      undercloud_networks:
        external:
          address: "{{ undercloud_external_network_cidr|nthhost(1) }}"
          netmask: "{{ undercloud_external_network_cidr|ipaddr('netmask') }}"
          address6: "{{ undercloud_external_network_cidr6|nthhost(1) }}"
          device_type: ovs
          type: OVSIntPort
          ovs_bridge: br-ctlplane
          ovs_options: '"tag=10"'
          tag: 10

  But it is possible to override this, when specific vlan options are needed:

      undercloud_networks:
        external:
          address: 172.20.0.254
          netmask: 255.255.255.0
          device_type: ovs
          type: OVSIntPort
          ovs_bridge: br-ctlplane
          ovs_options: '"tag=1005"'
          tag: 1005

  Or when the external network on the undercloud is and ethernet device instead
of a bridge:

      undercloud_networks:
        external:
          address: 172.20.0.254
          netmask: 255.255.255.0
          device_type: ethernet
          device_name: eth2

  What makes the difference in this case is the *device_type* set to *ethernet*
instead of *ovs* and the *device_name* which must be the name of the ethernet
device on the undercloud.

Dependencies
------------

This playbook does not deploy the overcloud. After this playbook runs, call
https://github.com/redhat-openstack/ansible-role-tripleo-overcloud.

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
