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
used as the base for the undercloud-install bash script and dev envs hacking. Note, the
defaults imply the 'openstack undercloud install' command will be invoked. See the undercloud
deployment methods section below for the alternative modes.
- `undercloud_install_log`: <'{{ working_dir }}/undercloud_install.log'> -- the full path
to the undercloud install log file.
- `undercloud_hieradata_override_file`: <'hieradata-overrides-classic-undercloud.yaml.j2'> -- the name of
jinja template used to override the undercloud's install hieradata. DEPRECATED. Use instead:
- `hieradata_override_file_classic_undercloud`: <hieradata-overrides-classic-undercloud.yaml.j2> --
the source template for hieradata overrides for instack-undercloud deployments.
- `hieradata_override_file_t_h_t_undercloud`: <hieradata-overrides-t-h-t-undercloud.yaml.j2> --
the source template for hieradata overrides for heat driven containerized undercloud deployments.
- `undercloud_ironic_ipxe_port`: <'3816'> -- port to use for httpd ipxe server
for ironic deploy
- `enable_vbmc`: <'true'> use a virtual bmc instead of pxe ssh
- `step_introspect`: <'false'> -- boolean value to enable/disable ironic introspection
- `bash_deploy_ramdisk`: <'false'> -- the variable allows older versions of tripleo to upload images
properly with the option --old-deploy-image
- `step_install_undercloud`: <'true'> -- turn on/off the undercloud deployment
- `libvirt_uri`: <'qemu:///session'> -- the URI used by libvirt, by default tripleo-quickstart uses
user sessions to provide greater flexixiblity to our users. ** additional documentation ** is at
https://docs.openstack.org/tripleo-quickstart/latest/accessing-libvirt.html
- `undercloud_conf_extra`: <''> -- extra options to be added to ~/undercloud.conf
- `undercloud_extra_args`: <''> -- extra options for undercloud deploy command.
- `undercloud_install_cli_options`: <''> -- extra options for undercloud install command.
- `undercloud_enable_mistral`: <'true'> -- sets up the 'enable_mistral' option
  in undercloud.conf.
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
- `undercloud_enable_novajoin`: <'false'> -- sets up the 'enable_novajoin'
  value from undercloud.conf. Note that using 'enable_tls_everywhere' will have
  the same effect.
- `novajoin_connect_timeout`: <5> Sets vendordata_dynamic_connect_timeout when novajoin is enabled
- `novajoin_read_timeout:` <20> Sets vendordata_dynamic_read_timeout when novajoin is enabled
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
- update_containers: <false> -- whether to update containers from the local registry.
- `undercloud_enable_tempest`: <null> -- The tempest container will be available on the undercloud.
- `undercloud_roles_data`: <null> -- A custom t-h-t roles file (the path must be relative to
   ``overcloud_templates_path``).

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
- `undercloud_resource_registry_args`: Sets up network config for Undercloud
  (resource_registry for heat templates). Defaults to Noop.
- `undercloud_network_environment_args`: Complements Undercloud networking
  setup with the default parameters for heat templates (parameter_defaults).
- `undercloud_net_config_override`: <null> -- a j2 template for os-net-config
  used to override network configuration. Accepts instack tags like LOCAL_IP et al.

Undercloud deployment methods
-----------------------------

By default, the undercloud uses ``openstack undercloud install`` command,
`{{working_dir}}/undercloud.conf` config and the file coming from the
``hieradata_override_file_classic_undercloud`` variable to set the hieradata
overrides that will be used for the puppet deployment.

However, there exists more methods for setting up the undercloud based on
containers with the ``openstack undercloud install --use-heat`` and
``openstack undercloud deploy`` commands. Both methods are based on
tripleo-heat-templates. The former one provides the instack compatible
`undercloud.conf` format. It may be requested via settings:
```
undercloud_install_cli_options: --use-heat
undercloud_install_script: undercloud-install.sh.j2
```
And the latter deployment method is more "free to go". It can be
enabled with:
```
containerized_undercloud: true
undercloud_install_script: undercloud-deploy.sh.j2
```
For these cases, hiera override data is consumed from
``hieradata_override_file_t_h_t_undercloud``.

Note, the containerized undercloud is a hacking mode for developers, that allows
to test containerized components undercloud, with custom, like very minimal,
setup layouts. Please do not expect more than that when using it.

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

Containerized dev environments (experimental feature)
-----------------------------------------------------

Firstly, update or create a custom undercloud install script template. It can be
found under the locally checked out tripleo-quickstart-extra repo (or at a remote
host, if you prefer to apply ansible playbooks from a non local virthost). The
template is located by the
`roles/undercloud-deploy/templates/undercloud-deploy-my-dev.sh.j2` path.
Once changes are done, update the ``undercloud_install_script`` var, like:

```yaml
undercloud_install_script: undercloud-deploy-dev.sh.j2
```

or use the updated template:
```
undercloud_install_script: undercloud-deploy.sh.j2
```

Note, it is important to change the default value for the ``undercloud_install_script``
to switch from the classic 'install' to the experimental 'deploy' method.

Secondly, you may want to refer an unpackaged t-h-t change refspec or a dev
branch. To do so, override the custom t-h-t repo and branch/refspec
for t-h-t templates to be fetched, for example:

```yaml
overcloud_templates_repo: https://github.com/johndoe/tripleo-heat-templates
overcloud_templates_branch: dev
```

Note, these vars are shared with the overcloud role vars and point to
the same templates path, branch/refspec and repo. The templates path should be
R/W accessible by the given `non_root_user` without sudoing. So it is better
off using the home dir or tmp dirs with sticky bits.

Also note that you should normaly rely on the openstack-tripleo-heat-templates
package. The custom t-h-t repo vars may break that package and should be used with
caution.

Note, checkout/install steps for the remaining yet unpackaged custom changes
like dev branches for puppet modules, tripleo client, heat agent hooks, need
to be covered in the custom ``undercloud-install.sh`` script body (rendered
from a given in the ``undercloud_install_script`` template file name).

The last step is to define the ``undercloud_extra_args`` as needed. For
example you may want to deploy:

 * an optional non containerized Octavia,
 * containerized Keystone,
 * optional containerized Etcd,

with disabled telemetry, default docker images from `docker.io` namespace,
debug logs for services and puppet, given a decent timeout, and keeping
the ephemeral undercloud heat agent running for debug purposes:

```yaml
undercloud_custom_env_files: >-
  {{overcloud_templates_path}}/environments/disable-telemetry.yaml
  {{overcloud_templates_path}}/environments/docker-minimal.yaml
  {{overcloud_templates_path}}/environments/services/etcd.yaml
  {{overcloud_templates_path}}/environments/services/octavia.yaml
  {{overcloud_templates_path}}/environments/debug.yaml
  {{overcloud_templates_path}}/environments/config-debug.yaml
undercloud_extra_args: >-
  --timeout 60
```

Where the t-h-t's `environments/docker-minimal.yaml` is like:

```
resource_registry:
  OS::TripleO::Services::Docker: ../puppet/services/docker.yaml
  OS::TripleO::Services::Keystone: ../docker/services/keystone.yaml
  OS::TripleO::PostDeploySteps: ../docker/post.yaml
  OS::TripleO::PostUpgradeSteps: ../docker/post-upgrade.yaml
  OS::TripleO::Services: ../docker/services/services.yaml

parameter_defaults:
  DockerNamespace: tripleomaster
  ComputeServices: {}
  SwiftCeilometerPipelineEnabled: false
```

Note, this template complements the default t-h-t's `environments/docker.yaml`
setup that deploys everything in containers. The default template for
the ``undercloud-install.sh`` also provides an additional set of required
services used for underlcoud to deploy overclouds (Ironic, Zaqar, MongoDB,
Mistral). If you need a lightweight undercloud, make sure your custom
undercloud installation script template omits those services and the
`environments/docker.yaml` defaults.

You may also override ``undercloud_roles_data`` with a custom roles file
(the path must be relative to the t-h-t templates ``overcloud_templates_path``).
For the example above, custom undercloud roles may look like:

```
- name: Undercloud
  CountDefault: 1
  disable_constraints: True
  tags:
    - primary
    - controller
  ServicesDefault:
    - OS::TripleO::Services::Etcd
    - OS::TripleO::Services::Keystone
    - OS::TripleO::Services::OctaviaApi
    - OS::TripleO::Services::OctaviaHealthManager
    - OS::TripleO::Services::OctaviaHousekeeping
    - OS::TripleO::Services::OctaviaWorker
```

And an example playbook to call the role is:

```yaml
# Deploy the undercloud
- name:  Deploy undercloud (experimental)
  hosts: undercloud
  gather_facts: no
  vars:
    containerized_undercloud: true
    undercloud_install_script: undercloud-deploy.sh.j2
    overcloud_templates_repo: https://github.com/johndoe/tripleo-heat-templates
    overcloud_templates_branch: dev
    undercloud_custom_env_files: >-
      {{overcloud_templates_path}}/environments/disable-telemetry.yaml
      {{overcloud_templates_path}}/environments/docker-minimal.yaml
      {{overcloud_templates_path}}/environments/services/etcd.yaml
      {{overcloud_templates_path}}/environments/services/octavia.yaml
      {{overcloud_templates_path}}/environments/debug.yaml
      {{overcloud_templates_path}}/environments/config-debug.yaml
    undercloud_extra_args: >-
      --timeout 60
  roles:
    - undercloud-deploy
```
