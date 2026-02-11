function AdminFeatureToggles({ flags, onChange }) {
  return (
    <section className="card" aria-label="Admin feature toggles">
      <h2 className="text-lg font-semibold">Feature Toggles</h2>
      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        {Object.entries(flags).map(([key, value]) => (
          <label key={key} className="flex items-center justify-between gap-2 rounded border border-slate-300 p-2 dark:border-slate-700">
            <span className="text-sm">{key}</span>
            <input type="checkbox" checked={value} onChange={(event) => onChange(key, event.target.checked)} />
          </label>
        ))}
      </div>
    </section>
  );
}

export default AdminFeatureToggles;
