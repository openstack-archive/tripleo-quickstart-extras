undercloud-setup
================

This role encompasses the setup required when using a standard CentOS/RHEL
undercloud host in substitution for a 'ready-made' undercloud image. If an
undercloud machine or node is launched a 'vanilla' CentOS and RHEL image,
there are a number of steps that need to be run to get the undercloud to the
point where TripleO Quickstart can be run.

Some steps are generic to all undercloud nodes or machines and some
steps are specific to the environment in which the undercloud is
launched.

Steps to download or build overcloud images are included in the
overcloud-images role. Steps to prepare the undercloud repos are
included in the repo-setup role.

Requirements
------------

This role should not be included in a generic virtual TripleO Quickstart
playbook. Therefore including environment-specific code (which is switch
cased to run only on the desired environment) is acceptable. It will
not add complexity to the default TripleO Quickstart workflow.

Role Variables
--------------

- local_working_dir: <"{{ lookup('env', 'HOME') }}/.quickstart"> -- Directory for quickstart.sh script
- non_root_user: <stack>  -- The non-root user operating on the virthost
- undercloud_user: <stack> -- The non-root user operating on the undercloud
- undercloud_key: <"{{ local_working_dir }}/id_rsa_undercloud"> -- Key to access the undercloud node/machine
- non_root_user_setup: <true> -- Switch to setup a non-root user
- toci_vxlan_networking: <false> -- Switch to setup the VXLAN networking from devstack-gate
- toci_vxlan_networking_multinode: <false> -- Switch to setup the VXLAN networking from devstack-gate on a multinode setup provided from nodepool.
- undercloud_hostname: <false> -- Optionally, the hostname to set on the host.
- hostname_correction: <false> -- Switch to set the transient hostname to the static hostname (TripleO requirement)
- step_set_undercloud_hostname: <false> -- Switch to set the undercloud hostname explicitly
- package_installs: <true> -- Switch to install required OpenStack packages for an undercloud (requires repos to already be setup)
- custom_nameserver: <8.8.8.8> -- Added to /etc/resolv.conf for access in custom environments
- ovb_setup_connectivity: <false> -- Setup external network, custom nameserver and set MTUS valuse for OVB environments

Dependencies
------------

This playbook has no dependencies. If a provisioning step is not included
in this role, it is assumed that the node/machine to set up already
exists and is accessible.

Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Set up CentOS undercloud node to run TripleO Quickstart
      hosts: undercloud
      gather_facts: no
      roles:
        - undercloud-setup

License
-------

Apache-2.0

Author Information
------------------

RDO-CI Team

