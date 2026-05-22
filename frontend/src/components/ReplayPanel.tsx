import { useEffect, useState } from 'react'
import { Play } from 'lucide-react'
import type { RequestRecord } from '../lib/types'

type ReplayPanelProps = {
  request: RequestRecord
  onReplay: () => void
  onReplayWithEdits: (body: unknown) => void
}

export function ReplayPanel({
  request,
  onReplay,
  onReplayWithEdits,
}: ReplayPanelProps) {
  const [bodyText, setBodyText] = useState(JSON.stringify(request.requestBody, null, 2))
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setBodyText(JSON.stringify(request.requestBody, null, 2))
    setError(null)
  }, [request])

  function submitEditedReplay() {
    try {
      const parsed = bodyText.trim() ? JSON.parse(bodyText) : null
      setError(null)
      onReplayWithEdits(parsed)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid JSON')
    }
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-4 py-3">
        <h2 className="text-base font-semibold">Replay</h2>
      </div>
      <div className="space-y-3 p-4">
        <button
          className="inline-flex h-10 items-center gap-2 rounded-md bg-slate-950 px-3 text-sm font-medium text-white hover:bg-slate-800"
          onClick={onReplay}
          type="button"
        >
          <Play className="h-4 w-4" />
          Replay original
        </button>
        <div>
          <p className="mb-1 text-sm font-medium">Edited JSON body</p>
          <textarea
            className="h-48 w-full resize-none rounded-md border border-slate-300 bg-slate-950 p-3 font-mono text-xs leading-5 text-slate-100 outline-none focus:border-indigo-500"
            onChange={(event) => setBodyText(event.target.value)}
            spellCheck={false}
            value={bodyText}
          />
          {error && <p className="mt-2 text-sm text-rose-700">{error}</p>}
        </div>
        <button
          className="inline-flex h-10 items-center gap-2 rounded-md bg-indigo-700 px-3 text-sm font-medium text-white hover:bg-indigo-800"
          onClick={submitEditedReplay}
          type="button"
        >
          <Play className="h-4 w-4" />
          Replay with edits
        </button>
      </div>
    </section>
  )
}
