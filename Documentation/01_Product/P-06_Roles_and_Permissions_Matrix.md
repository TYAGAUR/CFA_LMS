# P-06 Roles & Permissions (RBAC) Matrix

| Field | Value |
|---|---|
| Document ID | P-06 |
| Version | 0.1 — Draft |
| Owner | Product owner + Security lead |
| Last updated | 2026-10-23 |
| Related | BRD §3, §12; P-09 BR-ACC, BR-CNT; S-02 |

## 1. Model
- **Roles** grant **permissions** of the form `resource:action`, e.g. `question:approve`.
- **Entitlements** limit what a student can see: only subjects they are entitled to (BR-ENR-01).
- **Ownership** limits some actions to the user's own records (e.g. a student reads only their own attempts).
- **Segregation of duties** constraints are enforced in code, not just by role (§4).
- The backend checks permissions on every route through a dependency (A-01 §6). Frontend checks only hide UI and are never relied on.

## 2. Roles

| Role | Who | How assigned |
|---|---|---|
| `student` | Enrolled candidate | Self sign-up plus admin enrolment |
| `guardian` | Parent of an under-18 student | Created during the parental consent flow; no login in Phase 1 |
| `author` | Instructor / content author | Admin |
| `reviewer` | Academic reviewer | Admin |
| `admin` | Operations staff | Super admin |
| `super_admin` | Platform owner (2 people at most) | Super admin, with the second super admin's approval |

## 3. Permission matrix

✔ = allowed · **own** = own records only · **ent** = entitled subjects only · **unl** = unlocked LMs only · — = not allowed · Ph = phase the permission arrives

| Resource : action | student | author | reviewer | admin | super_admin | Ph |
|---|---|---|---|---|---|---|
| **Account** |||||||
| `profile:read/update` | own | own | own | own | own | 1 |
| `consent:manage` | own | — | — | read | read | 1 |
| `data_request:create` (access/erase) | own | own | own | — | — | 1 |
| `data_request:process` | — | — | — | ✔ | ✔ | 1 |
| **Users & access** |||||||
| `user:read` | — | — | — | ✔ | ✔ | 1 |
| `user:create/update/deactivate` | — | — | — | ✔ (non-staff and author/reviewer) | ✔ (all) | 1 |
| `role:assign admin` | — | — | — | — | ✔ | 1 |
| `batch:manage`, `enrolment:manage`, `entitlement:grant` | — | — | — | ✔ | ✔ | 1 |
| `session:revoke` (other users) | — | — | — | ✔ | ✔ | 1 |
| **Catalogue** |||||||
| `subject/lm/topic/los:read` | ent | ✔ | ✔ | ✔ | ✔ | 1 |
| `subject/lm/topic/los:create/update` | — | ✔ | — | ✔ | ✔ | 1 |
| `subject/lm:publish` | — | — | — | ✔ | ✔ | 1 |
| **Resources & notes** |||||||
| `resource:view` (stream/download) | ent+unl | ✔ | ✔ | ✔ | ✔ | 1 |
| `resource:upload/update` | — | ✔ | — | ✔ | ✔ | 1 |
| `resource:publish` | — | — | ✔ (Ph2+) | ✔ (Ph1 direct) | ✔ | 1 |
| `note/revision_sheet:draft` | — | ✔ | — | — | — | 3 |
| `note/revision_sheet:review/approve/return` | — | — (own) | ✔ (not own) | — | — | 3 |
| `note/revision_sheet:export` | own PDF (if published) | ✔ | ✔ | ✔ | ✔ | 3 |
| **Progress** |||||||
| `progress:write` (completion, learned, revision, EOC) | own | — | — | — | — | 1 |
| `progress:read` | own | — | — | ✔ | ✔ | 1 |
| `lm:manual_unlock` | — | — | — | ✔ | ✔ | 1 |
| `unlock_rule:manage` | — | — | — | ✔ | ✔ | 1 |
| **Bookmarks** | own | own | own | own | own | 1 |
| **Question bank** |||||||
| `question:read` (with answers) | — | ✔ | ✔ | ✔ | ✔ | 2 |
| `question:draft/update` | — | ✔ | — | — | — | 2 |
| `question:review/approve/return` | — | — | ✔ (not own) | — | — | 2 |
| `question:publish/retire` | — | — | ✔ | ✔ | ✔ | 2 |
| `qbank:validate` (release validation) | — | ✔ | ✔ | ✔ | ✔ | 2 |
| `qbank:export` | — | ✔ (student set only) | ✔ | ✔ | ✔ | 2 |
| **Tests** |||||||
| `test:create/attempt` | own, ent+unl | — | — | — | — | 2 |
| `test_template:manage` | own | — | — | — | — | 2 |
| `attempt:read` | own | — | — | ✔ | ✔ | 2 |
| `attempt:regrade` | — | — | ✔ (proposes) | ✔ (applies) | ✔ | 2 |
| **Flashcards** |||||||
| `flashcard:review` | own, ent | — | — | — | — | 3 |
| `flashcard:draft` / `approve` | — | ✔ / — | — / ✔ (not own) | — | — | 3 |
| **Mocks** |||||||
| `mock_entry:write/read` | own | — | — | read | read | 4 |
| `mock_rule:manage` | — | — | — | ✔ | ✔ | 4 |
| **Reports & audit** |||||||
| `report:progress/content` | — | own content stats | ✔ | ✔ | ✔ | 1 |
| `audit_log:read` | — | — | — | ✔ (excluding security events) | ✔ | 1 |
| `settings:global` (auth policy, retention, feature flags) | — | — | — | — | ✔ | 1 |
| **Engagement** |||||||
| `contest:manage`, `results:publish`, `announcement:manage` | — | — | — | ✔ | ✔ | 5 |
| `contest:register/attempt` | own, ent | — | — | — | — | 5 |

## 4. Segregation of duties (enforced in code)

| ID | Constraint |
|---|---|
| SoD-01 | A user cannot approve a content or question version they authored or last edited (BR-CNT-03). |
| SoD-02 | An admin cannot grant themselves the `super_admin` role. A super-admin grant needs a second super admin. |
| SoD-03 | A regrade proposed by a reviewer is applied by an admin, not by the same person. |
| SoD-04 | Staff cannot read a student's answers in an active (not yet submitted) contest attempt. |
| SoD-05 | Changes to audit-log retention or deletion need a super admin and raise an alert. |

## 5. Break-glass access
- A `break_glass` flag on a super-admin session allows emergency production data fixes through the admin API only. It never allows direct database writes.
- Using it needs a reason, expires after 60 minutes, sends an immediate alert to the other super admin, and is reviewed in the next access review (G-04).

## 6. Staff account requirements
- MFA (TOTP) is required for author, reviewer, admin and super_admin (S-02).
- Staff sessions time out after 30 minutes idle and 12 hours in total.
- Roles are recertified quarterly (G-04).
