Install the dependencies
------------------------

You need some software available on your local system before you can run
`quickstart.sh`. You can install the necessary dependencies by running:

::

    bash quickstart.sh --install-deps

Setup your virtual environment
------------------------------

tripleo-quickstart includes steps to set up libvirt on the undercloud host
machine and to create and setup the undercloud VM.

Deployments on baremetal hardware require steps from third-party repos,
in addition to the steps in tripleo-quickstart.
Below is an example of a complete call to quickstart.sh to run a full deploy
on baremetal overcloud nodes:

::

    # $HW_ENV_DIR is the directory where the baremetal environment-specific
    # files are stored

    pushd $WORKSPACE/tripleo-quickstart
    bash quickstart.sh \
        --ansible-debug \
        --bootstrap \
        --working-dir $WORKSPACE/ \
        --tags all \
        --no-clone \
        --teardown all \
        --requirements quickstart-role-requirements.txt \
        --requirements $WORKSPACE/$HW_ENV_DIR/requirements_files/$REQUIREMENTS_FILE \
        --config $WORKSPACE/$HW_ENV_DIR/config_files/$CONFIG_FILE \
        --extra-vars @$WORKSPACE/$HW_ENV_DIR/env_settings.yml \
        --playbook $PLAYBOOK \
        --release $RELEASE \
        $VIRTHOST
    popd

