# C-01 DPDP Act 2023 Compliance Assessment / DPIA

| Field | Value |
|---|---|
| Document ID | C-01 |
| Version | 0.1 — Draft; **must be reviewed by qualified Indian legal counsel before go-live** |
| Owner | Privacy owner (Product owner until a DPO / privacy contact is appointed) + Legal |
| Last updated | 2026-10-23 |
| Related | C-02 Privacy policy, C-03 Consent, C-04 Data inventory, C-05 Retention, S-06 Incident response |

> **Legal note.** This is an engineering and product assessment against the Digital Personal Data Protection Act, 2023 ("Act") and the Digital Personal Data Protection Rules, 2025 ("Rules"). It is not legal advice. The Rules apply in phases, and section and rule references and timelines must be confirmed by counsel (open decision O-11 and risk R-02). The platform is designed to comply from day one regardless of the commencement dates.

## 1. Processing description

| Item | Description |
|---|---|
| Data Fiduciary | The legal entity operating Karan Sir Classes / CFA Learning Hub [entity name TBD] |
| Data Processors | AWS (hosting), Bunny (video), MSG91 (SMS), Amazon SES (email), Sentry (errors). Full list in C-07. |
| Data Principals | Students (including **children under 18**), parents/guardians, staff and contractors |
| Purposes | (P1) Provide the learning service: accounts, access, progress, tests. (P2) Security, fraud and abuse prevention. (P3) Legal compliance. (P4) Product analytics to improve the service (optional consent). (P5) Marketing messages (optional consent). (P6) Leaderboard name display (Phase 5, optional consent). |
| Personal data | See C-04. Name, mobile, email, DOB/age, guardian name and mobile, device/session data, IP address, learning progress, test answers and scores, consent records, support requests. **No** government ID, financial account data or biometrics in Phase 1. |
| Volume | Pilot: ~2,000 students per year; growth expected |
| Storage location | India (AWS Mumbai; DR copy in AWS Hyderabad). Some processors may process outside India; see §8. |
| Significant Data Fiduciary? | Unlikely at this scale. Re-assess if notified by the government. |

## 2. Necessity and proportionality

| Data element | Needed for | Minimised? |
|---|---|---|
| Mobile number | Login (OTP), account recovery, service messages | Yes; it is the primary identifier |
| Email | Optional for students; required for staff | Optional for students |
| Date of birth | Only to work out whether the student is a minor (needed for §5 obligations) | Could be reduced to an "Are you 18 or older?" declaration plus a year of birth. **Recommendation:** store DOB only until the 18th birthday, then keep only `is_minor=false`. |
| Guardian name and mobile | Verifiable parental consent | Yes; used for no other purpose |
| IP address, user agent | Security, session management, legal log retention | Retention-limited (C-05) |
| Progress, answers, scores | Core service | Yes |
| Analytics events | Service improvement | Pseudonymised; only with consent (P4) |

## 3. Obligation-by-obligation assessment

| # | Obligation (Act / Rules) | How the platform meets it | Status |
|---|---|---|---|
| 1 | **Lawful processing:** consent or a legitimate use (Act s.4, s.6, s.7) | Consent at sign-up for P1 (itemised notice). Legitimate use or legal obligation for P2/P3 where available, confirmed by counsel. Separate optional consents for P4–P6 (C-03). | Designed |
| 2 | **Notice** in clear, plain language, itemised, with how to withdraw and complain (s.5; Rules on notice) | A notice screen before consent; versioned; available in English, with Hindi planned; links to the privacy policy (C-02) | Designed |
| 3 | **Consent:** free, specific, informed, unconditional, unambiguous, by clear affirmative action; as easy to withdraw as to give (s.6) | Optional purposes unticked by default; consent dashboard in the profile (US-3.03); withdrawal effective within 24 hours; append-only consent records with notice version | Designed |
| 4 | **Children's data:** verifiable consent of a parent or lawful guardian before processing (s.9(1)) | Age gate at sign-up; account inactive until guardian OTP consent (WF-02, C-03 §5); unverified accounts deleted after 30 days | Designed. **Verification method to be confirmed by counsel** against the Rules (the Rules describe verifying the parent's identity and age using reliable details or a virtual token, e.g. via DigiLocker). |
| 5 | **Children:** no processing likely to harm a child's well-being; **no tracking, behavioural monitoring or targeted advertising directed at children** (s.9(2)–(3)) | No advertising on the platform. Product analytics (P4) **off** for under-18 accounts. Leaderboard (P6) off for under-18 accounts. Learning progress tracking is core to the service. Counsel to confirm whether the educational-institution exemption in the Rules applies to a coaching institute (O-11). Feature flag `minor_restrictions` enforces this. | Designed; legal opinion pending |
| 6 | **Accuracy and completeness** where data is used for decisions (s.8(3)) | Self-service profile editing; correction requests (WF-10) | Designed |
| 7 | **Reasonable security safeguards** (s.8(5); Rules on security safeguards: encryption/masking, access control, logging and monitoring, backups, log retention, contracts with processors) | S-01/S-02 controls; encryption with KMS; RBAC; audit logs; backups (D-06); logs and related data kept for at least one year where the Rules require it (C-05); processor DPAs (C-07) | Designed |
| 8 | **Breach notification** to the Data Protection Board and to each affected Data Principal (s.8(6); Rules set the content and timelines; the Board needs a detailed report, expected within 72 hours) | Incident Response Plan (S-06) with DPDP and CERT-In tracks; notification templates; contact data available | To do (S-06) |
| 9 | **Erasure** when the purpose is served or consent withdrawn, unless retention is legally required (s.8(7)); notice before erasure where the Rules require it | Retention schedule (C-05); automated deletion jobs; 48-hour advance notice to the user before scheduled inactivity deletion | Designed |
| 10 | **Processor contracts** (s.8(2)) | DPAs with every processor (C-07) | To do |
| 11 | **Contact for questions** published (s.8(9)) and a grievance mechanism (s.13) | Grievance officer contact in the privacy policy and app footer; grievance requests through WF-10; response SLA (C-05 §6) | Designed |
| 12 | **Rights of Data Principals:** access/summary (s.11), correction and erasure (s.12), grievance redressal (s.13), nomination (s.14) | Data requests module (US-3.04); export as JSON + PDF summary; nomination form (record a nominee contact) in Phase 1 | Designed; nomination to be added to US-3.04 |
| 13 | **Cross-border transfer** (s.16): allowed except to countries the government restricts | Primary storage in India; processors outside India are checked against any restricted list (§8) | Monitor |
| 14 | **Consent Managers** (s.6(7)–(9)) | Not needed; support later if users ask | N/A |

## 4. Risk assessment

| ID | Risk to Data Principals | Likelihood | Severity | Controls | Residual |
|---|---|---|---|---|---|
| PR-1 | A child's data is processed without valid parental consent | Medium | High | Age gate, guardian OTP, account inactive until consent, audit trail | Medium (self-declared age); review the verification method with counsel |
| PR-2 | Behavioural monitoring of minors through analytics or leaderboard | Medium | High | Flags off for minors; legal opinion O-11 | Low |
| PR-3 | Breach of personal data (e.g. a database leak) | Low | High | Encryption, least privilege, monitoring, pen tests | Low |
| PR-4 | Excess retention of inactive accounts | Medium | Medium | Retention jobs, user notices | Low |
| PR-5 | Leaderboard shows names without consent | Low | Medium | Opt-in only (BR-GAM-04) | Low |
| PR-6 | Staff misuse of student data | Low | Medium | RBAC, audit, export alerts, access reviews | Low |
| PR-7 | PII leaks to third parties via logs or error tracking | Medium | Medium | Scrubbing, no request bodies in logs, DPAs | Low |
| PR-8 | Watermark shows personal data on screen recordings that get shared | Medium | Low | Watermark uses a short student code, not the full name or mobile number (US-5.04 updated) | Low |

> **Change triggered by this DPIA:** the video/PDF watermark shows the **student code** (e.g. `KSC27-0412`) and a **masked mobile number** (last 4 digits), not the full name. PDF download watermarks may include the name, because the file is issued to that student. P-03 US-5.04/5.05 are to be aligned with this.

## 5. Penalty exposure (for prioritisation)
The Act's schedule sets penalties of up to ₹250 crore for failing to take reasonable security safeguards, and up to ₹200 crore each for failing to notify breaches and failing to meet the children's data obligations. Confirm the current figures with counsel. These items are therefore **must-have before go-live**.

## 6. Go-live privacy checklist
- [ ] Legal review of this DPIA, the notice, the privacy policy (C-02) and the consent flows (C-03).
- [ ] Guardian consent flow tested end to end, with audit evidence.
- [ ] Minor-restriction flags verified for under-18 accounts.
- [ ] Data request (access/erasure/grievance) workflow tested, with SLAs.
- [ ] Retention jobs running in staging, with deletion evidence.
- [ ] DPAs signed with all processors in C-07.
- [ ] Grievance officer named and contact published.
- [ ] Breach response playbook (S-06) rehearsed in a tabletop exercise.

## 7. Review
Review every year, at each phase gate that adds new data or purposes (e.g. Phase 4 analytics, Phase 5 leaderboard, AI features), and whenever the Rules or guidance change.

## 8. Processors and location (summary; full detail in C-07)

| Processor | Data | Location | Notes |
|---|---|---|---|
| AWS | All | India (Mumbai, Hyderabad) | — |
| Bunny | Video files; playback logs with IP | Global CDN; storage region chosen in Asia/India where available | No user identifiers sent except an opaque token |
| MSG91 | Mobile numbers, OTP text | India | DLT-compliant |
| Amazon SES | Email addresses | ap-south-1 | — |
| Sentry | Error events (scrubbed); pseudonymous user ID | EU/US (choose the EU region) | PII scrubbing enforced |
