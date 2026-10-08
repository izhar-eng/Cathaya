#!/bin/sh
set -eu
: "${PORT:=10000}"
: "${OPENMRS_BACKEND_HOST:?Missing backend host}"
: "${OPENMRS_FRONTEND_HOST:?Missing frontend host}"
DNS_RESOLVER=$(awk '$1 == "nameserver" {print $2; exit}' /etc/resolv.conf)
: "${DNS_RESOLVER:?Missing DNS resolver}"
export PORT DNS_RESOLVER OPENMRS_BACKEND_HOST OPENMRS_FRONTEND_HOST
envsubst '${PORT} ${DNS_RESOLVER} ${OPENMRS_BACKEND_HOST} ${OPENMRS_FRONTEND_HOST}' < /etc/nginx/templates/carthaya.conf.template > /etc/nginx/conf.d/default.conf
nginx -t
exec nginx -g 'daemon off;'
