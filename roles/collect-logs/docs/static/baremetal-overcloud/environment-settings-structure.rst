Settings for hardware environments
==================================

Throughout the documentation, there are example settings and custom files to
overwrite the virt defaults in TripleO Quickstart. It is recommended to use a
organized directory structure to store the settings and files for each hardware
environment.

Example Directory Structure
---------------------------

Each baremetal environment will need a directory structured as follows:

|-- environment_name
|    |-- instackenv.json
|    |-- vendor_specific_setup
|    |-- <architecture diagram/explanation document>
|    |-- network_configs
|    |    |--<network-islation-type-1>
|    |    |    |-- <network-environment.yaml file>
|    |    |    |-- env_settings.yml
|    |    |    |-- nic_configs
|    |    |    |    |-- ceph-storage.yaml
|    |    |    |    |-- cinder-storage.yaml
|    |    |    |    |-- compute.yaml
|    |    |    |    |-- controller.yaml
|    |    |    |    |-- swift-storage.yaml
|    |    |    |-- config_files
|    |    |    |    |--config.yml
|    |    |    |    |--<other config files>
|    |    |    |-- requirements_files
|    |    |    |    |--requirements1.yml
|    |    |    |    |--requirements2.yml
|    |    |--<network-islation-type-2>
|    |    |    |-- <network-environment.yaml file>
|    |    |    |-- env_settings.yml
|    |    |    |-- nic_configs
|    |    |    |    |-- ceph-storage.yaml
|    |    |    |    |-- cinder-storage.yaml
|    |    |    |    |-- compute.yaml
|    |    |    |    |-- controller.yaml
|    |    |    |    |-- swift-storage.yaml
|    |    |    |-- config_files
|    |    |    |    |--config.yml
|    |    |    |    |--<other config files>
|    |    |    |-- requirements_files
|    |    |    |    |--requirements1.yml
|    |    |    |    |--requirements2.yml


Explanation of Directory Contents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 - instackenv.json (required)

    The instackenv.json file added at this top-level directory will replace the templated instackenv.json file for virt deployments.

 - vendor_specific_setup (optional)

   If any script needs to run to do environment setup before deployment, such as RAID configuration, it can be included here.

 - architecture diagram (optional)

    Although not required, if there is a diagram or document detailing the network architecture, it is useful to include that document or diagram here as all the settings and network isolation files will be based off of it.

 - network_configs (required)

    This directory is used to house the directories divided by network isolation type.

 - network-isolation-type (required)

    Even if deploying without network isolation, the files should be included in a 'none' directory.
    There are files examples of the following network isolation types: single-nic-vlans, multiple-nics, bond-with-vlans, public-bond, none [1].
    Network isolation types 'single_nic_vlans', 'bond_with_vlans', 'multi-nic' will be deprecated.

    [1] Names are derived from the `tripleo-heat-templates configuration <https://github.com/openstack/tripleo-heat-templates/tree/master/network/config>`_

 - network-environment.yaml (required, unless deploying with no network isolation)

    This file should be named after the network-isolation type, for example:  bond_with_vlans.yaml. This naming convention follows the same pattern used by the default, virt workflow.

 - env_settings.yaml (required)

    This file stores all environment-specific settings to override default settings in TripleO quickstart and related repos, for example: the location of instackenv.json file, and setting 'overcloud_nodes' to empty so that quickstart does not create VMs for overcloud nodes. All settings required for undercloud.conf are included here.

 - nic_configs (optional)

    If the default nic-config files are not suitable for a particular hardware environment, specific ones can be added here and copied to the undercloud. Ensure that the network-environment.yaml file points to the correct location for the nic-configs to be used in deploy.

 - config_files (required)

    The deployment details are stored in the config file. Different config files can be created for scaling up nodes, HA, and other deployment combinations.

 - requirements_files (required)

   Multiple requirements files can be passed to quickstart.sh to include additional repos. For example, to include IPMI validation, the requirements files would need to include are `here <https://github.com/redhat-openstack/ansible-role-tripleo-validate-ipmi>`_

