#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "[!] Run as root (or via sudo)." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

CERBERUS_USER="cerberus"
CERBERUS_GROUP="cerberus"
CERBERUS_HOME="/opt/cerberus"
ENV_FILE="${CERBERUS_HOME}/.env"
DB_NAME="${CERBERUS_DB_NAME:-cerberus}"
DB_USER="${CERBERUS_DB_USER:-cerberus_app}"
DB_PASSWORD="${CERBERUS_DB_PASSWORD:-$(openssl rand -base64 24 | tr -d '\n')}"
TIMEZONE="${CERBERUS_TIMEZONE:-UTC}"
LOCALE_VALUE="${CERBERUS_LOCALE:-en_US.UTF-8}"

log() {
  printf '\n[%s] %s\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$*"
}

install_base_packages() {
  log "Updating apt metadata and applying latest patches"
  apt-get update
  apt-get -y upgrade

  log "Installing baseline security and utility packages"
  apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    ufw \
    fail2ban \
    chrony \
    locales \
    postgresql \
    postgresql-contrib \
    redis-server \
    unattended-upgrades
}

configure_time_locale_ntp() {
  log "Configuring timezone, locale, and NTP"
  timedatectl set-timezone "${TIMEZONE}"

  if ! locale -a | grep -qx "${LOCALE_VALUE}"; then
    sed -i "s/^# *${LOCALE_VALUE}/${LOCALE_VALUE}/" /etc/locale.gen || true
    grep -q "^${LOCALE_VALUE} UTF-8$" /etc/locale.gen || echo "${LOCALE_VALUE} UTF-8" >> /etc/locale.gen
    locale-gen
  fi

  update-locale LANG="${LOCALE_VALUE}" LC_ALL="${LOCALE_VALUE}"

  systemctl enable --now chrony
}

configure_firewall() {
  log "Configuring UFW firewall"
  ufw --force reset
  ufw default deny incoming
  ufw default allow outgoing
  ufw allow OpenSSH
  ufw allow 80/tcp
  ufw allow 443/tcp
  ufw --force enable
  ufw status verbose
}

install_docker() {
  log "Installing Docker Engine + Docker Compose plugin"
  install -m 0755 -d /etc/apt/keyrings
  if [[ ! -f /etc/apt/keyrings/docker.gpg ]]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
  fi

  local arch
  arch="$(dpkg --print-architecture)"
  local codename
  codename="$(. /etc/os-release && echo "${VERSION_CODENAME}")"
  cat > /etc/apt/sources.list.d/docker.list <<DOCKER_REPO
deb [arch=${arch} signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${codename} stable
DOCKER_REPO

  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

  systemctl enable --now docker
}

configure_postgres() {
  log "Configuring PostgreSQL role and database"
  systemctl enable --now postgresql

  sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASSWORD}' NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;"

  sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

  PG_HBA="/etc/postgresql/$(psql -V | awk '{print $3}' | cut -d. -f1,2)/main/pg_hba.conf"
  if [[ -f "${PG_HBA}" ]] && ! grep -q "^local\s\+${DB_NAME}\s\+${DB_USER}\s\+scram-sha-256" "${PG_HBA}"; then
    echo "local   ${DB_NAME}   ${DB_USER}   scram-sha-256" >> "${PG_HBA}"
    systemctl restart postgresql
  fi
}

configure_redis() {
  log "Hardening Redis for local-only access"
  local redis_conf="/etc/redis/redis.conf"
  sed -i 's/^supervised .*/supervised systemd/' "${redis_conf}"
  sed -i 's/^bind .*/bind 127.0.0.1 ::1/' "${redis_conf}"
  sed -i 's/^protected-mode .*/protected-mode yes/' "${redis_conf}"
  systemctl enable --now redis-server
  systemctl restart redis-server
}

configure_fail2ban() {
  log "Configuring fail2ban for SSH protection"
  cat > /etc/fail2ban/jail.d/sshd.local <<'JAIL'
[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = systemd
maxretry = 5
findtime = 10m
bantime = 1h
ignoreip = 127.0.0.1/8 ::1
JAIL

  systemctl enable --now fail2ban
  systemctl restart fail2ban
}

configure_users_and_paths() {
  log "Creating least-privilege service user and directory layout"
  getent group "${CERBERUS_GROUP}" >/dev/null || groupadd --system "${CERBERUS_GROUP}"

  if ! id -u "${CERBERUS_USER}" >/dev/null 2>&1; then
    useradd \
      --system \
      --gid "${CERBERUS_GROUP}" \
      --home-dir "${CERBERUS_HOME}" \
      --create-home \
      --shell /usr/sbin/nologin \
      "${CERBERUS_USER}"
  fi

  usermod -aG docker "${CERBERUS_USER}"

  install -d -m 0750 -o "${CERBERUS_USER}" -g "${CERBERUS_GROUP}" "${CERBERUS_HOME}"
  install -d -m 0750 -o "${CERBERUS_USER}" -g "${CERBERUS_GROUP}" "${CERBERUS_HOME}/logs"

  umask 027
  cat > "${ENV_FILE}" <<ENVVARS
CERBERUS_DB_NAME=${DB_NAME}
CERBERUS_DB_USER=${DB_USER}
CERBERUS_DB_PASSWORD=${DB_PASSWORD}
CERBERUS_TIMEZONE=${TIMEZONE}
ENVVARS
  chown "${CERBERUS_USER}:${CERBERUS_GROUP}" "${ENV_FILE}"
  chmod 0640 "${ENV_FILE}"
}

configure_unattended_upgrades() {
  log "Enabling unattended security upgrades"
  dpkg-reconfigure -f noninteractive unattended-upgrades
}

install_systemd_units() {
  log "Installing Cerberus systemd units"
  install -m 0644 "$(dirname "$0")/../systemd/cerberus-deploy.service" /etc/systemd/system/cerberus-deploy.service
  install -m 0755 "$(dirname "$0")/deploy-cerberus.sh" /usr/local/bin/deploy-cerberus.sh
  systemctl daemon-reload
  systemctl enable cerberus-deploy.service
}

main() {
  install_base_packages
  configure_time_locale_ntp
  configure_firewall
  install_docker
  configure_postgres
  configure_redis
  configure_fail2ban
  configure_users_and_paths
  configure_unattended_upgrades
  install_systemd_units

  log "Phase 0 bootstrap complete"
  log "DB password stored in ${ENV_FILE}"
}

main "$@"
