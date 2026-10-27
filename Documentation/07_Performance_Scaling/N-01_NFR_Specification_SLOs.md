# N-01 Non-Functional Requirements Specification (SLOs / SLIs)

| Field | Value |
|---|---|
| Document ID | N-01 |
| Version | 0.1 |
| Owner | Tech lead |
| Last updated | 2026-10-23 |
| Related | BRD §14, A-01 §11, A-05, D-05, D-06, N-04 |

BRD §14 states its targets as planning assumptions. This document turns them into measurable requirements.

## 1. Workload assumptions (Phase 1–2, re-validated each phase)

| Parameter | Value |
|---|---|
| Registered students | 2,000 (year 1); design headroom to 10,000 |
| Daily active students | 600 |
| Peak concurrent users | 300 (evening 20:00–23:00 IST; batch start; contest start in Phase 5: 500) |
| Peak API request rate | ~150 req/s (heartbeats dominate: 300 users × 1 per 15 s = 20 req/s; navigation and other calls make up the rest) |
| Content | 56 LMs, ~200 h video, ~1,000 PDFs/notes, 5,000 questions by end of Phase 2 |
| Data growth | ~5 GB/year relational (excluding analytics); analytics ~2–5M events/month |

## 2. Service level objectives

| ID | SLI | SLO | Measurement window | Source |
|---|---|---|---|---|
| SLO-1 | **Availability:** share of successful (non-5xx) responses for `/api/v1/*` excluding `/events` | **99.5%** monthly (≈ 3 h 39 min error budget) | 30 days rolling | ALB/CloudFront logs |
| SLO-2 | **API latency (interactive):** p95 for GET endpoints in the student app | **≤ 400 ms**; p99 ≤ 1 s | 7 days | OTel / ALB target response time |
| SLO-3 | **API latency (writes):** p95 for progress and submit endpoints | ≤ 300 ms (progress); ≤ 1 s (test submit, Ph2) | 7 days | OTel |
| SLO-4 | **Page experience:** LCP p75 on the dashboard and subject view, mobile, Fast 3G | **≤ 2.5 s**; INP p75 ≤ 200 ms; CLS ≤ 0.1 | 28 days | Real-user monitoring (web-vitals → `/events`, consented users) + Lighthouse CI |
| SLO-5 | **End-to-end action time** (BRD: "common dashboard and test actions within 2 seconds") | p95 ≤ **2 s** from user action to rendered result | 7 days | Synthetic canary + RUM |
| SLO-6 | **Video start time** | p90 ≤ 3 s to first frame (India) | 7 days | Player events / vendor analytics |
| SLO-7 | **Autosave durability:** progress or answer acknowledged by the API is never lost | 100% (no acknowledged write lost) | — | Tests + incident review |
| SLO-8 | **OTP delivery:** SMS delivered within 30 s | ≥ 97% | 7 days | Provider delivery reports |
| SLO-9 | **Async jobs:** CSV import (≤ 2,000 rows) done | p95 ≤ 60 s | 7 days | Job metrics |

**Error budget policy:**
- If SLO-1 has consumed more than 50% of the budget by mid-month, feature releases go to the PO and tech lead for review.
- If the budget is exhausted, there is a release freeze except for reliability fixes until the window recovers.

## 3. Performance budgets (engineering guardrails)

| Item | Budget |
|---|---|
| JS shipped on student routes (gzipped, first load) | ≤ 180 KB |
| Fonts | Figtree subset, WOFF2, ≤ 4 weights preloaded (≤ 120 KB total); no base64 inlining |
| API DB queries per request | ≤ 10 (N+1 detection in tests with SQLAlchemy event counters) |
| DB statement timeout (API role) | 5 s; long reports run as jobs |
| API payload size | ≤ 200 KB typical; lists paginated (max 200 items) |
| Images | Responsive `next/image`, AVIF/WebP, lazy below the fold |

## 4. Scalability
- Stateless web, API and worker tiers that scale horizontally (A-05 §3).
- Must sustain **3× the peak workload** in §1 (900 concurrent users, ~450 req/s) on staging-sized production for 30 minutes with SLO-2 met. Verified by the load test (N-04).
- Database: vertical scaling up to db.r6g.xlarge, then a read replica for reports and analytics (N-03).

## 5. Reliability and recovery

| Item | Target |
|---|---|
| RPO (data loss) | ≤ 15 minutes (regional disaster); ≈ 0 for an AZ failure (Multi-AZ synchronous) |
| RTO | ≤ 5 minutes (AZ failure, automatic); ≤ 4 hours (regional disaster, runbook) |
| Backups | PITR 14 days; daily snapshots kept 35 days; cross-region copy |
| Restore test | Quarterly; result recorded (D-06) |
| Planned maintenance | Zero-downtime deploys (rolling, expand/contract migrations). Database maintenance window Sunday 03:00–05:00 IST |

## 6. Security (summary)
Covered by S-01, S-02 and S-03. Measurable items:
- TLS rating A+ (SSL Labs).
- 0 open Critical findings; High findings fixed within 30 days.
- 100% of endpoints covered by the authorisation matrix.
- MFA on 100% of staff accounts.

## 7. Data integrity
- Answers and progress are autosaved on every change (BR-TST-08, BR-PRG-05); writes are idempotent.
- An interrupted session resumes without loss of acknowledged data (SLO-7).
- Referential integrity through foreign keys; versioned content is immutable (ADR-007).

## 8. Accessibility
WCAG 2.1 AA on all student and staff screens (C-08). Zero serious or critical axe violations in CI on key routes.

## 9. Compatibility
Browser and device matrix in Q-01 §7. Works with a 360px-wide viewport and on Fast 3G.

## 10. Maintainability and operability
- **Deployment frequency:** at least weekly to production; lead time from merge to production ≤ 1 day.
- **Change failure rate** ≤ 15%; **MTTR** ≤ 1 hour for S1 incidents.
- Observability: every request traceable by `request_id` (D-05); dashboards for every SLO.
- Documentation: the ADR for any significant decision is merged before the code.

## 11. Privacy
Covered by C-01 to C-06. Measurable items:
- Data requests closed within the SLA in C-05 §6.
- Retention jobs show 100% success each month.

## 12. Verification matrix

| NFR | Verified by | When |
|---|---|---|
| SLO-2/3/5 | Load test (N-04), canary | Pre-release, continuous |
| SLO-4 | Lighthouse CI on PR (budgets), RUM | PR, continuous |
| SLO-1 | Monitoring | Continuous |
| RPO/RTO | Restore drill, DR exercise | Quarterly / yearly |
| Security | S-03 gates, pen test | PR / release |
| Accessibility | axe in E2E, manual audit | Nightly / phase |
