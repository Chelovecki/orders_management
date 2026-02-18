#!/bin/sh
set -e

echo "Running database migrations..."
uv run alembic upgrade head
echo "Migrations complete"

# Запускаем приложение (то, что в CMD)
exec "$@"