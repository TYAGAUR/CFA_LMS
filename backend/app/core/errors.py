"""RFC 9457 problem+json errors (A-04 §1.3)."""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.context import request_id_var


class AppError(Exception):
    status = 400
    code = "bad_request"
    title = "Bad request"

    def __init__(self, detail: str = "", *, code: str | None = None, status: int | None = None,
                 meta: dict[str, Any] | None = None):
        super().__init__(detail)
        self.detail = detail or self.title
        if code:
            self.code = code
        if status:
            self.status = status
        self.meta = meta or {}


class Unauthenticated(AppError):
    status, code, title = 401, "unauthenticated", "Sign in required"


class Forbidden(AppError):
    status, code, title = 403, "forbidden", "Not allowed"


class NotEntitled(AppError):
    status, code, title = 403, "not_entitled", "You are not registered for this subject"


class NotFound(AppError):
    status, code, title = 404, "not_found", "Not found"


class Conflict(AppError):
    status, code, title = 409, "conflict", "Conflict"


class Invalid(AppError):
    status, code, title = 422, "validation_failed", "Validation failed"


class RateLimited(AppError):
    status, code, title = 429, "rate_limited", "Too many requests"


def _problem(status: int, code: str, title: str, detail: str, **extra: Any) -> JSONResponse:
    body = {
        "type": f"about:blank#{code}",
        "title": title,
        "status": status,
        "code": code,
        "detail": detail,
        "request_id": request_id_var.get(),
        **extra,
    }
    return JSONResponse(body, status_code=status, media_type="application/problem+json")


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return _problem(exc.status, exc.code, type(exc).title, exc.detail, meta=exc.meta)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [
            {"loc": [str(p) for p in e.get("loc", [])], "msg": e.get("msg"), "type": e.get("type")}
            for e in exc.errors()
        ]
        return _problem(422, "validation_failed", "Validation failed", "Some fields are invalid.", errors=errors)

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = {404: "not_found", 405: "method_not_allowed"}.get(exc.status_code, "http_error")
        return _problem(exc.status_code, code, str(exc.detail), str(exc.detail))
