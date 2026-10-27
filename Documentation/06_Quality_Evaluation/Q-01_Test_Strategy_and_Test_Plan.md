# Q-01 Test Strategy & Test Plan

| Field | Value |
|---|---|
| Document ID | Q-01 |
| Version | 0.1 — strategy for all phases; detailed plan for Phase 1 |
| Owner | QA lead |
| Last updated | 2026-10-23 |
| Related | BRD §16, P-03 §8, P-09, S-03, N-01, N-04 (load test plan, later) |

## 1. Objectives
1. Prove that each phase meets its acceptance criteria (BRD §16, P-03).
2. Prevent regressions in the high-risk areas: **authorisation, unlock rules, grading, consent, data deletion**.
3. Keep feedback fast. The PR pipeline must finish in under 12 minutes.

## 2. Test pyramid and tools

| Level | Scope | Tools | Owner | Runs |
|---|---|---|---|---|
| Unit (backend) | Pure functions: rule evaluator, progress interval merging, scoring, SRS, validators | pytest, hypothesis (property-based) | Devs | Every commit |
| Unit (frontend) | Components, hooks, formatters | Vitest + React Testing Library | Devs | Every commit |
| Integration (API) | Endpoint + DB + Redis in containers; RBAC, entitlement, unlock, audit writes | pytest + httpx AsyncClient + testcontainers (Postgres 16, Redis 7) + factory_boy | Devs | Every PR |
| Contract | OpenAPI schema diff; generated TS client compiles; assessment payloads exclude answer fields | schemathesis (fuzzing), `openapi-diff`, tsc | Devs | Every PR |
| End-to-end | Critical journeys through the real UI on staging-like stack | Playwright (Chromium, WebKit, mobile viewport) | QA | PR (smoke), nightly (full) |
| Accessibility | WCAG 2.1 AA automated checks + manual audit | axe-core (Playwright), manual keyboard / screen-reader (NVDA, VoiceOver) | QA + Design | Nightly + per phase |
| Security | SAST, deps, secrets, ZAP baseline, authz matrix, pen test | See S-03 | Devs + Security | PR / nightly / per release |
| Performance | Load and soak on staging | Locust (N-04) | QA + DevOps | Pre-release |
| Visual regression | Key screens light/dark, mobile/desktop | Playwright screenshots | QA | Nightly |
| UAT | Business acceptance by PO, academic lead, ops | Scripted scenarios (Q-02) | PO | End of phase |

## 3. Coverage targets
- Backend line coverage ≥ 85% overall. **≥ 95% branch coverage** for the `rules`, `auth`, `privacy`, `audit` and (Phase 2) `tests` grading modules.
- Frontend: ≥ 70% for shared components and hooks. Critical flows are covered by E2E rather than by unit-test percentage.
- **Authorisation matrix:** 100% of endpoints × roles (generated test, §5.2).

## 4. Test data
- **Factories** (`factory_boy`) for every model. Each test creates its own data inside a transaction that is rolled back.
- **Seed dataset** `seed/` (from the prototype): 10 subjects, 56 LMs, Equities LM1–3 notes. Used for E2E and demos.
- **Synthetic personas** for E2E: `adult_student`, `minor_pending`, `minor_active`, `author`, `reviewer`, `admin`, `super_admin`. Mobile numbers come from a reserved test range, and OTPs are fixed by the fake SMS provider in non-production environments only.
- **No production data** in any non-production environment (S-02 6.3).

## 5. Phase 1 test plan

### 5.1 Feature test scope

| Epic | Key scenarios | Level |
|---|---|---|
| E1 Auth | OTP happy path; expiry; 5 wrong attempts; rate limits; email fallback; session limit evicts the oldest; refresh rotation and reuse detection; staff password + TOTP; lockout; idle timeout | Unit, API, E2E |
| E2 Users and enrolment | Batch CRUD and validation; CSV import with mixed valid/invalid rows; entitlement activation and expiry; deactivation revokes sessions | API, E2E |
| E3 Consent and DSR | Optional consents default off; minor sign-up → guardian OTP → activation; day-30 purge; consent withdrawal stops analytics; export content; erasure removes personal data and keeps aggregates | API, E2E, job tests |
| E4 Catalogue | `lm_no` uniqueness; reorder; `source_ref` never appears in any student API response (schema test) | API |
| E5 Resources | Upload flows with fake providers; scan failure quarantines; publish blocked without provenance or licence; signed URL expiry; locked LM → 403 | API, E2E |
| E6 Library | Rail states; notes renderer for every block type; XSS payloads in blocks are rendered as text; search respects entitlement and lock; bookmarks | Unit, API, E2E |
| E7 Progress | Interval merge (overlaps, seeks, duplicates); 90% threshold; idempotent heartbeats from two tabs; learned undo window; revision once per IST day (test at 23:59/00:01 IST); EOC validation | Unit (hypothesis), API |
| E8 Rules | Grammar validation; every condition type; `all`/`any`/`not`; sticky unlock after a stricter rule; manual unlock audited; open mode; dry-run evaluation | Unit (property-based), API |
| E9 Dashboard | Next-action priority order (BR-PRG-07) for each state | Unit, E2E |
| E10 Audit and reports | Each event in G-01 §3 written with the required fields; hash chain verification; CSV export audited | API, job tests |

### 5.2 Generated authorisation matrix
A test enumerates every route in the FastAPI app and calls it as each persona: anonymous, student (not entitled), student (entitled, locked), student (entitled, unlocked), author, reviewer, admin, super_admin. It asserts the expected status from `tests/authz_expectations.yaml`, which is derived from P-06. A new route without an entry fails the build.

### 5.3 Critical E2E journeys (smoke, run on every PR)
1. Adult sign-up → consent → dashboard → open Equities LM1 → play video to 90% (accelerated fake player) → mark learned → LM2 unlocks → refresh shows the same state.
2. Minor sign-up → blocked → guardian consents (second browser context) → student can access content.
3. Admin creates a batch → imports a CSV → student sees the entitled subjects.
4. Author uploads a PDF → admin publishes → student views it with a watermark.
5. Admin changes the unlock rule → the locked student sees the new unmet message → a previously unlocked LM stays unlocked.

### 5.4 Non-functional tests in Phase 1
- Load smoke test: 300 virtual users doing dashboard, subject view and progress heartbeats for 15 minutes. Pass when p95 < 1.5 s and error rate < 0.5% (N-01).
- Restore drill from a snapshot to a new RDS instance, with the erasure-ledger replay (D-06, C-05 §4).
- Accessibility: zero axe "serious" or "critical" issues on S-01..S-11, plus a manual keyboard pass.
- Browser and device matrix (§7).

## 6. Defect management

| Severity | Definition | Fix before release? |
|---|---|---|
| S1 Critical | Security or privacy breach, data loss, wrong grading or unlock for many users, outage | Yes, immediately |
| S2 Major | Core flow broken for some users, no workaround | Yes |
| S3 Minor | Has a workaround; cosmetic issue on a core screen | Product owner decides |
| S4 Trivial | Cosmetic | No |

Defects are tracked in the issue tracker with a severity, a link to the failing test, and the BR/US ID.

## 7. Browser and device matrix
- **Desktop:** Chrome, Edge and Firefox (latest 2 versions); Safari (latest 2 versions) on macOS.
- **Mobile:** Android Chrome (Android 11+), iOS Safari (iOS 16+).
- **Viewports:** 360×800, 390×844, 768×1024, 1366×768, 1920×1080.
- **Network:** throttled "Fast 3G" profile for the student flows (common for commuting students).

## 8. Entry and exit criteria (per phase release)
**Entry:**
- The feature is merged with green CI.
- Deployed to staging.
- Release notes drafted.

**Exit:**
- All S1/S2 defects closed.
- E2E full suite green on staging two nights in a row.
- Authorisation matrix 100% passing.
- Pen-test High and Critical findings fixed or covered by an exception.
- UAT signed off (Q-02).
- Performance targets met.

## 9. Traceability
Each test names the IDs it verifies in a docstring or tag (e.g. `@pytest.mark.br("BR-UNL-06")`, Playwright `test.describe('US-7.02 ...')`). A CI report produces the BR/US → test mapping, so coverage gaps against P-09 and P-03 are visible.
