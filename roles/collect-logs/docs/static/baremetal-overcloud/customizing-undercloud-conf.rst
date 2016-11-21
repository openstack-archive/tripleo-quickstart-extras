Customizing undercloud.conf
===========================

The undercloud.conf file is copied to the undercloud VM using a template where the system values
are variables. <https://github.com/openstack/tripleo-quickstart/blob/master/roles/tripleo/undercloud/templates/undercloud.conf.j2>.
The tripleo-quickstart defaults for these variables are suited to a virtual overcloud,
but can be overwritten by passing custom settings to tripleo-quickstart in a settings file
(--extra-vars @<file_path>). For example:
::

    undercloud_network_cidr: 10.0.5.0/24
    undercloud_local_ip: 10.0.5.1/24
    undercloud_network_gateway: 10.0.5.1
    undercloud_undercloud_public_vip: 10.0.5.2
    undercloud_undercloud_admin_vip: 10.0.5.3
    undercloud_local_interface: eth1
    undercloud_masquerade_network: 10.0.5.0/24
    undercloud_dhcp_start: 10.0.5.5
    undercloud_dhcp_end: 10.0.5.24
    undercloud_inspection_iprange: 10.0.5.100,10.0.5.120

