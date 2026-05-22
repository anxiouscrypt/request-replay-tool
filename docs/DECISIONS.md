# Decisions

## Local-Only Proxy

The tool is intentionally local-only because it captures sensitive request and response data.

## SQLite Request History

SQLite provides durable local history without a separate service dependency.

## Store Replays as New Records

Replay results are stored as normal captured records so developers can compare original and replayed behavior.
