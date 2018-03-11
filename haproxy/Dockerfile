FROM haproxy:alpine

ENV CONSUL_TEMPLATE_VERSION=0.19.4

# Update wget to get support for SSL
RUN apk --update add haproxy wget

# Download consul-template
RUN ( wget --no-check-certificate https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip -O /tmp/consul_template.zip && unzip /tmp/consul_template.zip && mv consul-template /usr/bin && rm -rf /tmp/* )

COPY hup.sh /tmp/hup.sh
COPY  consul-template.conf /tmp/consul-template.conf
COPY haproxy.cfg.ctmpl /tmp/haproxy.cfg.ctmpl

ENTRYPOINT ["consul-template","-config=/tmp/consul-template.conf"]
