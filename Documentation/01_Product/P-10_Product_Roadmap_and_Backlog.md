# P-10 Product Roadmap & Backlog

| Field | Value |
|---|---|
| Document ID | P-10 |
| Version | 0.1 |
| Owner | Product owner |
| Last updated | 2026-10-23 |
| Related | M-02 Timeline, P-03 PRD |

## 1. Roadmap

| Phase | Window (proposed) | Theme | Exit criteria |
|---|---|---|---|
| 0 Set-up | 2 Nov – 27 Nov 2026 | Docs, design system, repo, CI, staging | Phase 0–1 docs approved; staging deploys from `main` |
| 1 Foundation | 30 Nov 2026 – 5 Mar 2027 | Library, roles, progress, unlock rules, consent | P-03 §8 acceptance met; pilot batch live |
| 2 Assessment | Mar – May 2027 | QBank, review workflow, test builder | ≥ 1,500 approved questions; builder and engine live |
| 3 Revision | May – Jul 2027 | Notes studio, revision sheets, flashcards, SRS | All published LMs have revision sheets and cards |
| 4 Exam readiness | Jul – Sep 2027 | Mock and Premium Pack tracking, analytics | Analytics validated with pilot data |
| 5 Engagement | Sep – Oct 2027 | XP, contests, leaderboard, certificates | First monthly contest run |
| Later | 2028 | Payments, PWA, AI-assisted authoring, parent view | Decisions O-03, O-04, O-12 |

## 2. Phase 1 backlog (ordered)

Size uses story points (1, 2, 3, 5, 8, 13). Epic IDs match M-02; story IDs match P-03.

| # | Story | Epic | Size | Sprint (proposed) | Depends on |
|---|---|---|---|---|---|
| 1 | Repo skeleton, CI, local docker compose (U-04, D-02) | E11 | 5 | P0 | — |
| 2 | Data model migration v1: users, roles, sessions, audit | E1/E10 | 5 | S1 | 1 |
| 3 | US-1.01/1.02 Student OTP sign-up and sign-in | E1 | 8 | S1 | 2 |
| 4 | US-1.03 Staff sign-in + TOTP | E1 | 5 | S1 | 2 |
| 5 | US-3.01 Privacy notice and consents | E3 | 5 | S1 | 3 |
| 6 | Audit log service and middleware (G-01) | E10 | 5 | S1 | 2 |
| 7 | US-4.01/4.02 Catalogue admin | E4 | 8 | S2 | 4 |
| 8 | Seed import from prototype (subjects, LMs, notes, flashcards) | E4 | 3 | S2 | 7 |
| 9 | US-2.01/2.02 Batches and CSV enrolment | E2 | 8 | S2 | 3 |
| 10 | US-2.03–2.05 Staff and user management | E2 | 5 | S2 | 4 |
| 11 | US-5.01 Video upload (Bunny) + US-5.04 secure playback | E5 | 13 | S3 | 7 |
| 12 | US-5.02/5.05 PDF upload, scan, viewer, watermark | E5 | 8 | S3 | 7 |
| 13 | US-6.02/6.03 Subject view and notes renderer | E6 | 8 | S3 | 8 |
| 14 | US-3.02 Parental consent flow | E3 | 8 | S3 | 5 |
| 15 | US-7.01 Resource completion tracking | E7 | 5 | S4 | 11, 12 |
| 16 | US-7.02–7.04 Learned, revision log, EOC entry | E7 | 5 | S4 | 13 |
| 17 | US-8.02 Rule engine (server) | E8 | 8 | S4 | 16 |
| 18 | US-8.01 Rule editor UI | E8 | 5 | S5 | 17 |
| 19 | US-6.05 Search (Postgres FTS) | E6 | 5 | S5 | 13 |
| 20 | US-6.06 Bookmarks | E6 | 3 | S5 | 13 |
| 21 | E9 Dashboard | E9 | 5 | S5 | 15–17 |
| 22 | US-3.03/3.04 Consent management + data requests | E3 | 5 | S5 | 5 |
| 23 | US-10.01–10.03 Audit viewer and reports | E10 | 5 | S6 | 6, 15 |
| 24 | Production infra, WAF, backups, alerts (A-05, D-05, D-06) | E11 | 8 | S6 | — |
| 25 | E2E suite, accessibility audit, load smoke test (Q-01) | E12 | 8 | S6 | all |
| 26 | Pen test fixes, UAT, pilot launch | E12 | 5 | UAT | 25 |

## 3. Later-phase epics (unordered)
- **Phase 2:** QBank CRUD and versions · XLSX import · review workflow · release validator · test builder · test engine (autosave, resume) · chapter/master quiz templates · switch default unlock rule · question statistics · exports · basic analytics.
- **Phase 3:** block editor · revision-sheet builder with 2-page fit · DOCX/PDF export · flashcard authoring · SRS review · revision dashboard.
- **Phase 4:** EOC/Premium/mock trackers with prerequisites · weak-LOS analytics · revision queue · readiness estimate.
- **Phase 5:** XP ledger · streaks · badges · contests · leaderboard with consent · announcements · certificates with verification.

## 4. Fixes from the prototype to carry into the backlog
| Prototype issue | Fix | Phase |
|---|---|---|
| `pct > 80` pass check | `≥` threshold, configurable (BR-SCR-02) | 2 |
| `chapterPool()` falls back to the whole subject | Insufficient-pool handling (BR-TST-02, BR-TST-09) | 2 |
| Answers sent to the client | Server grading (BR-SCR-04) | 2 |
| `innerHTML` with content | JSON block renderer + sanitisation | 1 |
| XP farming | Idempotent XP ledger (BR-GAM-01) | 5 |
| Static streak; badges that can't be earned | Computed streaks and badge rules | 5 |
| Escape silently discards a quiz | Confirm dialog | 2 |
| Options not a radio group | ARIA radio group | 2 |
| Fonts inlined as base64 | `next/font/local` | 1 |
