Copying over customized instackenv.json, network-environment.yaml, nic-configs
------------------------------------------------------------------------------

instackenv.json
^^^^^^^^^^^^^^^

``instackenv.json`` file is generated from a template in tripleo-quickstart:
<https://github.com/openstack/tripleo-quickstart/blob/master/roles/libvirt/setup/overcloud/tasks/main.yml#L91>.
A customized ``instackenv.json`` can be copied to the undercloud by overwriting the
``undercloud_instackenv_template`` variable with the path to the customized file.

Below is an explanation of, and example of, the ``instackenv.json`` file:

The JSON file describing your Overcloud baremetal nodes, is called
``instackenv.json``. The file should contain a JSON object with the only field
``nodes`` containing list of node descriptions.

Each node description should contains required fields:

* ``pm_type`` - driver for Ironic nodes, see `Ironic Drivers`_ for details

* ``pm_addr`` - node BMC IP address (hypervisor address in case of virtual
  environment)

* ``pm_user``, ``pm_password`` - node BMC credentials

Some fields are optional if you're going to use introspection later:

* ``mac`` - list of MAC addresses, optional for bare metal

* ``cpu`` - number of CPU's in system

* ``arch`` - CPU architecture (common values are ``i386`` and ``x86_64``)

* ``memory`` - memory size in MiB

* ``disk`` - hard driver size in GiB

It is also possible (but optional) to set Ironic node capabilities directly
in the JSON file. This can be useful for assigning node profiles or setting
boot options at registration time:

* ``capabilities`` - Ironic node capabilities.  For example::

    "capabilities": "profile:compute,boot_option:local"

For example::

    {
        "nodes": [
            {
                "pm_type":"pxe_ipmitool",
                "mac":[
                    "fa:16:3e:2a:0e:36"
                ],
                "cpu":"2",
                "memory":"4096",
                "disk":"40",
                "arch":"x86_64",
                "pm_user":"admin",
                "pm_password":"password",
                "pm_addr":"10.0.0.8"
            },
            {
                "pm_type":"pxe_ipmitool",
                "mac":[
                    "fa:16:3e:da:39:c9"
                ],
                "cpu":"2",
                "memory":"4096",
                "disk":"40",
                "arch":"x86_64",
                "pm_user":"admin",
                "pm_password":"password",
                "pm_addr":"10.0.0.15"
            },
            {
                "pm_type":"pxe_ipmitool",
                "mac":[
                    "fa:16:3e:51:9b:68"
                ],
                "cpu":"2",
                "memory":"4096",
                "disk":"40",
                "arch":"x86_64",
                "pm_user":"admin",
                "pm_password":"password",
                "pm_addr":"10.0.0.16"
            }
        ]
    }


network-environment.yaml
^^^^^^^^^^^^^^^^^^^^^^^^

Similarly, the ``network-environment.yaml`` file is generated from a template,
<https://github.com/openstack/tripleo-quickstart/blob/master/roles/tripleo/undercloud/tasks/post-install.yml#L32>
A customized ``network-environment.yaml`` file can be copied to the undercloud by overwriting the
`` network_environment_file`` variable with the path to the customized file.

nic-configs
^^^^^^^^^^^

By default, the virtual environment deployment uses the standard nic-configs files are there is no
ready section to copy custom nic-configs files.
The ``ansible-role-tripleo-overcloud-prep-config`` repo includes a task that copies the nic-configs
files if they are defined,
<https://github.com/redhat-openstack/ansible-role-tripleo-overcloud-prep-config/blob/master/tasks/main.yml#L15>

