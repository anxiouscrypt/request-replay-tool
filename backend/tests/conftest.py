import json

import pytest
from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app


class FakeUpstreamResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self.content = json.dumps(payload or {"ok": True}).encode("utf-8")
        self.headers = {"content-type": "application/json"}


class FakeAsyncClient:
    calls = []

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def request(self, method, url, content=None, headers=None):
        body = json.loads(content) if content else None
        self.calls.append(
            {
                "method": method,
                "url": url,
                "content": body,
                "headers": headers or {},
            }
        )
        return FakeUpstreamResponse(
            status_code=201,
            payload={"received": body, "method": method, "url": url},
        )


@pytest.fixture()
def fake_http_client(monkeypatch):
    FakeAsyncClient.calls = []
    monkeypatch.setattr("app.proxy.httpx.AsyncClient", FakeAsyncClient)
    monkeypatch.setattr("app.replay.httpx.AsyncClient", FakeAsyncClient)
    return FakeAsyncClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.db")
    monkeypatch.setenv("TARGET_BASE_URL", "http://target.local")
    init_db()

    with TestClient(app) as test_client:
        yield test_client
