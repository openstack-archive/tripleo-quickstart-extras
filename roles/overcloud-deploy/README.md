Role Name
=========

ansible-role-tripleo-overcloud

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

* `overcloud_ipv6`: enables IPv6 deployment on the overcloud
* `enable_cinder_backup`: false/true - enables cinder-backup service.
* `deployed_server`: false/true - enables support for nodepool deployed server deployment (default: false)
* `overcloud_cloud_name`: Sets the FQDN for the overcloud's public VIP.
* `overcloud_cloud_name_internal`: Sets the FQDN for the overcloud's VIP for the internal network.
* `overcloud_cloud_name_storage`: Sets the FQDN for the overcloud's VIP for the storage network.
* `overcloud_cloud_name_storage_management`: Sets the FQDN for the overcloud's VIP for the storage management network.
* `overcloud_cloud_name_ctlplane`: Sets the FQDN for the overcloud's VIP for the ctlplane network.
* `overcloud_cloud_domain`: Sets the domain for the nodes' internal hostnames.
* `enable_swap`: Enables swap in the overcloud nodes.
* `swap_type`: Defines the approach to adding swap that will be used, the
  available options are 'file' and 'partition'. Defaults to 'file'.
* `composable_services`: false/true - whether to use customized list of services
* `overcloud_services`: structure specifying services for roles. See
  the overcloud-deploy role's defaults.yaml file for an example.
* `composable_roles`: false/true - whether to use custom `roles_data.yaml`
* `overcloud_roles`: contents of custom `roles_data.yaml` (as a YAML
  structure, not a string). See `roles_data.yaml` in the
  tripleo-heat-templates repository for example contents.
* `tripleo_config_download_log`: Sets the TripleO config-download log file path.
* `ansible_steps_log`: Sets the TripleO Ansible steps log file path.
* `config_download_args`: Sets the arguments to load config-download
  environment in THT.
* `step_tripleo_config_download`: false/true - whether to enable config-download.
* `deploy_steps_ansible`: false/true - whether to deploy the overcloud with
  config-download Ansible steps.


Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
