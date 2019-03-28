check-to-build-or-not-to-build
==============================

An Ansible role created from the original playbook
to decide whether we need to build images. The role
was created to allow this functionality to run on
hosts other than the undercloud.

This output of this role is a to_build variable,
that is set to true or false to make image build and
other related workflow decisions in later steps.

Role Variables:
---------------
* ` default_projects_need_build_list` -- list of repos can affect the image building itelf

Example Usage
-------------

```yaml
---
- name: Decide whether we need to build images
  hosts: undercloud
  tasks:
    - include_role:
         name: check-to-build-or-not-to-build
```

License
-------

Apache
