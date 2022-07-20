ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /app
RUN apk add --update --no-cache dumb-init python3 py3-pip

RUN pip3 install --no-cache-dir -U requests paho-mqtt sseclient
COPY /app/ /app/
COPY start.sh /app/start.sh

ENTRYPOINT ["/app/start.sh"]

LABEL io.hass.version="VERSION" io.hass.type="addon" io.hass.arch="armhf|aarch64|i386|amd64"
