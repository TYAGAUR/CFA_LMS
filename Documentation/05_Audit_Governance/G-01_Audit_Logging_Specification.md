# G-01 Audit Logging Specification

| Field | Value |
|---|---|
| Document ID | G-01 |
| Version | 0.1 |
| Owner | Tech lead + Security lead |
| Last updated | 2026-10-23 |
| Related | BRD FR-12, A-03 `audit_log`, S-01 T-13, C-05 retention, D-05 observability |

## 1. Purpose
The application audit log answers **who did what, to which record, when, from where, and what changed**. It is used for:
- accountability for content approvals (FR-12);
- security investigations;
- evidence for privacy compliance (consent, data requests);
- dispute resolution (e.g. "my unlock disappeared").

It is separate from technical logs (D-05). Technical logs are for debugging; the audit log is a business record.

## 2. Principles
1. **Complete:** every event type in §3 is recorded by the service layer, in the same database transaction as the change. If the change commits, the audit row commits too.
2. **Tamper-evident:** append-only, hash-chained, and anchored daily to write-once storage.
3. **Minimal:** no secrets, OTPs, passwords, tokens or answer content. Personal data only where needed: actor and target IDs; IP for security events.
4. **Readable:** the admin viewer shows human-readable summaries; the raw JSON is available to super admins.

## 3. Event catalogue

| Category | Action code | Trigger | Before/after captured | Phase |
|---|---|---|---|---|
| **Auth** | `auth.login_succeeded` / `auth.login_failed` | Sign-in | Method, failure reason | 1 |
| | `auth.mfa_enrolled` / `auth.mfa_reset` | Staff MFA | — | 1 |
| | `auth.session_revoked` | Logout, limit, admin, reuse detected | Reason | 1 |
| | `auth.account_locked` | Lockout | — | 1 |
| **Users** | `user.created` / `user.updated` / `user.deactivated` / `user.reactivated` | Admin or self | Changed fields (personal values masked) | 1 |
| | `user.role_granted` / `user.role_revoked` | Admin / super admin | Role | 1 |
| | `user.break_glass_started` / `_ended` | Super admin | Reason | 1 |
| **Privacy** | `consent.changed` | User or guardian | Purpose, granted, notice version | 1 |
| | `guardian.consent_verified` / `guardian.consent_withdrawn` | Guardian | Method | 1 |
| | `data_request.created` / `_status_changed` / `_export_downloaded` | User / admin | Type, status | 1 |
| | `privacy.erasure_completed` | Job | Counts only | 1 |
| **Enrolment** | `batch.created/updated`, `enrolment.created/withdrawn`, `enrolment.bulk_imported`, `entitlement.granted/revoked` | Admin | Fields; import row counts | 1 |
| **Catalogue and content** | `subject/lm/topic/los.created/updated/deleted`, `lm.published/unpublished` | Admin / author | Fields (`source_ref` included; internal) | 1 |
| | `resource.uploaded/updated/published/retired`, `resource.scan_failed` | Author / admin / system | Fields, provenance, licence | 1 |
| | `content_version.submitted/returned/approved/published/retired` | Author / reviewer | Version, comment | 1 (publish) / 3 |
| | `licence.created/updated` | Admin | Fields | 1 |
| **Progress** (student-originated) | `lm.marked_learned` / `lm.learned_undone` | Student | — | 1 |
| | `lm.unlocked` | System (rule) / admin (manual, with reason) | Source, rule version | 1 |
| | `eoc.updated`, `revision.logged` | Student | Values | 1 |
| **Rules and settings** | `unlock_rule.updated` | Admin | Old/new rule JSON, reason | 1 |
| | `settings.updated`, `feature_flag.changed` | Super admin | Key, old/new | 1 |
| **Reports and exports** | `report.exported`, `audit_log.exported` | Admin | Report type, filters, row count | 1 |
| **QBank and tests** | `question_version.*` (as content), `qbank.validation_run`, `qbank.exported` | Author / reviewer | Results summary | 2 |
| | `attempt.submitted`, `attempt.regraded` | Student / admin | Score old/new | 2 |
| **Engagement** | `contest.created/published_results`, `xp.adjusted_manual`, `certificate.issued/revoked` | Admin | Fields | 5 |

Progress heartbeats and page views are **not** audited. They belong in analytics (Q-05) or technical logs.

## 4. Record schema (`audit_log`)

| Field | Type | Notes |
|---|---|---|
| id | bigint identity | Monotonic |
| occurred_at | timestamptz | Server time (UTC) |
| actor_user_id | uuid nullable | Null for system |
| actor_type | enum | `user`, `system`, `job`, `webhook` |
| actor_roles | text[] | Roles at the time of the action |
| action | text | From §3 (`category.verb`) |
| target_type | text | e.g. `learning_module` |
| target_id | text | UUID or composite key |
| subject_user_id | uuid nullable | The student the event concerns (for DSR export and retention) |
| request_id | text | Correlates with technical logs |
| ip_address | inet nullable | Auth and admin events only |
| user_agent | text nullable | Auth events only |
| reason | text nullable | Required for manual unlock, break-glass, rule and settings changes |
| changes | jsonb | `{"field": {"old": x, "new": y}}`; personal values masked (`"+91******1234"`) |
| metadata | jsonb | Extra context (counts, filters) |
| prev_hash | bytea | Hash of the previous row |
| hash | bytea | `SHA-256(prev_hash ‖ canonical_json(row without hash))` |

**Storage:** partitioned monthly by `occurred_at`.

**Database permissions:**
- `app_rw` has INSERT and SELECT only.
- `app_migrator` owns the table.
- No role has UPDATE or DELETE except the retention job role, which can only `DROP PARTITION` for partitions past retention.

## 5. Tamper evidence
- **Hash chain:** a single writer sequence (the insert function takes an advisory lock) computes `hash` from `prev_hash`.
- **Daily anchor:** at 00:30 IST a job writes `{date, last_id, last_hash}` to `s3://backups-prod/audit-anchors/` with Object Lock (compliance mode, 3 years).
- **Verification:** a weekly job recomputes the chain for the last 8 days and compares it with the anchors. A mismatch raises a P1 security alert.

## 6. Access
- **Admin viewer** (US-10.01): filter by actor, action, target, subject user and date. Security-category events (`auth.*`, `user.break_glass*`) are visible to super admins only.
- **Exports** are themselves audited (`audit_log.exported`).
- **Data principal access requests:** events where `subject_user_id` = the requester are included in the export, with staff identities redacted.

## 7. Retention
Per C-05:
- Staff, content, rule and settings events: **3 years**.
- Student-originated events: **1 year**.
- Implemented by dropping monthly partitions. Events in different retention classes go to different partitioned tables: `audit_log_staff` and `audit_log_student`, behind a view `audit_log`. Each table keeps its own hash chain and daily anchor.

## 8. Alerts driven by audit events

| Condition | Severity | Route |
|---|---|---|
| `user.role_granted` with role `admin` or `super_admin` | High | Security channel + email to super admins |
| `user.break_glass_started` | High | Immediate page to the other super admin |
| More than 10 `auth.login_failed` for one staff account in 15 min | Medium | Security channel |
| `report.exported` or `audit_log.exported` with row_count > 1,000 | Medium | Security channel |
| `unlock_rule.updated`, `settings.updated` | Info | Daily digest to the product owner |
| Hash-chain verification failure | Critical | Page the on-call engineer and the security lead |

## 9. Implementation notes
- Use `audit.record(action, target, changes=..., reason=...)` from the services. A FastAPI middleware puts `request_id`, actor, IP and user agent into a context variable, which the recorder reads.
- `changes` is computed with a helper that diffs Pydantic models and masks fields flagged as `C3`/`C4` in model metadata.
- Tests: each event in §3 has a test asserting it is written with the right fields. The hash chain is property-tested.
