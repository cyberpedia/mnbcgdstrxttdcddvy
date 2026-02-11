import { useRef, useState } from 'react';

import useKeyboardNav from '../hooks/useKeyboardNav';

function ChallengeList({ challenges, selectedId, onSelect }) {
  const ref = useRef(null);
  const [announce, setAnnounce] = useState('');

  useKeyboardNav(ref, (id) => {
    onSelect(Number(id));
    const challenge = challenges.find((entry) => entry.id === Number(id));
    setAnnounce(challenge ? `Selected ${challenge.title}` : 'Selected challenge');
  });

  return (
    <section className="card">
      <h2 className="mb-3 text-lg font-semibold">Challenges</h2>
      <p aria-live="polite" className="sr-only">
        {announce}
      </p>
      <ul ref={ref} className="space-y-2" role="listbox" aria-label="Challenge list">
        {challenges.map((challenge) => {
          const locked = challenge.locked;
          return (
            <li key={challenge.id}>
              <button
                type="button"
                className={`w-full rounded border px-3 py-2 text-left ${
                  selectedId === challenge.id ? 'border-sky-500 bg-sky-100 dark:bg-sky-950' : 'border-slate-300 dark:border-slate-700'
                } ${locked ? 'opacity-60' : ''}`}
                onClick={() => onSelect(challenge.id)}
                disabled={locked}
                aria-disabled={locked}
                aria-label={`${challenge.title}${locked ? ' locked' : ''}`}
                data-key={challenge.id}
              >
                <div className="flex items-center justify-between gap-2">
                  <span>{challenge.title}</span>
                  <span className="text-xs uppercase">{challenge.category}</span>
                </div>
                {locked ? <p className="text-xs">Complete prerequisite challenge first.</p> : null}
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

export default ChallengeList;
