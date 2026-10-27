# C-05 Data Retention & Deletion Policy

| Field | Value |
|---|---|
| Document ID | C-05 |
| Version | 0.1 — Draft; legal confirmation of statutory periods required |
| Owner | Privacy owner |
| Last updated | 2026-10-23 |
| Related | C-01, C-04, D-06 Backup/DR, G-01 Audit |

## 1. Principles
1. Keep personal data only as long as the purpose needs it, or as long as a law requires.
2. Delete or irreversibly anonymise data when the period ends. Prefer automated deletion to manual.
3. Retention periods are settings (`settings.retention.*`), so they can change without a release. Every change is audit-logged.
4. Legal hold overrides deletion. A super admin sets it with a reason, and it is reviewed every 90 days.

## 2. Retention schedule

| Data (C-04 ref) | Retention period | Trigger | End-of-life action |
|---|---|---|---|
| Unverified sign-ups (OTP done, profile incomplete) | 7 days | Created | Hard delete |
| Minor accounts without guardian consent | 30 days | Created | Hard delete (user, guardian, consents) |
| OTP challenges | 24 hours | Created | Hard delete |
| Sessions (revoked or expired) | 180 days | Expiry | Hard delete |
| D1 identity and contact | Until account closure + 90 days | Account deactivated or erasure request | Delete. A tombstone stays (`users.id`, `status=deleted`, `deleted_at`). Name, mobile and email are nulled; mobile kept as an HMAC for 90 days to stop the same number re-registering during the period |
| D2 DOB | Until the 18th birthday or account end | Event | Null DOB; keep `is_minor=false` |
| D3 guardian data and consent evidence | While the student is a minor + 3 years | 18th birthday or account end | Delete |
| D6 enrolment | Account closure + 3 years | Closure | Keep with the pseudonymous user ID (business and tax records); delete names |
| D7/D8/D9 progress, attempts, mock entries | Account closure + 90 days | Closure | Delete individual rows; keep anonymised aggregates (per LM/question statistics, no user link) |
| **Inactive accounts** | 24 months after the last enrolment ends and no sign-in | Inactivity | Warning email/SMS **48 hours** (and 30 days) before erasure, then treated as closure |
| D10 consent records | Account closure + 3 years | Closure | Delete |
| D11 data requests | Closure of request + 3 years | Closure | Delete |
| D12 audit log — staff and content events | 3 years | Event | Delete partitions older than 3 years |
| D12 audit log — student-originated events | 1 year | Event | Delete partitions |
| D5 infrastructure logs (ALB, CloudFront, VPC, app logs) | **1 year**, of which 180 days readily searchable | Event | S3 lifecycle expiry. 180 days meets the CERT-In minimum; 1 year meets the DPDP Rules log retention as understood (confirm with counsel) |
| D13 analytics raw events | 13 months | Event | Drop monthly partitions |
| D16 error telemetry (Sentry) | 90 days | Event | Vendor setting |
| D15 vendor playback logs | Shortest available vendor setting | Event | Vendor setting; record the value in C-07 |
| Data export files (DSR, admin CSV) | 7 days | Created | S3 lifecycle delete |
| Database backups / snapshots | 35 days (PITR 14 days, daily snapshots 35 days) | Created | Automatic expiry; Object Lock 35 days |
| Content (non-personal) | Indefinite while in use; retired versions kept for audit | — | Retired items archived |

## 3. Erasure procedure (on request or at end of retention)
1. Check for a legal hold or a pending dispute (e.g. an open grievance). If there is one, record the reason and tell the user what is being kept and why.
2. Revoke all sessions and deactivate the account.
3. Run the erasure job `privacy.erase_user(user_id)`. It:
   - nulls or deletes the personal columns listed in §2;
   - deletes the user's rows in progress and attempt tables;
   - writes anonymised aggregates first;
   - removes the user from marketing lists (keeping a hashed suppression entry);
   - asks processors to delete (MSG91 and SES suppression; Sentry user deletion API).
4. Write the audit event `privacy.erasure_completed` with counts only, no personal data.
5. Confirm to the user by email/SMS. The confirmation is sent before the contact details are deleted, at the last step.

**Target:** complete within **30 days** of a verified request (confirm against any period the Rules set), and usually within 7 days.

## 4. Backups and erasure
Backups are not edited. Erased data in backups expires naturally within 35 days. If a backup is restored, the **erasure ledger** (`privacy_erasures`: user ID hash and date) is replayed straight after the restore, so erased users are erased again. This step is in the restore runbook (D-07).

## 5. Implementation
- **Celery beat jobs (daily 02:00 IST):** `purge_otps`, `purge_sessions`, `purge_unverified_signups`, `purge_pending_minors`, `inactive_account_warnings`, `inactive_account_erasure`, `drop_old_partitions` (audit, analytics), `minor_birthday_transition`.
- Each job logs the counts it processed and raises an alert on failure (D-05).
- Partitioned tables (`audit_log`, `analytics_events`) are dropped by partition for efficiency.

## 6. Data principal request SLAs

| Request | Acknowledge | Complete |
|---|---|---|
| Access / summary | Immediately (on screen) | 15 days |
| Correction | Immediately | 7 days (self-service fields are instant) |
| Erasure | Immediately | 30 days (target 7) |
| Consent withdrawal | Immediately | 24 hours |
| Grievance | 24 hours | Within the period the Rules set (confirm with counsel); internal target 15 days |

## 7. Evidence
A monthly report lists the jobs run, the rows deleted per category, requests received and closed, and any SLA breaches. The privacy owner keeps it for 3 years.
