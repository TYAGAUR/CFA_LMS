# CFA Learning Hub (Karan Sir Classes LMS) — Documentation Register

This is the master list of documents needed to build, launch and run the LMS in a production environment.
Each document goes in the numbered category folder next to this file.

**Stack:** Next.js (frontend) · FastAPI (backend) · PostgreSQL
**Source requirements:** [LMS BRD.docx](01_Product/LMS%20BRD.docx) · **Prototype:** [Karan_Sir_Classes_Platform_Demo.html](01_Product/Karan_Sir_Classes_Platform_Demo.html)

**"Needed by" values**
- **Phase 0:** project setup
- **Phase 1:** Foundation
- **Phase 2:** Assessment
- **Phase 3:** Revision
- **Phase 4:** Exam readiness
- **Phase 5:** Engagement (contests, XP, leaderboard, certificates)
- **AI phase:** before any AI or LLM feature
- **Pre-launch:** must be finished before production go-live

**Status values:** Exists · To do · Draft · In review · Approved

---

## 01 Product — `01_Product/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| P-01 | Business Requirements Document | Vision, scope, roles, FR-01–FR-14, NFRs, roadmap, open decisions | Product owner | Done | **Exists** |
| P-02 | Clickable demo / prototype | Student UX: learn → quiz → unlock, custom quiz, flashcards, contests, certificate | Product / Design | Done | **Exists** |
| P-03 | [Product Requirements / Functional Spec (PRD)](01_Product/P-03_Product_Requirements_Specification.md) | User stories and acceptance criteria per FR, screen list, edge cases, error states | Product owner | Phase 1 | Draft |
| P-04 | [Personas & Journey Maps](01_Product/P-04_Personas_and_Journey_Maps.md) | Student, instructor/author, academic reviewer, admin, super-admin, parent | Product / Design | Phase 1 | Draft |
| P-05 | [User Workflow Specifications](01_Product/P-05_User_Workflow_Specifications.md) | Swimlane flows: enrollment, study → mark learned → unlock, test build/attempt/resume, author → review → approve → publish, mock self-entry, flashcard review, contest (Phase 5), user and entitlement admin | Business analyst | Phase 1 | Draft |
| P-06 | [Roles & Permissions (RBAC) Matrix](01_Product/P-06_Roles_and_Permissions_Matrix.md) | Role × resource × action, entitlement rules for licensed content | Product + Security | Phase 1 | Draft |
| P-07 | [UI/UX Spec & Design System](01_Product/P-07_UI_UX_Spec_and_Design_System.md) | Tokens carried over from the demo, components, states, responsive and dark mode, wireframes | Design | Phase 1 | Draft |
| P-08 | Content Authoring Style Guide | Notes/revision-sheet templates (navy/gold/teal, Bahnschrift, 2-page sheets), question-writing rules, A/B/C format, LOS command words, LM naming rules (FSA −26, Equities −38), no source labels | Academic lead | Phase 2 | To do |
| P-09 | [Business Rules Specification](01_Product/P-09_Business_Rules_Specification.md) | Unlock rule engine conditions, pass thresholds (≥ vs >), mock prerequisites, test-builder rules, spaced-repetition scheduling | Product + Tech lead | Phase 1 | Draft |
| P-10 | [Product Roadmap & Backlog](01_Product/P-10_Product_Roadmap_and_Backlog.md) | Phases 1–5, release scope, prioritisation | Product owner | Ongoing | Draft |
| P-11 | [Glossary](01_Product/P-11_Glossary.md) | LM, LOS, EOC, Premium Pack, Set 1/Set 2, practice vs assessment mode | Business analyst | Phase 1 | Draft |
## 02 Architecture — `02_Architecture/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| A-01 | [Software Architecture Document](02_Architecture/A-01_Software_Architecture_Document.md) | C4 context/container/component views: Next.js, FastAPI, PostgreSQL, worker queue, object storage, video host | Solution architect | Phase 1 | Draft |
| A-02 | [Architecture Decision Records (ADRs)](02_Architecture/A-02_Architecture_Decision_Records.md) | One record per key decision: stack, auth (OTP/JWT), video host, SRS algorithm, search, hosting | Solution architect | Ongoing | Draft |
| A-03 | [Data Model, ERD & Data Dictionary](02_Architecture/A-03_Data_Model_ERD_and_Data_Dictionary.md) | Every table and field, content/question versioning model, data classification per field | Tech lead / DBA | Phase 1 | Draft |
| A-04 | [API Specification & Standards](02_Architecture/A-04_API_Specification_and_Standards.md) | OpenAPI spec, versioning, error format, pagination, idempotency, rate limits | Backend lead | Phase 1 | Draft |
| A-05 | [Infrastructure Architecture](02_Architecture/A-05_Infrastructure_Architecture.md) | Cloud provider and India region, VPC/network, WAF/CDN, managed PostgreSQL, Redis, object storage, video CDN, environment topology | Cloud architect | Phase 1 | Draft |
| A-06 | Integration Specifications | Video host, email/SMS/WhatsApp, payments, SSO/OTP, LLM provider, analytics | Tech lead | Per phase | To do |
| A-08 | [Payments & Registration Integration Spec](02_Architecture/A-08_Payments_and_Registration_Integration.md) | Provider-neutral payment module, Razorpay adapter, order/webhook lifecycle, event contract for distributed teams | Tech lead | Phase 1 | Draft (implemented) |
| A-07 | Domain Engine Specifications | Test engine (draw, randomise, autosave, scoring), release validator (BRD §8.1), DOCX/PDF export generator | Backend lead | Phase 2 | To do |

## 03 Security — `03_Security/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| S-01 | [Security Architecture & Threat Model](03_Security/S-01_Security_Architecture_and_Threat_Model.md) | STRIDE per component, trust boundaries, attack surfaces (answer leakage, file uploads, rich-text XSS, account sharing) | Security lead | Phase 1 | Draft |
| S-02 | [Information Security Policies](03_Security/S-02_Information_Security_Policies.md) | Access control, authentication/MFA, passwords, encryption in transit and at rest, key and secrets management | Security lead | Phase 1 | Draft |
| S-03 | [Secure SDLC Policy](03_Security/S-03_Secure_SDLC_Policy.md) | Code review, SAST/DAST, dependency and container scanning, OWASP ASVS Level 2 checklist | Security + DevOps | Phase 1 | Draft |
| S-04 | Assessment Integrity Specification | Server-side grading, no answers sent to the client, contest windows, one-attempt rule, suspicious-activity logging | Tech lead | Phase 2 | To do |
| S-05 | Vulnerability Management & Pen-test Plan | Scan cadence, patch SLAs, external penetration test before launch | Security lead | Pre-launch | To do |
| S-06 | Incident Response Plan | Severity levels, roles, communications, CERT-In 6-hour reporting, post-mortem template | Security lead | Pre-launch | To do |

## 04 Privacy & Compliance — `04_Privacy_Compliance/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| C-01 | [DPDP Act 2023 Compliance Assessment / DPIA](04_Privacy_Compliance/C-01_DPDP_Compliance_Assessment_DPIA.md) | Lawful basis, notice, consent, data-principal rights, children's data (verifiable parental consent under 18), grievance officer | Privacy / Legal | Phase 1 | Draft |
| C-02 | Privacy Policy & Terms of Use | Student-facing; includes the disclaimer that the readiness score is an LMS estimate | Legal | Pre-launch | To do |
| C-03 | [Consent Management Specification](04_Privacy_Compliance/C-03_Consent_Management_Specification.md) | Leaderboard name display, marketing, analytics, parent access | Product + Privacy | Phase 1 | Draft |
| C-04 | [Data Inventory & Classification (RoPA)](04_Privacy_Compliance/C-04_Data_Inventory_and_Classification_RoPA.md) | What personal data is held, where, why, who can access it | Privacy | Phase 1 | Draft |
| C-05 | [Data Retention & Deletion Policy](04_Privacy_Compliance/C-05_Data_Retention_and_Deletion_Policy.md) | Retention period per data type, deletion and anonymisation jobs | Privacy + Tech lead | Phase 1 | Draft |
| C-06 | [Content Licensing & IP Register](04_Privacy_Compliance/C-06_Content_Licensing_and_IP_Register.md) | Provenance per asset, third-party permissions, CFA Institute trademark and disclaimer use, confirmation that licensed EOC/Premium content is not hosted | Academic lead + Legal | Phase 1 | Draft |
| C-07 | Vendor / Sub-processor Register & DPAs | Cloud, video, email/SMS, payments and LLM vendors | Legal / Procurement | Pre-launch | To do |
| C-08 | Accessibility Conformance Report | WCAG 2.1 AA audit results and remediation | QA / Design | Pre-launch | To do |

## 05 Audit & Governance — `05_Audit_Governance/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| G-01 | [Audit Logging Specification](05_Audit_Governance/G-01_Audit_Logging_Specification.md) | Events (logins, role changes, content approvals, grade changes, exports, data access), fields, tamper-evidence, retention | Tech lead + Security | Phase 1 | Draft |
| G-02 | Content Governance & Versioning Policy | Draft → review → approve → publish, reviewer SLAs, rollback, change history | Academic lead | Phase 2 | To do |
| G-03 | Change Management Policy | Approval process for production changes, emergency changes | DevOps lead | Pre-launch | To do |
| G-04 | Periodic Access Review Procedure | Quarterly recertification of roles and entitlements | Admin + Security | Post-launch | To do |

## 06 Quality & Evaluation — `06_Quality_Evaluation/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| Q-01 | [Test Strategy & Test Plan](06_Quality_Evaluation/Q-01_Test_Strategy_and_Test_Plan.md) | Unit, integration, end-to-end and regression testing, test data, coverage targets | QA lead | Phase 1 | Draft |
| Q-02 | UAT Plan & Sign-off | Scenarios mapped to BRD §16 acceptance criteria | Product owner + QA | Per phase | To do |
| Q-03 | QBank Quality & Psychometric Evaluation | §8.1 must-pass checks, item difficulty (p-value), discrimination index, distractor analysis, item retirement rules | Academic lead + Data | Phase 2 | To do |
| Q-04 | Learning Effectiveness & KPI Framework | Completion, revision adherence, accuracy gains, mock score improvement, correlation with pass rates | Product + Academic | Phase 4 | To do |
| Q-05 | [Product Analytics / Telemetry Plan](06_Quality_Evaluation/Q-05_Product_Analytics_Telemetry_Plan.md) | Event taxonomy, dashboards, privacy-safe tracking | Product + Data | Phase 1 | Draft |
## 07 Performance & Scaling — `07_Performance_Scaling/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| N-01 | [NFR Specification (SLOs / SLIs)](07_Performance_Scaling/N-01_NFR_Specification_SLOs.md) | p95 under 2 s for common actions, 99.5% monthly availability, error budgets | Tech lead | Phase 1 | Draft |
| N-02 | Performance Optimisation Guide | Caching (Redis/CDN), DB indexing and query budgets, pagination, asset and font optimisation, Next.js rendering strategy | Tech lead | Phase 2 | To do |
| N-03 | Capacity Planning & Scaling Strategy | Peak loads (contest start, exam season), horizontal scaling, read replicas, connection pooling, autoscaling | Cloud architect | Phase 2 | To do |
| N-04 | Performance & Load Test Plan | Load-test scenarios (Locust), targets, pass/fail criteria | QA + DevOps | Pre-launch | To do |

## 08 DevOps & SRE — `08_DevOps_SRE/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| D-01 | [Environment Strategy](08_DevOps_SRE/D-01_Environment_Strategy.md) | Dev / staging / prod, data seeding, configuration per environment | DevOps lead | Phase 1 | Draft |
| D-02 | [CI/CD Pipeline Design](08_DevOps_SRE/D-02_CI_CD_Pipeline_Design.md) | Build, test, scan, database migration, deploy, rollback | DevOps lead | Phase 1 | Draft |
| D-03 | [Branching & Release Management](08_DevOps_SRE/D-03_Branching_and_Release_Management.md) | Branching model, versioning, release notes | DevOps lead | Phase 1 | Draft |
| D-04 | [Infrastructure-as-Code Standards](08_DevOps_SRE/D-04_Infrastructure_as_Code_Standards.md) | Terraform modules, state management, review process | DevOps lead | Phase 1 | Draft |
| D-05 | [Observability Specification](08_DevOps_SRE/D-05_Observability_Specification.md) | Structured logs, metrics, tracing (OpenTelemetry), alerts, dashboards | SRE | Phase 1 | Draft |
| D-06 | Backup, DR & Business Continuity Plan | RPO/RTO, backup schedule, restore drills | SRE | Pre-launch | To do |
| D-07 | Runbooks / Operations Manual | Deploy, rollback, DB restore, incident playbooks, contest-day checklist | SRE | Pre-launch | To do |
| D-08 | SLA & Support Model | Support tiers, on-call rota, escalation | Operations | Pre-launch | To do |

## 09 AI & LLMOps — `09_AI_LLMOps/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| L-01 | AI Use-Case & Responsible AI Policy | Allowed uses (authoring drafts, doubt assistant), mandatory human review, disclosure to students | Product + Academic | AI phase | To do |
| L-02 | LLM Solution Architecture | Retrieval (RAG) over approved notes only, model selection, context limits, fallback behaviour | Solution architect | AI phase | To do |
| L-03 | Prompt Management & Versioning | Prompt registry, change control, A/B testing | ML engineer | AI phase | To do |
| L-04 | LLM Evaluation Plan | Golden datasets, factual and calculation accuracy, groundedness, LOS alignment, reviewer rejection rate, regression gates | ML engineer + Academic | AI phase | To do |
| L-05 | AI Safety & Guardrails | Prompt-injection defence, PII redaction, output filtering, copyright checks on generated content | Security + ML | AI phase | To do |
| L-06 | LLM Monitoring & Cost Management | Token usage, latency, cost per student, budget alerts, model version tracking | ML engineer + DevOps | AI phase | To do |

## 10 User & Training — `10_User_Training/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| U-01 | Student User Guide & FAQ | How to study, build tests, log mocks and read analytics | Product / Support | Pre-launch | To do |
| U-02 | Author & Reviewer Handbook | Authoring tools, review checklist, approval workflow | Academic lead | Phase 2 | To do |
| U-03 | Administrator Manual | Users, batches, entitlements, unlock rules, reports | Product / Support | Pre-launch | To do |
| U-04 | [Developer Onboarding Guide & Coding Standards](10_User_Training/U-04_Developer_Onboarding_and_Coding_Standards.md) | Repository layout, local setup, conventions, review rules | Tech lead | Phase 1 | Draft |
## 11 Project Management — `11_Project_Management/`

| ID | Document | Purpose / key contents | Owner | Needed by | Status |
|---|---|---|---|---|---|
| M-01 | [Project Charter & RACI](11_Project_Management/M-01_Project_Charter_and_RACI.md) | Scope, stakeholders, decision rights | Project manager | Phase 0 | Draft |
| M-02 | [Estimates, Timeline & Budget](11_Project_Management/M-02_Estimates_Timeline_and_Budget.md) | Effort per phase, milestones, cost | Project manager | Phase 0 | Draft |
| M-03 | [Risk & Issue Register](11_Project_Management/M-03_Risk_and_Issue_Register.md) | Content licensing, content volume, reviewer bandwidth, contest-day load | Project manager | Ongoing | Draft |
| M-04 | [Open Decisions Log](11_Project_Management/M-04_Open_Decisions_Log.md) | BRD §17 items and their resolutions (see below) | Product owner | Ongoing | Draft |
---

### Decisions already taken (seed for M-04)
| Date | Decision |
|---|---|
| 2026-10-23 | Tech stack: Next.js + FastAPI + PostgreSQL |
| 2026-10-23 | ~~Chapter unlocking uses configurable rules per subject~~. Superseded: no chapter locking (D-009) |
| 2026-10-23 | Gamification from the demo (XP, streaks, badges, contests, leaderboard, certificates) is kept and scheduled for Phase 5 |
| 2026-10-23 | EOC, Premium Pack and Premium Mocks are tracked by student self-entry; the LMS does not host licensed CFA Institute content |
| 2026-10-23 | Students register for a course and pay online (Razorpay first, provider-neutral) (D-010) |
