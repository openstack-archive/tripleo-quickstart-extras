snapshot-libvirt
================

An Ansible role for snapshotting a libvirt environment using
external snapshots with backing files.

The role will shutdown all of the VMs specified in the
overcloud_nodes list, then proceed with either creating or
restoring a previous snapshot depending on the settings for
snapshot_create and snapshot_restore. The default is to
do nothing since both of these operations are potentially
destructive.

When run with snapshot_create=true, the role will check if
there is already a backing file. If one exists, it will
commit all new changes to that backing file. If there is
not already a backing file, the role will create one, and
make an empty snapshot pointing to it.

When run with snapshot_restore=true, the role will delete
the current snapshot and create an empty snapshot pointing
to the backing file.

Limitations
-----------

- This role does not currently support any "management" of snapshots,
  i.e. there is only one maintained.
- The role uses qemu-img directly to create the snapshots, this means
  the snapshots will not show up with commands like `virsh-snapshot`
- The role does not currently implement any method to remove the backing
  files. This means when starting over from scratch, these *.bak files
  will need to be manually deleted (if reusing the same libvirt_volume_path).

Example Usage
-------------

```yaml
---
- name:  Create a snapshot (or update a snapshot)
  hosts: virthost
  gather_facts: yes
  vars:
    - snapshot_create: true
    - libvirt_volume_path: /opt/vm_images
    - libvirt_uri: qemu:///system
    - overcloud_nodes:
      - name: subnode-0
      - name: subnode-1
  roles:
    - snapshot-libvirt
  become: true

- name:  Restore a snapshot
  hosts: virthost
  gather_facts: yes
  vars:
    - snapshot_restore: true
    - libvirt_volume_path: /opt/vm_images
    - libvirt_uri: qemu:///system
    - overcloud_nodes:
      - name: subnode-0
      - name: subnode-1
  roles:
    - snapshot-libvirt
  become: true
```

License
-------

Apache
