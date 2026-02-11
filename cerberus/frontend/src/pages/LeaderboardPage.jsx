import { useMemo, useState } from 'react';

import LeaderboardTable from '../components/LeaderboardTable';

const rowsSeed = [
  { name: 'alice', score: 420, role: 'user', category: 'web', timeline: 'T1' },
  { name: 'bob', score: 390, role: 'event_admin', category: 'crypto', timeline: 'T1' },
  { name: 'charlie', score: 300, role: 'challenge_author', category: 'web', timeline: 'T2' }
];

function LeaderboardPage() {
  const [view, setView] = useState('timeline');
  const [roleFilter, setRoleFilter] = useState('all');

  const filtered = useMemo(() => {
    return rowsSeed.filter((row) => (roleFilter === 'all' ? true : row.role === roleFilter));
  }, [roleFilter]);

  const grouped = useMemo(() => {
    if (view === 'category') {
      return [...filtered].sort((a, b) => a.category.localeCompare(b.category));
    }
    return [...filtered].sort((a, b) => b.score - a.score);
  }, [filtered, view]);

  return (
    <section className="space-y-4">
      <div className="card flex flex-wrap items-end gap-3">
        <label className="text-sm" htmlFor="leaderboard-view">
          View
        </label>
        <select
          id="leaderboard-view"
          className="rounded border border-slate-300 p-2 text-sm dark:border-slate-700 dark:bg-slate-900"
          value={view}
          onChange={(event) => setView(event.target.value)}
        >
          <option value="timeline">Timeline</option>
          <option value="category">Category</option>
        </select>

        <label className="text-sm" htmlFor="role-filter">
          Role filter
        </label>
        <select
          id="role-filter"
          className="rounded border border-slate-300 p-2 text-sm dark:border-slate-700 dark:bg-slate-900"
          value={roleFilter}
          onChange={(event) => setRoleFilter(event.target.value)}
        >
          <option value="all">All</option>
          <option value="user">User</option>
          <option value="event_admin">Event Admin</option>
          <option value="challenge_author">Challenge Author</option>
        </select>
      </div>

      <LeaderboardTable rows={grouped} title={`Leaderboard (${view})`} />
    </section>
  );
}

export default LeaderboardPage;
