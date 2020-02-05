baremetal-undercloud
====================

This role aims to build a baremetal undercloud machine from scratch. Using
tripleo-quickstart, this means that you will be able to provide, prepare and
install the undercloud on a physical machine.

From the tripleo-quickstart perspective virthost and undercloud will be the
same host.

Requirements
------------

To make all the things working you need to have an environment with all the
things in place:

**Hardware requirements**

* A physical machine for the undercloud that can be accessed as root from the
  jump host
* At least two other physical machines that will become controller and compute,
  for HA three controllers and one compute are needed
* A working network link between overcloud and undercloud, typically the second
  net device of the undercloud will talk to the first net device of all the
  overcloud machines

**Software requirements**

* The tripleo-quickstart quickstart.sh script:
    * A config file (i.e. ha.yml) containing all the customizations for the
      baremetal environment
* This set of files, dependent from the hardware:
    * File undercloud-provisioning.sh - optional, name is not important
    * File network-environment.yaml - mandatory
    * Directory nic-configs - mandatory if declared inside the
      resource_registry section in network-environment.yaml and must contain
      all the needed files
    * File instackenv.json - mandatory, must contain the ipmi credentials for
      the nodes

Role Variables
--------------

A typical configuration file will contain something like this:

```yaml
# Virthost key for accessing newly provided machine
virthost_key: ~/.ssh/customkey

# Type of undercloud (we're deploying on baremetal otherwise this should be
# virtual)
undercloud_type: baremetal

# Specify the secondary net interface for overcloud provisioning
undercloud_local_interface: eth1

# Specify the external network for undercloud that will be used to route
# overcloud traffic
undercloud_external_network_cidr: 172.20.0.0/24

# Declare the additional interface on undercloud to route overcloud traffic
undercloud_networks:
  external:
    address: 172.20.0.254
    netmask: 255.255.255.0
    device_type: ovs
    type: OVSIntPort
    ovs_bridge: br-ctlplane
    ovs_options: '"tag=1105"'
    tag: 1105

# Define all the flavors
flavor_map:
  control: baremetal
  cellcontrol: baremetal
  compute: baremetal
  storage: baremetal
  ceph: baremetal
  swift: baremetal

# Will be used by baremetal-undercloud role
step_provide_undercloud: true
# Will be used by baremetal-prep-overcloud role
step_install_upstream_ipxe: true
# Will be used by overcloud-prep-images role
step_introspect: true

# Explicitly declare kvm since we are on BM and disable vBMC
libvirt_type: kvm
libvirt_args: "--libvirt-type kvm"
enable_vbmc: false

# Environment specific variables
baremetal_provisioning_script: "/path/to/undercloud-provisioning.sh"
baremetal_network_environment: "/path/to/network-environment.yaml"
baremetal_instackenv: "/path/to/instackenv.json"
baremetal_nic_configs: "/path/to/nic_configs"

# Public (Floating) network definition
public_physical_network: "floating"
floating_ip_cidr: "<FLOATING NETWORK CIDR>"
public_net_pool_start: "<FLOATING NETWORK POOL START>"
public_net_pool_end: "<FLOATING NETWORK POOL END>"
public_net_gateway: "<FLOATING NETWORK GATEWAY>"

extra_args: "--ntp-server <NTP SERVER IP> --control-scale 3 --compute-scale 2 --ceph-storage-scale 0 --block-storage-scale 0 --swift-storage-scale 0 --templates -e /usr/share/openstack-tripleo-heat-templates/environments/puppet-pacemaker.yaml -e /usr/share/openstack-tripleo-heat-templates/environments/network-isolation.yaml -e /home/stack/network-environment.yaml"
```

A brief explanation of the variables:

* The variable **undercloud_type** is checked in some of the dependent roles
  (see @Dependencies).
* The variable **virthost_key** is optional, if defined it must be a path to a
  private ssh key file needed to access to virthost. If you access to the
  virthost with the default ssh key of the user launching quickstart.sh then
  you don't need to set it.
* The **undercloud_local_interface** needs to be changed accordingly to the
  baremetal hardware.
* The **undercloud_external_network_cidr** will be the overcloud external
  network that undercloud will route.
* A specific **flavor_map** (in this case baremetal) needs to be applied to
  each node kind.
* With **step_provide_undercloud** you can choose if you want to provide the
  virthost.
* With **step_introspect** you can choose if you want to introspect nodes.
* With **step_install_upstream_ipxe** you can choose if you want to install
  upstream ipxe (useful with some hardware issues).
* The **libvirt_type** and **libvirt_args** must be set to kvm, since we will
  work on baremetal with native virtual capabilities.
* **baremetal_provisioning_script** is the script to provide the machine, if
  **step_provide_undercloud is false** than this can be omitted.
* **baremetal_network_environment**, **baremetal_instackenv** and *optionally*
  **baremetal_nic_configs** will contain all the environment files.
* Depending on the network in which spawned instances will be exposed all the
  related parameters (**floating_ip_cidr** and **public_net**\*) must be
  declared explicitly.
* **extra_args** will contain all deploy specific (like HA settings)

The main task of the role is this one:

```yaml
---
# tasks file for baremetal-undercloud

# Do machine provisioning
- include: machine-provisioning.yml
  tags:
    - machine-provision

# Prepare machine to be used with TripleO
- include: machine-setup.yml
  tags:
    - machine-setup

# Configure repos and packages
- include: undercloud-repos-conf.yml
  delegate_to: "{{ virthost }}"
  tags:
    - undercloud-repos-conf

# Get overcloud images
- include: overcloud-images.yml
  delegate_to: "{{ virthost }}"
  tags:
    - overcloud-images
```

This is basically what each specific tasks does:

* **machine-provisioning.yml** provides the machine and make it become both
  virthost/undercloud
* **machine-setup.yml** prepares the undercloud with ssh connections, users,
  sudoers and inventory addition
* **undercloud-repos-conf.yml** repositories and packages configurations
* **overcloud-images.yml** overcloud images retrieving

Some notes:

* Even if virthost and undercloud are the same machine, the name "undercloud"
  will be inventoried in any case
* Each action is tagged so it is possible to exclude a specific section
* Some variables can be controlled via configuration settings (look above in
  @Role usage)

Dependencies
------------

If you don't need to change anything in how the environments gets deployed,
then all the dependencies should be satisfied by the default
**quickstart-extras-requirements.txt** file.

In any case the roles you will need to deploy an entire environment from
scratch (see @Example Playbook) are:

* **baremetal-undercloud** (this role)
* **tripleo-inventory** (part of *tripleo-quickstart*)
* **tripleo/undercloud** (part of *tripleo-quickstart*)
* **baremetal-prep-overcloud**
* **overcloud-prep-{config,images,flavors,network}**
* **overcloud-deploy**
* **overcloud-validate** or **overcloud-validate-ha** (if you want to test HA
  capabilities)

Example Playbook
----------------

Here's is an example playbook that uses this role in combination to all the
others coming from various related to tripleo-quickstart:

```yaml
---
# Provision and initial undercloud setup
- name: Baremetal undercloud install
  hosts: localhost
  roles:
    - baremetal-undercloud
  tags:
    - undercloud-bm-install

# Machine at this point is provided
- name: Add the undercloud node to the generated inventory
  hosts: localhost
  gather_facts: true
  roles:
    - tripleo-inventory
  tags:
    - undercloud-inventory

# Deploy the undercloud
- name: Install undercloud
  hosts: undercloud
  gather_facts: false
  roles:
    - tripleo/undercloud
  tags:
    - undercloud-install

# Baremetal preparation (with workarounds)
- name: Prepare baremetal for the overcloud deployment
  hosts: undercloud
  roles:
    - baremetal-prep-overcloud
  tags:
    - baremetal-prep-overcloud

# Prepare any additional configuration files required by the overcloud
- name: Prepare configuration files for the overcloud deployment
  hosts: undercloud
  gather_facts: false
  roles:
    - overcloud-prep-config
  tags:
    - overcloud-prep-config

# Prepare the overcloud images for deployment
- name: Prepare the overcloud images for deployment
  hosts: undercloud
  gather_facts: false
  roles:
    - overcloud-prep-images
  tags:
    - overcloud-prep-images

# Prepare the overcloud flavor configuration
- name: Prepare overcloud flavors
  hosts: undercloud
  gather_facts: false
  roles:
    - overcloud-prep-flavors
  tags:
    - overcloud-prep-flavors

# Prepare the undercloud networks for the overcloud deployment
- name: Prepare the undercloud networks for the overcloud deployment
  hosts: undercloud
  gather_facts: false
  roles:
    - overcloud-prep-network
  tags:
    - overcloud-prep-network

# Deploy the overcloud
- name: Deploy the overcloud
  hosts: undercloud
  gather_facts: true
  roles:
    - overcloud-deploy
  tags:
    - overcloud-deploy

- name: Add the overcloud nodes to the generated inventory
  hosts: undercloud
  gather_facts: true
  vars:
      inventory: all
  roles:
    - tripleo-inventory
  tags:
    - overcloud-inventory

# Check the results of the deployment, note after inventory has executed
- name: Check the result of the deployment
  hosts: localhost
  tasks:
    - name: ensure the deployment result has been read into memory
      include_vars: "{{ local_working_dir }}/overcloud_deployment_result.json"

    # overcloud_deploy_result = ["failed", "passed"]
    - name: did the deployment pass or fail?
      debug: var=overcloud_deploy_result
      failed_when: overcloud_deploy_result == "failed"
  tags:
    - overcloud-deploy-check
```

The steps of the sample playbook are these:

* First invoked role is baremetal-undercloud
* Then undercloud is inventoried
* Undercloud is prepared for deploying
* Overcloud is then deployed, inventoried and validated

Quickstart invocation
---------------------

You can invoke *quickstart.sh* like this:

```console
./quickstart.sh \
  --clean \
  --playbook baremetal-undercloud.yml \
  --working-dir /path/to/workdir \
  --config /path/to/config.yml \
  --release <RELEASE> \
  --tags all \
  <HOSTNAME or IP>
```

Basically this command:

* Uses the playbook **baremetal-undercloud.yml**
* Uses a custom workdir that is rebuilt from scratch (so if it already exists,
  it is dropped, see *--clean*)
* Get all the extra requirements
* Select the config file
* Chooses release (liberty, mitaka, newton, or "master" for ocata)
* Performs all the tasks in the playbook
* Starts the installation on virthost

License
-------

Apache

Author Information
------------------

Raoul Scarazzini <rasca@redhat.com>
