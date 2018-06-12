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
- standalone_ip: <'192.168.24.1'> --  The IP address of the standalone deployment
- standalone_interface: <'eth1'> --  The interface for the standalone deployment

- standalone_deploy_script: <'standalone.sh.j2'> -- The script name use to deploy the standalone server
- standalone_deploy_log: <'standalone_deploy.log'> --  The log of the deployment

- standalone_role: <'Standalone.yaml'> -- The TripleO Heat Template role definition of the deployment

Dependencies
------------

The dependencies documented for TripleO Quickstart and TripleO