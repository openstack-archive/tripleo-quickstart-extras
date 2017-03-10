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
- `undercloud_ironic_ipxe_port`: <'3816'> -- port to use for httpd ipxe server
for ironic deploy
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
- `undercloud_undercloud_hostname`: Sets up the 'undercloud_hostname' value from
  undercloud.conf.
- `undercloud_enable_novajoin`: Sets up the 'enable_novajoin' value from
  undercloud.conf. Note that using 'enable_tls_everywhere' will have the same
  effect. Defaults to false.
- `novajoin_connect_timeout`: <5> Sets vendordata_dynamic_connect_timeout when novajoin is enabled
- `novajoin_read_timeout:` <5> Sets vendordata_dynamic_read_timeout when novajoin is enabled
- `prepare_novajoin`: If set to true, it will install novajoin in the undercloud,
  and run a script that will create the required privileges/permissions in
  FreeIPA, as well as the undercloud host entry. this requires
  'enable_tls_everywhere' to be set to true, and the following variables to be
  properly defined: 'freeipa_admin_password', 'freeipa_server_hostname',
  'overcloud_cloud_domain', 'undercloud_undercloud_hostname'. If you plan to do
  this yourself, you can set this variable to false. Defaults to true.
- `freeipa_admin_password`: The password for the admin principal for FreeIPA.
  This will be used to run the script to prepare FreeIPA for novajoin.
- `freeipa_server_hostname`: The hostname for the FreeIPA server.
  This will be used to run the script to prepare FreeIPA for novajoin.
- `overcloud_cloud_domain`: The domain configured for use by the FreeIPA server. Note: This also
  affects `CloudDomain` in the `cloud-names.yaml` template used by the `overcloud-deploy` role.

Role Network Variables
----------------------
- `undercloud_network_cidr`: <'192.168.24.0/24'> -- the network cidr for the undercloud, note this
also currently the default cidr used in other CI environments for tripleo.

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
