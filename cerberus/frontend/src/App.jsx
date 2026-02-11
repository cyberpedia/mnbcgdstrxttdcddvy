import { Link, Navigate, Route, Routes } from 'react-router-dom';

import ThemeControls from './components/ThemeControls';
import { can } from './hooks/useRbac';
import { ThemeProvider } from './hooks/useTheme';
import AdminPanelPage from './pages/AdminPanelPage';
import ChallengePage from './pages/ChallengePage';
import GuestPreviewPage from './pages/GuestPreviewPage';
import LeaderboardPage from './pages/LeaderboardPage';
import NotificationCenterPage from './pages/NotificationCenterPage';
import ProfilePage from './pages/ProfilePage';

const NAV_ITEMS = [
  { to: '/challenges', label: 'Challenges', capability: 'view_leaderboard' },
  { to: '/leaderboard', label: 'Leaderboard', capability: 'view_leaderboard' },
  { to: '/profile', label: 'Profile', capability: 'submit_flags' },
  { to: '/notifications', label: 'Notifications', capability: 'send_notifications' },
  { to: '/admin', label: 'Admin', capability: 'manage_ui_config' },
  { to: '/guest-preview', label: 'Guest Preview', capability: 'submit_flags' }
];

function App() {
  const role = 'admin';
  const navItems = NAV_ITEMS.filter((item) => can(role, item.capability));

  { to: '/challenges', label: 'Challenges' },
  { to: '/leaderboard', label: 'Leaderboard' },
  { to: '/profile', label: 'Profile' },
  { to: '/notifications', label: 'Notifications' },
  { to: '/admin', label: 'Admin' },
  { to: '/guest-preview', label: 'Guest Preview' }
];

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-100" data-testid="app-shell">
        <a href="#main-content" className="sr-only focus:not-sr-only focus:p-2 focus:bg-sky-600 focus:text-white">
          Skip to content
        </a>
        <header className="border-b border-slate-300 dark:border-slate-700">
          <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 p-4">
            <h1 className="text-xl font-semibold">Cerberus Platform</h1>
            <ThemeControls />
          </div>
          <nav aria-label="Primary" className="mx-auto max-w-7xl px-4 pb-4">
            <ul className="flex flex-wrap gap-2">
              {navItems.map((item) => (
              {NAV_ITEMS.map((item) => (
                <li key={item.to}>
                  <Link
                    className="inline-block rounded-md border border-slate-400 px-3 py-1 text-sm hover:bg-slate-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-500 dark:border-slate-600 dark:hover:bg-slate-800"
                    to={item.to}
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </header>

        <main id="main-content" className="mx-auto max-w-7xl p-4">
          <Routes>
            <Route path="/" element={<Navigate to="/challenges" replace />} />
            <Route path="/challenges" element={<ChallengePage />} />
            <Route path="/leaderboard" element={<LeaderboardPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/notifications" element={<NotificationCenterPage />} />
            <Route path="/admin" element={<AdminPanelPage />} />
            <Route path="/guest-preview" element={<GuestPreviewPage />} />
          </Routes>
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;
