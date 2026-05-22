import os
import sqlite3
from pathlib import Path


def database_path() -> Path:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./request_replay.db")

    if database_url.startswith("sqlite:///"):
        return Path(database_url.replace("sqlite:///", "", 1))

    return Path(database_url)


def get_connection() -> sqlite3.Connection:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
              id TEXT PRIMARY KEY,
              method TEXT NOT NULL,
              path TEXT NOT NULL,
              target_url TEXT NOT NULL,
              request_headers TEXT NOT NULL,
              request_body TEXT,
              response_status INTEGER NOT NULL,
              response_body TEXT,
              duration_ms REAL NOT NULL,
              created_at TEXT NOT NULL
            )
            """
        )
