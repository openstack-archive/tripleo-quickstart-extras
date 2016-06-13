ansible-role-tripleo-collect-logs
=================================

An Ansible role for aggregating logs from TripleO nodes.

Requirements
------------

This role gathers logs and debug information from a target system and
gathers the log in a designated directory on the localhost.

The role also takes care of uploading these logs to an rsync server.

Role Variables
--------------

* `artcl_collect_list` -- A list of files and directories to gather from
  the target. Directories are collected recursively. Can include joker
  characters that bash understands. Should be specified as a YaML list,
  e.g.:

```yaml
artcl_collect_list:
    - /etc/nova
    - /home/stack/*.log
    - /var/log
```

* `artcl_collect_dir` -- a local directory where the logs should be
  gathered, without a trailing slash.
* `artcl_gzip_only`: false/true  -- When true, gathered files are gzipped one by
  one in `artcl_collect_dir`, when false, a tar.gz file will contain all the
  logs.
* `artcl_rsync_logs`: true/false -- If true, the role will attempt to rsync logs
  to the target specified by `artcl_rsync_url`. Uses `BUILD_URL`, `BUILD_TAG`
  vars from the environment (set during a Jenkins job run) and requires the
  next to variables to be set.
* `artcl_rsync_url` -- rsync target for uploading the logs. The localhost
  needs to have passwordless authentication to the target or the
  `PROVISIONER_KEY` var specificed in the environment.
* `artcl_artifact_url` -- a HTTP URL at which the uploaded logs will be
  accessible after upload.

Example Playbook
----------------

```yaml
---
- name: Gather logs
  hosts: all:!localhost
  roles:
    - tripleo-collect-logs
```

License
-------

Apache

Author Information
------------------

RDO-CI Team
