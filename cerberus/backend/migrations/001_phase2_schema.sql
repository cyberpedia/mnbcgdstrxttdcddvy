BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Optional least-privilege runtime role (safe to run repeatedly).
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'cerberus_app_rw') THEN
        CREATE ROLE cerberus_app_rw LOGIN;
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(128) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS capabilities (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS roles (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(64) NOT NULL,
    capabilities JSONB NOT NULL DEFAULT '[]'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, name),
    CONSTRAINT roles_capabilities_array CHECK (jsonb_typeof(capabilities) = 'array')
);

CREATE TABLE IF NOT EXISTS role_capabilities (
    role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    capability_id BIGINT NOT NULL REFERENCES capabilities(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (role_id, capability_id)
);

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(320) NOT NULL,
    hashed_password TEXT NOT NULL,
    role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    preferences JSONB NOT NULL DEFAULT '{}'::JSONB,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, username),
    UNIQUE (tenant_id, email),
    CONSTRAINT users_hashed_password_not_plaintext CHECK (
        hashed_password <> '' AND
        hashed_password !~* '^(password|123456|qwerty)$'
    ),
    CONSTRAINT users_preferences_object CHECK (jsonb_typeof(preferences) = 'object')
);

CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    theme VARCHAR(128),
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT events_time_window CHECK (end_time > start_time),
    CONSTRAINT events_status_valid CHECK (status IN ('draft', 'scheduled', 'live', 'paused', 'archived')),
    UNIQUE (tenant_id, name)
);

CREATE TABLE IF NOT EXISTS challenges (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL,
    difficulty VARCHAR(16) NOT NULL,
    type VARCHAR(32) NOT NULL,
    hierarchical_rule JSONB NOT NULL DEFAULT '{}'::JSONB,
    visibility VARCHAR(16) NOT NULL DEFAULT 'private',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT challenges_difficulty_valid CHECK (difficulty IN ('easy', 'medium', 'hard', 'expert')),
    CONSTRAINT challenges_visibility_valid CHECK (visibility IN ('public', 'private', 'event_only')),
    CONSTRAINT challenges_hierarchical_rule_object CHECK (jsonb_typeof(hierarchical_rule) = 'object'),
    UNIQUE (event_id, title)
);

CREATE TABLE IF NOT EXISTS sub_challenges (
    id BIGSERIAL PRIMARY KEY,
    challenge_id BIGINT NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    "order" INTEGER NOT NULL,
    flag TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT sub_challenges_order_positive CHECK ("order" > 0),
    CONSTRAINT sub_challenges_flag_not_empty CHECK (length(trim(flag)) > 0),
    UNIQUE (challenge_id, "order"),
    UNIQUE (challenge_id, title)
);

CREATE TABLE IF NOT EXISTS hints (
    id BIGSERIAL PRIMARY KEY,
    challenge_id BIGINT NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    penalty INTEGER NOT NULL DEFAULT 0,
    enabled BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT hints_penalty_range CHECK (penalty >= 0 AND penalty <= 1000)
);

CREATE TABLE IF NOT EXISTS teams (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (event_id, name)
);

CREATE TABLE IF NOT EXISTS team_members (
    team_id BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (team_id, user_id)
);

CREATE TABLE IF NOT EXISTS submissions (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    challenge_id BIGINT NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    sub_challenge_id BIGINT REFERENCES sub_challenges(id) ON DELETE SET NULL,
    flag TEXT NOT NULL,
    result VARCHAR(16) NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT submissions_result_valid CHECK (result IN ('correct', 'incorrect', 'duplicate', 'error')),
    CONSTRAINT submissions_flag_not_empty CHECK (length(trim(flag)) > 0)
);

CREATE TABLE IF NOT EXISTS leaderboard (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    team_id BIGINT REFERENCES teams(id) ON DELETE CASCADE,
    score INTEGER NOT NULL DEFAULT 0,
    "timestamp" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT leaderboard_owner_present CHECK (
        (user_id IS NOT NULL AND team_id IS NULL) OR
        (user_id IS NULL AND team_id IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS notifications (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(64) NOT NULL,
    content TEXT NOT NULL,
    "read" BOOLEAN NOT NULL DEFAULT FALSE,
    "timestamp" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    actor_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    event_id BIGINT REFERENCES events(id) ON DELETE SET NULL,
    action VARCHAR(128) NOT NULL,
    target VARCHAR(255) NOT NULL,
    before JSONB,
    after JSONB,
    "timestamp" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT audit_logs_before_object CHECK (before IS NULL OR jsonb_typeof(before) = 'object'),
    CONSTRAINT audit_logs_after_object CHECK (after IS NULL OR jsonb_typeof(after) = 'object')
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_roles_tenant ON roles (tenant_id);
CREATE INDEX IF NOT EXISTS idx_users_tenant_role ON users (tenant_id, role_id);
CREATE INDEX IF NOT EXISTS idx_users_tenant_email ON users (tenant_id, email);
CREATE INDEX IF NOT EXISTS idx_events_tenant_status_window ON events (tenant_id, status, start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_challenges_event_category ON challenges (event_id, category);
CREATE INDEX IF NOT EXISTS idx_sub_challenges_challenge ON sub_challenges (challenge_id);
CREATE INDEX IF NOT EXISTS idx_hints_challenge_enabled ON hints (challenge_id, enabled);
CREATE INDEX IF NOT EXISTS idx_submissions_lookup ON submissions (event_id, user_id, challenge_id, "timestamp" DESC);
CREATE INDEX IF NOT EXISTS idx_submissions_result ON submissions (result);
CREATE INDEX IF NOT EXISTS idx_leaderboard_event_score ON leaderboard (event_id, score DESC, "timestamp" DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_user_read ON notifications (user_id, "read", "timestamp" DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_time ON audit_logs (actor_id, "timestamp" DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_event_time ON audit_logs (event_id, "timestamp" DESC);

-- Least-privilege grant model (application role gets DML only)
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO cerberus_app_rw;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO cerberus_app_rw;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO cerberus_app_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO cerberus_app_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO cerberus_app_rw;

COMMIT;
