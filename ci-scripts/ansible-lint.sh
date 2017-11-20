#!/bin/bash

# ANSIBLE0006: Using command rather than module
#   we have a few use cases where we need to use curl and rsync
# ANSIBLE0007: Using command rather than an argument to e.g file
#   we have a lot of 'rm' command and we should use file module instead
# ANSIBLE0010: Package installs should not use latest.
#   Sometimes we need to update some packages.
# ANSIBLE0012: Commands should not change things if nothing needs doing
# ANSIBLE0013: Use Shell only when shell functionality is required
# ANSIBLE0016: Tasks that run when changed should likely be handlers
#   this requires refactoring roles, skipping for now
SKIPLIST="ANSIBLE0006,ANSIBLE0007,ANSIBLE0010,ANSIBLE0012,ANSIBLE0013,ANSIBLE0016"

# lint the playbooks separately to avoid linting the roles multiple times
pushd playbooks
for playbook in `find . -type f -regex '.*\.y[a]?ml'`; do
    ansible-lint -vvv -x $SKIPLIST $playbook || lint_error=1
done
popd

# lint all the possible roles
# Due to https://github.com/willthames/ansible-lint/issues/210, the roles
# directories need to contain a trailing slash at the end of the path.
for rolesdir in `find ./roles -maxdepth 1 -type d`; do
    ansible-lint -vvv -x $SKIPLIST $rolesdir/ || lint_error=1
done

## exit with 1 if we had a least an error or warning.
if [[ -n "$lint_error" ]]; then
    exit 1;
fi

