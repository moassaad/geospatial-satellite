#!/bin/sh

set -e

echo "Waiting for database..."

until python -c "
import socket
s = socket.socket()
s.connect(('db',5432))
s.close()
"; do
    sleep 2
done

echo "Running migrations..."

alembic upgrade head

echo "Starting application..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000