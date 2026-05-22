import { useEffect, useState } from 'react'
import { RefreshCw, Trash2 } from 'lucide-react'
import { RequestDetail } from './components/RequestDetail'
import { RequestTable } from './components/RequestTable'
import {
  clearRequests,
  listRequests,
  replayRequest,
  replayRequestWithEdits,
} from './lib/api'
import type { RequestRecord } from './lib/types'

function App() {
  const [requests, setRequests] = useState<RequestRecord[]>([])
  const [selectedRequest, setSelectedRequest] = useState<RequestRecord | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    void refresh()
  }, [])

  async function refresh() {
    try {
      const nextRequests = await listRequests()
      setRequests(nextRequests)
      setSelectedRequest((current) => {
        if (!current) {
          return null
        }
        return nextRequests.find((request) => request.id === current.id) ?? current
      })
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load requests')
    }
  }

  async function clear() {
    await clearRequests()
    setSelectedRequest(null)
    await refresh()
  }

  async function replayOriginal() {
    if (!selectedRequest) {
      return
    }

    const replayed = await replayRequest(selectedRequest.id)
    await refresh()
    setSelectedRequest(replayed)
  }

  async function replayEdited(body: unknown) {
    if (!selectedRequest) {
      return
    }

    const replayed = await replayRequestWithEdits(selectedRequest.id, body)
    await refresh()
    setSelectedRequest(replayed)
  }

  return (
    <main className="min-h-screen bg-[#f4f5f7] px-4 py-5 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-5 flex flex-col gap-3 border-b border-slate-200 pb-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-medium text-indigo-700">Request Replay Tool</p>
            <h1 className="text-2xl font-semibold text-slate-950">
              Capture, inspect, and replay API requests
            </h1>
          </div>
          <div className="flex gap-2">
            <button
              className="inline-flex h-10 items-center gap-2 rounded-md border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
              onClick={() => void refresh()}
              type="button"
            >
              <RefreshCw className="h-4 w-4" />
              Refresh
            </button>
            <button
              className="inline-flex h-10 items-center gap-2 rounded-md bg-slate-950 px-3 text-sm font-medium text-white hover:bg-slate-800"
              onClick={() => void clear()}
              type="button"
            >
              <Trash2 className="h-4 w-4" />
              Clear
            </button>
          </div>
        </header>
        {error && <p className="mb-4 text-sm text-rose-700">{error}</p>}
        <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_420px]">
          <div className="rounded-lg border border-slate-200 bg-white">
            <RequestTable
              onSelect={setSelectedRequest}
              requests={requests}
              selectedId={selectedRequest?.id ?? null}
            />
          </div>
          <RequestDetail
            request={selectedRequest}
            onReplay={() => void replayOriginal()}
            onReplayWithEdits={(body) => void replayEdited(body)}
          />
        </div>
      </div>
    </main>
  )
}

export default App
