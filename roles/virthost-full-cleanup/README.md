Role Name
=========

This role, virthost-full-cleanup, will remove any known tripleo related rpms
from the system and remove libvirt.  This role is destructive and will remove ALL libvirt guests.  This is done to ensure a clean starting point for deployments.

Requirements
------------



Role Variables
--------------



Dependencies
------------

Example:
----------------
./deploy.sh -c -p cleanup-destructive <testbox>


License
-------

Apache 2.0

Author Information
------------------
