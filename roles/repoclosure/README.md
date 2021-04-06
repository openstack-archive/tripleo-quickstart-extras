repoclosure
================

This role will execute repoclosure against the enabled repos on a system.
It runs repoclosure per repo to better determine what needs to be fixed in the
yum repo.

You can exclude certain repos w/ the *repoclosure_exclude_repos* variable.
You can exclude certain packages via excludepkgs w/ *repoclosure_exclude_pkgs*

Requirements
------------

Available yum repos

Role Variables
--------------

repoclosure_script_source: <repoclosure.sh.j2> the jina template used
repoclosure_script: <repoclosure.sh>  out of jinja2 template
repoclosure_log: the log file
repoclosure_exclude_repos: a list of repos that are not worthy of repoclosure.
repoclosure_include_repos:
  - "--enablerepo delorean-*"
  - "--enablerepo quickstart-*"
  - "--enablerepo advanced-virt*"
  - "--enablerepo centos-rabbitmq*"
  - "--enablerepo centos-opstools"
  - "--enablerepo centos-nfv-ovs"
repoclosure_exclude_pkgs:
  - "*-test*"
  - "*.src"
  - "*-devel"
  - "*-debug"
  - "*-docs"


Dependencies
------------

This role has no dependencies.
Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Set up CentOS undercloud node to run TripleO Quickstart
      hosts: undercloud
      gather_facts: false
      roles:
        - repoclosure

License
-------

Apache-2.0

Author Information
------------------

RDO-CI Team
