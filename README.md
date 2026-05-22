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

## Tech Stack

- React, TypeScript, Vite
- Tailwind CSS
- FastAPI, SQLite, httpx
- Pytest

## Local Setup

Setup instructions will be completed with the MVP.

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
