function SolversDisplay({ showSolvers, solvers }) {
  if (!showSolvers) {
    return <p className="text-sm">Solver visibility disabled by admin config.</p>;
  }

  return (
    <section className="card" aria-label="Solvers display">
      <h3 className="text-lg font-semibold">Solvers</h3>
      <ul className="mt-2 list-disc pl-6 text-sm">
        {solvers.map((solver) => (
          <li key={solver.userId}>{solver.name}</li>
        ))}
      </ul>
    </section>
  );
}

export default SolversDisplay;
