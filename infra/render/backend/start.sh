#!/bin/sh
set -eu
: "${OMRS_CONFIG_ADMIN_USER_PASSWORD:?Set a unique administrator password}"
: "${OMRS_CONFIG_CONNECTION_PASSWORD:?Missing database password}"
mkdir -p /openmrs/data
chown -R 1001:0 /openmrs/data
exec setpriv --reuid=1001 --regid=0 --clear-groups /usr/bin/tini -- /openmrs/startup.sh
