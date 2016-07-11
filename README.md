ansible-role-tripleo-baremetal-undercloud
=========

This role aims to build a baremetal undercloud machine from scratch. Using tripleo-quickstart, this means that you will be able to provide, prepare and install the undercloud on a physical machine.

From the tripleo-quickstart perspective virthost and undercloud will be the same host.

Requirements
------------

For make all the things working you need to have an environment with all the things in place:

Hardware requirements

* A physical machine for the undercloud that can be accessed as root from the jump host
* At least two other physical machines that will become controller and compute, for HA three controllers and one compute are needed
* A working network link between overcloud and undercloud, typically the second net device of the undercloud will talk to the first net device of all the overcloud machines

Software requirements

* The tripleo-quickstart quickstart.sh script:
    * A config file (i.e. ha.yml) containing all the customizations for the baremetal environment
* This set of files, dependent from the hardware:
    * File undercloud-provisioning.sh - optional, name is not important
    * File network-environment.yaml - mandatory
    * Directory nic-configs - mandatory if declared inside the resource_registry section in network-environment.yaml and must contain all the needed files
    * File instackenv.json - mandatory, must contain the ipmi credentials for the nodes

Role Variables
--------------

A typical config file will contain something like this:

    undercloud_type: baremetal

    flavor_map:
      control: baremetal
      compute: baremetal
      storage: baremetal
      ceph: baremetal

    overcloud_nodes:
      - name: control_0
        flavor: baremetal
      - name: control_1
        flavor: baremetal
      - name: control_2
        flavor: baremetal

      - name: compute_0
        flavor: baremetal
      - name: compute_1
        flavor: baremetal

    # Steps
    step_introspect: true
    step_introspect_with_retry: true
    step_provide_undercloud: true
    step_overcloud_images: true
    step_install_undercloud: true
    step_prepare_undercloud: true

    libvirt_type: kvm
    libvirt_args: "--libvirt-type kvm"

    undercloud_local_interface: eth1

    baremetal_provisioning_script: "/path/to/undercloud-provisioning.sh"
    baremetal_network_environment: "/path/to/network-environment.yaml"
    baremetal_instackenv: "/path/to/instackenv.json"
    baremetal_nic_configs: "/path/to/nic_configs"

    floating_ip_cidr: "<FLOATING NETWORK CIDR>"
    public_net_pool_start: "<FLOATING NETWORK POOL START>"
    public_net_pool_end: "<FLOATING NETWORK POOL END>"
    public_net_gateway: "<FLOATING NETWORK GATEWAY>"

    extra_args: "--ntp-server <NTP SERVER IP> --control-scale 3 --compute-scale 2 --ceph-storage-scale 0 --block-storage-scale 0 --swift-storage-scale 0 --templates -e /usr/share/openstack-tripleo-heat-templates/environments/puppet-pacemaker.yaml -e /usr/share/openstack-tripleo-heat-templates/environments/network-isolation.yaml -e /home/stack/network-environment.yaml --neutron-bridge-mappings datacentre:br-floating"
    tempest: false

A brief explanation of the variables:

* The variable **undercloud_type** is checked in all the dependent roles (see @Dependencies)
* A specific **flavor_map** (in this case baremetal) needs to be applied to each node kind
* The list of all the **overcloud_nodes** must be explicited
* With **step_introspect** and **step_introspect_with_retry** you can choose if you want to introspect and even retry again for host that failed introspection
* The **libvirt_type** and **libvirt_args** must be set to kvm, since we will work on baremetal with native virtual capabilities
* The **undercloud_local_interface** needs to be changed accordingly to the baremetal hardware
* If the user does not need to provide the machine, then **baremetal_provisioning_script**  can be omitted while setting also **step_provide_undercloud: false**
* **baremetal_network_environment**, **baremetal_instackenv** and *optionally* **baremetal_nic_configs** will contain all the environment files.
* **extra_args** will contain all deploy specific (like HA settings)
* **tempest** will enable tempest tests
* If instances needs to be accessible from the outside network then all the parameters (so **floating_ip_cidr** and **public_net_***) of this floating network must be explicited.

The main task of the role is this one:

    ---
    # tasks file for ansible-role-tripleo-baremetal-undercloud

    - include: machine-provisioning.yml
      tags:
        - machine-provision

    - include: machine-setup.yml
      tags:
        - machine-setup

    - include: undercloud-scripts.yml
      delegate_to: "{{ virthost }}"
      tags:
        - undercloud-scripts

    - include: undercloud-pre-install.yml
      delegate_to: "{{ virthost }}"
      tags:
        - undercloud-pre-install

    - include: undercloud-install.yml
      delegate_to: "{{ virthost }}"
      tags:
        - undercloud-install

    - include: overcloud-images.yml
      delegate_to: "{{ virthost }}"
      tags:
        - overcloud-images

Some notes about the main task file:

* Even if virthost and undercloud are the same machine, the name “undercloud” will be inventoried after (see the baremetal playbook slide)
* Each action is tagged so it is possible to exclude a specific section, but...
* In any case some variables can be controlled via config settings:
    * step_provide_undercloud: choose if you want to do machine provisioning
    * step_install_repos_undercloud: choose if you want to prepare the undercloud machine wirh repositories and all the packages needed
    * step_install_undercloud: choose if you want to install the undercloud
    * step_overcloud_images: choose if you want to download overcloud images

This is basically what the specific tasks does:

* **machine-provisioning.yml** provides the machine and make it become both virthost/undercloud 
* **machine-setup.yml** prepares the undercloud with ssh connections, users, sudoers and inventory addition
* **undercloud-scripts.yml** copies all the needed scripts into virthost/undercloud
* **undercloud-pre-install.yml** selinux, firewall, repositories and packages 
* **undercloud-install.yml** installs the undercloud
* **overcloud-images.yml** retrieves the overcloud images

Dependencies
------------

If you don't need to change anything in how the environments gets deployed, then all the dependencies should be satisfied by the default requirements.txt file.

In any case the roles you will need to deploy an entire environment from scratch (see @Example Playbook) are:

* **ansible-role-tripleo-inventory**
* **ansible-role-tripleo-undercloud-post**
* **ansible-role-tripleo-overcloud**
* **ansible-role-tripleo-overcloud-validate**
* **ansible-role-tripleo-overcloud-validate-ha** (this is optional if you want to test HA capabilities)

Example Playbook
----------------

Here's is an example on host to use this role in combination to all the others coming from various related to tripleo-quickstart:

    ---
    - name:  Baremetal undercloud install
      hosts: localhost
      roles:
        - tripleo-baremetal-undercloud
      tags:
        - undercloud-bm-install

    - name:  Inventory the undercloud
      hosts: localhost
      vars:
          inventory: undercloud
      roles:
        - tripleo-inventory
      tags:
        - undercloud-inventory

    - name:  Post undercloud install steps
      hosts: undercloud
      roles:
        - tripleo-undercloud-post
      tags:
        - undercloud-post-install

    - name:  Deploy the overcloud
      hosts: undercloud
      gather_facts: no
      roles:
        - tripleo-overcloud
      tags:
        - overcloud-deploy

    - name:  Inventory the overcloud
      hosts: undercloud
      vars:
          inventory: all
      roles:
        - tripleo-inventory
      tags:
        - overcloud-inventory

    - name:  validate the overcloud
      hosts: undercloud
      gather_facts: no
      roles:
        - tripleo-overcloud-validate
      tags:
        - overcloud-validate

The steps of the sample playbook are these:

* First invoked role is tripleo-baremeal-undercloud undercloud
* Then undercloud is inventoried
* In the post task all the env files are pushed into undercloud, introspection is performed and a default route external interface is created for the overcloud network access
* Overcloud is then deployed, inventoried and validated

Then you can invoke *quickstart.sh* like this:

    ./quickstart.sh -v --clean --playbook baremetal-undercloud.yml --working-dir /path/to/workdir --requirements /path/to/requirements.txt --config /path/to/config.yml --release mitaka --tags all <HOSTNAME or IP>

Basically this command:

* Uses the playbook **baremetal-undercloud.yml**
* Uses a custom workdir that is rebuilt from scratch (so if it already exists, it is dropped)
* Performs all the tasks in the playbook
* Chooses release (liberty, mitaka or “master” for newton)
* Starts the installation on virthost

License
-------

BSD

Author Information
------------------

Raoul Scarazzini <rasca@redhat.com>
