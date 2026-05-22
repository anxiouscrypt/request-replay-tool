import type { RequestRecord } from '../lib/types'
import { JsonViewer } from './JsonViewer'
import { ReplayPanel } from './ReplayPanel'

type RequestDetailProps = {
  request: RequestRecord | null
  onReplay: () => void
  onReplayWithEdits: (body: unknown) => void
}

export function RequestDetail({
  request,
  onReplay,
  onReplayWithEdits,
}: RequestDetailProps) {
  if (!request) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <p className="text-sm text-slate-500">Select a captured request to inspect it.</p>
      </section>
    )
  }

  return (
    <div className="space-y-4">
      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-4 py-3">
          <h2 className="text-base font-semibold">Request detail</h2>
          <p className="mt-1 font-mono text-xs text-slate-500">{request.targetUrl}</p>
        </div>
        <div className="space-y-4 p-4">
          <div className="grid gap-3 text-sm sm:grid-cols-3">
            <div>
              <p className="text-slate-500">Method</p>
              <p className="font-mono font-semibold">{request.method}</p>
            </div>
            <div>
              <p className="text-slate-500">Status</p>
              <p className="font-semibold">{request.responseStatus}</p>
            </div>
            <div>
              <p className="text-slate-500">Duration</p>
              <p className="font-semibold">{request.durationMs}ms</p>
            </div>
          </div>
          <JsonViewer label="Request headers" value={request.requestHeaders} />
          <JsonViewer label="Request body" value={request.requestBody} />
          <JsonViewer label="Response body" value={request.responseBody} />
        </div>
      </section>
      <ReplayPanel
        request={request}
        onReplay={onReplay}
        onReplayWithEdits={onReplayWithEdits}
      />
    </div>
  )
}
