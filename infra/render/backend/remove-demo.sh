#!/bin/sh
set -eu
props=/openmrs/distribution/openmrs-distro.properties
# Only the inspected stable distribution is supported by this transformation.
grep -Fqx 'version=3.7.1' "$props"
grep -Fqx 'war.openmrs=2.8.8' "$props"
grep -Fqx 'content.referenceapplication-demo=1.9.2' "$props"
grep -Fqx 'omod.referencedemodata=2.6.1' "$props"
find /openmrs/distribution/openmrs_config -type d -name referenceapplication-demo -prune -exec rm -rf {} +
rm /openmrs/distribution/openmrs_modules/referencedemodata-*.omod
sed -i '/^content.referenceapplication-demo=/d; /^omod.referencedemodata=/d' "$props"
test -z "$(find /openmrs/distribution/openmrs_config -name referenceapplication-demo -print -quit)"
test -z "$(find /openmrs/distribution/openmrs_modules -name 'referencedemodata-*.omod' -print -quit)"
