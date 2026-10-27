# S-02 Information Security Policies

| Field | Value |
|---|---|
| Document ID | S-02 |
| Version | 0.1 — Draft for management approval |
| Owner | Security lead |
| Approver | Sponsor |
| Last updated | 2026-10-23 |
| Review | Annually, or after a major incident or change |
| Applies to | All staff, contractors and systems of the CFA Learning Hub platform |

"Must" statements are mandatory. Exceptions need written approval from the security lead and are recorded with an expiry date in the exceptions register (§12).

## 1. Governance
1.1 The sponsor is accountable for information security. The security lead owns these policies and reports on them monthly to the steering group.
1.2 Every person with access must read these policies and acknowledge them on joining and once a year.
1.3 Information is classified C0–C4 (A-03 §1). Handling follows §9.

## 2. Access control
2.1 Access is granted on least privilege and need-to-know, through the roles in P-06.
2.2 Every access is tied to an individual identity. Shared accounts are not allowed, except service accounts that have a named owner.
2.3 Access requests and changes go through the admin console or IAM Identity Center and are audit-logged.
2.4 When someone leaves or changes role, their access is removed within **24 hours** (same day for privileged roles).
2.5 Privileged access (admin, super_admin, production cloud access) is reviewed **quarterly** (G-04).
2.6 Production cloud access is time-bound (maximum 8 hours) through permission sets with MFA. There is no standing administrator access.
2.7 Break-glass access follows P-06 §5.

## 3. Authentication
3.1 Students sign in with a one-time password (SMS or email). OTPs are 6 digits, valid for 5 minutes, and limited in attempts.
3.2 Staff need a password plus TOTP MFA. Passwords are at least 12 characters, are checked against a breached-password list, and do not need forced periodic rotation (NIST SP 800-63B).
3.3 Accounts lock for 15 minutes after 5 consecutive failed logins.
3.4 Sessions: access tokens last at most 15 minutes. Student sessions last at most 30 days. Staff sessions time out after 30 minutes idle and 12 hours in total.
3.5 Step-up authentication (TOTP again) is required for role changes, unlock-rule changes, bulk exports and settings changes.
3.6 Cloud console, GitHub and SaaS admin accounts must use SSO or MFA. Hardware security keys are recommended for super admins.

## 4. Cryptography and key management
4.1 Data in transit uses TLS 1.2 or higher with modern cipher suites. Plain HTTP is redirected; HSTS is enabled.
4.2 Data at rest is encrypted with AES-256 through AWS KMS customer-managed keys, with separate keys per data class.
4.3 Passwords are hashed with Argon2id (memory ≥ 64 MB, t=3). Refresh tokens and OTPs are stored as hashes only.
4.4 Application-level secrets (TOTP seeds) use envelope encryption with KMS.
4.5 JWT signing keys (Ed25519) are rotated every 90 days, with overlapping validity.
4.6 KMS keys rotate automatically every year. Key deletion needs super-admin approval and a 30-day waiting period.

## 5. Secrets management
5.1 Secrets live only in AWS Secrets Manager (cloud) and in `.env` files that are never committed (local).
5.2 Secrets must not appear in code, logs, tickets, chat or documents.
5.3 Database credentials rotate every 30 days; third-party API keys every 180 days, and immediately if exposure is suspected.
5.4 CI uses OIDC federation, with no long-lived cloud keys.

## 6. Secure development
6.1 All code changes go through pull requests with at least one approving review (two for `auth`, `rules`, `tests`, `audit` and `infra`).
6.2 CI security gates must pass before merge (S-03).
6.3 Production data must not be used in development or staging. Staging uses synthetic or anonymised data.
6.4 Developers follow the OWASP ASVS Level 2 requirements listed in S-03.

## 7. Logging and monitoring
7.1 Security-relevant events are logged as set out in G-01, including authentication, authorisation failures, admin actions and data exports.
7.2 Logs must not contain passwords, OTPs, tokens, full mobile numbers, DOB or answer content.
7.3 Logs are kept for at least **180 days** within India (CERT-In Directions, 2022). Audit-log retention follows C-05.
7.4 Alerts for security events go to the on-call channel and are triaged within 1 business hour, or 15 minutes for critical alerts.
7.5 System clocks synchronise to the AWS Time Sync Service (NTP). CERT-In requires NTP sync to approved sources; AWS time sync is used and recorded.

## 8. Vulnerability and patch management
8.1 Dependencies and container images are scanned on every build and every week.
8.2 Fix deadlines from discovery: Critical **7 days**, High **30 days**, Medium **90 days**, Low at the next planned upgrade.
8.3 An external penetration test runs before each major release (Phase 1 and Phase 2 at least) and every year.
8.4 Security reports from outside are received at `security@<domain>`, with a published `security.txt`.

## 9. Data handling

| Class | Storage | Sharing | Disposal |
|---|---|---|---|
| C0 Public | Anywhere | Free | Normal |
| C1 Internal | Company systems | Staff and contractors under NDA | Normal deletion |
| C2 Confidential IP | Company systems; access-controlled | Need-to-know; watermarking for student distribution | Secure deletion |
| C3 Personal | Production systems in India | Only processors listed in C-07 with DPAs | Per C-05; crypto-shred backups at expiry |
| C4 Restricted | Encrypted, restricted columns or tables | No export without DPO approval | Per C-05 |

9.1 Personal data must not be downloaded to personal devices. Admin CSV exports containing C3/C4 data are logged and expire after 7 days.
9.2 Screenshots of student data must not be shared in public chat groups.

## 10. Third-party (vendor) security
10.1 Before onboarding, a vendor that processes personal data or content needs a security review (questionnaire plus SOC 2/ISO 27001 evidence where available), a DPA and an entry in the C-07 register.
10.2 Vendors are reviewed every year.

## 11. Incident management
11.1 Suspected incidents are reported immediately to the security lead and the on-call engineer.
11.2 Incidents are handled under the Incident Response Plan (S-06). This includes reporting to CERT-In within **6 hours** for reportable incidents, and notifying the Data Protection Board and affected people for personal data breaches under the DPDP Act (C-01).

## 12. Exceptions register
| ID | Policy clause | Exception | Compensating control | Approved by | Expires |
|---|---|---|---|---|---|
| EX-01 | A-05 §4 | One NAT gateway in production | Outbound SMS/email failover runbook (D-07) | [TBD] | Phase 2 review |

## 13. Endpoint and acceptable use (staff)
- Company work happens only on devices with disk encryption, an OS screen lock (≤ 5 minutes), current OS patches and anti-malware.
- Unapproved tools must not be used to process student data or proprietary content. This includes pasting content into public AI tools, unless the AI policy (L-01) allows it.
- Report a lost device within 24 hours. Sessions are then revoked remotely.
