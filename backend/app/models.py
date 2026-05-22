from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RequestRecord(BaseModel):
    id: str
    method: str
    path: str
    targetUrl: str
    requestHeaders: dict[str, str]
    requestBody: Any
    responseStatus: int
    responseBody: Any
    durationMs: float
    createdAt: datetime


class ReplayWithEditsRequest(BaseModel):
    requestBody: Any
