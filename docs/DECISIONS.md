# Decisions

## Local-Only Proxy

The tool is intentionally local-only because it captures sensitive request and response data.

## SQLite Request History

SQLite provides durable local history without a separate service dependency.

## Store Replays as New Records

Replay results are stored as normal captured records so developers can compare original and replayed behavior.

## Header Scope

The MVP forwards basic request headers and avoids hop-by-hop headers. Header editing is useful, but body editing proves the core replay workflow with less complexity.

## JSON-First UI

The dashboard optimizes for JSON APIs because those are the most common local debugging targets for this project.
