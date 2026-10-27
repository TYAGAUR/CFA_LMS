# Karan Sir Classes · CFA Learning Hub

CFA Level I learning platform: paid course registration (Razorpay), class videos, notes, PDFs, progress tracking (no chapter locking), privacy/consent (DPDP), staff console and audit log.

- **Backend:** FastAPI · SQLAlchemy 2 (async) · PostgreSQL 16 · Alembic — `backend/`
- **Frontend:** Next.js 16 · React 19 · TypeScript — `frontend/`
- **Docs:** `Documentation/` (start with `00_Documentation_Register.md`)

## Features for students

Learn (all LMs open after payment) · chapter quiz on every LM · custom tests (subjects, chapters, Easy/Medium/Hard, conceptual/numerical, practice or assessment mode, optional timer) · subject tests · flashcards with spaced repetition · accuracy by subject and difficulty.

## Run locally (Windows, no Docker)

Prerequisites (already installed on this machine): Python + [uv](https://docs.astral.sh/uv/), Node.js 22+ (24 LTS installed), PostgreSQL 16 (service `postgresql-x64-16`, superuser password `localdev_pg`, local only).

One-time database setup (already done here):

```sql
-- psql -U postgres -h localhost
CREATE ROLE cfa_lms LOGIN PASSWORD 'cfa_lms_local';
CREATE DATABASE cfa_lms OWNER cfa_lms;
CREATE DATABASE cfa_lms_test OWNER cfa_lms;
```

Then:

```bash
cp .env.example .env                      # local defaults: mock payments, OTP shown on screen

cd backend
uv sync
uv run alembic upgrade head
uv run python ../scripts/extract_prototype.py   # optional: regenerate seed/*.json from the prototype
uv run python scripts/seed.py              # subjects, LMs, notes, courses, staff, demo student
uv run uvicorn app.main:app --port 8000 --reload --reload-dir app

cd ../frontend                             # in a second terminal
npm install
npm run dev                                # http://localhost:3000
```

The browser only talks to `http://localhost:3000`; Next.js proxies `/api/*` to FastAPI on port 8000 (same origin, cookie auth). API docs: http://localhost:8000/api/v1/docs.

## Local accounts

| Who | How to sign in |
|---|---|
| Demo student (already paid for the complete course) | `/login` · mobile `9876543210` · the OTP is shown on screen (and printed in the API console) |
| New student | `/login` with any valid Indian mobile → sign up → Courses → Register → test gateway |
| Super admin / admin / author / reviewer | `/staff/login` · `super@local.test`, `admin@local.test`, `author@local.test`, `reviewer@local.test` · password `LocalDev#2026!` |

Under-18 sign-ups go through the parental-consent flow; in local mode the guardian link is shown on screen.

## Payments

`PAYMENT_PROVIDER=mock` uses a built-in test gateway (no money moves). To switch to Razorpay test mode set `PAYMENT_PROVIDER=razorpay` and the three `RAZORPAY_*` variables, then register the webhook. Details: `Documentation/02_Architecture/A-08_Payments_and_Registration_Integration.md`.

## Deploy on Render

`render.yaml` is a Render Blueprint. It creates one Docker web service, `cfa-lms`, and one Postgres database, `cfa-lms-db`, both in Singapore. The container runs Next.js on Render's public port. Next.js proxies `/api/*` to FastAPI inside the same container (see `Dockerfile` and `deploy/start.sh`). Every start runs `alembic upgrade head`, then the idempotent seed while `SEED_ON_START=true`.

1. In the Render dashboard, choose **New → Blueprint**, connect this GitHub repo and select `render.yaml`.
2. When Render prompts for values, set **SEED_STAFF_PASSWORD**. It becomes the password for the four `@local.test` staff accounts. Leave the Razorpay keys blank for now.
3. Apply, wait for the first deploy, then open `https://<service>.onrender.com`. Staff sign-in asks each account to enrol an authenticator app (TOTP).

`DEMO_MODE=true` is allowed on staging only; production refuses to start with it. It shows OTP codes on screen and enables the mock payment gateway, because no SMS gateway or live Razorpay account is connected yet. Before real students sign up:

- Connect SMS, then set `OTP_DEBUG_ECHO=false`.
- Set `PAYMENT_PROVIDER=razorpay` with the three `RAZORPAY_*` keys and `DEMO_MODE=false`. Point the Razorpay webhook at `/api/v1/payments/webhooks/razorpay`.
- Move off the free plans. A free web service sleeps after 15 minutes idle (the first request then takes about a minute). It has no persistent disk, so uploaded PDFs are lost on each redeploy. Free Postgres expires after 30 days. On a paid plan, add a disk mounted at `/app/backend/var` or move uploads to object storage.

## Tests

```bash
cd backend && uv run pytest -q        # uses the cfa_lms_test database
cd frontend && npx tsc --noEmit && npm run build
```

## Layout

```
backend/app/core        config, db, security, rbac, errors, events/outbox, storage, notify
backend/app/modules     auth users privacy catalog content media progress enrolment
                        commerce payments learning admin audit
backend/alembic         migrations
backend/scripts/seed.py demo data
frontend/src/app        pages (student, registration/checkout, staff console under /admin)
seed/                   content extracted from the prototype (subjects, notes, questions, flashcards)
scripts/                one-off tools
```

## Not built yet (next phases)
Question review workflow and DOCX/PDF exports (rest of Phase 2), revision-sheet studio (rest of Phase 3), mock tracking and advanced analytics (Phase 4), contests/XP (Phase 5), real SMS/email adapters (MSG91/SES), video hosting on Bunny Stream, antivirus scanning of uploads, Celery/Redis workers and the cloud deployment (A-05).
