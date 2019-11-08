validate-tobiko
================

Ansible role for running [Tobiko](https://opendev.org/x/tobiko/)
tests on undercloud or overcloud.

This role should be run on deployed undercloud or overcloud. It may also be run
e.g. after update or upgrade of cloud.
This role supports run on standalone deployment too.
Example of tests which are run by this role are:

* tobiko.tests.scenario.neutron.test_floating_ip - to test connectivity to VM with
  floating IP,
* tobiko.tests.scenario.nova.test_server.ServerStackResourcesTest.test_server - to
  test server actions.

Role Variables
--------------

* `tobiko_config`: false/true - to prepare tobiko's config or not (default: yes)
* `tobiko_run`: false/true - to run tobiko tests or not (default: false)
* `tobiko_envlist`: <string> - The name of tox envlist to be run (default:
                               scenario)
* `tobiko_extra_args`: <string> - Extra arguments to be passed to tobiko tox
                                  command (default: "")
* `tobiko_config_dir`: <string> - directory where tobiko config files will be
                                  stored (default: "{{ working_dir }}/.tobiko")
* `tobiko_config_file`: <string> - name of tobiko config file (default:
                                   "tobiko.conf")
* `tobiko_log_dir`: <string> - directory where tobiko log files will be
                               stored (default: "{{ working_dir }}/.tobiko")
* `tobiko_log_file`: <string> - name of tobiko log file (default: "tobiko.log")
* `tobiko_key_file_name`: <string> - path to ssh key used by tobiko in tests
                                     (default: "~/.ssh/id_rsa")
* `tobiko_floating_ip_network`: <string> - name of floating IP network used by
                                           tobiko in tests (default: "public")
* `public_network_type`: <string> - type of public neutron network used for floating
                                    IPs during tobiko testing (default: flat)
* `public_network_pool_start`: <string> - neutron public network allocation pool start
                                          (default: {{ floating_ip_cidr|nthhost(100) }})
* `public_network_pool_end`: <string> - neutron public network allocation pool end
                                        (default: {{ floating_ip_cidr|nthhost(120) }})
* `public_network_gateway`: <string> - gateway IP for neutron public network, when
                                       not set, neutron will choose it automatically
                                       (default: {{ floating_ip_cidr|nthhost(1) }})
* `public_physical_network`: <string> - name of physical network used in neutron for public
                                        network (default: datacentre)
* `public_segmentation_id`: <string> - segmentation_id for neutron public network
                                       (default: '')
* `floating_ip_cidr`: <string> - the network CIDR to be used for a public floating IP
                                 network during testing (default: {{ undercloud_network_cidr }})


Using validate-tobiko role with tripleo-quickstart
---------------------------------------------------

To run tobiko with tripleo-quickstart, run the following command:

    $WORKSPACE/tripleo-quickstart

    bash quickstart.sh \
        --tags all \
        --no-clone \
        --release master \
        --extra-vars run_tobiko=True  \
        $VIRTHOST

Note: by using --extra-vars, we can change the validate-tobiko role variables.

Example Playbook
----------------

    ---
    - name:  Run tobiko
      hosts: undercloud
      gather_facts: false
      roles:
        - validate-tobiko

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
