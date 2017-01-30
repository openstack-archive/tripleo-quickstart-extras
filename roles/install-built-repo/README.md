install-built-repo
==================

Install built packages on host and/or within the image.
This Ansible role allows installation of packages which were built by DLRN
 on a live host or within an image.

Requirements
------------

No requirements.

Role Variables
--------------

* `ib_repo_install_script` - path to repositories install script template
* `ib_repo_install_log` - path to repositories install script log
* `ib_repo_run_live`: false/true - where to run repo install script on host (live host that playbook runs on it) (default: true)
* `ib_gating_repo_enabled`: true/false - whether to enable built repo or not (default: true)
* `ib_repo_file_path`: path to compressed repo built by `build-test-packages` role
* `ib_repo_image_inject`: false/true - where to inject and run repo install script on specified image (default: false)
* `ib_repo_image_path`: path to image, in case of injecting repositories into the image
* `ib_repo_host`: host where built repo exists, if it's not the same host where this roles runs

Dependencies
------------
* `modify-image` role in TripleO Quickstart extras repository


Example Playbook
----------------

Including an example of how to use this role

    ---
    - name:  Run repo install
      hosts: undercloud
      gather_facts: no
      roles:
        - install-built-repo

    - name:  Run repo install
      hosts: undercloud
      gather_facts: no
      vars:
        ib_repo_image_inject: true
        ib_repo_image_path: "{{ working_dir }}/overcloud-full.qcow2"
      roles:
        - install-built-repo


License
-------

Apache 2.0

Author Information
------------------

OpenStack
