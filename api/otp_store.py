"""Temporary in-memory OTP store for the Vercel prototype."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class OTPRecord:
    email: str
    hash: str
    createdAt: int
    expiresAt: int
    attempts: int


OTP_STORE: Dict[str, OTPRecord] = {}
SEND_HISTORY: Dict[str, list[int]] = {}


def now() -> int:
    return int(time.time())


def get(email: str) -> Optional[OTPRecord]:
    record = OTP_STORE.get(email)
    if record is None:
        return None
    if now() >= record.expiresAt:
        OTP_STORE.pop(email, None)
        return None
    return record


def set_record(record: OTPRecord) -> None:
    OTP_STORE[record.email] = record


def delete(email: str) -> None:
    OTP_STORE.pop(email, None)


def seconds_since_last_send(key: str) -> Optional[int]:
    history = SEND_HISTORY.get(key, [])
    return None if not history else now() - history[-1]


def register_send(key: str) -> None:
    timestamp = now()
    history = SEND_HISTORY.setdefault(key, [])
    history.append(timestamp)
    cutoff = timestamp - 3600
    SEND_HISTORY[key] = [value for value in history if value >= cutoff]


def sends_last_hour(key: str) -> int:
    timestamp = now()
    cutoff = timestamp - 3600
    history = SEND_HISTORY.get(key, [])
    filtered = [value for value in history if value >= cutoff]
    SEND_HISTORY[key] = filtered
    return len(filtered)
