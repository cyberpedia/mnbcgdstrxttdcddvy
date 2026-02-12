import { apiRequest } from './http';

export function getLeaderboard(eventId) {
  return apiRequest(`/leaderboard/${eventId}`);
}
