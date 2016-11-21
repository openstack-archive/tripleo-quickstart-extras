Additional steps preparing the environment for deployment
---------------------------------------------------------

Depending on the parameters of the baremetal overcloud environment in use,
other pre-deployment steps may be needed to ensure that the deployment succeeds.
<https://github.com/redhat-openstack/ansible-role-tripleo-overcloud-prep-baremetal/tree/master/tasks>
includes a number of these steps. Whether each step is run, depends on variable values
that can be set per environment.

Some examples of additional steps are:

- Adding disk size hints
- Adjusting MTU values
- Rerunning introspection on failure

