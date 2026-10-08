FROM openmrs/openmrs-reference-application-3-backend@sha256:929cfe5dca5f221460e0f4a57abb9294614df5f74fbb3bb865e01b8dfe7a985b
USER root
COPY infra/render/backend/remove-demo.sh /remove-demo.sh
RUN sh /remove-demo.sh && rm /remove-demo.sh
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*
COPY infra/render/backend/start.sh /carthaya-start.sh
RUN chmod 755 /carthaya-start.sh
ENTRYPOINT ["/carthaya-start.sh"]
