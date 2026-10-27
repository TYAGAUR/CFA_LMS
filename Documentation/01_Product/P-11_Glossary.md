# P-11 Glossary

| Field | Value |
|---|---|
| Document ID | P-11 |
| Version | 0.1 |
| Owner | Business analyst |
| Last updated | 2026-10-23 |

## 1. CFA and curriculum terms

| Term | Meaning in this project |
|---|---|
| **CFA Level I** | The first of three CFA Program exams, run by CFA Institute. This platform covers Level I only. |
| **Subject** | One of the ten Level I topic areas (§3). The prototype calls these "subjects"; CFA Institute calls them "topics". |
| **LM (Learning Module)** | A chapter within a subject, numbered LM1..LMn in curriculum order. |
| **LOS (Learning Outcome Statement)** | A specific, testable outcome in an LM, e.g. "calculate the value of a preferred share". Each LOS starts with a **command word**. |
| **Command word** | The verb of an LOS (describe, explain, calculate, compare, interpret…). It sets the depth a question may test. |
| **Topic** | An LMS teaching unit inside an LM (a notes page or video section). It maps to one or more LOS. |
| **Source reading / `source_ref`** | The reading number in a third-party study provider's material. Used internally for mapping only (BR-CAT-03). |
| **EOC questions** | End-of-chapter questions in the official CFA curriculum. Licensed; tracked by self-entry only. |
| **Premium Pack** | Official CFA Institute question-bank practice, available to candidates who bought it. Licensed; self-entry only. |
| **Premium Mocks** | Official CFA Institute mock exams (seven tracked). Licensed; self-entry only. |
| **Set 1 / Set 2** | The two halves (sessions) of a mock, attempted separately. |
| **Full mock** | Both sessions of a mock attempted in one sitting. Recorded separately from Set attempts. |
| **Schweser-derived notes** | Notes written independently by faculty after studying third-party material. They must be original wording (C-06). |

## 2. Platform terms

| Term | Meaning |
|---|---|
| **Resource** | A video, PDF, class note, in-app note or external reference attached to an LM or topic. |
| **Mandatory resource** | A resource that counts towards LM completion (BR-PRG-02). |
| **Mark as learned** | The student's declaration that they have studied an LM (BR-PRG-03). |
| **Revision** | A logged re-study of an LM; at most one counts per LM per day (BR-REV). |
| **Unlock rule** | A configurable condition that opens the next LM (BR-UNL). |
| **Sticky unlock** | An unlocked LM never re-locks (BR-UNL-06). |
| **Entitlement** | A student's right to access a subject, from batch enrolment or an admin grant. |
| **Batch** | A cohort of students preparing for the same exam window, e.g. KSC-27 (May 2027). |
| **QBank** | The repository of original questions written by the institute. |
| **Practice mode** | Feedback straight after each answer. |
| **Assessment mode** | Feedback only after submitting the test. |
| **Chapter quiz** | A 10-question assessment-mode test on one LM, used for unlocking. |
| **Master quiz** | A 50-question test across a whole subject. |
| **Custom test** | A test the student builds with filters (BRD §6). |
| **Test template** | A saved custom-test configuration (FR-14). |
| **Release validation** | Automated checks run before a question set is published (BR-QB-05). |
| **Provenance** | The origin and licence status of an asset (BR-CNT-04). |
| **Readiness estimate** | The LMS's indicator of preparation, always shown with the disclaimer in BR-ANL-04. |
| **XP / streak / badge** | Phase 5 engagement mechanics (BR-GAM). |

## 3. CFA Level I exam reference (verify each cycle)

| Item | Value used for planning |
|---|---|
| Format | 180 multiple-choice questions, 3 options (A/B/C), two sessions of 135 minutes each |
| Pace | 90 seconds per question on average |
| Negative marking | None |

| Subject | Code | Exam weight range |
|---|---|---|
| Ethical and Professional Standards | `eth` | 15–20% |
| Quantitative Methods | `qm` | 6–9% |
| Economics | `ec` | 6–9% |
| Financial Statement Analysis | `fsa` | 11–14% |
| Corporate Issuers | `cf` | 6–9% |
| Equity Investments | `eq` | 11–14% |
| Fixed Income | `fi` | 11–14% |
| Derivatives | `dv` | 5–8% |
| Alternative Investments | `ai` | 7–10% |
| Portfolio Management | `pm` | 8–12% |

Weights are planning defaults (BR-ANL-05). Check them against the current CFA Institute topic outline before every exam cycle.

## 4. Roles

| Role | Short code |
|---|---|
| Student | `student` |
| Instructor / content author | `author` |
| Academic reviewer | `reviewer` |
| Administrator | `admin` |
| Super administrator | `super_admin` |
| Parent / guardian (consent only in Phase 1) | `guardian` |

## 5. Abbreviations

| Abbr. | Expansion |
|---|---|
| BRD | Business Requirements Document |
| PRD | Product Requirements Document |
| DPDP | Digital Personal Data Protection Act, 2023 (India) |
| DPIA | Data Protection Impact Assessment |
| RoPA | Record of Processing Activities |
| RBAC | Role-Based Access Control |
| SRS | Spaced Repetition System |
| SLO / SLI | Service Level Objective / Indicator |
| RPO / RTO | Recovery Point / Recovery Time Objective |
| IST | Indian Standard Time (UTC+05:30); all day boundaries use IST |
