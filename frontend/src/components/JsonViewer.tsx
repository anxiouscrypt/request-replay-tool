type JsonViewerProps = {
  label: string
  value: unknown
}

export function JsonViewer({ label, value }: JsonViewerProps) {
  return (
    <div>
      <p className="mb-1 text-sm font-semibold text-slate-800">{label}</p>
      <pre className="max-h-72 overflow-auto rounded-md bg-slate-950 p-3 font-mono text-xs leading-5 text-slate-100">
        {JSON.stringify(value, null, 2)}
      </pre>
    </div>
  )
}
