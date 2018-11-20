Role Name
=========

An Ansible role to set up a machine to host a virtual undercloud for a TripleO deployment on baremetal nodes.

Requirements
------------

This role assumes that the host machine already has a nic on the provisioning network. The role assigns the nic an IP address.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/sect-Scaling_the_Overcloud.html)

- virthost_provisioning_interface: <eth1> --  NIC for the provisioning interface on the undercloud host
- virthost_provisioning_ip: <192.168.122.1> -- IP address for the provisioning interface on the undercloud host
- virthost_provisioning_netmask: <255.255.255.192> -- Netmask for the provisioning interface on the undercloud host
- virthost_provisioning_hwaddr: <52:54:00:00:76:00> -- MAC address the provisioning interface on the undercloud host
- working_dir: <'/home/stack'> -- working directory for the role.


Dependencies
------------

The playbook included in this role calls https://github.com/redhat-openstack/ansible-role-tripleo-validate-ipmi and https://github.com/redhat-openstack/ansible-role-tripleo-baremetal-overcloud.

Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Prepare the host for PXE forwarding
      hosts: virthost
      gather_facts: false
      roles:
        - ansible-role-tripleo-baremetal-prep-virthost

License
-------

Apache-2.0

Author Information
------------------

RDO-CI Team
