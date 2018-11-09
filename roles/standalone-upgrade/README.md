Standalone Upgrade
===================

An Ansible role to upgrade the Standalone ( all-in-one ) deployment of TripleO

Requirements
------------

An existing standalone deployment.

Role Variables
--------------

- standalone_config: <'standalone_config.yaml.j2'> -- jinja template of the upgrade configuration
- standalone_network: <'192.168.24'> -- First three octets of the network used
- standalone_network_prefix: <'24'> --  The subnet size for the standalone deployment network
- standalone_ip: <'192.168.24.1'> --  The IP address of the standalone upgrade
- standalone_interface: <'br-ex'> --  The interface for the standalone upgrade

- standalone_container_prep_options: <''> -- additional parameters for the container prep command
- standalone_container_prep_script: <'standalone-container-prep.sh.j2'> -- The script name use to perform container prep actions
- standalone_container_prep_log: <'standalone_container_prep_upgrade.log'> --  The log of the container prepa actions during upgrade

- standalone_upgrade_script: <'standalone.sh.j2'> -- The script name use to upgrade the standalone server
- standalone_upgrade_log: <'standalone_deploy.log'> --  The log of the upgrade

- standalone_role: <'Standalone.yaml'> -- The TripleO Heat Template role definition of the deployment

- standalone_libvirt_type: <'kvm'> -- The type of libvirt to run on the standalone (qemu|kvm)

- standalone_selinux_mode: <'permissive'> -- The selinux mode to use.

- standalone_custom_env_files: <'[]'> -- list of additional environment files to be added to the deployment command (do not include the -e)

Dependencies
------------

The dependencies documented for TripleO Quickstart and TripleO
