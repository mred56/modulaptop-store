#!/usr/bin/env bash

set -eo pipefail

# Run migrations
alembic upgrade head

exec "$@"
