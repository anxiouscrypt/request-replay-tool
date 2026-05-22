# Architecture

## System Components

- FastAPI proxy route receives local `/proxy/*` traffic.
- `httpx` forwards requests to `TARGET_BASE_URL`.
- SQLite stores request and response history.
- Replay routes reconstruct stored requests.
- React dashboard displays history, details, and replay controls.

## Data Flow

```txt
Client -> /proxy/{path} -> target API -> response
                     -> SQLite request history -> React dashboard
```

## Security Limitations

- Local development only.
- Captured headers and bodies may contain secrets.
- No authentication, access control, or production hardening.

## Proxy Design

`ANY /proxy/{path}` receives a request, builds a target URL from `TARGET_BASE_URL + path`, forwards method, query string, selected headers, and body, then returns the target response.

Hop-by-hop headers are not forwarded. The MVP focuses on JSON debugging flows and local APIs.

## Storage Model

```txt
requests
  id TEXT PRIMARY KEY
  method TEXT
  path TEXT
  target_url TEXT
  request_headers TEXT
  request_body TEXT
  response_status INTEGER
  response_body TEXT
  duration_ms REAL
  created_at TEXT
```

## Replay Workflow

Replay APIs load a stored request, send it to the original target URL, and store the replay result as a new request record. Edit-and-replay replaces the body before forwarding.
