import hashlib
import json
from sqlalchemy.orm import Session
from sqlalchemy import text


def acquire_client_lock(db: Session, client_name: str, date) -> None:
    key_str = f"{client_name}{date}"
    lock_key = int(hashlib.md5(key_str.encode()).hexdigest()[:8], 16)
    db.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock_key})


def make_request_hash(data) -> str:
    """
    Stable fingerprint of a request. Same client + same items + same
    amounts always produces the same hash. Order of items is normalized
    so [A, B] and [B, A] are treated as the same request.
    """
    # Convert Pydantic model to dict, sort item list for stability
    payload = data.model_dump()

    if "items" in payload:
        payload["items"] = sorted(
            payload["items"],
            key=lambda x: json.dumps(x, sort_keys=True)
        )

    canonical = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()