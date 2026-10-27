# One container for Render: Next.js (public $PORT) proxies /api/* to FastAPI on 127.0.0.1:8000,
# so the browser keeps a single origin exactly as in local dev (A-01 §4).

# ---- frontend build ----
FROM node:24-slim AS web
WORKDIR /web
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
ENV NEXT_OUTPUT=standalone NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# ---- backend deps ----
FROM python:3.12-slim AS api
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /bin/uv
WORKDIR /app/backend
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ---- runtime ----
FROM python:3.12-slim
COPY --from=web /usr/local/bin/node /usr/local/bin/node
WORKDIR /app
COPY --from=api /app/backend/.venv /app/backend/.venv
COPY backend/ /app/backend/
COPY seed/ /app/seed/
COPY --from=web /web/.next/standalone /app/frontend/
COPY --from=web /web/.next/static /app/frontend/.next/static
COPY deploy/start.sh /app/start.sh
RUN chmod +x /app/start.sh \
    && useradd --create-home app && mkdir -p /app/backend/var && chown -R app /app/backend/var /app/seed
USER app
ENV PATH="/app/backend/.venv/bin:$PATH" PYTHONUNBUFFERED=1 NODE_ENV=production HOSTNAME=0.0.0.0 PORT=10000
EXPOSE 10000
CMD ["/app/start.sh"]
