"""FastAPI application factory."""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from sqlalchemy import text

import app.models
import app.modules.commerce.service
from app.core.config import get_settings
from app.core.db import SessionLocal, engine
from app.core.errors import install_error_handlers
from app.core.events import outbox_loop
from app.core.middleware import RequestContextMiddleware
from app.modules.admin import catalog as admin_catalog
from app.modules.admin import commerce as admin_commerce
from app.modules.admin import ops as admin_ops
from app.modules.admin import users as admin_users
from app.modules.auth.router import router as auth_router
from app.modules.commerce.router import router as commerce_router
from app.modules.flashcards.router import router as flashcards_router
from app.modules.learning.router import router as learning_router
from app.modules.payments.router import router as payments_router
from app.modules.privacy.router import router as privacy_router
from app.modules.qbank.router import router as qbank_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    stop = asyncio.Event()
    task = asyncio.create_task(outbox_loop(stop))
    yield
    stop.set()
    await task
    await engine.dispose()


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(
        title="CFA Learning Hub API", version="0.1.0", lifespan=lifespan,
        docs_url="/api/v1/docs" if s.is_dev else None, redoc_url=None,
        openapi_url="/api/v1/openapi.json" if s.is_dev else None,
    )
    app.add_middleware(RequestContextMiddleware)
    install_error_handlers(app)

    api = APIRouter(prefix="/api/v1")
    for r in (auth_router, privacy_router, commerce_router, payments_router, learning_router, qbank_router,
              flashcards_router, admin_users.router, admin_commerce.router, admin_catalog.router, admin_ops.router):
        api.include_router(r)

    @api.get("/healthz", tags=["system"])
    async def healthz() -> dict:
        return {"status": "ok"}

    @api.get("/readyz", tags=["system"])
    async def readyz() -> dict:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready", "env": s.app_env, "payment_provider": s.payment_provider}

    app.include_router(api)
    return app


app = create_app()
