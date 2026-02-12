import { apiRequest } from './http';

export function sendNotification(payload) {
  return apiRequest('/notifications/ws-send', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function sendEmail(payload) {
  return apiRequest('/notifications/email', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function connectNotificationSocket(userId, onMessage) {
  const url = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://localhost:8000/notifications/ws/${userId}`;
  const socket = new WebSocket(url);
  socket.onmessage = (event) => {
    const parsed = JSON.parse(event.data);
    onMessage(parsed);
  };
  return socket;
}
