ansible-role-tripleo-overcloud-prep-config
==========================================

An Ansible role to copy configuration files to the undercloud prior to
overcloud deployment.

Requirements
------------

This  playbook expects that the undercloud has been installed and setup using
one of the roles relevant to baremetal overcloud deployments.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your
[initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/sect-Scaling_the_Overcloud.html).

- `working_dir`: <'/home/stack'> -- working directory for the role. Assumes
  stackrc file is present at this location
- `baremetal_instackenv`: <"{{ working_dir }}/instackenv.json"> -- location of
  instackenv.json to copy over
- `baremetal_network_environment`: <"{{ working_dir }}/network-isolation.yml">
  -- location of network-environment file to copy over
- `undercloud_type`: <virtual> -- can be overwritten with values like
  'baremetal' or 'ovb'
- `extra_tht_configs`: -- a list of files to copy to the overcloud and add as
  extra config to the overcloud-deployment command

Role Network Variables
----------------------
The following variables are nested under network_environment_args.  The values
are calculated at run time using ansible jinja filters. This are, in turn,
persisted to a heat environment file that is used in for the overcloud
deployment.

**Note:** See additional documentation at http://docs.ansible.com/ansible/playbooks_filters_ipaddr.html and
the ansible code base ansible/plugins/filter/ipaddr.py

```
network_environment_args:
  ExternalNetCidr: "{{ undercloud_external_network_cidr }}"
  ExternalAllocationPools: >
    [{'start': '{{ undercloud_external_network_cidr|nthhost(4) }}',
    'end': '{{ undercloud_external_network_cidr|nthhost(250) }}'}]
  NeutronExternalNetworkBridge: ""
  ControlPlaneSubnetCidr: "{{ undercloud_network_cidr|ipaddr('prefix') }}"
  ControlPlaneDefaultRoute: "{{ undercloud_network_cidr|nthhost(1) }}"
  EC2MetadataIp: "{{ undercloud_network_cidr|nthhost(1) }}"
  DnsServers: [ '{{ external_network_cidr|nthhost(1) }}' ]

```

Dependencies
------------

This playbook does not deploy the overcloud. After this playbook runs, call
https://github.com/redhat-openstack/ansible-role-tripleo-overcloud.

Example Playbook
----------------

Sample playbook to call the role

```yaml
- name: Copy configuration files
  hosts: undercloud
  roles:
    - ansible-role-tripleo-overcloud-prep-config
```

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
