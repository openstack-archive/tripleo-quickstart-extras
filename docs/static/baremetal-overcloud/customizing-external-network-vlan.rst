Customizing external network vlan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If network-isolation is used in the deployment, tripleo-quickstart will, by default,
add a NIC on the external vlan to the undercloud,
<https://github.com/openstack/tripleo-quickstart/blob/master/roles/tripleo/undercloud/templates/undercloud-install-post.sh.j2#L88>.
When working with a baremetal overcloud, the vlan values must be customized with the correct
system-related values. The default vlan values can be overwritten in a settings file passed
to triple-quickstart as in the following example:
::

    undercloud_networks:
      external:
        address: 10.0.7.13
        netmask: 255.255.255.192
        device_type: ovs
        type: OVSIntPort
        ovs_bridge: br-ctlplane
        ovs_options: '"tag=102"'
        tag: 102

