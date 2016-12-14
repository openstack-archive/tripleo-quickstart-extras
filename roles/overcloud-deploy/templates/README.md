Overcloud ansible templates
===========================

overcloud_services jinja template
---------------------------------

The overcloud_services jinja template is taking a dictionary from the default
variable `overcloud_services`.
The dictionary is composed by: nodes and services.
Those value would build the heat environment file required for deploying
the overcloud with the specify services.

Example: if you want to deploy only keystone, just override the
overcloud_services variable in a yaml file with:

overcloud_services:
  - name: 'ControllerServices:'
    services:
    - OS::TripleO::Services::Kernel
    - OS::TripleO::Services::Keystone
    - OS::TripleO::Services::RabbitMQ
    - OS::TripleO::Services::MySQL
    - OS::TripleO::Services::HAproxy
    - OS::TripleO::Services::Keepalived
    - OS::TripleO::Services::Ntp
    - OS::TripleO::Services::Timezone
    - OS::TripleO::Services::TripleoPackages

Or with keystone and nova:

overcloud_services:
  - name: 'ControllerServices:'
    services:
    - OS::TripleO::Services::Kernel
    - OS::TripleO::Services::Keystone
    - OS::TripleO::Services::RabbitMQ
    - OS::TripleO::Services::MySQL
    - OS::TripleO::Services::HAproxy
    - OS::TripleO::Services::Keepalived
    - OS::TripleO::Services::Ntp
    - OS::TripleO::Services::Timezone
    - OS::TripleO::Services::TripleoPackages
  - name: 'ComputeServices:'
    services:
    - OS::TripleO::Services::NovaCompute
