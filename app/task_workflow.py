from typing import Callable
from .types import Call, Clock, IdFactory, Record, Result, Scheduler, Sender
from .persistence import Persistence
from .access_control import AccessControl

def assign_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def list_tasks(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError


def upload_document(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, validate_document: Callable[[bytes, str, Record], None]) -> Result:
    raise NotImplementedError


def get_document(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError


def complete_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def get_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError
