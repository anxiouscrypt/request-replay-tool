import type { RequestRecord } from '../lib/types'

type RequestTableProps = {
  requests: RequestRecord[]
}

export function RequestTable({ requests }: RequestTableProps) {
  if (requests.length === 0) {
    return (
      <div className="p-4">
        <div className="rounded-md border border-dashed border-slate-300 px-4 py-14 text-center text-sm text-slate-500">
          Send requests through `/proxy/*` to capture history.
        </div>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[760px] text-left text-sm">
        <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase text-slate-500">
          <tr>
            <th className="px-4 py-3">Method</th>
            <th className="px-4 py-3">Path</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Duration</th>
            <th className="px-4 py-3">Captured</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {requests.map((request) => (
            <tr className="hover:bg-slate-50" key={request.id}>
              <td className="px-4 py-3">
                <span className="rounded-md bg-indigo-50 px-2 py-1 font-mono text-xs font-semibold text-indigo-700">
                  {request.method}
                </span>
              </td>
              <td className="px-4 py-3 font-mono text-slate-700">{request.path}</td>
              <td className="px-4 py-3">{request.responseStatus}</td>
              <td className="px-4 py-3">{request.durationMs}ms</td>
              <td className="px-4 py-3 text-slate-500">
                {new Date(request.createdAt).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
