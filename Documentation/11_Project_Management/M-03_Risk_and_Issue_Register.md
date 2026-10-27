# M-03 Risk & Issue Register

| Field | Value |
|---|---|
| Document ID | M-03 |
| Version | 0.1 — Initial register |
| Owner | Project manager |
| Last updated | 2026-10-23 |
| Review cadence | Weekly in the delivery meeting; top 5 reported monthly to the steering group |

**Scoring:** Likelihood (L) and Impact (I) are each rated 1–5. Score = L × I. **High ≥ 15**, Medium 8–14, Low ≤ 7.

## Risks

| ID | Risk | L | I | Score | Owner | Mitigation | Trigger / indicator |
|---|---|---|---|---|---|---|---|
| R-01 | Licensed CFA Institute or third-party content (curriculum, EOC, Premium, Schweser) is uploaded or reproduced by mistake, creating legal exposure | 3 | 5 | **15** | Academic lead | Licensing register (C-06); provenance field required on every asset; reviewer checklist includes originality; self-entry only for licensed items; takedown process | An asset without provenance; reviewer flags similarity |
| R-02 | DPDP Act obligations (including verifiable parental consent for students under 18) are not met at launch | 3 | 5 | **15** | Product owner + Legal | DPIA (C-01) in Phase 1; consent flows (C-03) built in Phase 1; legal sign-off at the go-live gate | Legal review not booked 6 weeks before go-live |
| R-03 | Content production (approved questions, notes) cannot keep pace with the platform, so features launch with empty subjects | 4 | 4 | **16** | Academic lead | Content plan per subject with weekly targets; seed from the prototype; launch a subject only when it has a minimum content set; author tools prioritised in Phase 2 | Approved-question count below plan for 2 weeks running |
| R-04 | Reviewer bandwidth bottleneck delays publication | 3 | 3 | 9 | Academic lead | Review SLA (G-02); more than one reviewer per subject; queue dashboard | Review queue older than 7 days |
| R-05 | Video piracy (downloads, screen recording, link sharing) | 4 | 3 | 12 | Tech lead | Signed, expiring URLs; token authentication; domain restriction; visible student-ID watermark; concurrent-session limits | Abnormal playback from one account |
| R-06 | Account sharing among students | 3 | 3 | 9 | Product owner | Device/session limits; OTP on new device; anomaly report | More than 3 devices per account in a week |
| R-07 | Answer-key leakage through the API or browser | 2 | 4 | 8 | Tech lead | Server-side grading; answers never sent before submission in assessment mode (S-04); API tests assert this | A test failure or a pen-test finding |
| R-08 | Scope creep from the prototype's extra features (contests, XP) pulling them into early phases | 3 | 3 | 9 | Product owner | Phase 5 decision recorded (M-04 D-003); change-control rule in M-01 | Backlog items tagged Phase 5 entering a sprint |
| R-09 | Unclear mock unlock rules and prerequisites (BRD §17) cause rework | 3 | 3 | 9 | Product owner | Rule engine is configurable; decision needed before Phase 4 starts (M-04 O-05) | Open item not closed by May 2027 |
| R-10 | Load spikes at contest start or before exams degrade performance | 2 | 4 | 8 | DevOps | Load tests (N-04); autoscaling; caching; staggered contest starts | p95 latency above 2 s in load test |
| R-11 | Small team: key-person dependency on the tech lead | 3 | 4 | 12 | PM | Documentation (U-04, ADRs), pair programming, code reviews by two people | Single reviewer on most PRs |
| R-12 | SMS OTP delivery problems (DLT template approval, operator filtering) block logins | 3 | 4 | 12 | Tech lead | Register DLT templates early in Phase 0; email OTP fallback; second SMS provider | OTP success rate below 95% |
| R-13 | Data loss or a long outage | 1 | 5 | 5 | DevOps | Multi-AZ database, PITR backups, restore drills (D-06) | A failed restore drill |
| R-14 | CFA Institute trademark misuse in branding or certificates | 2 | 4 | 8 | Legal | Trademark guidance in C-06; disclaimer on site and certificates; legal review of brand assets | New marketing copy not reviewed |
| R-15 | Analytics or leaderboard data on minors breaches the DPDP restrictions on tracking and behavioural monitoring of children | 2 | 4 | 8 | Product + Legal | C-01 assessment; feature flags to disable such features for under-18 accounts unless an exemption applies | Legal opinion pending |
| R-16 | Budget overrun on video delivery costs | 2 | 3 | 6 | PM | Usage model (M-02 §4.2); monthly cost review; adaptive bitrate caps | Monthly bill above forecast by 25% |

## Issues (current)

| ID | Issue | Raised | Owner | Action | Status |
|---|---|---|---|---|---|
| I-01 | The BRD and prototype use different product names ("CFA Learning Hub" vs "Karan Sir Classes") | 2026-10-23 | Sponsor | Decide the brand (M-04 O-08) | Open |
| I-02 | The default unlock rule (chapter quiz ≥ 80%) needs the question bank, which arrives in Phase 2 | 2026-10-23 | PO | Phase 1 uses "previous LM marked learned"; switches to the quiz rule in Phase 2 (P-09 BR-UNL-04) | Proposed |
| I-03 | The prototype's pass check is `> 80%` while copy says "above 80%"; the decision is `≥ 80%` | 2026-10-23 | PO | Implemented in P-09 | Closed |
