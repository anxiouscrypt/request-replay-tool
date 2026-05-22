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
