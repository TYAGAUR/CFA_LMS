"""Request context, CSRF (double submit) and security headers."""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.context import client_ip_var, request_id_var, user_agent_var
from app.core.ids import uuid7
from app.core.security import constant_time_equals

log = logging.getLogger("http")

UNSAFE = {"POST", "PUT", "PATCH", "DELETE"}
# Endpoints called before a session exists, or by third parties with their own signatures.
CSRF_EXEMPT_PREFIXES = (
    "/api/v1/auth/otp/",
    "/api/v1/auth/signup",
    "/api/v1/auth/staff/",
    "/api/v1/auth/refresh",
    "/api/v1/payments/webhooks/",
    "/api/v1/guardian-consent/",
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        rid = request.headers.get("x-request-id") or uuid7().hex
        request_id_var.set(rid)
        fwd = request.headers.get("x-forwarded-for")
        client_ip_var.set(fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else None))
        user_agent_var.set(request.headers.get("user-agent"))

        if (
            request.method in UNSAFE
            and request.url.path.startswith("/api/")
            and not request.url.path.startswith(CSRF_EXEMPT_PREFIXES)
            and request.cookies.get("access_token")
        ):
            cookie = request.cookies.get("csrf_token", "")
            header = request.headers.get("x-csrf-token", "")
            if not cookie or not header or not constant_time_equals(cookie, header):
                return JSONResponse(
                    {"type": "about:blank#csrf_failed", "title": "CSRF check failed", "status": 403,
                     "code": "csrf_failed", "detail": "Missing or invalid CSRF token.", "request_id": rid},
                    status_code=403, media_type="application/problem+json",
                )

        start = time.perf_counter()
        response = await call_next(request)
        ms = round((time.perf_counter() - start) * 1000, 1)
        response.headers["x-request-id"] = rid
        response.headers["x-content-type-options"] = "nosniff"
        response.headers["referrer-policy"] = "strict-origin-when-cross-origin"
        if request.url.path.startswith("/api/"):
            response.headers.setdefault("cache-control", "no-store")
        route = request.scope.get("route")
        log.info("%s %s %s %sms rid=%s", request.method,
                 getattr(route, "path", request.url.path), response.status_code, ms, rid)
        return response
