import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.database import get_connection
from app.models import RequestRecord


def record_id() -> str:
    return f"req_{uuid4().hex[:10]}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dumps(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value)


def _loads(value: str | None) -> Any:
    if value is None:
        return None
    return json.loads(value)


def save_request_record(
    method: str,
    path: str,
    target_url: str,
    request_headers: dict[str, str],
    request_body: Any,
    response_status: int,
    response_body: Any,
    duration_ms: float,
) -> RequestRecord:
    created_at = _now()
    request_id = record_id()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO requests
              (id, method, path, target_url, request_headers, request_body,
               response_status, response_body, duration_ms, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                method,
                path,
                target_url,
                json.dumps(request_headers),
                _dumps(request_body),
                response_status,
                _dumps(response_body),
                duration_ms,
                created_at,
            ),
        )

    return get_request_record(request_id)


def list_request_records() -> list[RequestRecord]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM requests ORDER BY created_at DESC"
        ).fetchall()

    return [_row_to_record(row) for row in rows]


def get_request_record(request_id: str) -> RequestRecord | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM requests WHERE id = ?", (request_id,)
        ).fetchone()

    return _row_to_record(row) if row else None


def delete_request_records() -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM requests")


def _row_to_record(row) -> RequestRecord:
    return RequestRecord(
        id=row["id"],
        method=row["method"],
        path=row["path"],
        targetUrl=row["target_url"],
        requestHeaders=json.loads(row["request_headers"]),
        requestBody=_loads(row["request_body"]),
        responseStatus=row["response_status"],
        responseBody=_loads(row["response_body"]),
        durationMs=row["duration_ms"],
        createdAt=datetime.fromisoformat(row["created_at"]),
    )
