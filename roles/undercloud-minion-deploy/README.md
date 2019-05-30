undercloud-minion-deploy
==========================================

An Ansible role to execute the deployment of the tripleo undercloud minion

Requirements
------------

This requiest an existing undercloud deployed somewhere and another host
to deploy the minion on.

Role Variables
--------------

- `minion_templates_path`: <'/usr/share/openstack-tripleo-heat-templates'> --
a path to git clone and check-out t-h-t templates from the corresponding repo/branch/ref paths.
- `minion_config_file`: <'minion.conf.j2'> -- the name of the jinja template
used as the base for the minion.conf
- `minion_install_script`: <'minion-install.j2'> -- the name of the jinja template
used as the base for the minion-install bash script and dev envs hacking. Note, the
defaults imply the 'openstack minion install' command will be invoked. See the minion
deployment methods section below for the alternative modes.
- `minion_install_log`: <'{{ working_dir }}/minion_install.log'> -- the full path
to the minion install log file.
- `minion_hieradata_override`: <null> -- the name of a file containing overrides (hieradata or parameter defaults)
- `step_install_minion`: <'true'> -- turn on/off the minion deployment
- `minion_conf_extra`: <''> -- extra options to be added to ~/minion.conf
- `minion_extra_args`: <''> -- extra options for minion deploy command.
- `minion_install_cmd`: <'openstack minion install'> -- command used to install the minion
- `minion_install_cli_options`: <''> -- extra options for minion install command.
- `minion_enable_heat_engine`: <'true'> -- sets up the 'enable_heat_engine' option
  in minion.conf.
- `minion_enable_ironic_conductor`: <'false'> -- sets up the 'enable_ironic_conductor'
  option in minion.conf.
- `minion_cloud_domain`: The domain configured for use by containerized
  minion via the tripleo client's `--local-domain` option. It is unset by default.
- `local_docker_registry_host`: <`docker_registry_host`> -- registry host/port
  for containerized minion services. Defaults to the value provided for overcloud.
  You may want to diverge it, if building locally, or fetching from remote registries
  not fitting the overcloud deployment needs.
- `minion_container_images_file`: <""> --
  The environment file with default parameters for containers to use with
  minion install CLI. This should only be used to override image prepare
  generating this during the minion install.
- `minion_custom_env_files`: <null> --
  A space-separate string for custom t-h-t env files for `minion.conf` used with heat installer.
- `minion_minion_output_dir`: <null> -- allows customize output directory for state, like
  downloaded ansible configs and processed heat templates for heat installer
- `minion_minion_cleanup`: <null> -- controls tear down of the processed heat templates
- `minion_upgrade_cleanup`: <null> -- controls post upgrade cleanup after we containerize the minion.
- `update_containers`: <false> -- whether to update containers from the local registry.
- `minion_roles_data`: <null> -- A custom t-h-t roles file. Consumed from ``minion_templates_path``
  or an alternative location as well.
- `minion_selinux_enabled`: <'true'> -- Enabled for RHEL by default, Disabled for CentOS by default
- `minion_container_cli`: <'podman'> -- Container CLI to use for the Undercloud deployment. Default to 'podman'.

Role Network Variables
----------------------
- `minion_local_ip`: <hostvars['minion'].minion_ip> -- Sets up the `local_ip`
parameter from an inventory. Must be belonging to the `minion_network_cidr`. It is used
by overcloud nodes to access the minion node via a routable
[ctlplane network]((https://docs.openstack.org/developer/tripleo-docs/advanced_deployment/network_isolation).
Note that the minion.conf takes the default value based on the `minion_network_cidr`
instead.
- `minion_minion_nameservers`: <['8.8.8.8']> -- Sets up the 'minion_minion_nameservers'
from minion.conf. May be a string or a sequence. Only the last item goes for
the minion deploy command.
- `minion_minion_hostname`: Sets up the 'minion_hostname' value from minion.conf.
- `minion_resource_registry_args`: Complements 'resource_registry' for minion
  heat templates. Defaults to nothing.
- `minion_network_environment_args`: Complements Undercloud networking
  setup with the default parameters for heat templates (parameter_defaults).
- `minion_net_config_override`: <null> -- a j2 template for os-net-config
  used to override network configuration, which is normally defined via
  'OS::TripleO::Undercloud::Net::SoftwareConfig'. Accepts instack tags like LOCAL_IP et al.
  When it is defined, the ``minion_resource_registry_args`` value will be discarded.

Example Playbook
----------------

Sample playbook to call the role

```yaml
# Deploy the minion
- name:  Install minion
  hosts: minion
  gather_facts: false
  roles:
    - minion-deploy
```
