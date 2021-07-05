modify-image
============

An Ansible role for modifying an image via the libguestfs tool, virt-customize.
The role requires an image and a script to run inside of that image via
virt-customize. It also has paramaters for how much memory and cpu to give
the virt-customize VM, and a list of artifacts to copy out of the VM after
running the script. The script will always produce a log of the same name as
the script with .log appended. This can be extracted via the
`modify_image_extract_list` variable.

Requirements
------------

* [libguestfs](http://libguestfs.org/)

Role Variables
--------------

* `image_to_modify` -- the image that virt-customize will operate on
* `modify_script` -- the script that will be run inside the image
* `modify_image_upload_files` -- list of src/dest of files to upload to image
  (files are uploaded before running the script)
* `modify_image_install_packages` -- list of packages to install in the image
  (packages are installed before running the script)
* `modify_image_extract_list` -- list of artifacts to extract after the image
   is modified
* `modify_image_working_dir` -- directory containing image and script. This is
   also where extracted files and logs will end up.
* `modify_image_vc_ram` -- amount of RAM to give the virt-customize VM (in MB)
* `modify_image_vc_cpu` -- number of CPUs to give the virt-customize VM
* `modify_image_vc_verbose` -- whether to run virt-customize with verbose flag
* `modify_image_vc_trace` -- whether to run virt-customize with trace flag
* `modify_image_vc_root_password` -- password for the root account of the image
  (useful for baremetal envs)

Example Usage
-------------

```yaml
---
- name: |
    Run a script inside an image via virt-customize without extracting anything
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/undercloud.qcow2"
    modify_script: "{{ working_dir }}/undercloud_convert.sh"
  roles:
    - modify-image

- name: Run a script inside an image and extract the log from the script
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/undercloud.qcow2"
    modify_script: "{{ working_dir }}/undercloud_convert.sh"
    modify_image_extract_list:
      - /tmp/builder.log
  roles:
    - modify-image

- name: Run a script inside an image that needs to have lots of resources
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/undercloud.qcow2"
    modify_script: "{{ working_dir }}/undercloud_convert.sh"
    modify_image_vc_cpu: 8
    modify_image_vc_ram: 16384
  roles:
    - modify-image

- name: Run a script inside an image with virt-customize in verbose mode
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/undercloud.qcow2"
    modify_script: "{{ working_dir }}/undercloud_convert.sh"
    modify_image_verbose: true
  roles:
    - modify-image

- name: Upload files to image
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/undercloud.qcow2"
    modify_image_upload_files:
      - src: /tmp/file_to_upload.tar.gz
        dest: /home/user/renamed_file.tar.gz
      - src: /home/local_user/file
        dest: /home/image_user/
  roles:
    - modify-image

- name: Upload files to image and run script
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/undercloud.qcow2"
    modify_image_upload_files:
      - src: /tmp/file_to_upload.tar.gz
        dest: /home/user/renamed_file.tar.gz
      - src: /home/local_user/file
        dest: /tmp/
    modify_script: "{{ working_dir }}/undercloud_convert.sh"
  roles:
    - modify-image

- name: Install packages in the image
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/{{ overcloud_image }}.qcow2"
    modify_image_install_packages:
      - 'package_to_be_installed_1'
      - 'package_to_be_installed_2'
      - 'package_to_be_installed_3'
  include_role:
    name: modify-image

- name: Upload an RPM file and install it in the image
  hosts: virthost
  vars:
    image_to_modify: "{{ working_dir }}/{{ overcloud_image }}.qcow2"
    modify_image_upload_files:
      - src: "/tmp/rpm_to_be_uploaded.rpm"
        dest: /root/rpm_to_be_installed.rpm
    modify_image_install_packages:
      - '/root/rpm_to_be_installed.rpm'
  include_role:
    name: modify-image

```

License
-------

Apache
