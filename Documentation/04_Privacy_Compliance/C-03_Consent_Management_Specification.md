# C-03 Consent Management Specification

| Field | Value |
|---|---|
| Document ID | C-03 |
| Version | 0.1 — Draft; legal review required |
| Owner | Product owner + Privacy |
| Last updated | 2026-10-23 |
| Related | C-01 DPIA, A-03 `consents`, `guardians`; P-03 E3; P-05 WF-01, WF-02, WF-10 |

## 1. Consent purposes

| Code | Purpose | Required? | Default | Withdrawal effect | Minors |
|---|---|---|---|---|---|
| `service_delivery` | Create and run the account: sign-in, access to enrolled content, progress tracking, tests, service messages (OTP, account notices) | Required to use the service | — (accept to continue) | Cannot be withdrawn on its own; withdrawing means an account deletion request (WF-10) | Guardian gives it |
| `product_analytics` | Pseudonymous usage analytics to improve the product (Q-05) | Optional | Off | Event collection stops within 24 hours; past events stay pseudonymous and follow the retention schedule | **Not offered** while `is_minor` (C-01 PR-2) unless legal clearance flag `minor_analytics_allowed` is set |
| `marketing_messages` | Offers, new batches, events by SMS/WhatsApp/email | Optional | Off | Messaging stops within 24 hours; a suppression list is kept | Guardian decides |
| `leaderboard_display` (Phase 5) | Show my name on leaderboards | Optional | Off | Shown as "Student #code" from the next leaderboard refresh | **Not offered** while `is_minor` unless cleared |

Security logging, fraud prevention and legally required retention are covered by legitimate uses or legal obligations (C-01 §3 row 1). They are described in the notice but are **not** presented as optional choices.

## 2. Notice requirements
- **Itemised list:** the personal data collected and the purpose of each item.
- How to withdraw consent, and how to exercise rights (access, correction, erasure, grievance, nomination).
- How to complain to the Data Protection Board of India.
- Grievance officer contact.
- **Version ID** (e.g. `2026-11-v1`), stored with every consent.
- Language: English at launch, Hindi in Phase 2. Shown before any optional consent is asked. Kept short, with a link to the full privacy policy (C-02).

## 3. UI flow — adult student (WF-01)

```
[Notice summary card]  "What we collect and why"  (expandable sections)
  ☑ Required: Account & learning service       (cannot untick; explained)
  ☐ Help improve the product (usage analytics)
  ☐ Send me updates about batches and events
[Read full privacy policy]    [Agree and continue]
```

- The agree button is enabled without the optional boxes being ticked; each optional box stays independent.
- No dark patterns: no pre-ticked boxes, and equal visual weight for accepting and declining optional purposes.

## 4. Consent records
- Stored append-only in `consents` (A-03 §3.2), one row per purpose per decision, with: `notice_version`, `actor` (self/guardian), `method`, timestamp, IP and user agent.
- The current state is the latest row per purpose. It is cached on the user session and refreshed on change.
- Records are kept for the life of the account plus **3 years** (as evidence; C-05).
- Every grant or withdrawal also writes an audit event `consent.changed` (G-01).

## 5. Verifiable parental consent (under 18)

**Trigger:** the DOB entered at sign-up gives an age under 18 on the sign-up date (IST).

**Flow (WF-02):**
1. The student enters the guardian's full name, relationship (parent / legal guardian) and mobile number. The guardian's number must differ from the student's.
2. The system sends the guardian an SMS: "{Student first name} has asked to join {Product}. Review and give consent: {short link}". The link is a signed token valid for 7 days.
3. The guardian page shows the notice for guardians in plain language. It covers what data is collected about the child, purposes, rights, and that analytics and leaderboard are disabled for minors.
4. The guardian enters the OTP sent to their number, confirms "I am the parent or lawful guardian of {student}", and accepts.
5. The system records: guardian record (`verified_at`, method `sms_otp`), a `consents` row with `actor=guardian`, and an audit event. The student account becomes `active`.
6. A reminder goes out on day 3 and day 7. If there is no consent by day 30, the account and its data are deleted (C-05).

**Strength of verification:** SMS OTP to a separate number shows control of that number, but not that the person is the actual parent.
- Counsel must confirm whether this meets the Rules for verifiable consent. The alternatives are checking identity and age details against reliable records, or a virtual token from an authorised entity, e.g. DigiLocker.
- **Design allowance:** `verification_method` is an enum. Adding `digilocker` later needs no schema change.

**Guardian rights:**
- The guardian can withdraw consent (link in the confirmation SMS/email, or through support). The student account is then suspended immediately and handled as an erasure request.
- Optional purposes for a minor (`marketing_messages`) are chosen by the guardian on the same page.

**Turning 18:**
- A daily job flags accounts whose holder has turned 18.
- At next sign-in the student sees the adult notice and makes their own optional choices. The guardian link is retired, the DOB is reduced to `is_minor=false` (C-01 §2), and minor restrictions are lifted only for purposes the adult opts into.

## 6. Withdrawal and changes
- The profile has a "Privacy & consents" page (S-11) with a toggle per optional purpose and the date it was last changed.
- Withdrawal takes effect in the product immediately, and in downstream processors (e.g. marketing lists) within 24 hours. A Celery job syncs suppression lists.
- **Notice version change:**
  - Material changes (new purpose, new data category) need fresh consent at the next sign-in for the affected purposes.
  - Non-material changes are shown as a banner and logged.

## 7. Enforcement in code
- `privacy.has_consent(user, purpose)` is the only way to check consent. Analytics capture, marketing sends and leaderboard rendering call it.
- `privacy.minor_restricted(user, feature)` combines `is_minor` with the feature flags.
- Unit tests: analytics events are dropped without consent; minors never show on leaderboards; marketing sends skip suppressed users.

## 8. Reporting
The admin report "Consent status" shows counts per purpose, minors pending guardian consent (with age of request) and withdrawals in the last 30 days. It contains no personal details unless the admin opens a specific user.
