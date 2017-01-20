Virtual Environment
===================

|project| Quickstart can be used in a virtual environment using virtual machines instead
of actual baremetal. However, one baremetal machine ( VIRTHOST ) is still
needed to act as the host for the virtual machines.


Minimum System Requirements
---------------------------

By default, this setup creates 3 virtual machines:

* 1 Undercloud
* 1 Overcloud Controller
* 1 Overcloud Compute

.. note::
   Each virtual machine must consist of at least 4 GB of memory and 40 GB of disk
   space.
   The virtual machine disk files are thinly provisioned and will not take up
   the full 40GB initially.

You will need a baremetal host machine (referred to as ``$VIRTHOST``) with at least
**16G** of RAM, preferably **32G**, and you must be able to ``ssh`` to the
virthost machine as root without a password from the machine running ansible.
Currently the virthost machine must be running a recent Red Hat-based Linux
distribution (CentOS 7, RHEL 7, Fedora 22 - only CentOS 7 is currently tested),
but we hope to add support for non-Red Hat distributions too.

|project| Quickstart currently supports the following operating systems:

* CentOS 7 x86_64

TripleO Quickstart
------------------

TripleO Quickstart is a fast and easy way to setup and configure your virtual environment for TripleO.
Further documentation can be found at https://github.com/openstack/tripleo-quickstart

A quick way to test that your virthost machine is ready to rock is::

    ssh root@$VIRTHOST uname -a

Getting the script
^^^^^^^^^^^^^^^^^^

You can download the `quickstart.sh` script with `wget`::

    wget https://raw.githubusercontent.com/openstack/tripleo-quickstart/master/quickstart.sh

Install the dependencies
^^^^^^^^^^^^^^^^^^^^^^^^

You need some software available on your local system before you can run
`quickstart.sh`. You can install the necessary dependencies by running::

    bash quickstart.sh --install-deps

Setup your virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Deploy with the most basic default options virtual environment by running::

    bash quickstart.sh $VIRTHOST

There are many configuration options available in
tripleo-quickstart/config/general_config/ and also in
tripleo-quickstart-extras/config/general_config/
In the examples below the ha.yml config is located in the tripleo-quickstart repository
and the containers_minimal.yml is located in the tripleo-quickstart-extras repository.
All the configuration files will be installed to your working_directory.

This does require the user to know what the working directory is set to. The variable OPT_WORKDIR
by default is ~/.quickstart but can be overriden with -w or --working_dir

Please review these options and use the appropriate configuration for your deployment.

Below are some examples.::

    bash quickstart.sh --config=~/.quickstart/config/general_config/ha.yml $VIRTHOST
    bash quickstart.sh --config=~/.quickstart/config/general_config/containers_minimal.yml $VIRTHOST
