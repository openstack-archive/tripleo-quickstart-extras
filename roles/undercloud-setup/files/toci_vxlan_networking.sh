#!/usr/bin/env bash
set -eux

### --start_docs

## Setup the environment and networking for devstack-gate
## ======================================================

## .. note::
##   The following steps are needed:
##   * Create the environment that tripleo-ci/devstack-gate expects
##   * Clone tripleo-ci and run its multinode-setup script.
##   * Set up VXLAN tunnel networking based on the scripts located in devstack-gate.

## Prepare Your Environment
## ------------------------

## * Set the environment variables for tripleo-ci to function
## ::

export TRIPLEO_ROOT=${WORKSPACE}/tripleo
export BASE=${WORKSPACE}/tripleo

## * Create and enter the tripleo directory
## ::

mkdir -p ${WORKSPACE}/tripleo

cd ${WORKSPACE}/tripleo

## * Create a symlink to 'new'.

## .. note::
##    This is required to satisfy devstack-gate/functions.sh:ovs_vxlan_bridge()'s
##    requirement for the directory $BASE/new to exist as it sources
##    $BASE/new/devstack/functions-common for the install_package and
##    restart_service functions.
## ::

ln -sf ${WORKSPACE}/tripleo ${WORKSPACE}/tripleo/new

## * Clone tripleo-ci and run the multinode-setup script for VXLAN networking
## ::

git clone https://git.openstack.org/openstack-infra/tripleo-ci
cd tripleo-ci
./scripts/tripleo.sh --multinode-setup

### --stop_docs
