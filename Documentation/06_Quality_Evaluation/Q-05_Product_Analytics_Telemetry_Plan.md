# Q-05 Product Analytics / Telemetry Plan

| Field | Value |
|---|---|
| Document ID | Q-05 |
| Version | 0.1 |
| Owner | Product owner + Data analyst |
| Last updated | 2026-10-23 |
| Related | C-03 (consent `product_analytics`), C-04 D13, C-05, M-01 §3 success measures, Q-04 (later) |

## 1. Goals
1. Measure the charter's success measures (M-01 §3) and the phase KPIs.
2. Understand where students drop off (onboarding, LM completion, unlocks).
3. Improve the product while respecting consent and the rules for children.

## 2. Two data sources (important distinction)

| Source | What | Consent needed? | Use |
|---|---|---|---|
| **Operational data** (progress, attempts, enrolments) | Business records needed to provide the service | Covered by `service_delivery` | Admin and faculty reports; the student's own analytics; aggregated KPIs |
| **Behavioural events** (clicks, screen views, feature usage) | Optional product telemetry | **Yes:** `product_analytics` opt-in, **adults only** (C-03 §1) | Funnels, UX research, feature adoption |

Most charter KPIs (completion, revisions, tests) can be computed from **operational data in aggregate**, so they don't depend on the analytics opt-in rate.

## 3. Event design rules
- Names use the form `object_action`, in snake_case and past tense: `video_played`, `lm_opened`.
- Every event has: `event_id`, `name`, `occurred_at` (UTC), `pseudo_user_id` (HMAC-SHA256 of the user ID with a rotating annual key), `session_id`, `app_version`, `platform` (web, mobile-web), `viewport_class`.
- **No PII in properties:** no names, mobile numbers, emails, free text, search text, IP or exact DOB. Search queries are recorded only as `query_length` and `result_count`.
- Properties are typed and listed in the tracking plan (§4). Unknown properties are dropped at ingestion.
- **Consent gate:** events are only sent if `has_consent(user, 'product_analytics')` is true and the user is not a minor. The check happens **server-side at ingestion**, as well as client-side.

## 4. Tracking plan (Phase 1)

| Event | Trigger | Properties |
|---|---|---|
| `signup_started` | OTP requested (signup) | `channel` |
| `signup_completed` | Account created | `is_minor_flow` (bool; recorded only for the aggregate funnel and without a user ID if the user is a minor) |
| `guardian_consent_completed` | Guardian accepts | `days_to_consent` (no user ID) |
| `session_started` | App opened with a valid session | `entry_route` |
| `dashboard_viewed` | Dashboard render | `next_action_type` |
| `next_action_clicked` | Hero CTA | `next_action_type` |
| `subject_opened` | Subject view | `subject_code` |
| `lm_opened` | LM selected | `subject_code`, `lm_no`, `state` |
| `locked_lm_viewed` | Locked LM shown | `subject_code`, `lm_no`, `unmet_types[]` |
| `notes_viewed` | Notes tab | `subject_code`, `lm_no`, `topic_index`, `scroll_depth_pct` (on leave) |
| `video_played` / `video_paused` / `video_completed` | Player | `resource_kind`, `subject_code`, `lm_no`, `position_bucket` (10% buckets), `speed` |
| `pdf_opened` | Viewer | `subject_code`, `lm_no` |
| `lm_marked_learned` | Button | `subject_code`, `lm_no`, `mandatory_completion_pct` |
| `revision_logged` | Dialog | `activity`, `counted` |
| `eoc_saved` | Form | `subject_code`, `lm_no`, `completed` |
| `search_performed` | Search | `query_length`, `result_count`, `types[]` |
| `search_result_clicked` | Click | `result_type`, `rank` |
| `bookmark_added` | Click | `target_type` |
| `error_shown` | Error screen or toast | `code` (problem+json code), `route` |

Later phases add `test_built`, `test_submitted`, `flashcard_rated`, `mock_entry_saved`, `contest_registered`, and so on, with the same rules.

## 5. Pipeline
**Phase 1 (simple, first-party, low cost):**

```
Browser → POST /api/v1/events (batched, max 50/request, sendBeacon on unload)
       → API validates schema + consent + minor flag
       → INSERT analytics_events (monthly partition)
Metabase (self-hosted, read-only replica or reporting role) → dashboards
```

- Nothing is sent to third-party analytics SaaS in Phase 1, so no new processors are needed.
- **Later:** self-hosted PostHog if session-level funnels or feature flags are needed. This needs a C-07 update.

## 6. Dashboards

| Dashboard | Audience | Key metrics | Source |
|---|---|---|---|
| Executive KPIs | Sponsor, steering | Active students (WAU/MAU), subject completion distribution, LMs learned per week, revision adherence (O2), retention cohorts | Operational aggregates |
| Learning funnel | Product, academic lead | Per LM: opened → mandatory complete → learned → (Ph2) quiz pass; median days per LM; drop-off LMs | Operational + events |
| Content performance | Academic lead, authors | Video completion by resource, rewatch hotspots (position buckets), notes scroll depth, most-viewed locked LMs | Events (consented adults) |
| Onboarding | Product, ops | Sign-up funnel, OTP success rate, guardian consent time, enrolment lag | Events + operational |
| Reliability | Tech lead | `error_shown` by code and route (combined with Sentry, D-05) | Events |

**Small-number protection:** reports for academic and ops audiences hide segments with fewer than 5 students.

## 7. KPI definitions (Phase 1)

| KPI | Definition |
|---|---|
| Weekly active students (WAS) | Distinct students with ≥ 1 progress write or `session_started` in the IST week |
| LM completion rate | LMs marked learned ÷ LMs unlocked, per cohort |
| Mandatory-before-learned rate (O1) | LMs marked learned with 100% mandatory resources complete ÷ all LMs marked learned |
| Revision adherence (O2) | Students with ≥ 1 counted revision in every entitled subject in the last 8 weeks before the exam window ÷ active students in that batch |
| Time to first value | Median minutes from sign-up to first resource completion |
| Unlock friction | Median days an LM stays locked after the previous LM was opened |

## 8. Governance
- The tracking plan in §4 is the contract. New events need a PR that updates this document and the ingestion schema together.
- Every quarter, check that events contain no PII (sample 1,000 events) and that consent is enforced (test accounts).
- Retention: raw events are kept for 13 months (C-05).
