# C-06 Content Licensing & IP Register

| Field | Value |
|---|---|
| Document ID | C-06 |
| Version | 0.1 — Draft; legal review required |
| Owner | Academic lead (register) · Legal (approval) |
| Last updated | 2026-10-23 |
| Related | BRD §4, §7, §12, §19; P-09 BR-CNT-04; A-03 `licences`; M-04 D-004 |

## 1. Purpose
This document records, for every kind of learning material, who owns it, what the institute may do with it, and how the platform enforces that. It protects the institute from copyright and trademark claims, and protects the institute's own content from misuse.

## 2. Content classes and permitted use

| Class | Examples | Owner | May the LMS host it? | Provenance value | Rules |
|---|---|---|---|---|---|
| **A. Original LMS content** | Faculty-written notes, revision sheets, flashcards, original MCQs, infographics, worked examples in ₹ | The institute (via staff/contractor IP assignment) | Yes | `original` | Must be independently written; reviewer originality check; no copied stems or explanations |
| **B. Faculty recordings** | Class videos, class notes/handouts | The institute (IP assignment from faculty) | Yes | `faculty_recording` | Recordings must not show third-party copyrighted slides or text at length; review before publishing |
| **C. CFA Institute curriculum** | Curriculum readings, LOS statements, EOC questions | CFA Institute | **No** (text not hosted) | `reference_only` | LMS stores LOS **codes and short paraphrased statements** for mapping only; counsel to confirm whether LOS text may be reproduced. Links to the CFA Institute portal are allowed. EOC progress is self-entered. |
| **D. CFA Institute Premium Pack / Practice Pack / Mocks** | Official QBank, mocks | CFA Institute | **No** | `reference_only` | Self-entry tracking only (BR-MCK); no questions, screenshots or answer content stored |
| **E. Third-party prep provider material** (e.g. Schweser) | Notes, QBanks | Respective publisher | **No**, unless a written licence exists | `licensed_third_party` (with licence) or not uploaded | May be used internally to locate topics (`source_ref`). Derived notes must be **independently worded** with original examples; no reproduction of text, tables, diagrams or questions |
| **F. Licensed stock assets** | Icons, fonts (Figtree: SIL Open Font License), images | Licensors | Yes, per licence | `licensed_third_party` | Licence recorded; attribution where needed |
| **G. Student-generated data** | Bookmarks and notes (if added) | Student | Yes (service) | — | Not reused for content without consent |

## 3. Licence register

| Licence ID | Licensor | Asset(s) | Scope / permitted use | Territory | Valid from–to | Document | Recorded by | Status |
|---|---|---|---|---|---|---|---|---|
| LIC-001 | SIL / Figtree authors | Figtree font (web UI) | SIL OFL 1.1: use, embed, redistribute with the licence | Worldwide | Perpetual | OFL text in repo `frontend/public/fonts/OFL.txt` | Tech lead | Active |
| LIC-002 | [Microsoft] | Bahnschrift font (exported DOCX/PDF, BRD §9) | **To verify:** Bahnschrift is a Windows system font. Confirm whether it may be embedded in distributed PDFs, or use an open alternative (e.g. DIN-style open fonts) | — | — | — | Academic lead | **Open** |
| LIC-003 | CFA Institute | Use of "CFA®" trademarks in marketing | Per CFA Institute trademark and prep-provider guidelines (§5) | — | — | Guideline copy on file | Legal | **Open** |
| LIC-0xx | [Faculty name] | IP assignment for videos and notes | Assignment of copyright to the institute | — | — | Signed agreement | Legal | **To collect** for every author |

The application's `licences` table mirrors this register. A resource with provenance `licensed_third_party` cannot be published without an active licence record (BR-CNT-04).

## 4. Seed content from the prototype

| Asset | Class | Notes |
|---|---|---|
| Equities LM1–3 notes (AUTH) | A | Written for the prototype. Reviewer to confirm originality before migration. |
| 61 questions (BANK) | A | Reviewer to confirm originality and the answer keys before approval. |
| Flashcards (CARDS) | A | As above. |
| Demo leaderboard names, contest names | Demo | Not migrated to production. |

## 5. CFA Institute trademark and positioning rules (to verify with counsel)
CFA Institute publishes guidelines for prep providers on using its trademarks. Until counsel confirms the current text, the platform follows these working rules:
1. Use "CFA®" and "Chartered Financial Analyst®" with the ® symbol at the first prominent use on each page or document. Do not alter the marks or use CFA Institute logos.
2. Show this disclaimer in the footer of the site and on exported documents: *"CFA Institute does not endorse, promote, or warrant the accuracy or quality of the products or services offered by [Entity]. CFA® and Chartered Financial Analyst® are registered trademarks owned by CFA Institute."* (Confirm the exact current wording.)
3. Do not suggest affiliation, endorsement or official status. Avoid product names that imply official status. The working name "CFA Learning Hub" needs legal review (O-08).
4. Faculty may use the "CFA" designation personally ("Karan Singh, CFA") under CFA Institute's rules for charterholders.
5. Certificates (Phase 5) must say "Certificate of completion — [Subject] course, [Institute]". They must state clearly that they are not a CFA Institute credential, and must not use the CFA marks as a title.
6. Readiness estimates carry the BR-ANL-04 disclaimer.

## 6. Controls in the platform
- **Provenance is required** on every resource, content version and question version (BR-CNT-04).
- **Review checklist** item 1 is originality (P-05 WF-06). Phase 2 adds a similarity check of new question stems against the existing bank (trigram) and against an internal reference corpus where licensing permits.
- `source_ref` is internal (BR-CAT-03) and never appears in exports.
- Watermarking and access control protect class A and B content from redistribution (S-01 T-09, T-10).

## 7. Takedown and complaint process
1. Complaints go to `legal@<domain>` (address published in the terms).
2. Within 2 business days, the academic lead unpublishes the item(s) concerned (status `retired`, audit-logged) while the complaint is checked.
3. Legal decides; the outcome is recorded in this register (§8).
4. If the complaint is upheld: remove the item permanently, review related items by the same author, and retrain.

## 8. Complaint log
| Date | Complainant | Asset | Action | Outcome |
|---|---|---|---|---|
| — | — | — | — | — |

## 9. Contracts to put in place (Phase 0–1)
- [ ] IP assignment and confidentiality agreements for all faculty, authors and reviewers (employees and contractors).
- [ ] Terms of Use for students: licence to view, no redistribution, consequences of sharing (account suspension).
- [ ] Vendor terms checked for content ownership (Bunny: the customer keeps ownership).
