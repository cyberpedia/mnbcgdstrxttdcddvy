import { apiRequest } from './http';

export function getUiConfig() {
  return apiRequest('/ui-config');
}

export function setUiConfig(payload) {
  return apiRequest('/ui-config', {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
}
