multinodes
==========

Provision openstack cloud with subnodes for multinode jobs

Requirements
------------

This Ansible role allows sets up a particular amount of subnodes for reproducing
CI jobs on them.

Role Variables
--------------

* `os_region`: OS region, by default is taken from environment variable OS_REGION_NAME
* `os_tenant`: OS tenant ID, by default is taken from environment variables OS_TENANT_ID
* `os_identity_api_version`: OS identity API version, by default is taken from environment variable OS_IDENTITY_API_VERSION
* `os_password`: OS password, by default is taken from environment variable OS_PASSWORD
* `os_auth_url`: OS auth URL, by default is taken from environment variable OS_AUTH_URL
* `os_username`: OS username, by default is taken from environment variable OS_USERNAME
* `os_tenant_name`: OS tenant name, by default is taken from environment variable OS_TENANT_NAME
* `os_endpoint_type`: OS endpoint type, by default is taken from environment variable OS_ENDPOINT_TYPE
* `prefix`: (default: '') prefix for stack and hosts names
* `remove_previous_stack:`: bool, (default: true) whether to remove previous stack with same name
* `stack_log`: log file for this role
* `key_name`: (default: multinode_admins) keypair name to inject into subnodes, if not present will be
   created from "key_location"
* `private_key_location`: (default: ~/.ssh/id_rsa) users private key
* `key_location`: (default: ~/.ssh/id_rsa.pub) users public key, used for creating keypair
* `stack_name`: (default: multinode_stack) name of Heat stack to create
* `public_net_name:`:  (default: 38.145.32.0/22) name of public network on the cloud
* `private_net_name`: (default: private_net) name of private network in stack
* `private_net_base`: (default:  192.168.54) base IP range for private network
* `private_net_cidr`: (default:  192.168.54.0/24) CIDR for private network
* `private_net_gateway`: (default:  192.168.54.1) gateway address for private network
* `private_net_pool_start`: (default:  192.168.54.5) DHCP pool start for private network
* `private_net_pool_end`: "(default:  192.168.54.150) DHCP pool end for private network
* `subnode_count`: (default: 2) how many nodes to create
* `subnode_flavor`: (default: m1.large) flavor for nodes
* `subnode_groups`: (default: subnodes) ansible host group names for subnodes
* `image_id`: (default: last image from the cloud) Image ID or name in the cloud, by default
   it's image with property "latest" in public images in the cloud

Dependencies
------------

No dependencies

Example Playbook
----------------

    ---
    - name: Multinode
      hosts: localhost
      gather_facts: false
      roles:
        - role: multinodes

For deleting stack it's possible to run playbook with "--tags delete".

License
-------

Apache 2.0

Author Information
------------------

RDO-CI Team
