import { apiRequest, setSessionTokens } from './http';

export async function login(username, password) {
  const payload = await apiRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  });
  setSessionTokens(payload);
  return payload;
}

export async function refresh(refreshToken) {
  const payload = await apiRequest('/auth/refresh', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  setSessionTokens(payload);
  return payload;
}
