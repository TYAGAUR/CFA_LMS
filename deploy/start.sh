#!/bin/sh
# Container entrypoint: migrate, optionally seed, then run FastAPI (internal) and Next.js (public).
set -e
cd /app/backend
alembic upgrade head
if [ "${SEED_ON_START:-false}" = "true" ]; then
  python scripts/seed.py
fi
uvicorn app.main:app --host 127.0.0.1 --port 8000 --proxy-headers --forwarded-allow-ips=127.0.0.1 &
API_PID=$!
cd /app/frontend
node server.js &
WEB_PID=$!
# If either process exits, stop the container so Render restarts it.
while kill -0 "$API_PID" 2>/dev/null && kill -0 "$WEB_PID" 2>/dev/null; do sleep 5; done
kill "$API_PID" "$WEB_PID" 2>/dev/null || true
exit 1
