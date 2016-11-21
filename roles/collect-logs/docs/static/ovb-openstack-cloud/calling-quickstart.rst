Install the dependencies for TripleO Quickstart
-----------------------------------------------

You need some software available on your local system before you can run
`quickstart.sh`. You can install the necessary dependencies by running:

::

    bash quickstart.sh --install-deps

Deploy TripleO using Quickstart on Openstack Instances
------------------------------------------------------

Deployments on Openstack instances require steps from third-party repos,
in addition to the steps in TripleO Quickstart.
Below is an example of a complete call to quickstart.sh to run a full deploy
on Openstack Instances launched via Openstack Virtual Baremetal (OVB/Heat):

::

    # $HW_ENV_DIR is the directory where the  environment-specific
    # files are stored

    pushd $WORKSPACE/tripleo-quickstart
    bash quickstart.sh \
        --ansible-debug \
        --bootstrap \
        --working-dir $WORKSPACE/ \
        --tags all \
        --no-clone \
        --requirements quickstart-role-requirements.txt \
        --requirements $WORKSPACE/$HW_ENV_DIR/requirements_files/$REQUIREMENTS_FILE \
        --config $WORKSPACE/$HW_ENV_DIR/config_files/$CONFIG_FILE \
        --extra-vars @$OPENSACK_CLOUD_SETTINGS_FILE \
        --extra-vars @$OPENSTACK_CLOUD_CREDS_FILE \
        --extra-vars @$WORKSPACE/$HW_ENV_DIR/env_settings.yml \
        --playbook $PLAYBOOK \
        --release $RELEASE \
        localhost
    popd


Modify the settings
^^^^^^^^^^^^^^^^^^^

After the undercloud connectivity has been set up, the undercloud is installed and the
overcloud is deployed following the 'baremetal' workflow, using settings relevant to the
undercloud and baremetal nodes created on the Openstack cloud.

Below are a list of example settings (overwriting defaults) that would be passed to quickstart.sh:

::

    # undercloud.conf
    undercloud_network_cidr: 192.0.2.0/24
    undercloud_local_ip: 192.0.2.1/24
    undercloud_network_gateway: 192.0.2.1
    undercloud_undercloud_public_vip: 192.0.2.2
    undercloud_undercloud_admin_vip: 192.0.2.3
    undercloud_local_interface: eth1
    undercloud_masquerade_network: 192.0.2.0/24
    undercloud_dhcp_start: 192.0.2.5
    undercloud_dhcp_end: 192.0.2.24
    undercloud_inspection_iprange: 192.0.2.25,192.0.2.39

    overcloud_nodes:
    undercloud_type: ovb
    introspect: true

    # file locations to be copied to the undercloud (for network-isolation deployment)
    undercloud_instackenv_template: "{{ local_working_dir }}/instackenv.json"
    network_environment_file: "{{ local_working_dir }}/openstack-virtual-baremetal/network-templates/network-environment.yaml"
    baremetal_nic_configs: "{{ local_working_dir }}/openstack-virtual-baremetal/network-templates/nic-configs"

    network_isolation: true

    # used for access to external network
    external_interface: eth2
    external_interface_ip: 10.0.0.1
    external_interface_netmask: 255.255.255.0
    external_interface_hwaddr: fa:05:04:03:02:01

    # used for validation
    floating_ip_cidr: 10.0.0.0/24
    public_net_pool_start: 10.0.0.50
    public_net_pool_end: 10.0.0.100
    public_net_gateway: 10.0.0.1

