#!/usr/bin/env bash

set -eo pipefail

APP_MODULE=${APP_MODULE:-"app.main:app"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"80"}
LOG_LEVEL=${LOG_LEVEL:-"info"}

# Start Gunicorn
uvicorn \
  --host "${HOST}" \
  --port "${PORT}" \
  --log-level "${LOG_LEVEL}" \
  --log-config "/uvicorn_log_config.json" \
  "${APP_MODULE}"
