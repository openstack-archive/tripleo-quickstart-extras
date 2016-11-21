ansible-role-tripleo-collect-logs
=================================

An Ansible role for aggregating logs from TripleO nodes.

Requirements
------------

This role gathers logs and debug information from a target system and
collates them in a designated directory, `artcl_collect_dir`, on the localhost.

Additionally, the role will convert templated bash scripts, created and used by
TripleO-Quickstart during deployment, into rST files. These rST files are
combined with static rST files and fed into Sphinx to create user friendly
post-build-documentation specific to an original deployment.

Finally, the role optionally handles uploading these logs to a rsync server or
to an OpenStack Swift object storage. Logs from Swift can be exposed with
[os-loganalyze](https://github.com/openstack-infra/os-loganalyze).

Role Variables
--------------

### Collection related

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

* `artcl_collect_dir` -- A local directory where the logs should be
  gathered, without a trailing slash.
* `artcl_gzip_only`: false/true  -- When true, gathered files are gzipped one
  by one in `artcl_collect_dir`, when false, a tar.gz file will contain all the
  logs.

### Documentation generation related

* `artcl_gen_docs`: true/false -- If true, the role will use build artifacts
  and Sphinx and produce user friendly documentation.
* `artcl_docs_source_dir` -- a local directory that serves as the Sphinx source
  directory.
* `artcl_docs_build_dir` -- A local directory that serves as the Sphinx build
  output directory.
* `artcl_create_docs_payload` -- Dictionary of lists that direct what and how
  to construct documentation.
    * `included_deployment_scripts` -- List of templated bash scripts to be
      converted to rST files.
    * `included_deployment_scripts` -- List of static rST files that will be
      included in the output documentation.
    * `table_of_contents` -- List that defines the order in which rST files
      will be laid out in the output documentation.

```yaml
artcl_create_docs_payload:
  included_deployment_scripts:
    - undercloud-install
    - undercloud-post-install
  included_static_docs:
    - env-setup-virt
  table_of_contents:
    - env-setup-virt
    - undercloud-install
    - undercloud-post-install
```

### Publishing related

* `artcl_publish`: true/false -- If true, the role will attempt to rsync logs
  to the target specified by `artcl_rsync_url`. Uses `BUILD_URL`, `BUILD_TAG`
  vars from the environment (set during a Jenkins job run) and requires the
  next to variables to be set.
* `artcl_use_rsync`: false/true -- use rsync to upload the logs
* `artcl_rsync_use_daemon`: false/true -- use rsync daemon instead of ssh to connect
* `artcl_rsync_url` -- rsync target for uploading the logs. The localhost
  needs to have passwordless authentication to the target or the
  `PROVISIONER_KEY` Var specificed in the environment.
* `artcl_use_swift`: false/true -- use swift object storage to publish the logs
* `artcl_swift_auth_url` -- the OpenStack auth URL for Swift
* `artcl_swift_username` -- OpenStack username for Swift
* `artcl_swift_password` -- password for the Swift user
* `artcl_swift_tenant_name` -- OpenStack tenant name for Swift
* `artcl_swift_container` -- the name of the Swift container to use,
  default is `logs`
* `artcl_swift_delete_after` -- The number of seconds after which Swift will
  remove the uploaded objects, the default is 2678400 seconds = 31 days.
* `artcl_artifact_url` -- a HTTP URL at which the uploaded logs will be
  accessible after upload.
* `artcl_collect_sosreport` -- true/false -- If true, create and collect a
  sosreport for each host.

Example Playbook
----------------

```yaml
---
- name: Gather logs
  hosts: all:!localhost
  roles:
    - tripleo-collect-logs
```

Templated Bash to rST Conversion Notes
--------------------------------------

Templated bash scripts used during deployment are converted to rST files
during the `create-docs` portion of the role's call. Shell scripts are
fed into an awk script and output as restructured text. The awk script
has several simple rules:

1. Only lines between `### ---start_docs` and `### ---stop_docs` will be
  parsed.
2. Lines containing `# nodoc` will be excluded.
3. Lines containing `## ::` indicate subsequent lines should be formatted
  as code blocks
4. Other lines beginning with `## <anything else>` will have the prepended
   `## ` removed. This is how and where general rST formatting is added.
5. All other lines, including shell comments, will be indented by four spaces.

Enabling sosreport Collection
-----------------------------

[sosreport](https://github.com/sosreport/sos) is a unified tool for collecting
system logs and other debug information. To enable creation of sosreport(s)
with this role, create a custom config (you can use centosci-logs.yml
as a template) and ensure that `artcl_collect_sosreport: true` is set.

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
