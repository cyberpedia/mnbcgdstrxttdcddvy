const ROLE_CAPABILITIES = {
  super_admin: ['*'],
  admin: ['manage_events', 'manage_challenges', 'manage_hints', 'send_notifications', 'manage_ui_config'],
  event_admin: ['manage_events', 'manage_challenges', 'manage_hints'],
  challenge_author: ['manage_challenges', 'manage_hints'],
  infra_admin: ['manage_ui_config', 'manage_notifications'],
  user: ['submit_flags', 'view_leaderboard']
};

export function can(role, capability) {
  const caps = ROLE_CAPABILITIES[role] || [];
  return caps.includes('*') || caps.includes(capability);
}
