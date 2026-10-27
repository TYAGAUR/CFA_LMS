# P-03 Product Requirements Specification (PRD)

| Field | Value |
|---|---|
| Document ID | P-03 |
| Version | 0.1 — Phase 1 detailed; Phases 2–5 at epic level |
| Owner | Product owner |
| Last updated | 2026-10-23 |
| Related | BRD v1.0 (P-01), prototype (P-02), P-05 Workflows, P-06 RBAC, P-09 Business rules, P-07 UI/UX |

## 1. Product summary
CFA Learning Hub is a web platform for CFA Level I students. It brings classes, notes, practice, revision and mock tracking together in one place. Students study one Learning Module at a time and unlock the next when they meet the subject's rule. Staff manage content through a controlled authoring and approval workflow.

## 2. Goals and non-goals
**Goals for Phase 1:**
- A usable, access-controlled learning library for all ten subjects.
- Reliable progress tracking.
- Configurable unlocking.
- Admin tools to run batches.
- Privacy compliance from day one.

**Non-goals for Phase 1:**
- Question bank and tests (Phase 2).
- Revision studio and flashcards (Phase 3).
- Mocks and advanced analytics (Phase 4).
- Contests and XP (Phase 5).
- Payments.
- Native apps.

## 3. Requirement traceability (BRD → PRD)

| BRD FR | Title | Phase | PRD section |
|---|---|---|---|
| FR-01 | Student dashboard | 1 (basic), 4 (full) | §5.9 |
| FR-02 | Learning library | 1 | §5.6 |
| FR-03 | Resource management | 1 | §5.5 |
| FR-04 | Notes and revision studio | 1 (render), 3 (studio) | §5.6, §6.2 |
| FR-05 | Flashcards | 3 | §6.2 |
| FR-06 | Question repository | 2 | §6.1 |
| FR-07 | Custom test builder | 2 | §6.1 |
| FR-08 | Test delivery | 2 | §6.1 |
| FR-09 | Mock workflow | 4 | §6.3 |
| FR-10 | Analytics | 2 (basic), 4 | §6.1, §6.3 |
| FR-11 | Content approval | 1 (direct publish), 2–3 (workflow) | §5.4, §6.1 |
| FR-12 | Audit and versioning | 1 | §5.10 |
| FR-13 | Question export | 2 | §6.1 |
| FR-14 | Test templates | 2 | §6.1 |

## 4. Users
See P-04 for personas and P-06 for permissions. Phase 1 roles: student, author, reviewer (read only until Phase 2), admin, super_admin, and guardian (consent only).

## 5. Phase 1 requirements (detailed)

Stories use the format **US-x.yy**. Each has acceptance criteria (AC) in Given / When / Then form. Business rules are cited by ID.

### 5.1 E1 — Authentication and sessions

**US-1.01 Student sign-up with mobile OTP**
As a prospective student, I want to sign up with my mobile number, so that I don't need to remember a password.
- AC1: Given a valid Indian mobile number, when I request an OTP, then a 6-digit code is sent by SMS. It is valid for 5 minutes, at most 5 OTP requests per number per hour are allowed, and at most 5 wrong attempts per code.
- AC2: When I enter the correct code, I am asked for my name, date of birth and (optionally) email. I must accept the privacy notice and terms before the account is created.
- AC3: If my date of birth makes me under 18, the account is created with status `pending_guardian_consent` and I am taken to the parental consent flow (US-3.02) (BR-ACC-04).
- AC4: If SMS delivery fails 2 times, I am offered an email OTP instead.

**US-1.02 Student sign-in**
- AC1: An OTP sign-in creates a session: a 15-minute access token and a rotating refresh token in an httpOnly, Secure, SameSite=Lax cookie (ADR-003).
- AC2: Signing in on a new device when 2 sessions are already active ends the oldest one (BR-ACC-05), and I see a notice saying so.
- AC3: I can see my active devices and sign out of any of them.

**US-1.03 Staff sign-in with MFA**
- AC1: Staff sign in with email + password + TOTP. Accounts lock for 15 minutes after 5 failed attempts.
- AC2: On first sign-in, staff must set a password (≥ 12 characters, checked against a breached-password list) and enrol TOTP. Recovery codes are shown once.
- AC3: Staff sessions follow the idle and total timeouts in P-06 §6.

### 5.2 E2 — Users, batches, enrolments, entitlements

**US-2.01 Admin manages batches**
An admin creates a batch with name, code (e.g. KSC-27), exam window, start/end dates and included subjects.
- AC: A batch can't end before it starts; the code is unique; changes are audit-logged.

**US-2.02 Admin enrols students**
An admin enrols students one by one (search by mobile or name) or in bulk by CSV upload (`mobile, name, email, batch_code`).
- AC1: The CSV import validates every row and shows a preview with errors before committing. Valid rows can be committed while errors are skipped.
- AC2: An enrolled student's entitlements appear immediately (BR-ENR-01/02).
- AC3: Students who don't have an account yet get an invitation SMS/email and are pre-linked to the batch.

**US-2.03 Admin creates staff accounts and assigns roles** (P-06; SoD-02)

**US-2.04 Admin deactivates a user.** All sessions are revoked immediately; history is kept under the retention policy.

**US-2.05 Admin views a student's profile**, enrolments, progress summary and sessions; can revoke sessions and manually unlock an LM (BR-UNL-07).

### 5.3 E3 — Consent, privacy notice, data requests

**US-3.01 Privacy notice and consent at sign-up.** Itemised purposes: mandatory (service delivery) and optional (product analytics, marketing messages, leaderboard name display in Phase 5) (C-03).
- AC: Optional purposes are unticked by default. Choices are stored with the notice version and a timestamp.

**US-3.02 Parental consent for under-18 students**
- AC1: The student enters a parent/guardian's mobile number and name. The guardian receives an OTP link and a plain-language notice. When the guardian enters the OTP and accepts, consent is recorded with the guardian's identity, method and timestamp (C-03 §5).
- AC2: Until consent is given, the student's account cannot access content. Unverified accounts are deleted after 30 days.
- AC3: For under-18 accounts, Phase 5 leaderboard display and any behavioural-monitoring features stay off unless a legal clearance flag is set (O-11).

**US-3.03 Manage my consents.** I can view and withdraw optional consents at any time, and withdrawal takes effect within 24 hours.

**US-3.04 Data requests.** I can request a copy of my data or deletion of my account.
- AC1: A request creates a ticket for an admin and is acknowledged on screen. The response is due within the policy period (C-05).
- AC2: An export is a JSON + PDF summary of my profile, enrolments, progress, attempts and consents.
- AC3: I can nominate a person to exercise my rights if I die or become incapacitated, by recording their name and contact (DPDP right to nominate; C-01 §3 row 12).

### 5.4 E4 — Catalogue administration

**US-4.01 Manage subjects and LMs.** An admin or author creates and edits subjects (code, name, icon, order) and LMs (number, title, summary, internal `source_ref`, status).
- AC1: `lm_no` is unique per subject; LMs can be reordered by drag and drop.
- AC2: `source_ref` is visible only in admin screens (BR-CAT-03).

**US-4.02 Manage topics and LOS.** Topics are ordered within an LM. LOS have a code, statement and command word (picked from a list).
- AC: Topics can be mapped to one or more LOS.

**US-4.03 Publish / unpublish an LM** (BR-CAT-05). Phase 1: admin only, audit-logged.

**US-4.04 Bulk import of the catalogue** from a CSV/XLSX template (subjects, LMs, LOS), with validation and a preview.

### 5.5 E5 — Resources

**US-5.01 Upload a video.** An author or admin uploads a class video against an LM (and optionally a topic), with title, duration, order, and a mandatory/optional flag.
- AC1: The upload goes directly from the browser to the video host (resumable). Processing status is shown, and the video can't be published until encoding finishes.
- AC2: Chapters/timestamps can be added (title + start time). These become the "topic by topic" list from the prototype.

**US-5.02 Upload a PDF or class note.** Max 50 MB, PDF only, virus-scanned before it is available.

**US-5.03 Add a reference link** (e.g. to a curriculum page on the CFA Institute portal), with provenance `reference_only` (BR-CNT-04).

**US-5.04 Watch a video securely**
- AC1: Playback uses a signed URL that expires within 2 hours and is restricted to our domain.
- AC2: A moving watermark shows the student code (e.g. `KSC27-0412`) and the last 4 digits of the mobile number. The full name is not shown (C-01 §4).
- AC3: Playback resumes from the last position (BR-PRG-05).
- AC4: Speeds 0.75–2× are available, along with captions if uploaded.

**US-5.05 View a PDF securely.** It opens in an in-app viewer with a watermark. Download is allowed only if the resource is marked downloadable; downloads are watermarked server-side with the student's name and ID.

**US-5.06 Provenance required.** Every resource needs provenance before it can be published (BR-CNT-04).

### 5.6 E6 — Learning library

**US-6.01 Browse subjects.** The home page shows the ten subjects with completion rings, as in the prototype.

**US-6.02 Subject view.** A left rail lists LMs with states: done ✓, current, locked 🔒 (with unmet conditions), learned score. The right pane shows the selected LM with tabs: Notes · Videos · Resources · Revision sheet (Phase 3) · Infographic/Game (if present).

**US-6.03 Notes renderer.** Renders structured note blocks: paragraph, heading, list, table, worked example, watch out, formula, funny use case, infographic, image.
- AC: Notes are rendered from a JSON block schema, never from raw HTML. Any rich text is sanitised (S-01 T-07).

**US-6.04 Locked LM view** shows plain-language unmet conditions (BR-UNL-08).

**US-6.05 Search** across published subjects, LMs, topics, LOS statements and note text the student is entitled to.
- AC1: Results are grouped by type. Results in locked LMs show the title only, with a lock icon.
- AC2: Results appear within 1 second at p95 (N-01).

**US-6.06 Bookmarks.** I can bookmark a topic, resource or video timestamp, and see my bookmarks in a list with links.

### 5.7 E7 — Progress

**US-7.01 Automatic resource completion** (BR-PRG-01).

**US-7.02 Mark LM as learned** (BR-PRG-03). There is an undo window of 24 hours.

**US-7.03 Log a revision** (BR-REV-01/02). A button on the LM opens a dialog with date (default today) and activity type.

**US-7.04 EOC self-entry** (BR-PRG-06). A per-LM form; the "Complete" badge shows on the LM.

### 5.8 E8 — Unlock rules

**US-8.01 Rule editor.** An admin selects a subject and builds a rule from the condition list (P-09 §3.1) in a form builder (no raw JSON needed), sees a plain-language preview, and saves it.
- AC1: A rule can be tested against a sample student ("What would Aarav see?").
- AC2: The editor warns when a rule is stricter than the current one, and explains that unlocks are sticky (BR-UNL-06).
- AC3: Every saved version is kept and can be restored.

**US-8.02 Server enforcement** (BR-UNL-09). A request for a locked LM's content returns 403 with the unmet conditions.

### 5.9 E9 — Student dashboard (FR-01 basic)
- A "Continue where you left off" card with the next action (BR-PRG-07).
- Subject completion rings.
- Pending items: incomplete mandatory resources in the current LMs, EOC not done for learned LMs.
- Recent activity (last 10 events).
- Batch info and exam window countdown.

### 5.10 E10 — Audit log and basic reports
- **US-10.01:** The audit log records the events in G-01. An admin can filter by actor, event type and date, and export to CSV.
- **US-10.02:** Batch progress report: per student, the % of LMs learned per subject, last active date and EOC completion. Exportable to CSV.
- **US-10.03:** Content report: per LM, published resources, mandatory count and average completion.

## 6. Later phases (epic level, refined before each phase starts)

### 6.1 Phase 2 — Assessment
- **QBank:** question CRUD with full metadata (BRD §7.1), versioning (BR-QB-02), and bulk import from the XLSX template.
- **Workflow:** author → reviewer → approve or return, with comments and an SLA dashboard.
- **Release validator:** BR-QB-05, with a report per LM.
- **Custom test builder (BRD §6):** filters for subject, LM, topic, LOS, difficulty, type, mode and timing; shows the eligible count; save as a template.
- **Test engine:** BR-TST, autosave and resume, review screen, explanations.
- **Chapter quiz and master quiz** as fixed templates; the unlock rule switches to `quiz_best_pct` (BR-UNL-04).
- **Reports:** accuracy by subject and LM, attempt history, question statistics (p-value, discrimination).
- **Exports (FR-13):** Practice Set, Testing Set A/B, answer keys, worked solutions, LOS audit, student question-only set, master QBank (DOCX/PDF).

### 6.2 Phase 3 — Revision
- Notes studio: block editor, versioning, review, export to DOCX/PDF using the BRD §9 templates.
- Two-page revision sheet builder: two-column template with page-fit validation.
- Flashcards from approved revision content; review sessions; SRS (BR-FC); personal decks; overdue queue.
- Revision dashboard: counts per LM and subject, a heat map, auto-logged revisions (BR-REV-04).

### 6.3 Phase 4 — Exam readiness
- Premium Pack and mock self-entry (BR-MCK) with prerequisites shown.
- Analytics: accuracy trend, time per question, weak LOS (BR-ANL-02), repeated errors, flashcard recall.
- Revision queue with recommendations; readiness estimate with disclaimer (BR-ANL-04).

### 6.4 Phase 5 — Engagement
- XP ledger, levels, streaks, badges (BR-GAM).
- Contests: scheduling, registration, reminders, one-attempt window, result publication.
- Leaderboards with opt-in (C-03); announcements ticker; certificates with a verification URL.

## 7. Screen inventory (Phase 1)

| # | Screen | Roles |
|---|---|---|
| S-01 | Sign-up / sign-in (OTP) | Public |
| S-02 | Staff sign-in + MFA enrolment | Staff |
| S-03 | Privacy notice and consent | Student |
| S-04 | Guardian consent page (from SMS link) | Guardian |
| S-05 | Student dashboard / home | Student |
| S-06 | Subject view (rail + LM pane) | Student |
| S-07 | Video player view | Student |
| S-08 | PDF viewer | Student |
| S-09 | Search results | Student |
| S-10 | Bookmarks | Student |
| S-11 | Profile, devices, consents, data requests | All |
| S-12 | Admin: users list / detail | Admin |
| S-13 | Admin: batches and enrolments (incl. CSV import) | Admin |
| S-14 | Admin: catalogue tree (subjects/LMs/topics/LOS) | Admin, author |
| S-15 | Admin: resource upload and list | Admin, author |
| S-16 | Admin: unlock rule editor | Admin |
| S-17 | Admin: audit log | Admin, super admin |
| S-18 | Admin: reports | Admin |
| S-19 | Admin: data requests queue | Admin |
| S-20 | Super admin: settings and feature flags | Super admin |

## 8. Phase 1 acceptance (maps to BRD §16)

| BRD §16 criterion | Phase 1 evidence |
|---|---|
| Students can access authorised resources by subject and LM | US-5.04/5.05, US-6.02, entitlement and unlock tests |
| Instructors can upload and map approved learning materials | US-5.01–5.03, US-4.02 |
| Access controls and recovery procedures have been tested | RBAC test matrix (Q-01), restore drill (D-06) |
| Students can view progress | US-7.x, E9 |

## 9. Edge cases
- A student's entitlement expires while a video is playing: the current session continues, and the next URL request fails with a friendly message.
- An LM is unpublished while students are in it: they keep their progress, and the LM disappears from the rail with a notice.
- A rule refers to an LM that is later deleted: the rule editor blocks deletion while any rule refers to that LM.
- Clock differences: all day-based rules use the server's IST date.
- Two tabs record progress at the same time: progress updates are idempotent and keep the maximum position and completion.
