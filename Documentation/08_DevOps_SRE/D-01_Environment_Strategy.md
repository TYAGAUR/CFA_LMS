# D-01 Environment Strategy

| Field | Value |
|---|---|
| Document ID | D-01 |
| Version | 0.1 |
| Owner | DevOps lead |
| Last updated | 2026-10-23 |
| Related | A-05, D-02, D-04, S-02 §6.3 |

## 1. Environments

| Env | Purpose | Where | Deployed from | Data | Access |
|---|---|---|---|---|---|
| **local** | Development | Developer laptop, `docker compose` | Working copy | Seed + factories | Developer |
| **ci** | Automated tests | GitHub Actions runners (testcontainers) | PR head | Ephemeral, factories | CI only |
| **preview** (optional, Phase 2+) | Review UI changes per PR | ECS service per PR in the staging account; shared staging DB schema per PR | PR | Seed | Team |
| **staging** | Integration, UAT, load tests, pen tests | AWS `staging` account, ap-south-1 | `main` (auto) | Seed + synthetic data; **no production personal data** | Team, UAT users (named accounts) |
| **production** | Live service | AWS `production` account, ap-south-1 | Tagged release (manual approval) | Real | Students, staff; engineers time-bound |

## 2. Parity
- The same container images are promoted from staging to production. Images are never rebuilt between environments.
- The same Terraform modules are used, with different variable files (sizes, counts, domains).
- **Allowed differences:** instance sizes, single-AZ database in staging, separate Bunny library, test SMS sender ID, feature flags.

## 3. Configuration
- 12-factor: all configuration through environment variables, loaded by `pydantic-settings` (backend) and `next.config` with runtime env (frontend).
- Non-secret configuration lives in Terraform (`ecs` task definitions). Secrets come from Secrets Manager references.
- Naming: `APP_ENV`, `DATABASE_URL`, `REDIS_URL`, `JWT_PRIVATE_KEY`, `BUNNY_LIBRARY_ID`, `BUNNY_API_KEY`, `SMS_PROVIDER` (`msg91`\|`console`), `VIDEO_PROVIDER` (`bunny`\|`fake`), `SENTRY_DSN`, `FEATURE_FLAGS_DEFAULTS`.
- `.env.example` in the repo lists every variable with a description. `.env` is git-ignored.

## 4. Domains

| Env | Web + API | Video | Email sender |
|---|---|---|---|
| local | `http://localhost:3000` (API proxied at `/api`) | fake | Mailpit |
| staging | `https://staging.<domain>` | Bunny staging library | `noreply@staging.<domain>` |
| production | `https://app.<domain>` | Bunny production library | `noreply@<domain>` |

Staging is protected by WAF IP allow-listing (office/VPN) and basic access controls. It is not indexable (`X-Robots-Tag: noindex`).

## 5. Data policy per environment
- Production personal data must never be copied to other environments (S-02 6.3).
- When a production-like data volume is needed (load tests), a **synthetic data generator** (`backend/scripts/gen_synthetic.py`) creates N students with realistic progress patterns.
- Content (non-personal, C2) may be copied from production to staging for UAT, with the academic lead's approval, using the content export/import tool.

## 6. Feature flags
- Stored in `settings.feature_flags` per environment. Flags are named `phase2_qbank`, `minor_restrictions`, `contest_mode`, and so on.
- Production flag changes go through the super-admin settings UI and are audited (G-01).
- Flags have an owner and a removal date. Stale flags are reviewed every month.

## 7. Database migrations across environments
- Alembic migrations run as a one-off ECS task before the new application version deploys (D-02).
- They follow the expand/contract pattern so old and new versions can run at the same time (D-03 §5).

## 8. Access
| Env | Engineers | Method |
|---|---|---|
| staging | Read/write for the dev team | IAM Identity Center, permission set `StagingDeveloper` |
| production | Read-only by default; write is time-bound and approved | `ProdReadOnly` (8 h); `ProdOperator` (needs approval, 4 h); break-glass (P-06 §5) |

Database access in production goes through an SSM Session Manager port-forward to RDS with IAM authentication. Every session is logged.
