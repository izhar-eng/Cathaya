#!/bin/sh
set -eu
: "${OMRS_CONFIG_ADMIN_USER_PASSWORD:?Set a unique administrator password in Render}"
: "${OMRS_CONFIG_CONNECTION_PASSWORD:?Missing database password}"
mkdir -p /openmrs/data
chown -R 1001:0 /openmrs/data
exec gosu 1001:0 /usr/bin/tini -- /openmrs/startup.sh
