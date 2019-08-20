validate-minion
===============

A basic role to validate that a minion is correctly reporting into the undercloud.

Requirements
------------

N/A

Role Variables
--------------

- `validate_minion_heat_engine`: <'true'> -- Should the heat-engine service be checked
- `validate_minion_ironic_conductor`: <'false'> -- Should the ironic-conductor service be checked
- `validate_minion_simple_script`: <'validate_minion_simple.sh.j2'> -- Simple validation script source
- `validate_minion_simple_log`: <'False'> -- Log file for the validations
- `undercloud_user`: <'stack'> -- User that the undercloud was installed under.

Dependencies
------------

N/A

Example Playbook
----------------

    - name: Validate minion
      hosts: undercloud
      vars:
        validate_minion_heat_engine: true
        validate_minion_ironic_conductor: true
      roles:
        - validate-minion

License
-------

Apache
