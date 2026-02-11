function MultiPartChallenge({ challenge, selectedPartId, onSelectPart }) {
  if (!challenge) {
    return <p>Select a challenge to view details.</p>;
  }

  return (
    <section className="card" aria-labelledby="challenge-title">
      <h2 id="challenge-title" className="text-lg font-semibold">
        {challenge.title}
      </h2>
      <p className="text-sm text-slate-600 dark:text-slate-300">Difficulty: {challenge.difficulty}</p>

      <h3 className="mt-4 font-medium">Multi-part questions</h3>
      <ul className="mt-2 space-y-2">
        {challenge.parts.map((part) => (
          <li key={part.id}>
            <button
              type="button"
              className={`w-full rounded border px-3 py-2 text-left ${selectedPartId === part.id ? 'border-sky-500' : 'border-slate-300 dark:border-slate-700'}`}
              onClick={() => onSelectPart(part.id)}
            >
              Part {part.order}: {part.title}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default MultiPartChallenge;
