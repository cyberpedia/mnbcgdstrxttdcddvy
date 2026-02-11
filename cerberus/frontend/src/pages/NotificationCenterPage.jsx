import { useState } from 'react';

import NotificationCenter from '../components/NotificationCenter';

const initialData = [
  { id: 1, type: 'event', content: 'Event freeze starts in 30 minutes.', read: false },
  { id: 2, type: 'hint', content: 'A new hint was enabled for Web Warmup.', read: false }
];

function NotificationCenterPage() {
  const [notifications, setNotifications] = useState(initialData);

  const markRead = (id) => {
    setNotifications((current) => current.map((n) => (n.id === id ? { ...n, read: true } : n)));
  };

  return <NotificationCenter notifications={notifications} markRead={markRead} />;
}

export default NotificationCenterPage;
