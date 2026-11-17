from typing import Callable
from .types import Call, Clock, IdFactory, Record, Result, Scheduler, Sender
from .persistence import Persistence
from .access_control import AccessControl

def assign_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def list_tasks(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    patient_id = call.path["patient_id"]
    access.authorize(call.authorization, "list_tasks", patient_id, store=store, clock=clock)
    return Result(200, {"items": [task for task in store.list("tasks")
                                  if task.get("patient_id") == patient_id]})


def upload_document(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, validate_document: Callable[[bytes, str, Record], None]) -> Result:
    raise NotImplementedError


def get_document(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError


def complete_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def get_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError
