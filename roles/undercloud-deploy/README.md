undercloud-deploy
==========================================

An Ansible role to execute the deployment of the tripleo undercloud

Requirements
------------

This requires a running host to deploy the undercloud.

Role Variables
--------------

- `undercloud_config_file`: <'undercloud.conf.j2'> -- the name of the jinja template
used as the base for the undercloud.conf
- `undercloud_install_script`: <'undercloud-install.j2'> -- the name of the jinja template
used as the base for the undercloud-install bash script
- `undercloud_install_log`: <'{{ working_dir }}/undercloud_install.log'> -- the full path
to the undercloud install log file.
- `network_environment_file`: <'network-environment.yaml.j2'> -- the name of the jinja template
used as the base for the network-environment for tripleo.
- `undercloud_hieradata_override_file`: <'quickstart-hieradata-overrides.yaml.j2'> -- the name of
jinja template used to override the undercloud's install hieradata
- `step_introspect`: <'false'> -- boolean value to enable/disable ironic introspection
- `bash_deploy_ramdisk`: <'false'> -- the variable allows older versions of tripleo to upload images
properly with the option --old-deploy-image
- `step_install_undercloud`: <'true'> -- turn on/off the undercloud deployment
- `libvirt_uri`: <'qemu:///session'> -- the URI used by libvirt, by default tripleo-quickstart uses
user sessions to provide greater flexixiblity to our users. ** additional documentation ** is at
http://docs.openstack.org/developer/tripleo-quickstart/accessing-libvirt.html
- `undercloud_conf_extra`: "" -- extra options to be added to ~/undercloud.conf
- undercloud_undercloud_public_host: Sets up the 'undercloud_public_host'
  parameter from undercloud.conf.
- undercloud_undercloud_admin_host: Sets up the 'undercloud_admin_host' from
  undercloud.conf.

Role Network Variables
----------------------
- `undercloud_network_cidr`: <'192.168.24.0/24'> -- the network cidr for the undercloud, note this
also currently the default cidr used in other CI environments for tripleo.

The following variables are nested under network_environment_args.  The values are calculated at
run time using ansible jinja filters.

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

Example Playbook
----------------

Sample playbook to call the role

```yaml
# Deploy the undercloud
- name:  Install undercloud
  hosts: undercloud
  gather_facts: no
  roles:
    - undercloud-deploy
```
