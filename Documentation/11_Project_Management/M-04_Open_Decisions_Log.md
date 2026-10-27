# M-04 Decisions Log

| Field | Value |
|---|---|
| Document ID | M-04 |
| Version | 0.1 |
| Owner | Product owner |
| Last updated | 2026-10-23 |

## Decisions taken

| ID | Date | Decision | Decided by | Rationale / reference |
|---|---|---|---|---|
| D-001 | 2026-10-23 | Tech stack: Next.js (frontend), FastAPI (backend), PostgreSQL (database) | Sponsor | ADR-001 (A-02) |
| D-002 | 2026-10-23 | **Superseded by D-009.** LM unlocking uses admin-configurable rules per subject. The default in Phase 2 onwards is chapter quiz best score ≥ 80% on the previous LM. | Sponsor | P-09 §3 |
| D-003 | 2026-10-23 | Prototype gamification (XP, streaks, badges, contests, leaderboard, certificates) is kept and scheduled for Phase 5 | Sponsor | P-10 |
| D-004 | 2026-10-23 | EOC questions, Premium Pack and Premium Mocks are tracked by student self-entry. The LMS does not host licensed CFA Institute material. | Sponsor | C-06; BRD §12 |
| D-005 | 2026-10-23 | The pass threshold is inclusive (≥). The prototype's `> 80%` is treated as a defect. | PO (proposed) | M-03 I-03 |
| D-006 | 2026-10-23 | **Superseded by D-009.** Phase 1 default unlock rule: the previous LM is marked learned. It switches to the quiz rule when Phase 2 ships. | PO (proposed) | M-03 I-02 |
| D-007 | 2026-10-23 | **Superseded by D-009.** Unlocks are sticky: once a student has unlocked an LM, later rule changes do not re-lock it | PO (proposed) | P-09 BR-UNL-06 |
| D-008 | 2026-10-23 | The BRD's navy/gold/teal and Bahnschrift styling applies to exported documents. The web UI keeps the prototype's design system (Figtree, indigo/cyan). | PO (proposed) | P-07 |
| D-009 | 2026-10-23 | **No chapter locking.** All sections of an entitled subject are open; progress is tracked but never blocks access. The unlock-rule engine is not built. | Sponsor | P-09 §3 (BR-OPN) |
| D-010 | 2026-10-23 | **Paid registration.** Students register for a course and pay online; Razorpay first, behind a provider-neutral payment module so other gateways or a separate payments service can be added. | Sponsor | P-09 §12 (BR-PAY), A-08 |
| D-011 | 2026-10-23 | Local development runs without Docker or Redis: native PostgreSQL 16 and Node 24 (installed with winget), background jobs run in-process. Celery and Redis return for cloud environments. | Tech lead | U-04, A-01 §4 |

"Proposed" items need confirmation at the next steering meeting.

## Open decisions (from BRD §17 and the analysis)

| ID | Question | Options | Recommendation | Needed by | Owner |
|---|---|---|---|---|---|
| O-01 | Initial audience | Own enrolled students; open subscription; internal team only | Own enrolled students (pilot batch) first | Phase 1 start | Sponsor |
| O-02 | Launch platform | Responsive web; web + native apps | Responsive web; PWA after Phase 3 | Decided by default (charter) | Sponsor |
| O-03 | Content workflow | Admin upload; AI-assisted authoring; both | Manual first; AI-assisted after L-01..L-06 are approved | Phase 3 | Academic lead |
| O-04 | Commercial model | — | **Closed by D-010:** paid course registration (fee per course) | Done | Sponsor |
| O-05 | Exact revision prerequisites and mock unlock rules (including whether mocks 6–7 have sets or full attempts only) | Configurable; see P-09 §7 | Confirm the defaults in P-09 §7 | Phase 4 start (Jul 2027) | Academic lead |
| O-06 | Licensing permissions for third-party notes, QBanks and mocks | — | Treat all as not licensed until written permission is filed in C-06 | Phase 1 | Legal |
| O-07 | Hosting, budget, timeline | See A-05, M-02 | AWS Mumbai; budget per M-02 | Phase 0 end | Sponsor |
| O-08 | Product name and brand | "CFA Learning Hub"; "Karan Sir Classes"; combined | Brand decision needed before the design system is final; note CFA Institute trademark rules on using "CFA" in product names (C-06 §5) | Phase 0 | Sponsor + Legal |
| O-09 | Video host | Bunny Stream; Mux; Vimeo; AWS IVS/MediaConvert | Bunny Stream (cost, India PoPs, DRM option) | Phase 0 | Tech lead |
| O-10 | SMS provider | MSG91; Gupshup; AWS SNS (India DLT) | MSG91 primary, email OTP fallback | Phase 0 (DLT registration lead time) | Tech lead |
| O-11 | Is the institute an "educational institution" for DPDP child-data exemptions? | — | Get a legal opinion; design so analytics and leaderboard can be switched off per under-18 account | Phase 1 | Legal |
| O-12 | Parent role scope | None; consent only; read-only progress view | Consent only in Phase 1; read-only view later | Phase 1 | PO |
