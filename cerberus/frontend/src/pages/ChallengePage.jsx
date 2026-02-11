import { useMemo, useState } from 'react';

import ChallengeList from '../components/ChallengeList';
import HintPanel from '../components/HintPanel';
import MultiPartChallenge from '../components/MultiPartChallenge';
import SolversDisplay from '../components/SolversDisplay';
import { submitFlag, toggleHint } from '../services/challengeService';

const challengeSeed = [
  {
    id: 1,
    title: 'Web Warmup',
    category: 'web',
    difficulty: 'easy',
    locked: false,
    parts: [
      { id: 11, order: 1, title: 'Find endpoint' },
      { id: 12, order: 2, title: 'Exploit misconfig' }
    ],
    hints: [
      { id: 101, content: 'Check robots.txt', penalty: 10, enabled: false },
      { id: 102, content: 'Try case-sensitive paths', penalty: 20, enabled: false }
    ],
    solvers: [
      { userId: 1, name: 'alice' },
      { userId: 2, name: 'bob' }
    ]
  },
  {
    id: 2,
    title: 'API Chain',
    category: 'api',
    difficulty: 'medium',
    locked: true,
    parts: [{ id: 21, order: 1, title: 'JWT claims' }],
    hints: [{ id: 201, content: 'Look at refresh endpoint', penalty: 25, enabled: false }],
    solvers: []
  }
];

function ChallengePage() {
  const [selectedChallengeId, setSelectedChallengeId] = useState(1);
  const [selectedPartId, setSelectedPartId] = useState(11);
  const [showSolvers, setShowSolvers] = useState(true);
  const [feedback, setFeedback] = useState('');
  const [flagInput, setFlagInput] = useState('');
  const [challenges, setChallenges] = useState(challengeSeed);

  const selectedChallenge = useMemo(
    () => challenges.find((entry) => entry.id === selectedChallengeId),
    [challenges, selectedChallengeId]
  );

  const onToggleHint = async (hintId, enabled) => {
    if (!selectedChallenge) return;
    setChallenges((current) =>
      current.map((entry) =>
        entry.id === selectedChallenge.id
          ? {
              ...entry,
              hints: entry.hints.map((hint) => (hint.id === hintId ? { ...hint, enabled } : hint))
            }
          : entry
      )
    );
    try {
      await toggleHint(hintId, enabled);
    } catch (_error) {
      setFeedback('Could not sync hint toggle with backend yet.');
    }
  };

  const onSubmitFlag = async (event) => {
    event.preventDefault();
    if (!selectedChallenge) return;

    try {
      const result = await submitFlag(1, selectedChallenge.id, flagInput, selectedPartId);
      setFeedback(`Submission result: ${result.result}`);
      setFlagInput('');
    } catch (error) {
      setFeedback(error.message);
    }
  };

  return (
    <div className="grid gap-4 lg:grid-cols-3">
      <div className="space-y-4">
        <ChallengeList
          challenges={challenges}
          selectedId={selectedChallengeId}
          onSelect={(id) => {
            setSelectedChallengeId(id);
            const next = challenges.find((entry) => entry.id === id);
            if (next?.parts[0]) setSelectedPartId(next.parts[0].id);
          }}
        />
        <label className="card flex items-center justify-between" htmlFor="show-solvers">
          <span className="text-sm">Display solver names</span>
          <input
            id="show-solvers"
            type="checkbox"
            checked={showSolvers}
            onChange={(event) => setShowSolvers(event.target.checked)}
          />
        </label>
      </div>

      <div className="space-y-4">
        <MultiPartChallenge
          challenge={selectedChallenge}
          selectedPartId={selectedPartId}
          onSelectPart={setSelectedPartId}
        />
        <form className="card" onSubmit={onSubmitFlag}>
          <label className="block text-sm" htmlFor="flag-input">
            Submit flag
          </label>
          <input
            id="flag-input"
            className="mt-1 w-full rounded border border-slate-300 bg-white p-2 text-sm dark:border-slate-700 dark:bg-slate-900"
            value={flagInput}
            onChange={(event) => setFlagInput(event.target.value)}
            maxLength={256}
            autoComplete="off"
            required
          />
          <button type="submit" className="mt-3 rounded bg-sky-600 px-3 py-2 text-sm text-white hover:bg-sky-700">
            Submit
          </button>
          <p aria-live="polite" className="mt-2 text-sm">
            {feedback}
          </p>
        </form>
      </div>

      <div className="space-y-4">
        <HintPanel hints={selectedChallenge?.hints || []} onToggleHint={onToggleHint} canRevealHints />
        <SolversDisplay showSolvers={showSolvers} solvers={selectedChallenge?.solvers || []} />
      </div>
    </div>
  );
}

export default ChallengePage;
