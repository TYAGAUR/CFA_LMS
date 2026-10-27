# P-09 Business Rules Specification

| Field | Value |
|---|---|
| Document ID | P-09 |
| Version | 0.1 — Draft |
| Owner | Product owner + Tech lead |
| Last updated | 2026-10-23 |
| Related | BRD §4–§11, P-03 PRD, A-07 Domain engine specs |

Every rule has a stable ID (e.g. `BR-PAY-04`). Code, tests and tickets cite these IDs. A rule marked **[config]** has an admin-editable value; the default is shown.

---

## 1. Accounts and enrolment (BR-ACC, BR-ENR)

| ID | Rule |
|---|---|
| BR-ACC-01 | A student account is identified by a verified mobile number (OTP). An email address is optional, and verified when given. |
| BR-ACC-02 | Staff accounts (author, reviewer, admin, super admin) log in with email + password + TOTP MFA. Staff accounts cannot be self-registered; an admin creates them. |
| BR-ACC-03 | A user can hold more than one role (e.g. author and reviewer), but segregation of duties applies (BR-CNT-03). |
| BR-ACC-04 | Students declare their date of birth at sign-up. If they are under 18, the account stays in `pending_guardian_consent` until verifiable parental consent is recorded (C-03). While pending, the student sees only the consent screen. |
| BR-ACC-05 | Maximum active sessions per student account: **2 devices** [config]. Signing in on a third device ends the oldest session. |
| BR-ACC-06 | Accounts inactive for **24 months** after the end of their last enrolment are flagged for deletion under the retention policy (C-05). |
| BR-ENR-01 | A student sees content only for subjects covered by an active **entitlement**. Entitlements come from enrolment in a batch, or from a direct admin grant. |
| BR-ENR-02 | A batch has a start date, end date, exam window (e.g. "May 2027") and a set of subjects. Enrolment gives entitlement to the batch's subjects from start to end date. |
| BR-ENR-03 | When an entitlement expires, the student keeps read-only access to their own history and analytics for **90 days** [config]. Content and tests become unavailable. |
| BR-ENR-04 | Licensed-resource entitlements (e.g. "has Premium Pack access") are student self-declarations in Phase 4. They only control whether the tracker is shown; no licensed content is served. |

## 2. Content structure (BR-CAT)

| ID | Rule |
|---|---|
| BR-CAT-01 | The hierarchy is Subject → Learning Module (LM) → Topic → LOS. An LOS belongs to exactly one LM. A topic can map to one or more LOS. |
| BR-CAT-02 | LMs are numbered within a subject (`lm_no` 1..n) and shown as "LM{n} · {title}". |
| BR-CAT-03 | Source reading references (`source_ref`) are internal. They must never appear on student screens, exported file names, headers or footers. Mapping: FSA LM = source reading − 26; Equities LM = source reading − 38 (BRD §9). Other subjects' mappings are recorded per subject by the academic lead. |
| BR-CAT-04 | Each LOS stores its command word (e.g. *describe*, *calculate*, *compare*). The command word drives question-alignment checks (BR-QB-07). |
| BR-CAT-05 | Only `published` items are visible to students. Unpublishing an LM hides it, but keeps student progress. |

## 3. Access to sections (BR-OPN) — no chapter locking

> **Decision D-009 (2026-10-23):** the platform has **no chapter locking**. The earlier unlock-rule engine (BR-UNL-01..10, rule grammar) is withdrawn and will not be built.

| ID | Rule |
|---|---|
| BR-OPN-01 | Every published LM, topic, note and resource of a subject is open to a student who holds an active entitlement for that subject. |
| BR-OPN-02 | Entitlements come from a **paid course registration** (BR-PAY) or an admin grant (BR-ENR-01). Without an entitlement the student sees the course catalogue and subject outlines (LM titles), but no content. |
| BR-OPN-03 | Progress (completion, learned, revisions, EOC) is still tracked and shown, but it never blocks access. |
| BR-OPN-04 | Phase 2+ features (chapter quiz, master quiz) and Phase 4 mock prerequisites (BR-MCK-03) become **recommendations**: the UI may suggest an order ("finish LM2 before the LM2 quiz"), but the server never refuses access on progress grounds. |
| BR-OPN-05 | Entitlement checks still run on the server for every content and resource request. |

## 4. Progress (BR-PRG)

| ID | Rule |
|---|---|
| BR-PRG-01 | **Resource completion.** Video: watched to ≥ **90%** of its duration, counting each second only once (seeking ahead does not count) [config]. PDF / class notes: the student reached the last page, or pressed "Mark as read". Notes (in-app): scrolled to the end, or "Mark as read". |
| BR-PRG-02 | Resources are flagged `mandatory` or `optional` per LM (default: class videos and class notes mandatory; solved examples optional). |
| BR-PRG-03 | **Mark LM as learned:** available on any entitled LM. If the subject setting `require_mandatory_before_learned` is on [config, default off], all mandatory resources must be complete first. A student can undo "learned" within 24 hours; after that only an admin can undo it. |
| BR-PRG-04 | **LM completion %** = completed mandatory resources ÷ mandatory resources. **Subject completion %** = LMs marked learned ÷ published LMs. |
| BR-PRG-05 | **Video resume:** the last position is saved at least every 15 s and on pause or close. |
| BR-PRG-06 | **EOC self-entry:** per LM, the student records attempted (yes/no), questions attempted, questions correct, date, and optionally the topics they found weak. `correct ≤ attempted`; the date cannot be in the future. Marking complete requires attempted = yes. |
| BR-PRG-07 | The dashboard's **suggested next action** uses this priority: (1) a test in progress, (2) the current LM's next incomplete mandatory resource, (3) mark the current LM learned, (4) the next LM not yet learned, (5) revision due (Phase 3), (6) review weak areas (Phase 4). |

## 5. Revision (BR-REV)

| ID | Rule |
|---|---|
| BR-REV-01 | A **revision** is a student-logged event against an LM, with a date and an optional activity type (notes re-read, revision sheet, flashcards, questions). |
| BR-REV-02 | At most **one revision per LM per calendar day** counts (IST). Extra logs on the same day are stored but not counted. |
| BR-REV-03 | The **revision count** of an LM is the number of counted revisions. Subject revision count = the minimum of its LMs' revision counts (a subject is revised N times when every LM is revised N times). |
| BR-REV-04 | From Phase 3, finishing a flashcard session of ≥ 10 cards for an LM, or a revision sheet marked read, auto-logs a revision for that LM. |

## 6. Question bank, tests and scoring (BR-QB, BR-TST, BR-SCR) — Phase 2

| ID | Rule |
|---|---|
| BR-QB-01 | Every question has three options, A/B/C, exactly one correct answer, a full worked solution and a rationale for each distractor. |
| BR-QB-02 | Questions are versioned. A published version is immutable; editing creates a new draft version. Attempts record the exact version answered. |
| BR-QB-03 | Only `approved` versions can be `published`. Approval needs a reviewer who is not the author (BR-CNT-03). |
| BR-QB-04 | `lock_option_order = true` when the options refer to their positions (e.g. "Both A and B"). Such options are never shuffled. |
| BR-QB-05 | Release validation before an LM's question set is published: correct answers balanced across A/B/C (each letter 25–42% of the set) [config]; no run of more than 3 identical keys in source order; answer key matches option text; options non-empty and distinct; no near-duplicate stems (trigram similarity ≥ 0.85); numerical items pass the recompute check. |
| BR-QB-06 | Questions are tagged `conceptual` or `numerical`, with difficulty E/M/H, and a calculation mechanic for numerical items. |
| BR-QB-07 | Questions whose LOS command word is *describe/explain/identify* should not need multi-step calculation, unless marked as a Set A exception (BRD §8). |
| BR-TST-01 | **Eligible pool** = published questions in the selected filters, in subjects the student is entitled to. |
| BR-TST-02 | If the pool is smaller than the requested count, the builder shows the available number and offers to continue with that number. It never pads with questions from outside the filters. (This fixes prototype defect: `chapterPool()` fell back to the whole subject.) |
| BR-TST-03 | No question appears twice in one test. |
| BR-TST-04 | **Draw order preference:** unseen by the student → seen and answered wrongly → seen and answered correctly, least recently first. Ties are broken at random. |
| BR-TST-05 | Question order is randomised. Option order is randomised unless BR-QB-04 applies. The order is stored on the attempt so review and resume show the same order. |
| BR-TST-06 | **Modes.** *Practice*: the correct answer and explanation are shown immediately after answering, and answers are then locked. *Assessment*: no feedback until submission; answers can be changed until then. |
| BR-TST-07 | **Timing.** Timed tests default to **90 seconds per question** (the CFA Level I pace) [config]. When time runs out the test auto-submits. Untimed tests record elapsed time only. |
| BR-TST-08 | Every answer change is saved to the server immediately (autosave). An interrupted attempt can be resumed until its time limit; untimed attempts can be resumed for **7 days** [config], after which they auto-submit. |
| BR-TST-09 | **Chapter quiz:** up to 10 questions [config] from the LM, assessment mode, timed (90 s each). If the LM has fewer than 10 published questions, the quiz uses all of them; below 3 the quiz is unavailable. The pass mark (80%) is a guide only (BR-OPN-04). |
| BR-TST-10 | **Subject test (master quiz):** up to 50 questions [config] across the subject, timed. Guide pass mark ≥ 75% [config]. |
| BR-SCR-01 | 1 mark per correct answer. No negative marking (CFA format). Score % = correct ÷ total questions × 100, rounded half up to an integer for display; comparisons use the unrounded value. |
| BR-SCR-02 | The chapter-quiz pass threshold is **≥ 80%** [config] (inclusive; decision D-005). |
| BR-SCR-03 | The **best score** per chapter quiz is shown on the LM. Every attempt is kept for analytics. |
| BR-SCR-04 | Grading happens only on the server. Answer keys and explanations are never sent to the client before an assessment-mode question is submitted. |

## 7. Mocks and Premium Pack (BR-MCK) — Phase 4, self-entry

| ID | Rule |
|---|---|
| BR-MCK-01 | Seven Premium Mocks (1–7) are tracked. Mocks 1–5 support separate **Set 1** and **Set 2** entries. Mocks 1–2 also support a **Full** entry. Entry kinds for mocks 6–7: **Full only** (default; open decision O-05). |
| BR-MCK-02 | A Full entry and Set entries for the same mock are separate records and are never merged in reports. |
| BR-MCK-03 | **Recommended order** (advisory only, BR-OPN-04) [config]: Set entries for mocks 1–5 need subject revision count ≥ **5** for every subject (BRD §4.1 "five-revision prerequisites"). Full mocks need ≥ 5 revisions and the Premium Pack marked complete for all subjects. |
| BR-MCK-04 | Each entry records: date, kind, questions, correct, unanswered, duration (minutes), and optionally the per-subject correct/total and weak topics. Subject breakdowns must add up to the totals. |
| BR-MCK-05 | Weak topics in a mock entry are added to the student's revision queue (Phase 3/4). |
| BR-MCK-06 | Premium Pack progress is self-entered per subject: questions attempted, correct, and marked complete. |

## 8. Flashcards (BR-FC) — Phase 3

| ID | Rule |
|---|---|
| BR-FC-01 | Cards are created only from approved revision content and link to that content version. |
| BR-FC-02 | Ratings: **Known**, **Needs revision**, **Difficult**. |
| BR-FC-03 | Scheduling uses a modified SM-2 algorithm. Known → interval × ease (ease starts at 2.5; first intervals 1 d, then 3 d). Needs revision → interval × 1.2, ease − 0.15. Difficult → interval reset to 1 d, ease − 0.2. Ease never goes below 1.3. A future switch to FSRS is allowed (ADR needed). |
| BR-FC-04 | Due cards are those whose next-review date is today or earlier (IST). Overdue cards are shown first, oldest first. |

## 9. Analytics (BR-ANL) — Phase 2 basic, Phase 4 advanced

| ID | Rule |
|---|---|
| BR-ANL-01 | Accuracy = correct ÷ answered (unanswered excluded), shown with the number of questions it is based on. |
| BR-ANL-02 | A **weak LOS** has accuracy < 60% over ≥ 5 answered questions in the last 60 days [config]. |
| BR-ANL-03 | Time per question = active time on the question (the time it was on screen), capped at 10 minutes. |
| BR-ANL-04 | Any **readiness score** must carry this label: "LMS estimate based on your activity on this platform. It does not predict or guarantee your CFA exam result." |
| BR-ANL-05 | Exam topic weights used in readiness calculations are configurable. The defaults come from the current CFA Level I topic outline (P-11 §3), checked each exam cycle. |

## 10. Content governance (BR-CNT)

| ID | Rule |
|---|---|
| BR-CNT-01 | Content status lifecycle: `draft → in_review → approved → published`. `in_review → returned → draft` loops back. `published → retired`. |
| BR-CNT-02 | Phase 1 (before the review workflow exists): an admin can publish resources directly; the action is audit-logged. From Phase 2, notes, questions, revision sheets and flashcards need reviewer approval. |
| BR-CNT-03 | **Segregation of duties:** the approver must differ from the author of that version. Super admins cannot bypass this; the system enforces it. |
| BR-CNT-04 | Every asset has provenance: `original`, `faculty_recording`, `licensed_third_party` (with licence reference) or `reference_only` (link, not hosted). `licensed_third_party` assets need a licence record in C-06 before publishing. |
| BR-CNT-05 | Exported notes and revision sheets: LM-based file names (e.g. `EQ_LM01_Equity_Instrument_Features_Revision.pdf`), footer "Karan Singh, CFA", no source-provider labels (BRD §9). |

## 11. Engagement (BR-GAM) — Phase 5

| ID | Rule |
|---|---|
| BR-GAM-01 | XP is written as an append-only ledger. Each event has an idempotency key, so the same achievement cannot earn XP twice (fixes prototype XP farming). |
| BR-GAM-02 | Defaults [config]: topic or resource first completion +5; chapter quiz first pass +50; master quiz pass +100; flashcard deck session +2 per card known, capped at 40/day. Retakes earn XP only for improving the best score. |
| BR-GAM-03 | Streak = consecutive IST days with at least one qualifying activity (resource completed, test submitted, or revision logged). |
| BR-GAM-04 | Leaderboards show only students who opted in (C-03). Other students see "Student #1234". Under-18 accounts are excluded unless legal clearance is recorded (O-11). |
| BR-GAM-05 | Contests: one attempt, a fixed window, graded on the server, results visible only after an admin publishes them. |

## 12. Registration and payment (BR-PAY)

> **Decision D-010 (2026-10-23):** students register for a **course** and pay the fee online. Razorpay is the first gateway; the payment module is provider-neutral (A-08).

| ID | Rule |
|---|---|
| BR-PAY-01 | A **course** is a purchasable offering: title, description, fee (INR, stored in paise, GST-inclusive), included subjects, access start/end (or validity in days from payment), optional seat limit, optional linked batch, status (draft, open, closed). |
| BR-PAY-02 | Registration flow: student signs in (OTP) → completes the registration form (name, email, city, qualification, target exam window) → creates an **order** → pays → on confirmed payment the registration becomes `active` and entitlements are granted for the course's subjects. |
| BR-PAY-03 | A student can hold only one `pending_payment` or `active` registration per course. Re-starting checkout reuses the open order if it is under 30 minutes old and the amount is unchanged; otherwise a new order is created and the old one expired. |
| BR-PAY-04 | **Payment is confirmed only by the server**: either a verified gateway webhook, or a verified checkout signature followed by a server-side fetch of the payment status. A browser redirect alone never grants access. |
| BR-PAY-05 | Webhooks are verified (HMAC signature), stored in an inbox with the provider's event ID, and processed **idempotently**. The same event processed twice has no further effect. |
| BR-PAY-06 | The order amount is set by the server from the course fee at order creation and is never taken from the client. A captured amount different from the order amount marks the order `amount_mismatch` for admin review and grants no access. |
| BR-PAY-07 | Under-18 students need guardian consent (BR-ACC-04) before they can pay. |
| BR-PAY-08 | Refunds are initiated by an admin with a reason. A full refund cancels the registration and ends its entitlements; partial refunds keep access. All refund actions are audit-logged. |
| BR-PAY-09 | Admins can register a student manually (offline payment: cash, bank transfer) by recording the reference. This creates an order with provider `offline` and status `paid`. |
| BR-PAY-10 | A receipt (order number, course, amount, date, payment reference, GSTIN placeholder) is shown in the student's "My orders" page. GST invoicing is out of scope until the business provides GST details. |
| BR-PAY-11 | Payment card or bank details are never seen or stored by the platform; they stay on the gateway's hosted checkout. |
