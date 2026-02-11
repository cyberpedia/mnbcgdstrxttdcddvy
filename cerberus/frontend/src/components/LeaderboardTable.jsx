function LeaderboardTable({ rows, title }) {
  return (
    <section className="card" aria-label={title}>
      <h3 className="mb-3 text-lg font-semibold">{title}</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse" role="table">
          <caption className="sr-only">{title}</caption>
          <thead>
            <tr className="border-b border-slate-300 dark:border-slate-700">
              <th className="px-2 py-1 text-left">Rank</th>
              <th className="px-2 py-1 text-left">Name</th>
              <th className="px-2 py-1 text-left">Score</th>
              <th className="px-2 py-1 text-left">Role</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={`${row.name}-${index}`}>
                <td className="px-2 py-1">{index + 1}</td>
                <td className="px-2 py-1">{row.name}</td>
                <td className="px-2 py-1">{row.score}</td>
                <td className="px-2 py-1">{row.role}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default LeaderboardTable;
