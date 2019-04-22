create-zuul-based-reproducer
============================

This role creates a launcher-playbook and a wrapper Bash script to
allow users to reproduce CI jobs using a local Zuul installation.

Role Variables
--------------

For the defaults of these variables, see the defaults/main.yml file in this role.

* reproducer_zuul_based_quickstart_script: Bash script to kick the generated launcher playbook
* reproducer_zuul_based_quickstart_readme_file: The documentation file with user instructions
* reproducer_zuul_based_launcher_playbook: Template to create a launcher playbook with variable
to reproduce the job run
* launcher_env_setup_playbook: Template to create a playbook to set up the launcher environment
From the extras-common role:
* artcl_collect_dir: "{{ local_working_dir }}/collected_files"

Dependencies
------------

The role is run within the collect-logs role.

Example Playbook
----------------

This role generates a launcher-playbook:

- hosts: localhost
  tasks:
    - name: Add the localhost to the inventory
      add_host:
        name: "localhost"
        groups: "localhost"
        ansible_host: 127.0.0.1
        ansible_connection: local

    - name: Add the primary to the inventory
      add_host:
        name: "localhost"
        groups: "primary"
        ansible_fqdn: "localhost"
        ansible_user: "{{ lookup('env', 'USER') }}"
        ansible_private_key_file: "/home/{{ ansible_user }}/.ssh/{{ user_pri_key | default('id_rsa') }}"
        ansible_host: "localhost"

- import_playbook: playbooks/pre.yaml

- hosts: localhost
  vars:
    depends_on:
      - https://review.opendev.org/xxxxxx
    zuul_yaml: >-
      - project:
          check:
            jobs:
              - tripleo-ci-centos-7-multinode-1ctlr-featureset010-dlrn-hash-tag

      - job:
          name: tripleo-ci-centos-7-multinode-1ctlr-featureset010-dlrn-hash-tag
          parent: tripleo-ci-centos-7-multinode-1ctlr-featureset010
          vars:
            mirror_fqdn: mirror.regionone.rdo-cloud.rdoproject.org
            featureset_override:
              dlrn_hash_tag:
                8127e43f39ac9b9e14d4a5a10bcbf41f122f32d7_d2efe5df
              dlrn_hash_tag_newest:
                ca4990cebac0be87ee4a7273f519574bc1027c8f_a1ff18dc
  tasks:
    - include_role:
        name: ansible-role-tripleo-ci-reproducer


License
-------

Apache 2.0

Author Information
------------------

OpenStack
