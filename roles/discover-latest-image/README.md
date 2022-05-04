Role Name
=========

An Ansible role to discover latest Centos image.

Requirements
------------

This role is currently written for Centos-9 and can be extended to Centos-8 on need basis.

Role Variables
--------------

* base_url: <https://cloud.centos.org/centos/{{ ansible_distribution_major_version }}-stream/x86_64/images/> Base Url from where we can pull the Centos Image.
* qcow_prefix: <CentOS-Stream-GenericCloud-> Qcow2 image prefix on base_url which will be used as a filter to find latest Centos Image.


Example Playbook
----------------

  1. Sample playbook to call the role

    - name: Discover latest CentOS qcow2 image
      include_role:
        name: discover-latest-image

  2. Sample config to use the facts from discover-latest-image

    - name: set_fact for undercloud base image
      set_fact:
        baseos_undercloud_image_url: "{{ discovered_image_url }}"
        baseos_image: "{{ ansible_distribution | lower }}"
        baseos_image_type: qcow2
        baseos_md5sum: "{{ discovered_md5sum }} {{ discovered_image_name }}"
        cacheable: true
