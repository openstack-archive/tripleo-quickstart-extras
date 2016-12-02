#!/usr/bin/env bash
set -eux

### --start_docs

## Set up vxlan networking on subnodes listed in /etc/nodepool/sub_nodes_private
## =============================================================================

## * Create the WORKSPACE variable if it didn't exist already
export WORKSPACE=${WORKSPACE:-$HOME}

while read sub; do

## * Create the expected directories and symlinks
## ::

  ssh $sub mkdir -p $WORKSPACE/tripleo
  ssh $sub ln -sf $WORKSPACE/tripleo $WORKSPACE/tripleo/new

## * Clone the appropriate repositories in the expected locations
## ::

  ssh $sub git clone https://git.openstack.org/openstack-infra/tripleo-ci $WORKSPACE/tripleo/tripleo-ci
  ssh $sub git clone https://git.openstack.org/openstack-dev/devstack $WORKSPACE/tripleo/devstack
  ssh $sub git clone https://git.openstack.org/openstack-infra/devstack-gate $WORKSPACE/tripleo/devstack-gate

done < /etc/nodepool/sub_nodes_private

### --stop_docs
