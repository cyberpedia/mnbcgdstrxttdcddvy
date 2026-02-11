import { useState } from 'react';

import { useTheme } from '../hooks/useTheme';

function ProfilePage() {
  const { brand, setBrand } = useTheme();
  const [tutorialReplay, setTutorialReplay] = useState(false);
  const [avatarUrl, setAvatarUrl] = useState('https://cdn.example.com/avatar.png');

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-semibold">Profile</h2>

      <div className="card space-y-3">
        <label className="block text-sm" htmlFor="avatar-url">
          Avatar URL
        </label>
        <input
          id="avatar-url"
          value={avatarUrl}
          onChange={(event) => setAvatarUrl(event.target.value)}
          className="w-full rounded border border-slate-300 p-2 text-sm dark:border-slate-700 dark:bg-slate-900"
        />

        <label className="block text-sm" htmlFor="logo-url">
          Custom logo URL
        </label>
        <input
          id="logo-url"
          value={brand.logo}
          onChange={(event) => setBrand({ ...brand, logo: event.target.value })}
          className="w-full rounded border border-slate-300 p-2 text-sm dark:border-slate-700 dark:bg-slate-900"
        />

        <label className="flex items-center gap-2 text-sm" htmlFor="tutorial-replay">
          <input
            id="tutorial-replay"
            type="checkbox"
            checked={tutorialReplay}
            onChange={(event) => setTutorialReplay(event.target.checked)}
          />
          Replay tutorial on next login
        </label>
      </div>
    </section>
  );
}

export default ProfilePage;
