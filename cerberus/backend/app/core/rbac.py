ROLE_HIERARCHY = {
    "super_admin": 100,
    "admin": 90,
    "event_admin": 70,
    "challenge_author": 50,
    "infra_admin": 60,
    "user": 10,
}

ROLE_CAPABILITIES = {
    "super_admin": {"*"},
    "admin": {
        "manage_users",
        "manage_events",
        "manage_challenges",
        "manage_hints",
        "view_audit",
        "send_notifications",
        "manage_ui_config",
    },
    "event_admin": {
        "manage_events",
        "manage_challenges",
        "manage_hints",
        "view_leaderboard",
        "send_notifications",
    },
    "challenge_author": {"manage_challenges", "manage_hints"},
    "infra_admin": {"view_audit", "manage_ui_config", "manage_notifications"},
    "user": {"submit_flags", "view_leaderboard"},
}


def has_capability(role: str, capability: str) -> bool:
    caps = ROLE_CAPABILITIES.get(role, set())
    return "*" in caps or capability in caps
