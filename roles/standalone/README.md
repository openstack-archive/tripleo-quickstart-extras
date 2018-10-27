Standalone
===================

An Ansible role to deploy the Standalone ( all-in-one ) deployment of TripleO

Requirements
------------

This role expects the requirements for deploying a TripleO undercloud to be met.
For example python-tripleoclient is installed and hardware requirements met.

Role Variables
--------------

- standalone_config: <'standalone_config.yaml.j2'> -- jinja template of the deployment configuration
- standalone_network: <'192.168.24'> -- First three octets of the network used
- standalone_network_prefix: <'24'> --  The subnet size for the standalone deployment network
- standalone_ip: <'192.168.24.1'> --  The IP address of the standalone deployment
- standalone_interface: <'br-ex'> --  The interface for the standalone deployment

- standalone_container_prep_options: <''> -- additional parameters for the container prep command
- standalone_container_prep_script: <'standalone-container-prep.sh.j2'> -- The script name use to perform container prep actions
- standalone_container_prep_log: <'standalone_container_prep.log'> --  The log of the container prepa ctions

- standalone_deploy_script: <'standalone.sh.j2'> -- The script name use to deploy the standalone server
- standalone_deploy_log: <'standalone_deploy.log'> --  The log of the deployment
- standalone_ansible_lint_log: <'standalone_ansible_lint.log'> -- The ansible lint output

- standalone_role: <'Standalone.yaml'> -- The TripleO Heat Template role definition of the deployment

- standalone_libvirt_type: <'kvm'> -- The type of libvirt to run on the standalone (qemu|kvm)

- standalone_selinux_mode: <'permissive'> -- The selinux mode to use.

- standalone_ansible_lint: <'false'> -- Perform ansible lint on the generated ansible playbooks

Dependencies
------------

The dependencies documented for TripleO Quickstart and TripleO
