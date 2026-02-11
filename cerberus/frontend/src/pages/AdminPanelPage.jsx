import { useState } from 'react';

import AdminFeatureToggles from '../components/AdminFeatureToggles';

const initialFlags = {
  guestPreview: true,
  showSolvers: true,
  hintsEnabledByDefault: false,
  allowThemeCustomization: true,
  notificationsEnabled: true
};

function AdminPanelPage() {
  const [flags, setFlags] = useState(initialFlags);
  const [content, setContent] = useState('Welcome to Cerberus CTF event portal!');

  const onChange = (key, value) => {
    setFlags((current) => ({ ...current, [key]: value }));
  };

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-semibold">Admin Panel</h2>
      <p className="text-sm">Role-aware controls should be backed by RBAC claims from backend auth.</p>
      <AdminFeatureToggles flags={flags} onChange={onChange} />
      <div className="card">
        <label className="block text-sm" htmlFor="dynamic-content">
          Dynamic home content
        </label>
        <textarea
          id="dynamic-content"
          className="mt-1 h-28 w-full rounded border border-slate-300 p-2 text-sm dark:border-slate-700 dark:bg-slate-900"
          value={content}
          onChange={(event) => setContent(event.target.value)}
          maxLength={1000}
        />
      </div>
    </section>
  );
}

export default AdminPanelPage;
