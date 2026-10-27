# M-01 Project Charter & RACI

| Field | Value |
|---|---|
| Document ID | M-01 |
| Version | 0.1 — Draft for stakeholder review |
| Owner | Project manager |
| Last updated | 2026-10-23 |
| Related | BRD v1.0 (P-01), M-02 Estimates, M-03 Risks, M-04 Decisions |

## 1. Purpose
This charter authorises the build of **CFA Learning Hub**, the Karan Sir Classes learning management system for CFA Level I. It sets out the objectives, scope, governance and decision rights for the build.

## 2. Background
The institute teaches CFA Level I through live and recorded classes, notes and practice questions. Today these sit in separate places, and nothing tracks a student's learning, revision and mock performance in one view. A clickable prototype (P-02) and a draft BRD (P-01) have been produced. This project turns them into a production platform.

## 3. Objectives and success measures

| # | Objective (BRD §1.1) | Success measure | Target |
|---|---|---|---|
| O1 | Conceptual understanding before memorisation | Share of active students who complete all mandatory resources of an LM before marking it learned | ≥ 70% |
| O2 | Easier revision planning across ten subjects | Students with at least one logged revision per subject 8 weeks before the exam | ≥ 60% |
| O3 | Original, exam-standard questions with worked explanations | Approved questions in the QBank at Phase 2 launch | ≥ 1,500 (≈ 150 per subject) |
| O4 | Student-built custom tests | Weekly active students who build at least one custom test | ≥ 50% |
| O5 | One place for learning, practice, revision and mocks | Students whose dashboard shows data from all four areas | ≥ 60% by Phase 4 |
| O6 | Controlled content workflow | Published questions with a recorded reviewer approval | 100% |

Targets are proposals for the steering group to confirm.

## 4. Scope

**In scope** (delivered in phases; see M-02 and P-10)
- Phase 1, Foundation: student portal, logins and five roles, ten subjects with LM/topic/LOS structure, resource uploads, progress tracking, unlock rules, audit log.
- Phase 2, Assessment: question bank, review workflow, custom test builder, scoring, basic reports, QBank exports.
- Phase 3, Revision: notes and revision-sheet studio, flashcards with spaced repetition, revision tracking.
- Phase 4, Exam readiness: self-entry tracking for Premium Pack and mocks, analytics, revision recommendations.
- Phase 5, Engagement: XP, streaks, badges, contests, leaderboard, certificates.

**Out of scope** (for this charter)
- Hosting or reproducing licensed CFA Institute material (curriculum text, EOC questions, Premium Pack, Premium Mocks). These are tracked by student self-entry only.
- Native mobile apps. v1 is responsive web; a PWA is a later option.
- Payments and subscriptions, until the commercial model is decided (M-04).
- AI features, until the AI documents L-01 to L-06 are approved.
- CFA Level II and III content.

## 5. Deliverables
1. Production web application (Next.js frontend, FastAPI backend, PostgreSQL) for students and staff.
2. Admin and authoring console.
3. Infrastructure as code, CI/CD pipeline, monitoring and runbooks.
4. The documentation set in `Documentation/` (see the register).
5. Seed content migrated from the prototype: 10 subjects, the LM list, 61 questions, Equities LM1–3 notes and the flashcards.

## 6. Stakeholders

| Stakeholder | Interest |
|---|---|
| Founder / lead faculty (Karan Singh, CFA) | Teaching quality, content ownership, brand |
| Students (CFA Level I candidates) | Easy study, reliable tests, progress visibility |
| Instructors / content authors | Efficient authoring tools |
| Academic reviewers | Quality control, originality, LOS mapping |
| Operations / administrators | User management, enrolment, reports |
| Parents (of students under 18) | Consent and, later, progress visibility |
| Legal / privacy adviser | DPDP Act compliance, licensing, trademarks |
| Delivery team | Clear requirements, stable decisions |

## 7. Project roles

| Role | Responsibility | Person |
|---|---|---|
| Sponsor | Funding, final escalation, scope sign-off | [TBD] |
| Product owner | Backlog, priorities, acceptance | [TBD] |
| Academic lead | Content standards, reviewer team, LOS mapping | Karan Singh, CFA (proposed) |
| Project manager | Plan, risks, status, coordination | [TBD] |
| Tech lead / architect | Architecture, code quality, technical decisions | [TBD] |
| Developers (full-stack) | Build and unit tests | [TBD] ×2 |
| UX / UI designer | Design system, screens | [TBD] (part-time) |
| QA engineer | Test strategy, automation, UAT support | [TBD] (part-time) |
| DevOps / SRE | Infrastructure, pipeline, monitoring | [TBD] (part-time) |
| Privacy / legal adviser | DPDP, licensing, terms | External counsel [TBD] |

## 8. RACI

R = Responsible · A = Accountable · C = Consulted · I = Informed

| Activity | Sponsor | PO | Academic lead | PM | Tech lead | Devs | Design | QA | DevOps | Legal |
|---|---|---|---|---|---|---|---|---|---|---|
| Approve scope and budget | A | R | C | C | C | I | I | I | I | I |
| Prioritise backlog | I | A/R | C | C | C | I | C | I | I | I |
| Requirements / PRD | I | A | C | C | C | C | C | C | I | C |
| UX design | I | A | C | I | C | C | R | C | I | I |
| Architecture and ADRs | I | C | I | I | A/R | C | I | C | C | I |
| Build features | I | C | I | I | A | R | C | C | C | I |
| Infrastructure and CI/CD | I | I | I | I | A | C | I | I | R | I |
| Security controls | I | C | I | I | A | R | I | C | R | C |
| DPDP compliance and consent | A | R | I | C | C | C | C | I | I | R |
| Content standards and style guide | I | C | A/R | I | I | I | C | I | I | C |
| Licensing and IP register | C | C | R | I | I | I | I | I | I | A |
| Testing and UAT | I | A | C | C | C | C | I | R | I | I |
| Go-live decision | A | R | C | R | C | I | I | C | C | C |
| Incident response | I | I | I | I | A | R | I | I | R | C |

## 9. Governance
- **Weekly delivery meeting** (PM, PO, tech lead): progress, blockers, risks.
- **Fortnightly demo** to the academic lead and operations after every sprint.
- **Monthly steering meeting** (sponsor, PO, academic lead, PM, tech lead): scope, budget, phase gates, major risks.
- **Phase gate:** each phase closes only after UAT sign-off (Q-02) against the BRD §16 acceptance criteria for that phase.
- **Change control:** scope changes go through the PO. A change affecting the budget or phase dates by more than 10% needs sponsor approval and is recorded in M-04.

**Decision rights**
- Product scope and priority: product owner.
- Academic content and standards: academic lead.
- Technical design: tech lead, recorded as ADRs (A-02).
- Legal and privacy matters: legal adviser has veto.

## 10. Constraints and assumptions
- Stack fixed: Next.js, FastAPI, PostgreSQL (M-04, D-001).
- Hosting in India (DPDP and latency). AWS Mumbai is proposed (A-05).
- Licensed CFA Institute material is not hosted (M-04, D-004).
- The team is small (see M-02), so the architecture is a modular monolith, not microservices.
- The academic team supplies reviewed content at the rate the phases assume (M-03, R-03).

## 11. High-level milestones
Proposed; see M-02 for detail.

| Milestone | Target |
|---|---|
| Phase 0 complete (docs approved, design system, repo and pipelines ready) | 27 Nov 2026 |
| Phase 1 live to pilot batch | 5 Mar 2027 |
| Phase 2 live (QBank and test builder) | 14 May 2027 |
| Phase 3 live (revision engine) | 9 Jul 2027 |
| Phase 4 live (mocks and analytics) | 3 Sep 2027 |
| Phase 5 live (engagement) | 15 Oct 2027 |

## 12. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | | | |
| Product owner | | | |
| Academic lead | | | |
| Tech lead | | | |
