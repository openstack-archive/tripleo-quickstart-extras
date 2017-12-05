create-reproducer-script
========================

This role creates a script to reproduce OVB and multinode jobs.

Role Variables
--------------

For the defaults of these variables, see the defaults/main.yml file in this role.

* env_vars_to_source_file: env_vars_to_src.sh
* reproducer_quickstart_script: reproducer-quickstart.sh.j2
From the extras-common role:
* artcl_collect_dir: "{{ local_working_dir }}/collected_files"

Dependencies
------------

The role is run within the collect-logs role.

Example Playbook
----------------

```yaml
---
- name: Create a file to reproduce the job
  hosts: localhost
  roles:
    - create-reproducer-script
```

License
-------

Apache 2.0

Author Information
------------------

OpenStack
