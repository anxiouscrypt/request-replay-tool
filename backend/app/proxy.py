import json
from dataclasses import dataclass
from typing import Any
from time import perf_counter

import httpx
from fastapi import Request
from fastapi.responses import Response

from app.settings import target_base_url

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


@dataclass
class ProxyResult:
    response: Response
    duration_ms: float
    target_url: str
    request_headers: dict[str, str]
    request_body: Any
    response_status: int
    response_body: Any


def build_target_url(path: str, query_string: bytes) -> str:
    target_path = path if path.startswith("/") else f"/{path}"
    url = f"{target_base_url()}{target_path}"

    if query_string:
        url = f"{url}?{query_string.decode('utf-8')}"

    return url


def forward_headers(request: Request) -> dict[str, str]:
    return {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in HOP_BY_HOP_HEADERS
    }


async def forward_request(path: str, request: Request) -> ProxyResult:
    target_url = build_target_url(path, request.scope.get("query_string", b""))
    body = await request.body()
    headers = forward_headers(request)
    started = perf_counter()

    async with httpx.AsyncClient(timeout=10.0) as client:
        upstream = await client.request(
            request.method,
            target_url,
            content=body,
            headers=headers,
        )

    duration_ms = (perf_counter() - started) * 1000
    response = Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=upstream.headers.get("content-type"),
    )

    return ProxyResult(
        response=response,
        duration_ms=round(duration_ms, 2),
        target_url=target_url,
        request_headers=headers,
        request_body=parse_body(body),
        response_status=upstream.status_code,
        response_body=parse_body(upstream.content),
    )


def parse_body(body: bytes) -> Any:
    if not body:
        return None

    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return body.decode("utf-8", errors="replace")
