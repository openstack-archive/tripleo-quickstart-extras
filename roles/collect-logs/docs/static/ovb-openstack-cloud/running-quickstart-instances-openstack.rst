Running TripleO Quickstart on Openstack instances
-------------------------------------------------

By default, TripleO Quickstart uses libvirt to create virtual machines (VM) to serve
as undercloud and overcloud nodes for a TripleO deployment.
With some steps and modification, TripleO Quickstart can setup an undercloud and
deploy the overcloud on instances launched on an Openstack cloud rather than libvirt VMs.

Beginning assumptions
^^^^^^^^^^^^^^^^^^^^^

This document details the workflow for running TripleO Quickstart on Openstack
instances. In particular, the example case is instances created via Heat and
Openstack Virtual Baremetal <https://github.com/openstack/openstack-virtual-baremetal>.

The following are assumed to have been completed before following this document:

* An Openstack cloud exists and has been set up
  (and configured as described in
  [Patching the Host Cloud](https://openstack-virtual-baremetal.readthedocs.io/en/latest/host-cloud/patches.html).
  if the cloud is pre-Mitaka release). From the Mitaka release the cloud should
  not require patching
* The undercloud image under test has been uploaded to Glance in the Openstack cloud.
* A heat stack has been deployed with instances for the undercloud, bmc, and overcloud nodes.
* The nodes.json file has been created (later to be copied to the undercloud as instackenv.json)

Below is an example `env.yaml` file used to create the heat stack that will support a
tripleo-quickstart undercloud and overcloud deployment with network isolation:

::

    parameters:
      os_user: admin
      os_password: password
      os_tenant: admin
      os_auth_url: http://10.10.10.10:5000/v2.0

      bmc_flavor: m1.medium
      bmc_image: 'bmc-base'
      bmc_prefix: 'bmc'

      baremetal_flavor: m1.large
      baremetal_image: 'ipxe-boot'
      baremetal_prefix: 'baremetal'

      key_name: 'key'
      private_net: 'private'
      node_count: {{ node_count }}
      public_net: 'public'
      provision_net: 'provision'

      # QuintupleO-specific params ignored by virtual-baremetal.yaml
      undercloud_name: 'undercloud'
      undercloud_image: '{{ latest_undercloud_image }}'
      undercloud_flavor: m1.xlarge
      external_net:  '{{ external_net }}'
      undercloud_user_data: |
            #!/bin/sh
            sed -i "s/no-port-forwarding.*sleep 10\" //" /root/.ssh/authorized_keys

    #parameter_defaults:
    ## Uncomment and customize the following to use an existing floating ip
    #  undercloud_floating_ip_id: 'uuid of floating ip'
    #  undercloud_floating_ip: 'address of floating ip'

    resource_registry:
    ## Uncomment the following to use an existing floating ip
    #  OS::OVB::UndercloudFloating: templates/undercloud-floating-existing.yaml

    ## Uncomment the following to use no floating ip
    #  OS::OVB::UndercloudFloating: templates/undercloud-floating-none.yaml

    ## Uncomment the following to create a private network
      OS::OVB::PrivateNetwork: {{ templates_dir }}/private-net-create.yaml

    ## Uncomment to create all networks required for network-isolation.
    ## parameter_defaults should be used to override default parameter values
    ## in baremetal-networks-all.yaml
      OS::OVB::BaremetalNetworks: {{ templates_dir }}/baremetal-networks-all.yaml
      OS::OVB::BaremetalPorts: {{ templates_dir }}/baremetal-ports-all.yaml

    ## Uncomment to deploy a quintupleo environment without an undercloud.
    #  OS::OVB::UndercloudEnvironment: OS::Heat::None


