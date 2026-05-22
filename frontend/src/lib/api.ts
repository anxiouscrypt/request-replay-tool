import type { RequestRecord } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`Request failed with ${response.status}`)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export function listRequests() {
  return request<RequestRecord[]>('/requests')
}

export function getRequest(requestId: string) {
  return request<RequestRecord>(`/requests/${requestId}`)
}

export function replayRequest(requestId: string) {
  return request<RequestRecord>(`/requests/${requestId}/replay`, {
    method: 'POST',
  })
}

export function replayRequestWithEdits(requestId: string, requestBody: unknown) {
  return request<RequestRecord>(`/requests/${requestId}/replay-with-edits`, {
    body: JSON.stringify({ requestBody }),
    method: 'POST',
  })
}

export function clearRequests() {
  return request<void>('/requests', { method: 'DELETE' })
}
