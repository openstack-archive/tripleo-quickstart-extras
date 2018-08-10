set-libvirt-type
================

Set Libvirt type for overcloud deploy.
This Ansible role allows provisioning overcloud with nested kvm or qemu full
virtualization mode based on cpu and OS capabilities.

Requirements
------------

No requirements.

Role Variables
--------------

No variables.

Dependencies
------------

No dependencies.

Example Playbook
----------------

Including an example of how to use this role

    ---
    - name:  Set Libvirt type
      hosts: overcloud
      roles:
        - set-libvirt-type
      tags:
        - overcloud-deploy


License
-------

Apache 2.0

Author Information
------------------

OpenStack
