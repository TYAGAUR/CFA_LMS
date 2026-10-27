"""Role → permission mapping (P-06 §3). Deny by default."""

STUDENT = {
    "profile:self", "consent:self", "data_request:create", "progress:write", "bookmark:self",
    "course:register", "order:self", "test:take", "flashcard:review",
}
AUTHOR = {
    "profile:self", "data_request:create", "bookmark:self",
    "catalog:read_admin", "catalog:write", "content:write", "resource:write", "staff:console",
    "qbank:write", "flashcard:write", "test:take", "flashcard:review",
}
REVIEWER = {
    "profile:self", "data_request:create", "bookmark:self",
    "catalog:read_admin", "content:publish", "resource:publish", "report:read", "staff:console",
    "qbank:publish", "test:take", "flashcard:review",
}
ADMIN = AUTHOR | REVIEWER | {
    "user:read", "user:write", "batch:manage", "enrolment:manage", "entitlement:grant",
    "course:manage", "order:read", "order:refund", "order:offline", "catalog:publish",
    "audit:read", "data_request:process", "session:revoke",
}
SUPER_ADMIN = ADMIN | {"role:assign_admin", "settings:global", "audit:read_security"}

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "student": STUDENT,
    "author": AUTHOR,
    "reviewer": REVIEWER,
    "admin": ADMIN,
    "super_admin": SUPER_ADMIN,
}


def permissions_for(roles: list[str]) -> set[str]:
    perms: set[str] = set()
    for r in roles:
        perms |= ROLE_PERMISSIONS.get(r, set())
    return perms
