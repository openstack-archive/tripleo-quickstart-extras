Role Name
=========

Ansible roles for managing a heat stack to deploy an OpenStack cloud using OpenStack Virtual Baremetal.

Requirements
------------

These roles assume that the host cloud has already been patched as per
https://github.com/cybertron/openstack-virtual-baremetal/blob/master/README.rst#patching-the-host-cloud.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](http://docs.openstack.org/developer/tripleo-docs/basic_deployment/basic_deployment_cli.html#deploy-the-overcloud)

To interact with the Openstack Virtual Baremetal host cloud, credentials are needed:
- os_username: <cloud_username>
- os_password: <user_password>
- os_tenant_name: <tenant_name>
- os_auth_url: <cloud_auth_url> # For example http://190.1.1.5:5000/v2.0

Parameters required to access the stack:
- prefix --used as in id for the image and the stack parameters
- stack_name: <'oooq-{{ prefix }}stack'> -- name for OVB heat stack
- rc_file: </home/stack/overcloudrc> -- file to reference the overcloud
- node_name: 'undercloud'
- existing_key_location: <local_working_dir> -- required to access the undercloud node
- ssh_extra_args: <'-F "{{ local_working_dir }}/ssh.config.ansible"'>
- undercoud_key: <"{{ local_working_dir }}/id_rsa_undercloud">

Parameters required for shade (See defaults/main.yml for default values):
- heat_template
- environment_list

Parameters used the env.yaml file to create the OVB heat stack (See defaults/main.yml for default values):
- bmc_flavor
- bmc_image
- bmc_prefix
- baremetal_flavor
- baremetal_image
- baremetal_prefix
- key_name
- private_net
- node_count
- public_net
- provision_net
- undercloud_name
- undercloud_image
- undercloud_flavor
- external_net
- templates_dir
- ovb_dir
- network_isolation_type: <multi-nic> -- other options are 'none' and 'public-bond'

- registered_releases -- releases for which images should be available for the undercloud

Dependencies
------------

This playbook depends on the shade library and https://github.com/cybertron/openstack-virtual-baremetal.

Example Playbook
----------------

Playbooks to create the strack prior to TripleO Quickstart deployments will require:

- name: Create the OVB stack
  hosts: localhost
  roles:
    - { role: ovb-manage-stack, ovb_manage_stack_mode: 'create' }

License
-------

Apache

Author Information
------------------

RDO-CI Team

