Virtual Undercloud VS. Baremetal Undercloud
-------------------------------------------

When deploying the overcloud on baremetal nodes, there is the option of using an undercloud
deployed on a baremetal machine or creating a virtual machine (VM) on that same baremetal machine
and using the VM to serve as the undercloud.

The advantages of using a VM undercloud are:

* The VM can be rebuilt and reinstalled without reprovisioning the entire baremetal machine
* The tripleo-quickstart default workflow is written for a Virtual Environment deployment.
  Using a VM undercloud requires less customization of the default workflow.

.. note:: When using a VM undercloud, but baremetal nodes for the overcloud
          deployment, the ``overcloud_nodes`` variable in tripleo-quickstart
          must overwritten and set to empty.

