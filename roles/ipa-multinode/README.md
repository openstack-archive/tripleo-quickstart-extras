ipa-multinode
=============

An Ansible role to install and configure a two-node setup where
the IPA server is running on the secondary node and a standalone
deployment is run on the primary node.

Requirements
------------

* https://opendev.org/x/tripleo-ipa

Role Variables
--------------

* `freeipa_internal_ip` -- IP for the FreeIPA server
* `standalone_hostname` -- Hostname for secondary node
* `freeipa_server_hostname` -- Hostname for the FreeIPA server
* `overcloud_cloud_name` -- Cloud name for overcloud
* `overcloud_cloud_domain` -- Cloud domain for overcloud
* `overcloud_cloud_name_internal` -- Internal name for overcloud
* `overcloud_cloud_name_storage` -- Storage cloud name for overcloud
* `overcloud_cloud_name_storage_management` -- Storage namangement cloud name for overcloud
* `overcloud_cloud_name_ctlplane` -- Controlplane cloud name for overcloud
* `freeipa_admin_password` -- FreeIPA server admin password
* `enable_tls` -- Boolean value if FreeIPA server will be used in the deployment
* `ipa_domain` -- IPA domain name
* `cloud_domain` -- IPA cloud domain name
* `ipa_nameserver` -- IPA name server
* `ipa_realm` -- IPA realm
* `freeipa_directory_password` -- Password for the directory manager
* `freeipa_principal` -- FreeIPA principal
* `undercloud_cloud_domain` -- Undercloud cloud domain
* `tls_packages` -- TLS dependacy packages
* `ipa_packages` -- FreeIPA packages

Example Usage
-------------

```yaml
---
- name: Setup the IPA server
  hosts: subnode-1
  tags:
    - standalone
  tasks:
    - include_role:
        name: ipa-multinode
        tasks_from: ipaserver-subnode-install.yml

- name: Setup the undercloud for IPA server
  hosts: undercloud
  tags:
    - standalone
  tasks:
    - include_role:
        name: ipa-multinode
        tasks_from: ipaserver-undercloud-setup.yml
```

License
-------

Apache

Author Information
------------------

TripleO-CI Team
