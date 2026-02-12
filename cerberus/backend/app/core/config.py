from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cerberus API"
    app_env: str = "development"
    app_debug: bool = True
    enforce_https: bool = True
    trust_proxy_headers: bool = True

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 15
    refresh_token_exp_minutes: int = 60 * 24 * 7
    csrf_secret: str = "change-csrf-secret"

    evidence_lock_mode: bool = False
    admin_confirmation_phrase: str = "CONFIRM-DESTRUCTIVE"

    rate_limit_per_minute_ip: int = 120
    rate_limit_per_minute_user: int = 300
    rate_limit_per_minute_team: int = 240

    tls_min_version: str = "TLSv1.2"
    tls_ciphers: str = "ECDHE+AESGCM:ECDHE+CHACHA20"

    signing_secret: str = "change-signing-secret"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
