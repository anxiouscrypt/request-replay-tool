from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.database import init_db
from app.models import ReplayWithEditsRequest, RequestRecord
from app.proxy import forward_request
from app.replay import replay_record
from app.request_store import (
    delete_request_records,
    get_request_record,
    list_request_records,
    save_request_record,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Request Replay Tool API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.api_route(
    "/proxy/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def proxy_request(path: str, request: Request) -> Response:
    result = await forward_request(path, request)
    save_request_record(
        method=request.method,
        path=f"/{path}",
        target_url=result.target_url,
        request_headers=result.request_headers,
        request_body=result.request_body,
        response_status=result.response_status,
        response_body=result.response_body,
        duration_ms=result.duration_ms,
    )
    return result.response


@app.get("/requests", response_model=list[RequestRecord])
def read_requests() -> list[RequestRecord]:
    return list_request_records()


@app.get("/requests/{request_id}", response_model=RequestRecord)
def read_request(request_id: str) -> RequestRecord:
    record = get_request_record(request_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return record


@app.delete("/requests", status_code=204)
def clear_requests() -> None:
    delete_request_records()


@app.post("/requests/{request_id}/replay", response_model=RequestRecord)
async def replay_request(request_id: str) -> RequestRecord:
    record = get_request_record(request_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return await replay_record(record)


@app.post("/requests/{request_id}/replay-with-edits", response_model=RequestRecord)
async def replay_request_with_edits(
    request_id: str,
    payload: ReplayWithEditsRequest,
) -> RequestRecord:
    record = get_request_record(request_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return await replay_record(record, edited_body=payload.requestBody)
