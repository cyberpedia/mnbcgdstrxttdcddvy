import { apiRequest } from './http';

export function createChallenge(payload) {
  return apiRequest('/challenges', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function updateChallenge(id, payload) {
  return apiRequest(`/challenges/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  });
}

export function createSubChallenge(challengeId, payload) {
  return apiRequest(`/challenges/${challengeId}/sub-challenges`, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function addHint(challengeId, payload) {
  return apiRequest(`/challenges/${challengeId}/hints`, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export function toggleHint(hintId, enabled) {
  return apiRequest(`/challenges/hints/${hintId}/toggle?enabled=${enabled ? 'true' : 'false'}`, {
    method: 'POST'
  });
}

export function submitFlag(eventId, challengeId, flag, subChallengeId) {
  const params = new URLSearchParams({
    event_id: String(eventId),
    challenge_id: String(challengeId),
    flag,
    ...(subChallengeId ? { sub_challenge_id: String(subChallengeId) } : {})
  });
  return apiRequest(`/leaderboard/submit?${params.toString()}`, { method: 'POST' });
}
