FROM library/nginx@sha256:0985e772fb9f729e6fa0980da05fca5d9c468e870eed43071545afa9d2e27d94
COPY infra/render/gateway/default.conf.template /etc/nginx/templates/carthaya.conf.template
COPY infra/render/gateway/start.sh /carthaya-start.sh
RUN chmod 755 /carthaya-start.sh
ENTRYPOINT ["/carthaya-start.sh"]
