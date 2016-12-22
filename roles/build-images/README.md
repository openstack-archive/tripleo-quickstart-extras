build-images
============

An Ansible role for building TripleO undercloud and overcloud images. The role
can either operate directly against a host (direct) or setup a build
environment inside of a libvirt guest using libguestfs-tools (isolated).

It starts by creating the overcloud images from the provided yaml files. It
then uses the convert-image role from tripleo-quickstart to turn the
overcloud-full.qcow2 image into an undercloud image. Finally, it injects the
previously created overcloud-full and ironic-python-agent images into this
new undercloud image.

Requirements
------------

* [convert-image](https://git.openstack.org/cgit/openstack/tripleo-quickstart/tree/roles/convert-image) role from tripleo-quickstart (if building an undercloud image)
* [fetch-images](https://git.openstack.org/cgit/openstack/tripleo-quickstart/tree/roles/fetch-images) role from tripleo-quickstart (if using isolated build)
* [modify-image](https://git.openstack.org/cgit/openstack/tripleo-quickstart-extras/tree/roles/modify-image) role from tripleo-quickstart-extras
* [repo-setup](https://git.openstack.org/cgit/openstack/tripleo-quickstart-extras/tree/roles/repo-setup) role from tripleo-quickstart-extras

Role Variables
--------------

* `images_working_dir` -- Directory on the host where images and logs will be
   placed
* `images_destroy_working_dir` -- Whether to destroy the previous image
   directory before starting. (Default true)
* `overcloud_image_build_script` -- Template used for the overcloud image build
* `overcloud_image_build_log` -- Log file for output from the image build
   script.
* `build_image_isolated` -- Whether to use libguestfs to create an isolated
   build environment. (Default true)
* `build_isolation_image_url` -- URL for image to use as the isolated build
   environment. (Currently requires an .md5 file in the same location because
   the fetch-images role from quickstart is used to get the image)
* `build_undercloud` -- Whether to build an undercloud image. (Default true)
* `package_images` -- Whether to create tarballs and md5s for all of the
   produced images. (Default true)
* `overcloud_repo_paths` -- List of repo paths that will be passed to DIB for
   package installs in the overcloud images. These repos will also be copied on
   to the undercloud image.
* `image_build_yaml_paths` -- List of yaml files to be passed to the overcloud
   image build. (Defaults to yamls packaged in tripleo-common)
* `image_build_extract_list` -- List of artifacts to extract from the isolated
   build environment after building.
* `inject_images` -- List of artifacts to inject into the undercloud image

Example Usage
-------------

```yaml
---
- name: Build images using an isolated build environment
  hosts: virthost
  roles:
    - build-images

- name: Build images with repos directly installed on the host
  hosts: virthost
  vars:
    build_image_isolated: false
  roles:
    - build-images

```

License
-------

Apache
