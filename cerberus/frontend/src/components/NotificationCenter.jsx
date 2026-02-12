function NotificationCenter({ notifications, markRead }) {
  return (
    <section className="card" aria-labelledby="notifications-heading">
      <h2 id="notifications-heading" className="text-lg font-semibold">
        Notification Center
      </h2>
      <ul className="mt-2 space-y-2">
        {notifications.map((item) => (
          <li key={item.id} className="rounded border border-slate-300 p-3 dark:border-slate-700">
            <p className="font-medium">{item.type}</p>
            <p className="text-sm">{item.content}</p>
            <button
              type="button"
              className="mt-2 rounded border border-slate-400 px-2 py-1 text-xs"
              onClick={() => markRead(item.id)}
              disabled={item.read}
            >
              {item.read ? 'Read' : 'Mark as read'}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default NotificationCenter;
