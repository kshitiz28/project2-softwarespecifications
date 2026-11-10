from dataclasses import dataclass
from datetime import datetime
from typing import Callable

Record = dict[str, object]
Clock = Callable[[], datetime]
IdFactory = Callable[[str], str]

@dataclass(frozen=True)
class Call:
    authorization: str | None
    path: dict[str, str]
    query: dict[str, str]
    body: bytes

@dataclass(frozen=True)
class Write:
    table: str
    key: str
    value: Record | None
    expected: Record | None = None
    require_absent: bool = False

@dataclass
class ContractError(Exception):
    status: int
    error: str
    message: str
    field: str | None = None

@dataclass(frozen=True)
class Result:
    status: int
    body: Record

Scheduler = Callable[[str, Record, int], Record]
Sender = Callable[[Record], Record]
