extras-common
=============

This Ansible role contains defaults for variables used in more than 2 roles
throughout the tripleo-quickstart-extras repository. All other roles in this
repository depend on this one.

Individual role variable defaults override the values from this role, so it is
important to remove their definitions from the original role defaults when
moving any variable over here.

This role depends on the "common" role from tripleo-quickstart repository which
serves the same purpose as this one.

Role Variables
--------------

- `containerized_overcloud: <false> -- use containers to deploy the overcloud
- `enable_tls_everywhere`: <false> -- enable TLS encryption on all OpenStack
  services
- `overcloud_ipv6`: <false> -- enable IPv6 deployment on the overcloud
- `undercloud_network_cidr`: <'192.168.24.0/24'> -- the network cidr for the
  undercloud, note this is also currently the default cidr used in other CI
  environments for tripleo.
- `timestamper_cmd`: beginning with the shell pipe character, this command
  prepends a timestamp to the deployment and test commands throughout the
  roles. Can be disabled by specifying this command as an empty string.
- `enable_libvirt_tripleo_ui`: <false> -- update the triple-ui javascript config
  for libvirt environments.
- `local_docker_registry_host`: <"{{undercloud_network_gateway|default(undercloud_network_cidr|nthhost(1))}}"> -- host of the local (undercloud) docker registry
- `docker_registry_host`: <'docker.io'> -- host of the primary docker registry
- `docker_registry_namespace`: <'tripleomaster'> -- namespace of
  docker images used for TripleO deployment
- `docker_image_tag`: <'latest'> -- tag of docker images used for
  TripleO deployment
- `composable_scenario`: <''> -- path to the composable scenarios used at deployment time
- `upgrade_composable_scenario`: <''> -- path to the composable scenarios used at upgrade time
- `undercloud_rpm_dependencies`: <'python-tripleoclient'> -- Dependency packages for undercloud deployments.
