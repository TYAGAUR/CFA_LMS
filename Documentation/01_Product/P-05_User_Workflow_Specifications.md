# P-05 User Workflow Specifications

| Field | Value |
|---|---|
| Document ID | P-05 |
| Version | 0.1 — Draft |
| Owner | Business analyst |
| Last updated | 2026-10-23 |
| Related | P-03 PRD, P-06 RBAC, P-09 Business rules, C-03 Consent |

Diagrams use Mermaid. They render in GitHub and in VS Code with a Mermaid preview extension.

---

## WF-01 Student sign-up and onboarding (Phase 1)

```mermaid
flowchart TD
  A[Enter mobile number] --> B{Rate limit OK?}
  B -- no --> B1[Show 'try again later'] 
  B -- yes --> C[Send SMS OTP]
  C --> D{OTP correct within 5 min?}
  D -- no, < 5 tries --> D1[Retry] --> D
  D -- SMS failed twice --> E[Offer email OTP] --> D
  D -- yes --> F{Existing account?}
  F -- yes --> Z[Sign in, go to dashboard]
  F -- no --> G[Name, DOB, optional email]
  G --> H[Privacy notice and consents\nmandatory + optional purposes]
  H --> I{Age < 18?}
  I -- no --> J[Account active]
  I -- yes --> K[Status: pending_guardian_consent\nWF-02]
  J --> L{Pre-enrolled in a batch?}
  L -- yes --> M[Entitlements active, welcome tour]
  L -- no --> N[Show 'Awaiting enrolment' screen\nand contact info]
```

**Exceptions**
- A number already linked to a deactivated account shows "Contact support"; no new account is created.
- An unverified under-18 account is deleted after 30 days (C-05).

## WF-02 Verifiable parental consent (Phase 1)

```mermaid
sequenceDiagram
  actor S as Student (<18)
  participant L as LMS
  actor G as Guardian
  S->>L: Enter guardian name + mobile
  L->>G: SMS with consent link + OTP
  G->>L: Open link, read notice (plain language)
  G->>L: Enter OTP, confirm relationship, accept
  L->>L: Record consent (guardian id, method=SMS-OTP, notice version, timestamp, IP)
  L-->>S: Account activated (notification)
  Note over L: No guardian action in 7 days → reminder.<br/>None in 30 days → account and data deleted.
```

A guardian can later withdraw consent through the link in their confirmation SMS or email. The student's account is then suspended and handled under C-05.

## WF-03 Batch creation and enrolment (Admin, Phase 1)

```mermaid
flowchart LR
  A[Create batch: code, exam window,\ndates, subjects] --> B[Upload CSV of students]
  B --> C[Validate rows]
  C --> D[Preview: valid / errors]
  D --> E{Commit valid rows?}
  E -- yes --> F[Create/attach accounts\nCreate enrolments + entitlements]
  F --> G[Send invites to new numbers]
  F --> H[Audit log: enrolment.bulk_create]
  E -- no --> B
```

## WF-04 Study an LM and unlock the next (Phase 1 → Phase 2)

```mermaid
flowchart TD
  A[Open subject] --> B[Rail shows LM states]
  B --> C{LM unlocked?\nserver check}
  C -- no --> C1[Show unmet conditions\nBR-UNL-08]
  C -- yes --> D[Study: videos, notes, PDFs]
  D --> E[Resource completion recorded\nBR-PRG-01]
  E --> F[Optional: log EOC self-entry]
  F --> G[Mark LM learned]
  G --> H{Phase 2+: take chapter quiz}
  H --> I[Score >= threshold?]
  I -- no --> J[Review explanations,\nrevisit notes, retake with new questions]
  J --> H
  I -- yes --> K[Evaluate subject rule for next LM]
  G -. Phase 1 default rule .-> K
  K --> L{Rule satisfied?}
  L -- yes --> M[Unlock next LM\nsticky, record time]
  L -- no --> C1
  M --> N{Last LM?}
  N -- yes --> O[Master quiz available\nPhase 2]
  N -- no --> A
```

## WF-05 Resource upload and publish (Author/Admin, Phase 1)

```mermaid
flowchart TD
  A[Choose LM/topic] --> B[Select type: video / PDF / class note / link]
  B --> C[Enter metadata: title, order, mandatory flag, provenance]
  C --> D{Provenance = licensed_third_party?}
  D -- yes --> D1{Licence record exists in C-06?}
  D1 -- no --> D2[Blocked: cannot publish]
  D1 -- yes --> E
  D -- no --> E[Upload directly to storage / video host]
  E --> F[Processing: encode / virus scan]
  F --> G{OK?}
  G -- no --> G1[Error shown, file quarantined]
  G -- yes --> H[Status: draft]
  H --> I[Phase 1: Admin publishes\nPhase 2+: Reviewer approves → publish]
  I --> J[Visible to entitled students\nAudit: resource.published]
```

## WF-06 Content and question review lifecycle (Phase 2–3)

```mermaid
stateDiagram-v2
  [*] --> draft
  draft --> in_review: author submits
  in_review --> returned: reviewer returns with comments
  returned --> draft: author edits (new version)
  in_review --> approved: reviewer approves (≠ author)
  approved --> published: publish (validator passed for QBank)
  published --> retired: retire
  published --> draft: edit creates NEW version (published version unchanged)
  retired --> [*]
```

**Review checklist** (completed by the reviewer before approving):
1. Original wording, with no copied source text (C-06).
2. Calculations recomputed.
3. Answer key matches the option text.
4. Distractors are plausible, with a rationale for each.
5. LOS mapping and command word are correct.
6. ₹ / Indian context is appropriate.
7. Formatting follows the style guide (P-08).

## WF-07 Custom test: build, attempt, resume, review (Phase 2)

```mermaid
sequenceDiagram
  actor S as Student
  participant UI as Next.js
  participant API as FastAPI
  S->>UI: Choose filters, mode, timing, count
  UI->>API: POST /tests/preview
  API-->>UI: eligible_count (BR-TST-01/02)
  S->>UI: Start
  UI->>API: POST /tests (create attempt)
  API->>API: Draw (BR-TST-03/04), shuffle (BR-TST-05), persist order
  API-->>UI: Questions WITHOUT answers
  loop each answer
    UI->>API: PUT /attempts/{id}/items/{n} (autosave)
    alt practice mode
      API-->>UI: correct + explanation
    end
  end
  Note over UI,API: Browser closes → GET /attempts/{id} resumes (BR-TST-08)
  S->>UI: Submit (or timer expires)
  UI->>API: POST /attempts/{id}/submit
  API->>API: Grade, update best score, evaluate unlocks
  API-->>UI: Score + review with explanations
```

## WF-08 EOC / Premium Pack / Mock self-entry (Phase 1 EOC, Phase 4 mocks)

```mermaid
flowchart TD
  A[Open tracker] --> B{Prerequisites met?\nBR-MCK-03}
  B -- no --> B1[Show what is missing]
  B -- yes --> C[Enter: date, kind set1/set2/full,\ncorrect, total, unanswered, minutes]
  C --> D[Optional: per-subject breakdown, weak topics]
  D --> E{Validation: sums match,\ncorrect ≤ total, date ≤ today}
  E -- fail --> C
  E -- pass --> F[Save entry]
  F --> G[Weak topics → revision queue]
  F --> H[Analytics updated]
```

## WF-09 Revision and flashcards (Phase 3)
1. The student opens the Revision tab for an LM. The revision sheet (2 pages) is shown and can be downloaded as a watermarked PDF.
2. "Start flashcards" shows the cards due for that LM, overdue cards first (BR-FC-04).
3. For each card: flip, then rate Known / Needs revision / Difficult. The next due date is computed (BR-FC-03).
4. A session of ≥ 10 cards logs one revision for the LM (BR-REV-04).

## WF-10 Data subject request (Phase 1)

```mermaid
flowchart LR
  A[Student: Profile → My data] --> B{Request type}
  B -- Access/export --> C[Ticket created] --> D[Admin verifies identity via OTP] --> E[System generates export JSON+PDF] --> F[Secure link, expires in 7 days]
  B -- Correction --> G[Self-service edit, or ticket for locked fields]
  B -- Erasure --> H[Ticket] --> I[Admin confirms no legal hold] --> J[Account deactivated → personal data deleted/anonymised per C-05] --> K[Confirmation sent]
  B -- Grievance --> L[Grievance officer queue, response SLA]
```

## WF-11 Staff onboarding and offboarding (Phase 1)
- **Onboarding:** an admin creates the staff user (WF actor: super admin for admin roles) → an invite email is sent → first login sets the password and enrols TOTP → roles become active → audit event.
- **Offboarding:** deactivate → sessions revoked → drafts the person owns are reassigned → access review records the removal.

## WF-12 Unlock rule change (Admin, Phase 1)
1. The admin opens the rule editor for a subject → edits conditions → sees a plain-language preview.
2. Tests the rule against sample students → sees how many students would be affected.
3. Saves with a reason → a new rule version is created → audit event `unlock_rule.updated`.
4. The new rule applies to future evaluations. Existing unlocks stay (BR-UNL-06).

## WF-13 Contest (Phase 5)
Admin creates the contest (window, timer, question set, eligibility) → announcement → students register → reminders sent 24 hours and 1 hour before → the window opens and each student gets one attempt → grading on the server → admin reviews and publishes results → the leaderboard updates (opt-in names only).
