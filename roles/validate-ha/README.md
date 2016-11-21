ansible-role-tripleo-overcloud-validate-ha
==========================================

This role acts on an already deployed tripleo environment, testing all HA related functionalities of the installation.

Requirements
------------

This role must be used with a deployed TripleO environment, so you'll need a working directory of tripleo-quickstart with this files:

- **hosts**: which will contain all the hosts used in the deployment;
- **ssh.config.ansible**: which will have all the ssh data to connect to the undercloud and all the overcloud nodes;
- A **config file** with a definition for the floating network (which will be used to test HA instances), like this one:

      public_physical_network: "floating"
      floating_ip_cidr: "10.0.0.0/24"
      public_net_pool_start: "10.0.0.191"
      public_net_pool_end: "10.0.0.198"
      public_net_gateway: "10.0.0.254"    

Quickstart invocation
---------------------

Quickstart can be invoked like this:

    ./quickstart.sh \
       --retain-inventory \
       --playbook overcloud-validate-ha.yml \
       --working-dir /path/to/workdir \
       --requirements /path/to/quickstart-extras-requirements.txt \
       --config /path/to/config.yml \
       --release <RELEASE> \
       --tags all \
       <HOSTNAME or IP>

Basically this command:

- **Keeps** existing data on the repo (it's the most important one)
- Uses the *overcloud-validate-ha.yml* playbook
- Uses the same custom workdir where quickstart was first deployed
- Get all the extra requirements
- Select the specific config file (which must contain the floating network data)
- Specifies the release (liberty, mitaka, newton or “master” for ocata)
- Performs all the tasks in the playbook overcloud-validate-ha.yml
- Starts the installation on virthost

**Important note**

If the role is called by itself, so not in the same playbook that already deploys the environment (see [baremetal-undercloud-validate-ha.yml](https://github.com/redhat-openstack/ansible-role-tripleo-baremetal-undercloud/blob/master/playbooks/baremetal-undercloud-validate-ha.yml), you need to export *ANSIBLE_SSH_ARGS* with the path of the *ssh.config.ansible* file, like this:

    export ANSIBLE_SSH_ARGS="-F /path/to/quickstart/workdir/ssh.config.ansible"

HA tests
--------

By default these tests are performed per version:

- Test: Look for failed actions (**all**)
- Test: Stop master slave resources (galera and redis), all the resources should come down (**all**)
- Test: Stop keystone resource (by stopping httpd), check no other resource is stopped (**mitaka**, **osp9**)
- Test: next generation cluster checks (**newton**):
  - Test: Stop every systemd resource, stop Galera and Rabbitmq, Start every systemd resource
  - Test: Stop Galera and Rabbitmq, stop every systemd resource, Start every systemd resource
  - Test: Stop Galera and Rabbitmq, wait 20 minutes to see if something fails
- Test: Instance deployment (**all**)

Tests are performed using an external application named [tripleo-director-ha-test-suite](https://github.com/rscarazz/tripleo-director-ha-test-suite).

Example Playbook
----------------

The main playbook couldn't be simpler:

    ---
    - name:  Validate overcloud HA status
      hosts: localhost
      gather_facts: no
      roles:
        - tripleo-overcloud-validate-ha

But it could also be used at the end of a deployment, like in this file [baremetal-undercloud-validate-ha.yml](https://github.com/redhat-openstack/ansible-role-tripleo-baremetal-undercloud/blob/master/playbooks/baremetal-undercloud-validate-ha.yml).

License
-------

Apache

Author Information
------------------

Raoul Scarazzini <rasca@redhat.com>
