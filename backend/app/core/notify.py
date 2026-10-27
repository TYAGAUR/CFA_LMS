"""Outbound SMS / email behind a provider interface. Local uses the console provider."""

import logging
from typing import Protocol

from app.core.config import get_settings

log = logging.getLogger("notify")


class SmsProvider(Protocol):
    async def send(self, to_e164: str, text: str) -> None: ...


class EmailProvider(Protocol):
    async def send(self, to: str, subject: str, text: str) -> None: ...


class ConsoleSms:
    async def send(self, to_e164: str, text: str) -> None:
        log.warning("[SMS to %s] %s", to_e164, text)
        print(f"\n=== SMS to {to_e164} ===\n{text}\n", flush=True)


class ConsoleEmail:
    async def send(self, to: str, subject: str, text: str) -> None:
        log.warning("[EMAIL to %s] %s", to, subject)
        print(f"\n=== EMAIL to {to}: {subject} ===\n{text}\n", flush=True)


def sms() -> SmsProvider:
    s = get_settings()
    if s.sms_provider == "console":
        return ConsoleSms()
    raise NotImplementedError("MSG91 adapter is added with cloud deployment (O-10)")


def email() -> EmailProvider:
    s = get_settings()
    if s.email_provider == "console":
        return ConsoleEmail()
    raise NotImplementedError("SES adapter is added with cloud deployment")
