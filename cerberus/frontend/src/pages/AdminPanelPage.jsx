import { useState } from 'react';

import AdminFeatureToggles from '../components/AdminFeatureToggles';
import { can } from '../hooks/useRbac';
import { deleteChallenge } from '../services/challengeService';

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
  const [role] = useState('admin');
  const [dangerStatus, setDangerStatus] = useState('');

  const onChange = (key, value) => {
    setFlags((current) => ({ ...current, [key]: value }));
  };

  const onDeleteChallenge = async () => {
    if (!can(role, 'manage_challenges')) {
      setDangerStatus('You are not allowed to run destructive operations.');
      return;
    }
    const confirmation = window.prompt('Type CONFIRM-DESTRUCTIVE to delete challenge 1');
    if (confirmation !== 'CONFIRM-DESTRUCTIVE') {
      setDangerStatus('Deletion cancelled: confirmation phrase mismatch.');
      return;
    }
    try {
      await deleteChallenge(1, confirmation);
      setDangerStatus('Challenge delete request sent successfully.');
    } catch (error) {
      setDangerStatus(error.message);
    }
  };

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-semibold">Admin Panel</h2>
      <p className="text-sm">Role-aware controls should be backed by RBAC claims from backend auth.</p>
      <AdminFeatureToggles flags={flags} onChange={onChange} />
      <div className="card">
        <h3 className="font-semibold">Destructive operations</h3>
        <p className="mt-1 text-sm">Requires explicit admin confirmation phrase.</p>
        <button
          type="button"
          onClick={onDeleteChallenge}
          className="mt-3 rounded bg-rose-700 px-3 py-2 text-sm text-white hover:bg-rose-800"
        >
          Delete Challenge #1
        </button>
        <p aria-live="polite" className="mt-2 text-sm">{dangerStatus}</p>
      </div>
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
