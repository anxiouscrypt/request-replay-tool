export type RequestRecord = {
  id: string
  method: string
  path: string
  targetUrl: string
  requestHeaders: Record<string, string>
  requestBody: unknown
  responseStatus: number
  responseBody: unknown
  durationMs: number
  createdAt: string
}
