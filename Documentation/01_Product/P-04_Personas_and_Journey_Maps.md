# P-04 Personas & Journey Maps

| Field | Value |
|---|---|
| Document ID | P-04 |
| Version | 0.1 — Draft; validate with 5–8 student interviews in Phase 0 |
| Owner | Product owner / Design |
| Last updated | 2026-10-23 |

These personas are working hypotheses based on the BRD and the prototype. Replace the assumptions with interview findings before the Phase 1 designs are final.

## 1. Student personas

### S1 — Working professional (primary)
- **Profile:** 26, analyst at a bank in Mumbai, preparing for the May 2027 window. Studies 1–2 hours on weekdays (often on a phone during the commute) and 5–6 hours at weekends.
- **Goals:** Finish the syllabus on time; know exactly what to do next; revise enough before mocks.
- **Frustrations:** Losing track across videos, PDFs and question banks; not knowing which topics are weak; little time.
- **Needs from the LMS:** A "continue" button; resume video on another device; short study units; a revision count; a clear weak-area list.
- **Devices:** Android phone (60%), laptop (40%).

### S2 — Final-year student (primary)
- **Profile:** 20, B.Com final year, in Pune. First attempt, and under pressure from parents. Has more hours available but less discipline. May be under 18 at sign-up if the batch starts early.
- **Goals:** Understand concepts properly; get practice and feedback; compare progress with peers.
- **Frustrations:** Dense curriculum text; theory without examples.
- **Needs:** Worked examples in ₹ with Indian context, "funny use case" boxes, quizzes that unlock progress, a leaderboard (Phase 5).
- **Devices:** Laptop and phone.

### S3 — Repeat candidate (secondary)
- **Profile:** 29, failed one attempt, retaking. Knows the content in parts.
- **Goals:** Find and fix weak LOS fast; take lots of mocks.
- **Needs:** Open mode or fast unlocks (BR-UNL-10); a custom test builder filtered by LOS; mock tracking; analytics.

## 2. Staff personas

### F1 — Lead faculty / author (Karan Singh, CFA)
- **Goals:** Publish high-quality notes, videos and questions quickly; protect the content from piracy; see which topics students struggle with.
- **Frustrations:** Repetitive formatting; manual answer-key checks.
- **Needs:** Upload once and map to LM/LOS; templates for notes and revision sheets; automatic validation; question statistics.

### F2 — Academic reviewer
- **Goals:** Review quickly and consistently; catch calculation errors and copied content.
- **Needs:** A review queue with diffs between versions, a checklist, comment and return, and approval that is recorded against their name.

### F3 — Operations admin
- **Goals:** Onboard batches fast; answer student queries; produce progress reports for faculty.
- **Needs:** CSV enrolment, a student lookup, session revocation, manual unlock with a reason, reports.

### F4 — Super admin (platform owner)
- **Goals:** Keep the platform secure and compliant; control global settings.
- **Needs:** Role management, an audit log, feature flags, retention settings.

### G1 — Parent / guardian
- **Goals:** Consent to their child's use of the platform and understand what data is collected.
- **Needs:** A simple, mobile-friendly consent page in plain language (Hindi option later).

## 3. Journey map — S1 Working professional, one study cycle (Phase 1–4 view)

| Stage | Actions | Touchpoints | Thoughts / feelings | Opportunities |
|---|---|---|---|---|
| 1. Onboard | OTP sign-up, consent, sees the enrolled batch | S-01, S-03, S-05 | "Quick, no password." | Prefilled batch; a 3-step welcome tour |
| 2. Plan | Opens the dashboard, sees the subject rings and the exam countdown | S-05 | "How far behind am I?" | Study-plan suggestion (later) |
| 3. Learn | Picks Equities LM1, watches the video on the commute, reads notes at night | S-06, S-07 | "Good that it resumed where I stopped." | Cross-device resume; short topic chapters |
| 4. Practise (Ph2) | Takes the chapter quiz, scores 70%, reads explanations, retakes with new questions | Test engine | Frustrated, then relieved | Explanations linked to the notes section |
| 5. Unlock | Scores 90%; LM2 unlocks | Rail | Motivated | Clear "next" call to action |
| 6. Curriculum + EOC | Does EOC questions on the CFA Institute site and logs the score | EOC form | "Nice to track it in one place." | Quick 3-field form |
| 7. Revise (Ph3) | Revision sheet + flashcards; the revision count goes up | Flashcards | "Spaced repetition actually helps." | Daily due-cards nudge |
| 8. Mocks (Ph4) | Self-enters Mock 1 Set 1 with subject scores | Mock tracker | Anxious | Weak topics pushed straight into the revision queue |
| 9. Final weeks | Focuses on weak LOS with custom tests | Analytics + builder | "I know exactly what to fix." | One-click "test my weak LOS" |

## 4. Journey map — F1 Author publishing an LM (Phase 2–3 view)

| Stage | Actions | Pain today | LMS support |
|---|---|---|---|
| Prepare | Maps the LM to LOS, notes source concepts internally | Spreadsheets | LOS import; internal `source_ref` |
| Record | Records the class; uploads the video with chapter markers | Manual timestamping | Chapter editor |
| Write notes | Drafts notes with example/trap/formula boxes | Formatting by hand | Block editor and templates |
| Write questions | Writes 3-option MCQs with solutions | Checking keys and balance by hand | Release validator |
| Review | Sends to the reviewer; fixes returned items | Email back-and-forth | Comments on versions |
| Publish | Reviewer approves; admin publishes | — | One-click publish of the LM bundle |
| Improve | Looks at question statistics; fixes poor items | No data | p-value and discrimination per item |

## 5. Design implications
1. Mobile-first for students, because most weekday study is on phones. Desktop-first for admin and authoring.
2. Always show the "next action". Avoid dead ends: a locked view must say exactly what to do.
3. Keep the prototype's friendly tone and Indian context; it is a differentiator.
4. Staff tools should favour bulk actions (CSV, multi-select) and validation before commit.
5. Under-18 users need simple, separate consent flows and privacy-safe defaults.
