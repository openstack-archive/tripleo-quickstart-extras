Role Name
=========

An Ansible role for aggregating logs.

Requirements
------------

This role assumes it will be executed against OpenStack systems deployed using
C.A.T..

Role Variables
--------------

TBD

Dependencies
------------

TBD

Example Playbook
----------------

    ----
    - name: Gather logs
      hosts: all:!localhost
      roles:
        - ansible-role-tripleo-collect-logs

License
-------

Apache

Author Information
------------------

RDO-CI Team