Role Name
=========

An Ansible role for scaling and deleting nodes from an overcloud.

Requirements
------------

This role assumes it will be executed against a host on which a Liberty or Mitaka under/overcloud have already been deployed.

**Note:** The ansible-role-tripleo-overcloud-validate role must be accessible.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

**Note:** Make sure to include all environment file and options from your [initial Overcloud creation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/7/html/Director_Installation_and_Usage/sect-Scaling_the_Overcloud.html#sect-Adding_Compute_or_Ceph_Storage_Nodes). This includes the same scale parameters for non-Compute nodes.

- artosn_scale_nodes: <true> -- boolean value that will scale nodes if true
- artosn_delete_original_node: <false> -- boolean value that will delete the original node of type that was scaled
- artosn_working_dir: <'/home/stack'> -- working directory for the role. Assumes stackrc file is present at this location


Dependencies
------------

1. [ansible-role-tripleo-overcloud-validate](https://github.com/redhat-openstack/ansible-role-tripleo-overcloud-validate)

Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Scale overcloud nodes
      hosts: undercloud
      roles:
        - ansible-role-tripleo-overcloud-scale-nodes

  2. Sample config file to scale from one compute node to two compute nodes on the overcloud

    control_memory: 6144
    compute_memory: 6144

    undercloud_memory: 8192
    undercloud_vcpu: 2

    overcloud_nodes:
      - name: control_0
        flavor: control

      - name: compute_0
        flavor: compute

      - name: compute_1
        flavor: compute

      - name: compute_2
        flavor: compute

    tempest: false
    pingtest: true
    deploy_timeout: 60

    # General deployment info
    libvirt_args: "--libvirt-type qemu"
    flavor_args: >-
      --control-flavor {{flavor_map.control
      if flavor_map is defined and 'control' in flavor_map else 'oooq_control'}}
      --compute-flavor {{flavor_map.compute
      if flavor_map is defined and 'compute' in flavor_map else 'oooq_compute'}}
      --ceph-storage-flavor {{flavor_map.ceph
      if flavor_map is defined and 'ceph' in flavor_map else 'oooq_ceph'}}
    timeout_args: "--timeout {{ deploy_timeout }}"
    # Pulled this out so we can hand these configs to the openstack overcloud node delete command
    scale_extra_configs: "-e /usr/share/openstack-tripleo-heat-templates/environments/network-isolation.yaml -e /usr/share/openstack-tripleo-heat-templates/environments/net-single-nic-with-vlans.yaml -e ~/network-environment.yaml"
    scale_extra_args: "--{{ node_to_scale }}-scale {{ final_scale_value }} --neutron-network-type vxlan --neutron-tunnel-types vxlan {{ scale_extra_configs }} --ntp-server pool.ntp.org"

    # Scale deployment info
    node_to_scale: compute # Type of node to scale
    initial_scale_value: 1 # Initial number of nodes to deploy
    final_scale_value: 2   # Number of additional nodes to add during the scale

    # Scale deployment arguments
    scale_args: >-
      {{ libvirt_args }}
      {{ flavor_args }}
      {{ timeout_args }}
      {{ scale_extra_args }}

License
-------

Apache

Author Information
------------------

RDO-CI Team
