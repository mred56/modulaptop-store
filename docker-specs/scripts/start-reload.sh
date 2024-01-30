#!/usr/bin/env bash

set -eo pipefail

APP_MODULE=${APP_MODULE:-"app.main:app"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"80"}
LOG_LEVEL=${LOG_LEVEL:-"info"}
export WEB_CONCURRENCY=${WEB_CONCURRENCY:-"1"}

# Start Uvicorn with live reload
uvicorn --reload --host "${HOST}" --port "${PORT}" --log-level "${LOG_LEVEL}" "${APP_MODULE}"
