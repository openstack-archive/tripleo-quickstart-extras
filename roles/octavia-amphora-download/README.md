Octavia-amphora-download
========================

An Ansible role to download Octavia amphora images to be used in CI or scripted deployments.

Requirements
------------

This playbook expects a supported version of Ansible and working Internet access.

Role Variables:
---------------

- octavia_amphora_path -- full path for the downloaded amphora image.
- amphora\_url -- url of image to download. If not provided a default location based on branch is used.

Dependenncies
-------------

No dependencies

Example Playbook
----------------

Download the amphora image for the stein branch to foo's home directory:

  - hosts: undercloud
    vars:
      release: "stein"
      target_dir: "/home/foo"
    roles:
      - octavia-amphora-dowload


License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
