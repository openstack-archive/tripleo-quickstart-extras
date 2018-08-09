ansible-role-tripleo-tht-prep-config
==========================================

An Ansible "meta" role (do not use it on its own, its for imports only) to
prepare TripleO Heat Templates for TripleO deployments with Heat and Ansible.

Requirements
------------

No requirements. The role should only be used via include/import_roles with
tasks_from.

Role Variables
--------------

- `working_dir`: -- the working dir to contain the cloned and checked-out t-h-t. Defined
  in roles/extras-common
- `download_templates_rpm`: if set to true, allow the user to
  download a tripleo-heat-templates rpm package from a url defined by the
  variable `tht_rpm_url`
- `tht_templates_path`: -- the destination path inside of the working dir to clone
  and checkout t-h-t from the given ``tht_templates_repo/_branch/_refspec``.
- `prep_post_hook_script`: if set to a non-empty string, it should be the content
  of a bash script that will be run at the end of the t-h-t preparation configuration step.
  This should only be use in rare case.
- `composable_scenario`: -- controls specific steps for the composable deployments.
- `upgrade_composable_scenario`: -- controls specific steps for the composable updates/upgrades.

Dependencies
------------

None

Example Playbook
----------------

Here is an example tasks snippet for a playbook (omitted the remaining parts):

```yaml
  vars:
    my_custom_tht_script: clone_tht_script.j2.sh
    my_custom_tht_log: clone_tht_script.log
  tasks:
    - name: Prepare custom t-h-t for my super deployment
      include_role:
        name: tht-prep-config
      vars:
        custom_tht_log: "{{ my_custom_tht_log }}"
        custom_tht_script: "{{ my_custom_tht_script }}"
        tht_templates_repo: "{{ my_templates_repo|default('') }}"
        tht_templates_refspec: "{{ my_templates_refspec|default('') }}"
        tht_templates_branch: "{{ my_templates_branch|default('') }}"
        tht_templates_path: "{{ my_templates_path }}"
        download_templates_rpm: "{{ download_my_templates_rpm|default('') }}"
        prep_post_hook_script: "{{ my_prep_post_hook_script|default('') }}"
```

This puts into the current directory `clone-tht-script.sh` j2 rendered from
`clone_tht_script.j2.sh` (it should be placed under `tht-prep-config/templates`),
then executes the script and logs results into `clone_tht_script.log`.

License
-------

Apache 2.0

Author Information
------------------

RDO-CI and Tripleo Deployment Framework teams
