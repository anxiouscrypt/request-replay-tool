# Request Replay Tool

A local debugging proxy that captures HTTP requests and lets developers inspect, edit, and replay them to reproduce API bugs faster.

## Problem

Rebuilding a specific API request by hand is slow and error-prone. This tool captures real proxied requests, stores request/response details, and makes replay available from a dashboard.

## Demo

Screenshot placeholder: `docs/screenshots/request-replay-tool.png`

## Features

- Proxy requests to a configured target API
- Store request method, path, headers, body, response status, response body, duration, and timestamp
- List and inspect captured requests
- Replay original requests
- Replay requests with an edited JSON body

## Architecture

Client request -> FastAPI proxy -> target API -> SQLite request history -> React dashboard.

```txt
Client
  -> /proxy/{path}
  -> TARGET_BASE_URL/{path}
  -> response
  -> SQLite request history
  -> React replay dashboard
```

## Tech Stack

- React, TypeScript, Vite
- Tailwind CSS
- FastAPI, SQLite, httpx
- Pytest

## Local Setup

Prerequisites:

- Node.js 20 or newer
- Python 3.11 or newer

Configure the target API:

```bash
cp .env.example .env
# edit TARGET_BASE_URL if needed
```

Run both services:

```bash
chmod +x scripts/dev.sh
./scripts/dev.sh
```

The frontend runs at `http://localhost:5173`.
The replay backend runs at `http://localhost:8000`.

Manual backend:

```bash
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
TARGET_BASE_URL=http://localhost:9000 PYTHONPATH=backend .venv/bin/uvicorn app.main:app --reload --port 8000
```

Manual frontend:

```bash
cd frontend
npm install
npm run dev
```

Run checks:

```bash
PYTHONPATH=backend .venv/bin/pytest backend/tests
cd frontend && npm run build
```

## Example Usage

With a target API running at `http://localhost:9000`, send traffic through the proxy:

```bash
curl -X POST http://localhost:8000/proxy/orders \
  -H 'Content-Type: application/json' \
  --data '{"sku":"latte"}'
```

Then open the dashboard to inspect and replay the captured request.

## What I Learned

- Debugging tools need to preserve context, not just the final response.
- Replay is most useful when it stores each replay result as a new comparable record.
- Proxy tools should document security limitations clearly because they can capture sensitive data.

## API Endpoints

- `GET /health`
- `ANY /proxy/{path:path}`
- `GET /requests`
- `GET /requests/{id}`
- `POST /requests/{id}/replay`
- `POST /requests/{id}/replay-with-edits`
- `DELETE /requests`

## Security Note

This is a local developer tool only. It may capture sensitive headers and bodies and should not be used as a production proxy.
