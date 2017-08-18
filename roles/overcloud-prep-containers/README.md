overcloud-prep-containers
=========

This role that prepares an environment for a containerized compute is under active development along
with active development of the containerized computer feature itself.

This role walks through the developer setup for a tripleo deployment with a containerized compute.
The developer documentation can be found here: https://etherpad.openstack.org/p/tripleo-containers-work

The instructions below use the master branch from delorean that has been vetted by CI, and then updates
any tripleo rpm to the latest version available from delorean.  It should be the same content as what
currently runs in tripleo-ci

This also git checks out https://git.openstack.org/openstack/tripleo-heat-templates
with refspec: refs/changes/59/330659/43 , this can be updated in config/general_config/containers_minimal.yml


Requirements
------------

https://github.com/openstack/tripleo-quickstart/blob/master/README.rst


overcloud-prep-containers variables
--------------

* working_dir: /home/stack
* containerized_overcloud: false
* overcloud_prep_containers_script: overcloud-prep-containers.sh.j2
* overcloud_prep_containers_log: overcloud_prep_containers.log
* undercloud_network_cidr: 192.168.24.0/24
* prepare_service_env_args: -e {{ overcloud_templates_path }}/environments/docker.yaml

overcloud-prep-config variables
-------------------------------

* overcloud_templates_path: /home/stack/tripleo-heat-templates
* overcloud_templates_repo: https://git.openstack.org/openstack/tripleo-heat-templates
* overcloud_templates_branch: master


tripleo-quickstart variables
----------------------------

* see config/general_config/containers_minimal.yml



Dependencies
------------

These dependencies are accounted for in the unmerged tripleo-quickstart review https://review.openstack.org/#/c/393348/

* Depends-On: https://review.openstack.org/#/c/393348/
* Depends-On: https://review.gerrithub.io/#/c/300328/

How to Execute:
---------------
Review https://github.com/openstack/tripleo-quickstart/blob/master/README.rst::

    mkdir quickstart_containers
    export WORKSPACE=$PWD/quickstart_containers
    cd $WORKSPACE
    git clone https://github.com/openstack/tripleo-quickstart.git
    git clone https://github.com/openstack/tripleo-quickstart-extras.git

    # Update quickstart to use the right review
    pushd tripleo-quickstart
    git remote add gerrit https://review.openstack.org/openstack/tripleo-quickstart
    git fetch --all
    git review -d I676b429cab920516a151b124fca2e26dd5c5e87b
    popd

    # Update quickstart-extras to use the right review
    pushd tripleo-quickstart-extras
    git remote add gerrit https://review.openstack.org/openstack/tripleo-quickstart-extras
    git fetch --all
    git-review -d Id91cfae8aff8652222a4e9adab0635be6c0f8f64
    git-review -x Ie1ca08de17ff0fddd9c9cbd124ae65735ea4b6bc
    popd

    mkdir /var/tmp/containers
    export WD=/var/tmp/containers
    export VIRTHOST=<virthost>

    pushd tripleo-quickstart
    sed -i "s|git+https://git.openstack.org/openstack|file://$WORKSPACE|g" quickstart-extras-requirements.txt

    ./quickstart.sh --no-clone --working-dir $WD --teardown all --requirements quickstart-extras-requirements.txt --playbook quickstart-extras.yml --config $PWD/config/general_config/containers_minimal.yml --tags all  --release master-tripleo-ci $VIRTHOST

How to Execute with Additional gerrit reviews
---------------------------------------------

This will install a local delorean instance and build the reviews into the undercloud/overcloud
Example change https://review.openstack.org/#/c/396460/

STEPS::

    export GERRIT_HOST=review.openstack.org
    export GERRIT_BRANCH=master
    export GERRIT_CHANGE_ID=396460
    export GERRIT_PATCHSET_REVISION=3ea99ef27f60157699c13acb64f88d2cd03d237b

    # Note.. FOR RHEL VIRTHOST's
    * ensure mock is installed on the virthost *, for rhel it comes from epel.. then remove the epel repo

    # Build the yum repo in  /home/stack of the $VIRTHOST
    ./quickstart.sh \
    --no-clone \
    --working-dir $WD \
    --teardown all \
    --requirements quickstart-extras-requirements.txt \
    --playbook dlrn-gate.yml \
    --config $PWD/config/general_config/containers_minimal.yml \
    --extra-vars compressed_gating_repo="/home/stack/gating_repo.tar.gz" \
    --tags all  \
    --release master-tripleo-ci \
    $VIRTHOST

    # Consume the local delorean repo in addition to the normal deployment
    ./quickstart.sh \
    --no-clone \
    --working-dir $WD \
    --teardown none \
    --retain-inventory \
    --requirements quickstart-extras-requirements.txt \
    --playbook quickstart-extras.yml \
    --config $PWD/config/general_config/containers_minimal.yml \
    --extra-vars compressed_gating_repo="/home/stack/gating_repo.tar.gz" \
    --skip-tags provision \
    --tags all  \
    --release master-tripleo-ci \
    $VIRTHOST
