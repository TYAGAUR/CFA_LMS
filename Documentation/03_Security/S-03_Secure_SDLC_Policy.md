# S-03 Secure SDLC Policy

| Field | Value |
|---|---|
| Document ID | S-03 |
| Version | 0.1 |
| Owner | Security lead + DevOps lead |
| Last updated | 2026-10-23 |
| Related | S-01, S-02, D-02 CI/CD, U-04 Coding standards |

## 1. Lifecycle activities

| Stage | Security activity | Output |
|---|---|---|
| Plan | Classify the data the feature touches; flag stories that change auth, RBAC, content rendering, uploads, tests or exports | `security-impact` label on tickets |
| Design | Threat-model delta for flagged features (update S-01); ADR for security-relevant choices | Updated threat table |
| Build | Secure coding standards (§3), pre-commit hooks, unit tests including negative authorisation cases | Code + tests |
| Verify | CI gates (§2), peer review (two reviewers for sensitive modules), ZAP baseline on staging | Green pipeline |
| Release | Release checklist (§5); migrations reviewed; feature flags | Release notes |
| Operate | Monitoring, vulnerability management (S-02 §8), incident response (S-06) | Alerts, tickets |

## 2. CI security gates (block merge on failure)

| Gate | Tool | Fails on |
|---|---|---|
| Secrets | gitleaks (pre-commit + CI) | Any finding |
| Python SAST | Semgrep (`p/python`, `p/fastapi`, custom rules) + Bandit | High severity |
| TS/JS SAST | Semgrep (`p/typescript`, `p/react`, `p/nextjs`) + ESLint security plugins | High severity |
| Python dependencies | `pip-audit` (uv/poetry lock) | Known vuln ≥ High with a fix available |
| JS dependencies | `npm audit --audit-level=high` (or `pnpm audit`) | ≥ High with a fix available |
| Containers | Trivy image scan | Critical/High with a fix available |
| IaC | `tflint`, `checkov` | High |
| Licences | `pip-licenses` / `license-checker` | Copyleft (GPL/AGPL) in a runtime dependency without approval |
| Authorisation tests | pytest marker `authz` | Any failure |
| API contract | Snapshot test that assessment payloads omit answer fields | Any failure |
| SBOM | Syft (CycloneDX) attached to the build | — (informational) |

Nightly: OWASP ZAP baseline against staging; Dependabot / Renovate PRs for updates.

## 3. Secure coding rules (enforced by review and lint where possible)

**Backend (FastAPI)**
1. Every router uses `Depends(require("<permission>"))`. A test fails if a route has no permission dependency, except an explicit allow-list of public routes.
2. Every service method that loads a user-owned record checks ownership.
3. Every content or resource access calls `rules.assert_unlocked` and `enrolment.assert_entitled`.
4. Use the ORM or `text()` with bound parameters only. No f-string SQL (Semgrep rule).
5. Pydantic models use `extra="forbid"`, length limits and enums. Response models are explicit, so internal fields (`source_ref`, `correct_index`) are never serialised by accident.
6. No `pickle`, `eval` or `yaml.load` on untrusted data. Use `defusedxml` if XML is ever parsed. XLSX parsing (openpyxl) runs in workers with size limits.
7. Errors return problem+json without stack traces. Exceptions are logged with `request_id`.
8. Outbound HTTP uses an allow-listed client wrapper with timeouts (5 s connect, 15 s read). No user-controlled URLs are fetched (SSRF).
9. Cryptography only through `app/core/security.py` helpers (Argon2id, HMAC, token generation with `secrets`).

**Frontend (Next.js)**
1. `dangerouslySetInnerHTML` is banned, except in `components/notes/BlockRenderer` (lint rule plus CODEOWNERS).
2. No tokens in `localStorage` or `sessionStorage`. Auth is cookie-only.
3. CSP nonces through middleware. No inline event handlers. Third-party scripts only from the CSP allow-list.
4. External links use `rel="noopener noreferrer"`.
5. Server components must not pass secrets or server-only fields to client components (`server-only` package used in data modules).

**Infrastructure**
1. Terraform only. Security groups never use `0.0.0.0/0` ingress except on CloudFront/ALB 443.
2. S3 buckets: Block Public Access, TLS-only policy, encryption required.

## 4. OWASP ASVS 4.0 Level 2 — checklist mapping (abridged)

| ASVS chapter | Key requirements | Where implemented | Verified by |
|---|---|---|---|
| V1 Architecture | Threat model, security controls centralised | S-01, `app/core` | Design review |
| V2 Authentication | MFA for privileged users, breached-password check, OTP limits | `auth` module | Unit + pen test |
| V3 Session management | httpOnly/Secure cookies, rotation, logout invalidation, idle timeout | `auth` | Unit + ZAP |
| V4 Access control | Deny by default, server-side, IDOR protection | RBAC dependency, services | authz test matrix |
| V5 Validation, sanitisation | Schema validation, output encoding, no raw HTML | Pydantic, block renderer | SAST + tests |
| V7 Error handling, logging | No sensitive data in logs; security events logged | D-05, G-01 | Log review |
| V8 Data protection | Cache-Control no-store, minimal data in responses | API middleware | ZAP |
| V9 Communication | TLS everywhere | A-05 | SSL Labs A+ |
| V10 Malicious code | Dependency hygiene, integrity | CI gates | Pipeline |
| V12 Files and resources | Upload limits, AV scan, served safely | `media` module | Pen test |
| V13 API | Rate limits, content-type checks, CSRF | Middleware | Tests |
| V14 Configuration | Hardened headers, secrets management, SBOM | Edge + CI | Scans |

The full ASVS L2 spreadsheet is kept in this folder (`S-03a_ASVS_L2_Checklist.xlsx`, to be created in Phase 1 sprint 1) and updated at each phase gate.

## 5. Release security checklist
- [ ] All CI gates green; no open Critical/High findings without an exception.
- [ ] Migrations reviewed for data exposure (new columns classified in A-03).
- [ ] New endpoints have permission dependencies and authz tests.
- [ ] New third-party services are in C-07 with a DPA.
- [ ] Feature flags set correctly in production (including under-18 restrictions).
- [ ] Threat model updated if `security-impact` stories shipped.
- [ ] Rollback plan documented (D-03).

## 6. Training
- Developers complete secure coding training (OWASP Top 10 and API Security Top 10) at onboarding and once a year.
- Authors and reviewers are trained on content provenance and copyright (C-06).
