function GuestPreviewPage() {
  return (
    <section className="card space-y-3" aria-labelledby="guest-preview-title">
      <h2 id="guest-preview-title" className="text-xl font-semibold">
        Guest Challenge Preview
      </h2>
      <p className="text-sm">
        Explore challenge descriptions and categories before registering. Submissions are disabled for guests.
      </p>
      <button type="button" className="rounded bg-emerald-600 px-3 py-2 text-sm text-white hover:bg-emerald-700">
        Register to start solving
      </button>
    </section>
  );
}

export default GuestPreviewPage;
