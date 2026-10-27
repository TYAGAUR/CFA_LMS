# U-04 Developer Onboarding Guide & Coding Standards

| Field | Value |
|---|---|
| Document ID | U-04 |
| Version | 0.1 — written ahead of the codebase; update as the repo is created |
| Owner | Tech lead |
| Last updated | 2026-10-23 |
| Related | A-01, A-02, A-03, A-04, S-03, D-01..D-03, Q-01 |

## 1. Read first (in this order, ~2 hours)
1. P-03 PRD, §1–§5 (what we're building in Phase 1).
2. P-09 Business rules (unlock, progress; cite BR IDs in code and tests).
3. A-01 Architecture + A-02 ADRs.
4. A-03 Data model (especially classification) + A-04 API standards.
5. S-03 Secure coding rules.
6. This guide.

## 2. Prerequisites
- Git; Docker Desktop (or Docker Engine + Compose v2).
- Python 3.12 with [uv](https://docs.astral.sh/uv/).
- Node.js 22 LTS with pnpm (via corepack).
- An editor with Ruff, ESLint and Prettier integration (VS Code recommended: extensions listed in `.vscode/extensions.json`).
- Pre-commit: `pipx install pre-commit` or `uv tool install pre-commit`.
- Access: GitHub org team, staging AWS (Identity Center), Sentry, the team chat.

## 3. Repository layout
See A-01 §12. Key paths:

```
backend/
  app/core/            settings, db, security, rbac, errors, logging, audit hooks
  app/modules/<name>/  router.py service.py repo.py models.py schemas.py events.py tasks.py
  alembic/             migrations
  tests/               unit/ integration/ authz_expectations.yaml conftest.py factories.py
  scripts/             seed_from_prototype.py, gen_synthetic.py
frontend/
  src/app/             (public) (student) (admin) route groups
  src/components/      ui/ (design system), notes/BlockRenderer, player/, admin/
  src/lib/api/         generated client (do not edit) + hooks
  src/styles/tokens.css
seed/                  prototype-derived JSON
infra/terraform/
```

## 4. First run (target: under 1 hour)

```bash
git clone <repo> cfa-lms && cd cfa-lms
cp .env.example .env                    # defaults use fakes for SMS and video
pre-commit install
docker compose up -d postgres redis mailpit
cd backend && uv sync && uv run alembic upgrade head && uv run python scripts/seed_from_prototype.py && cd ..
docker compose up api worker web         # or run each locally with hot reload
```

- Web: http://localhost:3000. API docs: http://localhost:3000/api/v1/docs (local only). Mail: http://localhost:8025.
- Sign in as a seeded persona: the mobile numbers are in `seed/personas.json`. In local, the OTP appears in the API console (`SMS_PROVIDER=console`).
- Staff persona: `admin@local.test`, password in `seed/personas.json`. TOTP is bypassed only when `APP_ENV=local`. This bypass is checked by a test that fails if it is enabled in any other environment.

## 5. Everyday commands

| Task | Command |
|---|---|
| Backend tests | `cd backend && uv run pytest -q` (`-m "not integration"` for fast) |
| Backend lint/type | `uv run ruff check . && uv run ruff format --check . && uv run mypy app` |
| New migration | `uv run alembic revision --autogenerate -m "add eoc_entries"` (review it by hand!) |
| Frontend dev | `cd frontend && pnpm dev` |
| Frontend tests | `pnpm test` · `pnpm lint` · `pnpm typecheck` |
| Regenerate API client | `pnpm gen:api` (reads the running API's OpenAPI; commit the result) |
| E2E | `pnpm e2e` (needs the compose stack) |

## 6. Coding standards — backend (Python / FastAPI)
- **Style:** Ruff (lint + format; line length 100), mypy strict on `app/core` and on sensitive modules. Type hints everywhere.
- **Layering:** router → service → repo. Routers contain no business logic or SQL. Services own transactions (`async with uow:`) and call other modules only through their services (A-01 §5, import-linter).
- **Schemas:** Pydantic v2 with `model_config = ConfigDict(extra="forbid")` for inputs. Explicit response models; never return ORM objects directly. Internal fields (`source_ref`, `correct_index`) live only in admin or internal schemas.
- **Permissions:** every route declares `dependencies=[Depends(require("perm:action"))]` or is listed in `PUBLIC_ROUTES`. Services call `assert_entitled` and `assert_unlocked` for student content.
- **Errors:** raise `AppError(code, status, detail, meta)` subclasses. The handler converts them to problem+json. Never leak exception text to clients.
- **Audit:** state-changing service methods in G-01 §3 call `audit.record(...)`.
- **Time:** `now_utc()` and `today_ist()` helpers; never `datetime.now()` without a timezone.
- **Async:** async SQLAlchemy sessions; no blocking I/O in request handlers (use `run_in_threadpool` or Celery for CPU-heavy or blocking work such as PDF handling).
- **Business rules:** reference IDs in docstrings, e.g. `"""Mark LM learned. BR-PRG-03."""`.
- **Naming:** modules and files snake_case; classes PascalCase; DB per A-03 conventions.

## 7. Coding standards — frontend (Next.js / TypeScript)
- **TypeScript** `strict: true`; no `any` (lint error) except in generated code.
- **Components:** server components by default; add `"use client"` only for interactivity. Data fetching goes through `src/lib/api` server helpers (cookie forwarding) or TanStack Query hooks on the client.
- **Styling:** CSS Modules with tokens from `tokens.css` (P-07). No hard-coded colours. Support dark mode through tokens.
- **Accessibility:** semantic elements, labelled controls; use the design-system primitives (`Button`, `Tabs`, `Dialog`, `RadioGroup`) that include ARIA patterns. Run `pnpm test:a11y` on new pages.
- **Security:** no `dangerouslySetInnerHTML` (lint rule; the only exception is `BlockRenderer`); no tokens in web storage; external links get `rel="noopener noreferrer"`.
- **Copy:** UI strings live in `src/messages/en.json`; follow the voice guidelines in P-07 §9.
- **Formatting:** Prettier; ESLint (`next/core-web-vitals`, `@typescript-eslint`, `jsx-a11y`, security plugin).

## 8. Database and migrations
- One migration per logical change. Review autogenerated SQL by hand. Follow expand/contract (D-03 §5).
- A new personal-data column must update A-03 (class) and C-04 in the same PR (privacy owner is a CODEOWNER).
- Indexes on large tables use `postgresql_concurrently=True` in a separate migration.

## 9. Testing expectations
- New business logic comes with unit tests that cite BR IDs (`@pytest.mark.br("BR-UNL-06")`).
- New endpoints come with integration tests and an entry in `authz_expectations.yaml`.
- Bug fixes come with a regression test.
- See Q-01 for levels and coverage targets.

## 10. Git and PRs
Trunk-based development with short branches, Conventional Commits, and the PR template (D-03 §2). Keep PRs small. Wait for green CI before asking for review.

## 11. Definition of Done
- [ ] Acceptance criteria met; BR/US IDs referenced.
- [ ] Tests at the right level; CI green; coverage thresholds kept.
- [ ] Permissions, entitlement and unlock checks in place; authz matrix updated.
- [ ] Audit events and logs added (no PII in logs).
- [ ] Docs updated (A-03, A-04 if the contract changed, C-04 if data changed, ADR if a decision was made).
- [ ] Accessible (keyboard, labels, contrast); works at 360px and in dark mode.
- [ ] Feature flag set up if partially released.
- [ ] Reviewed and approved per CODEOWNERS.

## 12. Getting help
- Architecture questions: tech lead. Business rule questions: product owner, citing the BR ID.
- Security concerns: the `#security` channel. If you suspect a vulnerability in production, follow S-06; do not discuss it in public channels.
