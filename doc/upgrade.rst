Tripleo - Upgrades
===================

This document describe how to handle the Upgrade role with Ansible.
The source of the Ansible role are located here:

    https://github.com/redhat-openstack/ansible-role-tripleo-overcloud-upgrade.git

Requirements
------------

In order to use the Upgrade role, you need to have:
  - a working Tripleo environment (undercloud and overcloud successful deployed)
  - a Ansible hosts file populated with the right access to the undercloud

Playbook
--------

The call of the role in the playbook should like this:

    ---
    - name:  Upgrade Tripleo
      hosts: undercloud
      gather_facts: no
      roles:
        - { role: ansible-role-tripleo-overcloud-upgrade }

You can specified which step you want to run or not. With this example you won't
execute the pre tasks for undercloud and overcloud.

    ---
    - name:  Upgrade Tripleo
      hosts: undercloud
      gather_facts: no
      roles:
        - { role: ansible-role-tripleo-overcloud-upgrade,
            step_pre_undercloud_upgrade: false,
            step_pre_overcloud_upgrade: false}

Parameters
----------

The upgrade role takes severals parameters as input. All those values are stored
under default/main.yml.
All of those values could be overriden.
With the default values, you can upgrade a basic Tripleo environment from Liberty
to Mitaka

Common Parameters
`````````````````

The common parameter that you will probably have to override is:

Network settings :
By default the network isolation is enabled.

    network_isolation: true
    # pre upgrade settings:
    upgrade_overcloud_dns_server: 8.8.8.8
    # this settings should be override by the network isolation settings
    # that it was previously passed.
    # it correspond to the cidr of the vlan on the UC
    network_isolation_ipv4_cidr: "10.0.0.1/24"

Repo settings:
The target_upgrade_version is the release where you want to upgrade your env
The delorean_hash is the pinned version of the delorean repo.

    # set-repo settings:
    target_upgrade_version: mitaka
    upgrade_delorean_hash: current-passed-ci
    repos:
      - delorean.repo
      - delorean-deps.repo
    yum_repo_path: /etc/yum.repos.d/
    # Url of the delorean repos:
    repos_url:
      - http://trunk.rdoproject.org/centos7-{{ target_upgrade_version }}/{{ upgrade_delorean_hash | default('current-passed-ci')}}/delorean.repo
      - http://trunk.rdoproject.org/centos7-{{ target_upgrade_version }}/delorean-deps.repo

.. Note:: If you don't use the delorean repo, you don't have to take care of
    this values. If you override the upgrade_undercloud_repo_script and upgrade_overcloud_repo_script
    script, those values will be useless

Templates and log files:
Those values could be overriden by your own script.
For example you can change the:

    upgrade_undercloud_repo_script: upgrade-repo.sh.j2

By:

    upgrade_undercloud_repo_script: script/upgrade/my_script

.. Note:: The relative path would be from your playbook directory.

All of those script and log files could be change by override those values:

    # scripts
    upgrade_undercloud_repo_script: upgrade-repo.sh.j2
    upgrade_overcloud_repo_script: upgrade-repo.sh.j2
    upgrade_script: upgrade-overcloud.sh.j2
    upgrade_non_controller_script: /bin/upgrade-non-controller.sh
    upgrade_overcloud_repo_template: overcloud-repo.yaml.j2
    # logs:
    upgrade_log: upgrade_console.log

Specific Parameters
```````````````````
The other parameters gives you the opportunity to add your own heat templates
to the upgrade command. The upgrade command is composed of three steps, so you
can add the template of your choice in each 3 steps.
You can use it like this:

    upgrade_custom_templates_script_delivery:
      - overcloud-repo.yaml
      - my-custom-heat-template-1.yaml
    upgrade_custom_templates_controller:
      - overcloud-repo.yaml
      - my-custom-heat-template-for-controller.yaml
    upgrade_custom_templates_converge:
      - overcloud-repo.yaml
    upgrade_templates:
      overcloud-repo:
        name: overcloud-repo.yaml
        src: "{{ upgrade_overcloud_repo_template }}"
      my-custom-1:
        name: my-custom-heat-template-1.yaml
        src: heat-templates/my-custom-heat-template-1.yaml.j2
      my-custom-controller:
        name: my-custom-heat-template-for-controller.yaml
        src: heat-templates/my-custom-heat-template-for-controller.yaml.j2

.. Note:: Note that, each custom templates provided are jinja2 template file. So
    you can add variables / condition or loop into, depending of your need, or
    non predictable values on your env.

.. Note:: An important thing to notice is that the overcloud repositories are set
    through a heat template and given to the upgrade command. The role assume that
    your env and especially the controller are well configured, meaning the yum
    repositories should reachable by the nodes and the dns server are able to
    resolv the names.

Jinja templates
---------------

The upgrade role provide three jinja templates:

    templates/
    ├── overcloud-repo.yaml.j2
    ├── upgrade-overcloud.sh.j2
    └── upgrade-repo.sh.j2

The overcloud-repo.yaml.j2 is the heat template for set up the overcloud yum repositories
The upgrade-overcloud.sh.j2 is the bash script for upgrade the overcloud, with the 3 steps.
The upgrade-repo.sh.j2 is the script for set up the upstream undercloud yum repositories.
This script should be overriden for downstream for example.

Known issues
------------

1/ The role doesn't manage Swift node upgrade yet
2/ The role only manage a 3 nodes deployments yet (1 controller / 1 compute / 1 ceph
