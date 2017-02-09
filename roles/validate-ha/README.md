overcloud-validate-ha
=====================

This role acts on an already deployed tripleo environment, testing all HA related functionalities of the installation.

Requirements
------------

This role must be used with a deployed TripleO environment, so you'll need a working directory of tripleo-quickstart with these files:

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
       --config /path/to/config.yml \
       --release <RELEASE> \
       --tags all \
       <HOSTNAME or IP>

Basically this command:

- **Keeps** existing data on the repo (it's the most important one)
- Uses the *overcloud-validate-ha.yml* playbook
- Uses the same custom workdir where quickstart was first deployed
- Select the specific config file (which must contain the floating network data)
- Specifies the release (mitaka, newton, or “master” for ocata)
- Performs all the tasks in the playbook overcloud-validate-ha.yml

**Important note**

If the role is called by itself, so not in the same playbook that already deploys the environment (see [baremetal-undercloud-validate-ha.yml](https://github.com/openstack/tripleo-quickstart-extras/blob/master/playbooks/baremetal-undercloud-validate-ha.yml), you need to export *ANSIBLE_SSH_ARGS* with the path of the *ssh.config.ansible* file, like this:

    export ANSIBLE_SSH_ARGS="-F /path/to/quickstart/workdir/ssh.config.ansible"

HA tests
--------

Each test is associated to a global variable that, if true, makes the test happen. Tests are grouped and performed by default depending on the OpenStack release.
This is the list of the supported variables, with test description and name of the release on which test is performed:

- **test_ha_failed_actions**: Look for failed actions (**all**)
- **test_ha_master_slave**: Stop master slave resources (galera and redis), all the resources should come down (**all**)
- **test_ha_keystone_constraint_removal**: Stop keystone resource (by stopping httpd), check no other resource is stopped (**mitaka**)
- **Test: next generation cluster checks (**newton**):
  - **test_ha_ng_a**: Stop every systemd resource, stop Galera and Rabbitmq, Start every systemd resource
  - **test_ha_ng_b**: Stop Galera and Rabbitmq, stop every systemd resource, Start every systemd resource
  - **test_ha_ng_c**: Stop Galera and Rabbitmq, wait 20 minutes to see if something fails
- **test_ha_instance**: Instance deployment (**all**)

It is also possible to omit (or add) tests not made for the specific release, using the above vars, like in this example:

    ./quickstart.sh \
      --retain-inventory \
      --ansible-debug \
      --no-clone \
      --playbook overcloud-validate-ha.yml \
      --working-dir /path/to/workdir/ \
      --config /path/to/config.yml \
      --extra-vars test_ha_failed_actions=false \
      --extra-vars test_ha_ng_a=true \
      --release mitaka \
      --tags all \
      <VIRTHOST>

In this case we will not check for failed actions (which is test that otherwise will be done in mitaka) and we will force the execution of the "ng_a" test described earlier, which is originally executed just in newton versions or above.

All tests are performed using an external application named [tripleo-director-ha-test-suite](https://github.com/rscarazz/tripleo-director-ha-test-suite).

Example Playbook
----------------

The main playbook couldn't be simpler:

    ---
    - name:  Validate overcloud HA status
      hosts: localhost
      gather_facts: no
      roles:
        - tripleo-overcloud-validate-ha

But it could also be used at the end of a deployment, like in this file [baremetal-undercloud-validate-ha.yml](https://github.com/openstack/tripleo-quickstart-extras/blob/master/playbooks/baremetal-undercloud-validate-ha.yml).

License
-------

Apache

Author Information
------------------

Raoul Scarazzini <rasca@redhat.com>
