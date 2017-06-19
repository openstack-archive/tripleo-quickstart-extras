validate-simple
===============

This role uses heat templates from
[THT](http://git.openstack.org/cgit/openstack/tripleo-heat-templates/)
to validate an OpenStack installation. By default it does a ping test between
two OpenStack instances.

Role Variables
--------------

For the defaults of these variables, see the defaults/main.yml file in this role.

* `tenantrc` -- file containing the auth variables for the cloud
* `validate_script` -- the jinja template used to create the validation script
* `validate_template_path` -- path where the heat templates can be found
* `validate_template` -- the filename of the heat template used for validation
* `validate_log` -- file to log the output of the validation script
* `validate_stack_name` -- the name of the heat stack used for validation
* `validate_success_status` -- output that signifies successful stack creation
* `validate_image_file` -- name of downloaded image file
* `validate_image_path` -- path to existing image file on disk
* `validate_image_url` -- URL to the image files (without the filenames)
* `image_disk`, `image_initramfs`, `image_kernel` -- name of the disk image,
  initramfs and kernel on the previous URL
* `validate_image_name` -- the name used in glance for the assembled image from
  the previous files
* `validate_image_dir` -- directory to store the downloaded images
* `release` -- release of the cloud to be validated (mitaka, newton, etc.);
  older releases use different heat commands
* `floating_ip_cidr` -- the network CIDR to be used for a public floating IP
  network during testing
* `public_net_name`, `public_net_type` -- the name and type of the public
  neutron network, used for floating IPs during the validation
* `public_net_pool_start`, `public_net_pool_end`, `public_net_gateway`,
  `public_physical_network`, `public_segmentation_id` -- parameters used to
  create the public floating IP network
* `validate_template_environment`: used to override variables inside the
  validation template, passed as an environment file to heat
* `skip_pingtest_cleanup`: false/true - whether to skip pingtest stack deletion
  or not (default is false)

Dependencies
------------

The role uses heat templates from the tripleo-heat-templates package/repository
and downloads Cirros images during the run.

Example Playbook
----------------

```yaml
---
- name: Validate the overcloud
  hosts: undercloud
  roles:
    - validate-simple
```

License
-------

Apache 2.0

Author Information
------------------

OpenStack
