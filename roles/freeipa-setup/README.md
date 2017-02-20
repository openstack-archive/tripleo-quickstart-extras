FreeIPA Setup
=============

An Ansible role to setup a FreeIPA server

Requirements
------------

This role requires a running host to deploy FreeIPA

Role Variables
--------------

- `freeipa_hostname`: <'ipa.tripleodomain'> -- Hostname for the FreeIPA server
- `freeipa_ip`: <'192.168.24.250'> -- IP for the the FreeIPA server
- `directory_manager_password`: <string> -- Password for the directory manager
- `freeipa_admin_password`: <string> -- FreeIPA server admin password
- `undercloud_fqdn`: <'undercloud.tripleodomain'> -- FQDN for the undercloud
- `provisioning_cidr`: <'{{ freeipa_ip }}/24'> -- If set, it adds the given CIDR to the
provisioning interface (which is hardcoded to eth1)
- `supplemental_user`: <stack> The user which is used to deploy FreeIpa on the supplemental node

Example Playbook
----------------

Sample playbook to call the role

```yaml
# Deploy the FreeIPA Server
- name:  Deploy FreeIPA
  hosts: freeipa_host
  gather_facts: no
  roles:
    - freeipa-setup
```
