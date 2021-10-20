undercloud-deploy
==========================================

An Ansible role to execute the deployment of the tripleo undercloud

Requirements
------------

This requires a running host to deploy the undercloud.

Role Variables
--------------

- `undercloud_templates_path`: <'/usr/share/openstack-tripleo-heat-templates'> --
a path to git clone and check-out t-h-t templates from the corresponding repo/branch/ref paths.
- `undercloud_config_file`: <'undercloud.conf.j2'> -- the name of the jinja template
used as the base for the undercloud.conf
- `undercloud_install_log`: <'{{ working_dir }}/undercloud_install.log'> -- the full path
to the undercloud install log file.
- `undercloud_hieradata_override_file`: <'hieradata-overrides-classic-undercloud.yaml.j2'> -- the name of
jinja template used to override the undercloud's install hieradata. DEPRECATED. Use instead:
- `hieradata_override_file_t_h_t_undercloud`: <hieradata-overrides-t-h-t-undercloud.yaml.j2> --
the source template for hieradata overrides for heat driven containerized undercloud deployments.
- `undercloud_ironic_ipxe_port`: <'3816'> -- port to use for httpd ipxe server
for ironic deploy
- `enable_vbmc`: <'true'> use a virtual bmc instead of pxe ssh
- `step_introspect`: <'false'> -- boolean value to enable/disable ironic introspection
- `step_install_undercloud`: <'true'> -- turn on/off the undercloud deployment
- `libvirt_uri`: <'qemu:///session'> -- the URI used by libvirt, by default tripleo-quickstart uses
user sessions to provide greater flexixiblity to our users. ** additional documentation ** is at
https://docs.openstack.org/tripleo-quickstart/latest/accessing-libvirt.html
- `undercloud_conf_extra`: <''> -- extra options to be added to ~/undercloud.conf
- `undercloud_extra_args`: <''> -- extra options for undercloud deploy command.
- `undercloud_enable_monitoring`: <'false'> -- sets up the 'enable_monitoring'
  option in undercloud.conf.
- `undercloud_enable_telemetry`: <'true'> -- sets up the 'enable_telemetry'
  option in undercloud.conf.
- `undercloud_enable_tempest`: <'true'> -- sets up the 'enable_tempest' option
  in undercloud.conf.
- `undercloud_enable_ui`: <'true'> -- sets up the 'enable_ui' option in
  undercloud.conf.
- `undercloud_enable_validations`: <'true'> -- sets up the 'enable_validations'
  option in undercloud.conf.
- `undercloud_enable_novajoin`: <'true'> -- sets up the 'enable_novajoin'
  value from undercloud.conf when 'enable_tls_everywhere' is enabled.
- `novajoin_connect_timeout`: <5> Sets vendordata_dynamic_connect_timeout when novajoin is enabled
- `novajoin_read_timeout:` <20> Sets vendordata_dynamic_read_timeout when novajoin is enabled
- `prepare_ipa`: If set to true, it will install novajoin or tripleo-ipa in the
  undercloud, and run a script that will create the required privileges/permissions
  in FreeIPA, as well as the undercloud host entry. This requires
  'enable_tls_everywhere' to be set to true, and the following variables to be
  properly defined: 'freeipa_admin_password', 'freeipa_server_hostname',
  'overcloud_cloud_domain', 'undercloud_undercloud_hostname'. If you plan to do
  this yourself, you can set this variable to false. Defaults to true.
- `freeipa_admin_password`: The password for the admin principal for FreeIPA.
  This will be used to run the script to prepare FreeIPA for novajoin.
- `freeipa_server_hostname`: The hostname for the FreeIPA server.
  This will be used to run the script to prepare FreeIPA for novajoin.
- `overcloud_cloud_domain`: The domain configured for use by the overcloud
  nodes. If TLS everywhere is enabled, this will also be the domain used by
  FreeIPA. This sets up the 'overcloud_domain_name' configuration option in
  undercloud.conf . Note: This also affects `CloudDomain` in the
  `cloud-names.yaml` template used by the `overcloud-deploy` role.
- `undercloud_cloud_domain`: The domain configured for use by containerized
  undercloud via the tripleo client's `--local-domain` option. It is unset by default.
- `tripleo_ui_secure_access`: Defaults to false due to the self signed certificate and
  usability issues. See the tripleo-quickstart documentation `accessing the undercloud` for details.
- `local_docker_registry_host`: <`docker_registry_host`> -- registry host/port
  for containerized undercloud services. Defaults to the value provided for overcloud.
  You may want to diverge it, if building locally, or fetching from remote registries
  not fitting the overcloud deployment needs.
- `undercloud_container_images_file`: <""> --
  The environment file with default parameters for containers to use with
  undercloud install CLI. This should only be used to override image prepare
  generating this during the undercloud install.
- `undercloud_custom_env_files`: <null> --
  A space-separate string for custom t-h-t env files for `undercloud.conf` used with heat installer.
- `undercloud_undercloud_output_dir`: <null> -- allows customize output directory for state, like
  downloaded ansible configs and processed heat templates for heat installer
- `undercloud_undercloud_cleanup`: <null> -- controls tear down of the processed heat templates
- `undercloud_upgrade_cleanup`: <null> -- controls post upgrade cleanup after we containerize the undercloud.
- `update_containers`: <false> -- whether to update containers from the local registry.
- `undercloud_enable_tempest`: <null> -- The tempest container will be available on the undercloud.
- `undercloud_roles_data`: <null> -- A custom t-h-t roles file. Consumed from ``undercloud_templates_path``
  or an alternative location as well.
- `undercloud_selinux_enabled`: <'true'> -- Enabled for RHEL by default, Disabled for CentOS by default
- `undercloud_enable_paunch`: <null> -- Enable or disable Paunch to manage containers. Undefined by default.
- `undercloud_container_cli`: <'podman'> -- Container CLI to use for the Undercloud deployment. Default to 'podman'.

Role Network Variables
----------------------
- `undercloud_network_cidr`: <'192.168.24.0/24'> -- the network cidr for the undercloud, note this
also currently the default cidr used in other CI environments for tripleo.
- `undercloud_network_gateway`: <a 1st host of the `undercloud_network_cidr`> -- Sets up the
`undercloud_network_gateway` parameter from undercloud.conf.
- `undercloud_local_ip`: <hostvars['undercloud'].undercloud_ip> -- Sets up the `local_ip`
parameter from an inventory. Must be belonging to the `undercloud_network_cidr`. It is used
by overcloud nodes to access the undercloud node via a routable
[ctlplane network]((https://docs.openstack.org/developer/tripleo-docs/advanced_deployment/network_isolation).
Note that the undercloud.conf takes the default value based on the `undercloud_network_cidr`
instead.
- `undercloud_undercloud_public_host`: <a 2nd host of the `undercloud_network_cidr`> -- Sets
up the 'undercloud_public_host' parameter from undercloud.conf. It is also used by overcloud
nodes to access the undercloud node via a VIP/hostname that resolves to a routable IP address.
- `undercloud_undercloud_admin_host`: <a 3rd host of the `undercloud_network_cidr`> -- Sets
up the 'undercloud_admin_host' from undercloud.conf.  Note, use the `undercloud_admin_vip`
instead for Mitaka/Newton releases.
- `undercloud_dhcp_start`: <a 5th host of the `undercloud_network_cidr`> -- Sets
up the 'undercloud_dhcp_start' from undercloud.conf.
- `undercloud_dhcp_end`: <a 30th host of the `undercloud_network_cidr`> -- Sets
up the 'undercloud_dhcp_end' from undercloud.conf.
- `undercloud_undercloud_nameservers`: <['8.8.8.8']> -- Sets up the 'undercloud_undercloud_nameservers'
from undercloud.conf. May be a string or a sequence. Only the last item goes for
the undercloud deploy command.
- `undercloud_undercloud_hostname`: Sets up the 'undercloud_hostname' value from undercloud.conf.
Note, use the `undercloud_public_vip` instead for Mitaka/Newton releases.
- `undercloud_heat_public_endpoints`: <'false'> -- when the ctlplane network is not routable
from overcloud nodes, for example pre-provisioned
[deployed servers](https://docs.openstack.org/developer/tripleo-docs/advanced_deployment/deployed_server.html#undercloud),
the ``undercloud deploy --local_ip`` (and `local_ip` in the undercloud.conf)
may not be used. Enable this variable instead. Doing so changes the heat endpoint
type from the default internal to public and changes the signaling method to use
TempURLs from OpenStack Object Storage (swift).
- `undercloud_resource_registry_args`: Complements 'resource_registry' for undercloud
  heat templates. Defaults to nothing.
- `undercloud_network_environment_args`: Complements Undercloud networking
  setup with the default parameters for heat templates (parameter_defaults).
- `undercloud_net_config_override`: <null> -- a j2 template for os-net-config
  used to override network configuration, which is normally defined via
  'OS::TripleO::Undercloud::Net::SoftwareConfig'. Accepts instack tags like LOCAL_IP et al.
  When it is defined, the ``undercloud_resource_registry_args`` value will be discarded.

Undercloud deployment methods
-----------------------------

The undercloud uses ``openstack undercloud install`` command,
`{{working_dir}}/undercloud.conf` config and the file coming from the
``hieradata_override_file_t_h_t_undercloud`` variable to set the hieradata
overrides that will be used for the containerized undercloud deploy.


Example Playbook
----------------

Sample playbook to call the role

```yaml
# Deploy the undercloud
- name:  Install undercloud
  hosts: undercloud
  gather_facts: false
  roles:
    - undercloud-deploy
```
``
