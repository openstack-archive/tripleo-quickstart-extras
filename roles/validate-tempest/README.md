validate-tempest
================

Ansible role for running tempest tests on undercloud or overcloud.

Requirements
------------

This Ansible role allows to run tempest tests against installed undercloud or overcloud from undercloud.
It can use upstream sources with virtualenv, RDO packages and kolla container image for tempest.

Role Variables
--------------

* `tempest_undercloud`: false/true - whether to run tempest on installed undercloud (default: false)
* `tempest_overcloud`: false/true - whether to run tempest on installed overcloud (default: true)
* `tempest_format`: venv/packages/container - Which tempest installation to use - either install python virtual environment
                    with installed there python modules from requirements file, or to use installed with RDO RPM packages
                    or to use Kolla provided tempest container image (default: packages)
* `tempest_log_file` - name of log file for tempest run (default: tempest_output.log)
* `test_white_regex` - tests regular expression for tempest run, i.e. smoke or tempest.api.object_storage|keystone_tempest_plugin.
* `run_tempest`: false/true - to run tempest or not (default: false)
* `post_tempest`: false/true - to run post processing of tempest results after tempest run
* `tempest_config`: false/true - whether to prepare the script which configures and runs tempest or not (default: true)
* `tempest_whitelist`: list - list of tests you want to be executed. set `skip_file_src`
                       to empty if you don't want to run with blacklist_file option (default: [])
* `skip_file_src`: path to skip tests file, set it empty if running without skip list: `skip_file_src=''`
* `tempest_workers`: int - how many parallel workers to run (default is half the number of cores/threads)
* `tempest_until_failure`: false/true - default is false, repeat the run again and again until failure occurs
* `tempest_exit_on_failure`: true/false - whether to exit from role with tempest exit code (default: true)
* `tempestmail_config`: config.yaml - name of config file for tempestmail script
* `tempestmail_log_server`: <string> - Server where the logs are saved
* `tempest_track_resources`: true/false - whether to save the state of resources after tempest run (default: true)
* `tempest_log_dir`: <directory path> - The directory path where tempest log file is stored (default: /var/log/tempest)
* `tempest_log_file`: <file name> - The name of tempest log file (default: tempest.log)
* `check_tempest_bugs`: true/false - Will check every bugzilla and launchpad bug in the yaml skip file
* `tempest_plugins`: list - List of openstack services tempest plugins to be
                     installed
* `tempest_extra_config`: dict - A dict of tempest configuration which needs to be overridden in tempest.conf,
                          It should be like section.key: value.
* `tempest_conf_removal`: dict - A dict of tempest configuration which will be
                          removed from tempest.conf file.
                          Format: section.key: value
* `public_physical_network`: <string> The name of the border physical network (default: datacentre).
* `tempest_container_registry`: <string> The name of the container registry to use (default: docker.io/tripleomaster)
* `tempest_container_namespace`: <string> The name of tempest container image to use (default: centos-binary-tempest)
* `tempest_container_tag`: <string> The tag of the tempest container image to use (default: current-tripleo)
* `tempest_dir`: <string> The path to tempest workspace directory (default: /home/stack/tempest)
* `tempest_data`: <string> The path to keep tempest related files used for running tempest (default: /home/stack)
* `test_black_regex`: <list> A set of tempest tests to skip (default: [])
* `tempest_version_dict`: <dict> A dict with release name as key and tempest tag version for that release as value
* `tempest_version`: <string> The tempest version to use for running tempest
* `tempest_conf_version_dict`: <dict> A dict with release name as key and python-tempestconf tag version for that release
                               as value
* `tempest_test_image_version`: <float> The version of the cloud image used by tempest for testing
* `tempest_test_image_name`: <string> The name of the cloud image used by tempest for testing
* `tempest_test_image_path`: <Image full path/URL> The full path or url of the cloud image used by tempest for testing
* `floating_ip_cidr`: the network CIDR to be used for a public floating IP network during testing
* `public_net_name`, `public_net_type` : the name and type of the public neutron network, used for floating IPs during
                                          the tempest testing
* `public_net_pool_start`, `public_net_pool_end`, `public_net_gateway`,
  `public_physical_network`, `public_segmentation_id` -- parameters used to create the public floating IP network
* `tempest_deployer_input_file`: <file path> The path to tripleo deployer input file which contains the pre configured
                                 configuration for the deployed cloud using TripleO.
* `tempest_os_cloud`: <string> String name of the cloud to export as OS_CLOUD when using clouds.yaml rather than stackrc
* `tempest_use_headless_chrome`: true/false - whether the headless chrome docker container should be pulled, and run
* `tempest_headless_chrome_port`: <int> - the entrypoint into the headless chrome container


Skip tests file
---------------

Tempest test can be skipped if they are in a skip file, using the whole test
name or a regular expression.
Since the intention is to use the list of skip tests in other parts of
quickstart-extras, it's easier to have this list of skip tests in yaml format
where you can set the skip test, reason and launchpad or bugzilla. This make
easier later to check whether the test still valid or not to be skipped.
Skip files are under roles/validate-tempest/vars/tempest_skip_VERSION.yaml.
In these files you can add a regex, together with a reason, a bugzilla
or launchpad bug and target host (undercloud/overcloud )related to that
particular test. If target host is set `undercloud:true`, it will be skipped
on the undercloud.Launchpad and/or bugzilla re optional, however you must
specify a reason why you are skipping the test.

Example of skip file:

    ---
    known_failures:
      - test: 'tempest.scenario.test_volume_boot_pattern'
        reason: 'rdo-manager tempest smoke test failing on "floating ip pool not found"'
        bz: 'https://bugzilla.redhat.com/show_bug.cgi?id=1272289'
      - test: 'tempest.api.volume.test_volumes_get'
        reason: 'rdo-manager tempest smoke test failing on "floating ip pool not found"'
      - test: 'tempest.api.identity.*v3'
        reason: 'Tempest Identify tests failed on V3 api on OSP-D puddle'
        bz: 'https://bugzilla.redhat.com/show_bug.cgi?id=1266947'
      - test: 'tempest.api.image.v2.test_images_metadefs_namespace_properties.MetadataNamespacePropertiesTest.test_basic_meta_def_namespace_property'
        reason: 'glance is not calling glance-manage db_load_metadefs'
        lp: 'https://bugs.launchpad.net/tripleo/+bug/1664995'
        # Skip list for undercloud
      - test: 'tempest.api.image.v2.test_images_metadefs_namespace_properties.MetadataNamespacePropertiesTest.test_basic_meta_def_namespace_property'
        reason: 'glance is not calling glance-manage db_load_metadefs'
        lp: 'https://bugs.launchpad.net/tripleo/+bug/1664995'
        undercloud: true


Real time bug check
-------------------

If check_tempest_bugs is set to true, a script will be called and will check
in real time, all tests who has a bugzilla or a launchpad bug. This will
generate a new skip file, removing all the bugs that were already closed but
wasn't updated in the yaml skip file yet.



Using validate-tempest role with tripleo-quickstart
---------------------------------------------------

To run tempest with tripleo-quickstart, run the following command:

    $WORKSPACE/tripleo-quickstart

    bash quickstart.sh \
        --bootstrap \
        --tags all \
        --config $WORKSPACE/config/general_config/$CONFIG.yml \
        --working-dir $WORKSPACE/ \
        --no-clone \
        --release master-tripleo-ci \
        --extra-vars test_ping=False \
        --extra-vars run_tempest=True  \
        $VIRTHOST

Note: by using --extra-vars, we can change the validate-tempest role variables.

Dependencies
------------

No dependencies

Example Playbook
----------------

    ---
    - name:  Run tempest
      hosts: undercloud
      gather_facts: no
      roles:
        - validate-tempest

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
