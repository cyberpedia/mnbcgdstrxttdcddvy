# Frontend Source

Phase 4 frontend implementation using React + TailwindCSS.

## Key modules

- `components/`: Theme controls, challenge widgets, leaderboard table, notification center, admin toggles.
- `pages/`: Challenge, leaderboard, profile, notifications, admin panel, guest preview.
- `services/`: Backend API clients for auth/challenges/leaderboard/notifications/ui-config.
- `hooks/`: Theme state and keyboard accessibility helpers.
- `assets/`: Tailwind/global styles.

## Security notes

- No backend secrets are exposed in JavaScript.
- API requests include CSRF token headers only after login.
- Text rendering avoids raw HTML injection patterns.
- `components/`: Reusable UI components.
- `pages/`: Route-level page components.
- `services/`: API clients and integration logic.
- `hooks/`: Shared React hooks.
- `assets/`: Static assets.
