# A-02 Architecture Decision Records (ADRs)

| Field | Value |
|---|---|
| Document ID | A-02 |
| Version | 0.1 — initial set |
| Owner | Tech lead |
| Last updated | 2026-10-23 |

Each ADR uses the format: Status · Context · Decision · Consequences.
- **Status values:** Proposed, Accepted, Superseded.
- New ADRs are added at the end. Old ADRs are never edited except to change their status.

---

## ADR-001 Technology stack
- **Status:** Accepted (D-001)
- **Context:** The sponsor chose the stack. The team is small, the platform is content-heavy, and the BRD needs a strong admin side and data work (validation, exports, analytics).
- **Decision:**
  - **Frontend:** Next.js (App Router, TypeScript).
  - **Backend:** FastAPI (Python 3.12) with SQLAlchemy 2, Alembic and Pydantic v2.
  - **Database:** PostgreSQL 16.
- **Consequences:**
  - Python suits document generation (python-docx), validation scripts and future AI work.
  - Two languages in one codebase, so OpenAPI is used to generate typed clients.

## ADR-002 Modular monolith
- **Status:** Accepted
- **Context:** 3–4 developers, one product, an early stage.
- **Decision:** One backend deployable with domain modules (A-01 §5). Boundaries are enforced with `import-linter`. An outbox handles async side effects.
- **Consequences:** Simple operations and transactions. Discipline is needed to keep boundaries clean. Modules can be extracted later.

## ADR-003 Authentication and sessions
- **Status:** Proposed
- **Context:** Students prefer phone login. Staff need strong authentication. Everything is served from a single domain.
- **Decision:**
  - Students sign in with SMS OTP and an email-OTP fallback.
  - Staff sign in with email + Argon2id password + TOTP.
  - Access token: JWT (EdDSA), 15 minutes, held in an httpOnly cookie.
  - Refresh token: an opaque random value, stored hashed, rotated on every use, with family-wide revocation if reuse is detected.
  - Cookies are `Secure; HttpOnly; SameSite=Lax`; CSRF is covered by SameSite plus a double-submit token on state-changing requests.
  - Session limit: 2 devices for students.
  - No third-party auth provider in Phase 1, to keep data in India and costs low.
- **Consequences:**
  - We own the security-critical code, so it needs focused tests and a pen test.
  - Google sign-in can be added later.

## ADR-004 Search with PostgreSQL full-text search
- **Status:** Proposed
- **Context:** The corpus is small (thousands of topics and questions).
- **Decision:**
  - `tsvector` generated columns with GIN indexes and the `english` dictionary.
  - `pg_trgm` for fuzzy titles.
  - Results are filtered by entitlement in SQL.
- **Consequences:** No extra infrastructure. If relevance needs exceed this, revisit with OpenSearch or Meilisearch.

## ADR-005 Video platform: Bunny Stream
- **Status:** Proposed (O-09)
- **Context:** Needs encoding, adaptive bitrate, token-signed playback, India delivery and low cost.
- **Options considered:** Bunny Stream; Mux; Vimeo; AWS MediaConvert + CloudFront.
- **Decision:**
  - Bunny Stream with token authentication and an allowed-referrer restriction.
  - TUS uploads straight from the browser.
  - A watermark overlay in our player.
  - DRM (MediaCage Enterprise) is evaluated if piracy becomes material.
- **Consequences:**
  - The video host is outside AWS. Bunny is added to the vendor register (C-07).
  - Videos contain no personal data; only an opaque user ID is used in the watermark.

## ADR-006 Cloud: AWS ap-south-1 (Mumbai)
- **Status:** Proposed (O-07)
- **Context:** Data should stay in India, latency should be low, and managed services are needed.
- **Decision:**
  - Primary region: AWS Mumbai.
  - Cross-region backup copies go to ap-south-2 (Hyderabad).
  - Managed services: RDS, ElastiCache, ECS Fargate, S3, CloudFront, WAF, Secrets Manager, KMS, SES.
- **Consequences:**
  - Some vendor lock-in, reduced by containers and Terraform.
  - Alternatives such as Azure Central India are viable if the commercial terms are better.

## ADR-007 Versioned, immutable published content
- **Status:** Accepted
- **Context:** The BRD requires version history, approvals and provenance (FR-12). Attempts must refer to the exact question version answered.
- **Decision:**
  - Each content item has a `*_versions` table.
  - Published and approved versions are immutable (enforced by a database trigger).
  - Edits create a new draft.
  - Items point to `current_published_version_id`.
- **Consequences:**
  - More rows and joins.
  - Full history and safe rollback.

## ADR-008 Unlock rules as JSON, evaluated on the server
- **Status:** Accepted (D-002)
- **Decision:**
  - Rules are stored as versioned JSON (grammar in P-09 §3.1), evaluated by a pure function with loaders for the facts it needs.
  - Unlocks are sticky (`lm_progress.unlocked_at`).
- **Consequences:**
  - Admins can change rules without a deployment.
  - The evaluator must be well covered by tests (property-based tests on the grammar).

## ADR-009 Background jobs with Celery and Redis
- **Status:** Proposed
- **Context:** Needs async jobs (imports, exports, scans) and scheduled jobs (retention, SRS rollups, reminders).
- **Decision:**
  - Celery 5 with a Redis broker and Celery beat for schedules.
  - Tasks are idempotent and keyed by job ID.
  - The outbox dispatcher runs every 2 s.
- **Consequences:** A well-known tool. Redis must run with persistence (AOF) or tolerate redelivery through the outbox.

## ADR-010 Server-side grading; answers never sent before submission
- **Status:** Accepted
- **Context:** In the prototype the answer keys were in the browser.
- **Decision:**
  - The test API returns stems and options only.
  - Correct answers and explanations are returned only after submission, or per item in practice mode.
  - Option order is shuffled and the mapping kept on the server.
- **Consequences:** More server round-trips (acceptable). Removes a whole class of cheating.

## ADR-011 Monorepo
- **Status:** Accepted
- **Decision:**
  - One Git repository with `frontend/`, `backend/`, `infra/`, `seed/` and `Documentation/`.
  - CI runs jobs filtered by changed path.
- **Consequences:**
  - Atomic changes across API and client, including regenerating the OpenAPI client in the same PR.

## ADR-012 Notes stored as structured JSON blocks, not HTML
- **Status:** Accepted
- **Context:** The prototype used `innerHTML`, which is an XSS risk. Exports to DOCX and PDF need structure.
- **Decision:** Use the block schema in A-03 §5. The web renderer and the DOCX/PDF exporters share it.
- **Consequences:** An editor is needed in Phase 3. Phase 1 seeds are converted from the prototype's HTML once, by a script.

## ADR-013 Primary keys: UUIDv7
- **Status:** Proposed
- **Decision:** UUIDv7 is generated by the application for all entities. The audit log uses `bigserial`.
- **Consequences:**
  - IDs can't be guessed, which reduces IDOR risk; authorisation checks are still mandatory.
  - Inserts arrive in roughly increasing order, which suits B-tree indexes.
