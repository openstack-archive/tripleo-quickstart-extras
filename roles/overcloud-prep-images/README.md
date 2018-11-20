Role Name
=========

An Ansible role to copy configuration files to the undercloud prior to deployment.

Requirements
------------

This  playbook expects that the undercloud has been installed and setup using one of the roles relevant to baremetal overcloud deployments.

Role Variables
--------------

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/sect-Scaling_the_Overcloud.html).

- working_dir: <'/home/stack'> -- working directory for the role. Assumes stackrc file is present at this location
- baremetal_instackenv: <"{{ working_dir }}/instackenv.json"> -- location of instackenv.json to copy over
- baremetal_network_environment: <"{{ working_dir }}/network-isolation.yml"> -- location of network-environment file to copy over
- undercloud_type: <virtual> -- can be overwritten with values like 'baremetal' or 'ovb'
- step_root_device_size: <false> -- add disk size hints if needed for the environment under test
- disk_root_device_size: <1843> -- size hint for selecting the correct disk during introspection
- step_root_device_hints: false -- add root device hints if needed for the environment under test
- root_device_hints: [] -- list of the root device hints to be associated with nodes. Needs to have this format::

    - root_device_hints:
        - ip: <<pm_addr>>
          key: <<string>>
          value: <<string>>

  Where key needs to be one of the valid Ironic root device hints, and value is the exact value that needs to be filtered.
  For reference on all the possible root device hints see ``http://docs.openstack.org/project-install-guide/baremetal/draft/advanced.html#specifying-the-disk-for-deployment-root-device-hints``.
  Please note that in order to match root device hints with the associated nodes on `instackenv.json`,
  the node `pm_address` will be used as a key.
  At the moment only equal operator is supported, is not possible to use other operators or logical combinations.
- whole_disk_images: false -- shows if we want to use partition or whole disk images (this will be available starting on Ocata)
- step_introspect_with_retry: <false> -- a more robust version of the step_introspect option

Dependencies
------------

This playbook does not deploy the overcloud. After this playbook runs, call https://github.com/redhat-openstack/ansible-role-tripleo-overcloud.

Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Copy configuration files
      hosts: virthost
      gather_facts: false
      roles:
        - ansible-role-tripleo-overcloud-prep-config

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team

