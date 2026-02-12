# Cerberus User Guide

> Version: Phase 7

## 1. Getting Started

### 1.1 Register an account
1. Open the Cerberus web app.
2. Select **Register**.
3. Enter:
   - username
   - email
   - strong password (12+ chars)
4. Confirm your email if email verification is enabled by admins.

### 1.2 Log in
1. Go to **Login**.
2. Enter username + password.
3. Cerberus issues access + refresh tokens.
4. Session security:
   - CSRF token is attached for mutating actions.
   - Session expires automatically.

## 2. Challenge Workflow

### 2.1 Challenge browser
- Navigate to **Challenges**.
- Filter by category/difficulty/event (if enabled).
- Locked challenges show dependency state.

### 2.2 Multi-part challenges
- Some challenges have ordered parts.
- Select a part before submitting a flag.
- Complete prerequisites to unlock dependent parts.

### 2.3 Hints and penalties
- If hints are enabled, you can reveal them.
- Each hint may apply a score penalty.
- Penalties affect leaderboard ranking immediately after recalculation.

### 2.4 Submissions
- Enter flag in the challenge page.
- Possible outcomes:
  - `correct`
  - `incorrect`
  - `duplicate`
  - `error`

## 3. Leaderboard

### 3.1 Views
- Timeline view: rank progression over time.
- Category view: rank by category scoring.
- Role-filtered views may be available depending on permissions.

### 3.2 Team and user modes
- Some events use team scoring.
- Others use user-only scoring.

## 4. Profile

### 4.1 Profile settings
- Avatar/profile assets.
- Theme preference (light/dark/system).
- Optional tutorial replay toggle.

### 4.2 Notifications
- Open **Notification Center** to review event notices and challenge updates.
- Mark notifications as read when completed.

## 5. Guest Preview

If guest preview is enabled:
- Unauthenticated users can browse challenge metadata.
- Solving/submission requires registration.
