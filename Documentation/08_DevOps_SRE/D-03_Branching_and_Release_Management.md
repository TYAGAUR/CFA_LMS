# D-03 Branching & Release Management

| Field | Value |
|---|---|
| Document ID | D-03 |
| Version | 0.1 |
| Owner | DevOps lead + Tech lead |
| Last updated | 2026-10-23 |
| Related | D-02, U-04 |

## 1. Branching model: trunk-based
- `main` is always deployable and deploys to staging automatically.
- Work happens in **short-lived branches** (≤ 3 days) named `<type>/<ticket>-<slug>`, e.g. `feat/LMS-142-unlock-rule-editor`, `fix/LMS-201-otp-expiry`.
- Unfinished features are merged behind **feature flags** (D-01 §6), not in long-lived branches.
- No direct pushes to `main`. Branch protection: required checks (D-02 §3), required reviews, linear history (squash merge), signed commits recommended.

## 2. Commits and pull requests
- **Conventional Commits** in the squash-merge title: `feat(rules): add revisions condition`, `fix(auth): rotate refresh on reuse`, `chore(deps): …`, `docs: …`, `refactor`, `test`, `perf`, `ci`.
- **PR template:**
  - What / Why / How.
  - Linked ticket and BR/US IDs.
  - Screenshots for UI.
  - Migration notes.
  - Security impact (yes/no + explanation).
  - Docs updated (A-03 / C-04 if data changes).
  - Rollback plan.
- PR size guide: under 400 changed lines excluding generated files. Larger PRs need a reason.
- Reviews: one approval by default; two for CODEOWNERS-protected paths (D-02 §3). The reviewer checks tests, authorisation, logging and data classification.

## 3. Versioning
- **Semantic versioning** for the platform release: `vMAJOR.MINOR.PATCH`.
  - MAJOR: a breaking API version (`/api/v2`) or a phase launch (optional).
  - MINOR: features.
  - PATCH: fixes.
- Release notes are generated from Conventional Commits (release-please or changesets), then edited for audience:
  - **internal notes** with technical detail;
  - **student-facing "What's new"** in plain language.

## 4. Release cadence
- **Staging:** continuous (every merge).
- **Production:** weekly release train, Tuesday 11:00 IST (low-traffic window). Hotfixes as needed.
- **Freeze windows:**
  - 3 weeks before any exam window that most enrolled students are sitting: releases limited to fixes, unless the PO approves otherwise.
  - Phase 5 contest days: no production deploys from 2 hours before a contest until results are published.
- The release calendar is kept in the project wiki and reviewed in the weekly delivery meeting.

## 5. Database change management (expand/contract)
1. **Expand:** add new nullable columns or tables. Deploy code that writes to both old and new structures (if needed) and reads the new one.
2. **Migrate:** backfill in batches with a background job (not inside the migration, for large tables). Must be idempotent.
3. **Contract:** at least one release later, remove the old column or table once no code uses it.

**Rules:**
- No table locks longer than 2 s (use `CREATE INDEX CONCURRENTLY`; add NOT NULL through a validated CHECK constraint first).
- Every migration has a `downgrade()` for non-destructive steps.
- Migrations touching personal data columns need privacy-owner review (C-04 §4).

## 6. Hotfix process
1. Branch from `main` as `hotfix/<ticket>`, with the minimal fix and a regression test.
2. Expedited review (one reviewer, the tech lead or delegate), full CI.
3. Merge → staging smoke → release tag `vX.Y.(Z+1)` → production with approval.
4. Post-incident review if the hotfix came from an incident (S-06).

## 7. Release checklist (production)
- [ ] Changes verified on staging; smoke E2E green.
- [ ] Release notes (internal and student-facing) ready.
- [ ] Migrations reviewed; expand/contract respected.
- [ ] Feature flags for this release planned (on/off per role or batch).
- [ ] Security checklist (S-03 §5) done.
- [ ] Not inside a freeze window, or an exception approved.
- [ ] On-call engineer aware; rollback command ready.
- [ ] After release: canary green for 15 minutes; announcement posted (if student-facing).

## 8. Environments and tags
| Ref | Deploys to |
|---|---|
| PR branch | CI only (preview environment optional) |
| `main` | staging |
| `vX.Y.Z` tag | production (same image SHA as staging) |
