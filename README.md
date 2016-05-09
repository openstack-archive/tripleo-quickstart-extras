Role Name
=========

This role, ansible-role-tripleo-cleanup-nfo (nuke from orbit) will remove any known tripleo related rpms
from the system and remove libvirt.  This role is destructive and will remove ALL libvirt guests.  This is done to ensure a clean starting point when using potentially dirty test boxes.

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

BSD

Author Information
------------------
