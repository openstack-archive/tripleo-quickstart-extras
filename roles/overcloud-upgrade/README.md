overcloud-upgrade
=================

This role aim to upgrade an existing Tripleo deployment, Undercloud and
Overcloud from the deployed version to the next version, major or minor version.
It supports upgrade for:
Liberty (major and minor)
Mitaka (major and minor)
Newton (major only)

It provides a set of tools and scripts to upgrade, the undercloud or the
overcloud or both.
Both upgrade workflow are supported, the legacy upgrade workflow and the
composable upgrade workflow.

Requirements
------------

This role can be used on top of an existing Overcloud deployment.
You just need to provide the required inventory file (see tests/ for more
details).

Composable Upgrade
------------------

The composable upgrade workflow has been implemented on Ocata release, for doing
major upgrade from Newton to Ocata.
This workflow aims to be more flexible than the previous one and decrease the
number of steps to be applied by the operator.
Also, it's using Ansible tasks to upgrade the services on the Overcloud nodes.

The workflow provides two possible methods for upgrading the Overcloud:
 * all-in-one step (mostly made for CI)
 * main upgrade steps and a converge step.
The goal of the second method is to give the option to the operator to not
upgrade all nodes in one shot. Then, it is possible to not stop the cloud and to
migrate the workload from one compute to another.

The upgrade step is done in major-upgrade-overcloud.sh.j2
(see lines below "execute overcloud upgrade"). This step allows
the user to provide custom environment files for the heat stack update.
The main point is that you can provide a custom file with only the
services that you want to deploy and upgrade
(see: tripleo-quickstart/config/general_config/composable_upgrade.yml)
For example, if you want to test the upgrade with only Neutron and Keystone
services, you just have to provide the extra file to your Ansible command
with this yaml:

    overcloud_services:
      - name: 'ControllerServices:'
        services:
        - OS::TripleO::Services::CACerts
        - OS::TripleO::Services::Core
        - OS::TripleO::Services::Kernel
        - OS::TripleO::Services::Keystone
        - OS::TripleO::Services::NeutronDhcpAgent
        - OS::TripleO::Services::NeutronL3Agent
        - OS::TripleO::Services::NeutronMetadataAgent
        - OS::TripleO::Services::NeutronServer
        - OS::TripleO::Services::NeutronCorePlugin
        - OS::TripleO::Services::NeutronOvsAgent
        - OS::TripleO::Services::MySQL
        - OS::TripleO::Services::RabbitMQ
        - OS::TripleO::Services::HAproxy
        - OS::TripleO::Services::Keepalived
        - OS::TripleO::Services::Memcached
        - OS::TripleO::Services::Ntp
        - OS::TripleO::Services::Timezone
        - OS::TripleO::Services::TripleoPackages
        - OS::TripleO::Services::TripleoFirewall

Legacy Upgrade Workflow
-----------------------

The legacy workflow supports Liberty to Mitaka, and Mitaka to Newton, upgrade.
It is composed of three main steps:
1. script delivery
2. controller upgrade
3. converge step

and few extras steps for upgrading Block Storage, Compute and Ceph nodes.

From Liberty to Mitaka, we need to apply two pre-upgrade steps to migrate Aodh
and Keystone. (see major-upgrade-overcloud.sh.j2 - lines following "execute aodh upgrade")

From mitaka to Newton, we need to apply one pre-upgrade step to migrate
Ceilometer Alarm: major-upgrade-ceilometer-wsgi-mitaka-newton.yaml
(see major-upgrade-overcloud.sh.j2- lines following "execute ceilometer migration")

The Block Storage should be upgraded before the Controller step, and the
Compute and Ceph nodes should be upgraded after the Controller step and before
the converge step.


Role Variables
--------------

Below are the default parameters for the overcloud upgrade role:

```
# pre upgrade settings:
oc_dns_server: 192.168.122.1
# set-repo settings:
target_upgrade_version: master
delorean_hash: current-passed-ci
repos:
  - delorean.repo
  - delorean-deps.repo
yum_repo_path: /etc/yum.repos.d/
# Url of the delorean repos:
repos_url:
  - https://trunk.rdoproject.org/centos7-{{ target_upgrade_version }}/{{ delorean_hash | default('current-passed-ci')}}/delorean.repo
  - https://trunk.rdoproject.org/centos7-{{ target_upgrade_version }}/delorean-deps.repo
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
