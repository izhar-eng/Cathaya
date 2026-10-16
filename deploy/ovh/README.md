# Carthaya OpenELIS OVH corrections (2026-10-17)

These files preserve deployment configuration recovered from the OVH corrective archive. They are not a complete standalone deployment.

- Backend image: `carthaya-openelis:sql-fix-07`
- Proxy image: `carthaya-openelis-proxy:route-fix-03`
- Frontend image: `carthaya-openelis-frontend:login-fix-01`

`openelis-proxy/nginx.conf` and the Compose overrides were recovered from the verified OVH archive. The proxy Dockerfile references `conf.d/` from the original archive; it must be preserved to rebuild that image.

**Not included here:** compiled backend Java classes, bundled frontend `dist` assets and full base Compose configuration. These artifacts remain in the private OVH backups. The frontend source changes were not supplied in the archive. The image tags refer to locally built images; they cannot be pulled from a registry without publishing them first.

Do not commit `.env`, credentials, database backups, private keys or production health data. Do not apply these overrides without verifying the corresponding images and base Compose files.
