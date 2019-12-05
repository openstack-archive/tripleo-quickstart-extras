container-update
================

This role levarages from the container-prep role which updates the needed
parameters to set up the containers-prepare-parameter file and updates with
the right values. It is mostly intended for upgrades and updates workflows in
which we need to update the containers registry details before performing the
upgrade.

Role Variables
--------------

- containers_file: <containers-prepare-parameter.yaml> -- File containing the ContainerImagePrepare definition.
