function HintPanel({ hints, onToggleHint, canRevealHints }) {
  return (
    <section className="card" aria-labelledby="hints-heading">
      <h3 id="hints-heading" className="text-lg font-semibold">
        Hints
      </h3>
      <ul className="mt-2 space-y-2">
        {hints.map((hint) => (
          <li key={hint.id} className="rounded border border-slate-300 p-3 dark:border-slate-700">
            <div className="flex items-center justify-between gap-2">
              <p className="text-sm">Penalty: {hint.penalty}</p>
              {canRevealHints ? (
                <button
                  type="button"
                  onClick={() => onToggleHint(hint.id, !hint.enabled)}
                  className="rounded border border-slate-400 px-2 py-1 text-xs"
                >
                  {hint.enabled ? 'Disable' : 'Enable'}
                </button>
              ) : null}
            </div>
            {hint.enabled ? <p className="mt-2 text-sm">{hint.content}</p> : <p className="mt-2 text-xs">Hint hidden</p>}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default HintPanel;
