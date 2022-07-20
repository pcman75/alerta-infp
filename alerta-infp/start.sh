#!/usr/bin/dumb-init bashio
set -e

bashio::log.info "==> Starting application"

exec python3 /app/app.py