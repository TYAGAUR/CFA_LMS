# D-05 Observability Specification

| Field | Value |
|---|---|
| Document ID | D-05 |
| Version | 0.1 |
| Owner | SRE / DevOps lead |
| Last updated | 2026-10-23 |
| Related | N-01 SLOs, A-05 §8, G-01 (audit, separate), S-02 §7, C-05 |

## 1. Goals
- Detect user-impacting problems before users report them.
- Answer "what happened to request X?" in under 5 minutes, using `request_id`.
- Measure every SLO in N-01.
- Keep PII out of telemetry.

## 2. Signals and tools

| Signal | Tool | Retention |
|---|---|---|
| Application logs (JSON) | CloudWatch Logs, then exported to S3 | 30 days hot; 1 year in S3 (C-05) |
| Infrastructure logs (ALB, CloudFront, VPC Flow, CloudTrail) | S3 (+ Athena for queries) | 1 year |
| Metrics | CloudWatch (Container Insights, RDS, ElastiCache, ALB, custom EMF metrics) | 15 months (CloudWatch default) |
| Traces | OpenTelemetry SDK (FastAPI, SQLAlchemy, httpx, Celery; Next.js server) → ADOT collector sidecar → AWS X-Ray | 30 days |
| Errors | Sentry (backend + frontend, source maps uploaded in CI) | 90 days |
| Synthetic | CloudWatch Synthetics canaries | 30 days |
| Real-user (web vitals) | `web-vitals` → `/api/v1/events` (consented adults) + Lighthouse CI | 13 months (analytics) |

## 3. Logging standard
**Format:** one JSON object per line. Fields:

```json
{
  "ts": "2026-10-23T10:15:00.123Z",
  "level": "info",
  "service": "api",
  "env": "production",
  "version": "v1.4.2+abc1234",
  "request_id": "01JB...",
  "trace_id": "4bf92f...",
  "span_id": "00f067...",
  "user": "u_7f3a...",          // pseudonymous HMAC, never raw ID/mobile
  "role": "student",
  "route": "GET /api/v1/lms/{id}",
  "status": 200,
  "duration_ms": 87,
  "module": "rules",
  "event": "unlock_evaluated",
  "msg": "LM locked",
  "extra": {"unmet_count": 1}
}
```

**Rules:**
- **Never log:** passwords, OTPs, tokens, cookies, Authorization headers, full mobile numbers, emails, DOB, guardian data, answer choices, request or response bodies. A `structlog` processor drops or masks keys matching a deny-list, plus mobile/email regexes, as a backstop.
- **Levels:** `debug` (off in production), `info` (business events, one per request summary), `warning` (handled anomalies), `error` (unhandled exceptions, also sent to Sentry).
- Access logs: one summary line per request (route template, not raw path with IDs).
- `request_id`: taken from `X-Request-ID` (set by CloudFront or ALB), or generated. Returned in responses and in problem+json. Passed on to Celery tasks.

## 4. Metrics

### 4.1 RED metrics (per service and route template)
`http_requests_total{route,method,status_class}`, `http_request_duration_seconds` histogram (p50/p95/p99), error rate.

### 4.2 USE metrics (resources)
ECS CPU and memory; RDS CPU, connections, free storage, read/write latency, replica lag; Redis memory, evictions, connections; Celery queue depth and task latency.

### 4.3 Business and product health metrics (custom, low cardinality)

| Metric | Why |
|---|---|
| `otp_sent_total{channel,result}`, `otp_verify_total{result}` | OTP health; SMS pumping detection |
| `login_total{role,result}` | Auth anomalies |
| `progress_heartbeat_total{result}` | Player health |
| `lm_unlock_total{source}` | Rule engine behaviour |
| `resource_playback_url_issued_total` / `denied_total{reason}` | Access control |
| `job_duration_seconds{task}`, `job_failures_total{task}` | Jobs (imports, retention) |
| `retention_rows_deleted_total{category}` | Privacy evidence |
| `sms_cost_estimate_inr` (daily) | Budget guard |

## 5. Dashboards (CloudWatch or Grafana)
1. **Service overview:** SLO-1/2/3 burn rates, request rate, error rate, p95 by top routes, deploy markers.
2. **Student experience:** canary success, web vitals p75, video start time, OTP success.
3. **Data tier:** RDS, Redis, top slow queries (Performance Insights).
4. **Async:** Celery queue depth, task failures, retention job results.
5. **Security:** auth failures, lockouts, WAF blocks, `denied_total`, audit-alert counts (G-01 §8).
6. **Cost:** daily spend by service tag; SMS spend.

## 6. Alerting
Alerts are based on **SLO burn rate** where possible, to avoid noisy threshold alerts.

| Alert | Condition | Severity | Route |
|---|---|---|---|
| Availability fast burn | 5xx ratio burns 2% of the monthly budget in 1 h (14.4× burn) | P1 page | On-call phone + Slack |
| Availability slow burn | 5% of the budget in 6 h (6× burn) | P2 | Slack, business hours |
| Latency | p95 > 1 s for 10 min on student GET routes | P2 | Slack |
| Canary failure | 2 consecutive failures of the sign-in/subject/video journey | P1 | Page |
| DB | CPU > 80% for 15 min; free storage < 15%; connections > 80% of max | P2 | Slack |
| Redis | Memory > 80%; evictions > 0 | P3 | Slack |
| Celery | Queue depth > 500 for 10 min; any retention-job failure | P2 | Slack |
| OTP | Verify success < 80% over 30 min, or OTP sends > 3× the 7-day hourly average | P2 (possible SMS pumping) | Slack + security |
| WAF | Blocked requests > 10× baseline | P3 | Security channel |
| Audit chain failure | G-01 §5 | P1 | Page + security lead |
| Budget | 80% of the monthly budget | Info | Email PM/DevOps |

Every P1/P2 alert links to a runbook entry (D-07, to be written before launch).

**On-call:**
- Business-hours rotation in Phase 1 (pilot).
- Evening coverage 18:00–23:00 IST during exam season, because peak usage is in the evening.

## 7. Tracing
- OTel auto-instrumentation: FastAPI, SQLAlchemy (statement sanitised; no parameter values), Redis, httpx (outbound to Bunny/MSG91), Celery (trace context propagated through task headers).
- Sampling: 100% of errors; 10% of successful requests in production (tail sampling in the collector); 100% in staging.
- Span attributes must follow the same PII rules as logs.

## 8. Sentry configuration
- `send_default_pii=False`. A `before_send` hook removes request bodies, cookies, headers other than an allow-list, and query strings; it masks mobile and email patterns.
- `user.id` = the pseudonymous ID only.
- Releases tagged with the version; source maps uploaded and **not** served publicly.
- Environment-separated projects; the data region is chosen per C-01 §8.

## 9. Health endpoints
- `/healthz`: process up (no dependencies). Used by the ALB.
- `/readyz`: DB `SELECT 1` and Redis `PING` with a 500 ms timeout. Used at deploy.
- Worker liveness: Celery `inspect ping` through an ECS health-check command.
