Ansible-role-tripleo-overcloud-upgrade
======================================

Requirements
------------

This role can be used on top of an existing Overcloud deployment.
You just need to provide the required inventory file (see tests/ for more
details).

Role Variables
--------------

Here is the default parameters for overcloud upgrade role:

```
# pre upgrade settings:
oc_dns_server: 192.168.122.1
# set-repo settings:
target_upgrade_version: mitaka
delorean_hash: current-passed-ci
repos:
  - delorean.repo
  - delorean-deps.repo
yum_repo_path: /etc/yum.repos.d/
# Url of the delorean repos:
repos_url:
  - http://trunk.rdoproject.org/centos7-{{ target_upgrade_version }}/{{ delorean_hash | default('current-passed-ci')}}/delorean.repo
  - http://trunk.rdoproject.org/centos7-{{ target_upgrade_version }}/delorean-deps.repo
```

Dependencies
------------

Depends on:
Tripleo-quickstart:
https://github.com/redhat-openstack/tripleo-quickstart.git
Ansible-role-tripleo-overcloud:
https://github.com/redhat-openstack/ansible-role-tripleo-overcloud.git


Example Playbook
----------------

```
- name:  Upgrade overcloud
  hosts: undercloud
  gather_facts: no
  become: yes
  roles:
    - ansible-role-tripleo-overcloud-upgrade
```

License
-------

Apache

Author Information
------------------

mbultel@redhat.com
