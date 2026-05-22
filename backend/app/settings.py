import os


def target_base_url() -> str:
    return os.getenv("TARGET_BASE_URL", "http://localhost:9000").rstrip("/")
