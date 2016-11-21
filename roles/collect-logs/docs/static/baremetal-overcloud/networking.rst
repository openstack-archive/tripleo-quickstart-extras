Networking
----------

With a Virtual Environment, tripleo-quickstart sets up the networking as part of the workflow.
The networking arrangement needs to be set up prior to working with tripleo-quickstart.

The overcloud nodes will be deployed from the undercloud machine and therefore the
machines need to have have their network settings modified to allow for the
overcloud nodes to be PXE boot'ed using the undercloud machine.
As such, the setup requires that:

* All overcloud machines in the setup must support IPMI
* A management provisioning network is setup for all of the overcloud machines.
  One NIC from every machine needs to be in the same broadcast domain of the
  provisioning network. In the tested environment, this required setting up a new
  VLAN on the switch. Note that you should use the same NIC on each of the
  overcloud machines ( for example: use the second NIC on each overcloud
  machine). This is because during installation we will need to refer to that NIC
  using a single name across all overcloud machines e.g. em2
* The provisioning network NIC should not be the same NIC that you are using
  for remote connectivity to the undercloud machine. During the undercloud
  installation, a openvswitch bridge will be created for Neutron and the
  provisioning NIC will be bridged to the openvswitch bridge. As such,
  connectivity would be lost if the provisioning NIC was also used for remote
  connectivity to the undercloud machine.
* The overcloud machines can PXE boot off the NIC that is on the private VLAN.
  In the tested environment, this required disabling network booting in the BIOS
  for all NICs other than the one we wanted to boot and then ensuring that the
  chosen NIC is at the top of the boot order (ahead of the local hard disk drive
  and CD/DVD drives).
* For each overcloud machine you have: the MAC address of the NIC that will PXE
  boot on the provisioning network the IPMI information for the machine (i.e. IP
  address of the IPMI NIC, IPMI username and password)

Refer to the following diagram for more information

i.. image:: _images/TripleO_Network_Diagram_.jpg
