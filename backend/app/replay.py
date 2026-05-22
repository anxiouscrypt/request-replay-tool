import json
from time import perf_counter
from typing import Any

import httpx

from app.models import RequestRecord
from app.proxy import HOP_BY_HOP_HEADERS, parse_body
from app.request_store import save_request_record


async def replay_record(
    record: RequestRecord,
    edited_body: Any = None,
) -> RequestRecord:
    request_body = record.requestBody if edited_body is None else edited_body
    headers = {
        key: value
        for key, value in record.requestHeaders.items()
        if key.lower() not in HOP_BY_HOP_HEADERS
    }
    content = encode_body(request_body)
    started = perf_counter()

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(
            record.method,
            record.targetUrl,
            content=content,
            headers=headers,
        )

    duration_ms = (perf_counter() - started) * 1000

    return save_request_record(
        method=record.method,
        path=record.path,
        target_url=record.targetUrl,
        request_headers=headers,
        request_body=request_body,
        response_status=response.status_code,
        response_body=parse_body(response.content),
        duration_ms=round(duration_ms, 2),
    )


def encode_body(body: Any) -> bytes | None:
    if body is None:
        return None
    if isinstance(body, (dict, list)):
        return json.dumps(body).encode("utf-8")
    if isinstance(body, str):
        return body.encode("utf-8")
    return json.dumps(body).encode("utf-8")
