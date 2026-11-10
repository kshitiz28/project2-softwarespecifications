from typing import Callable
from .types import Call, Clock, IdFactory, Record, Result, Scheduler, Sender
from .persistence import Persistence
from .access_control import AccessControl

def list_slots(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, schedule: Scheduler) -> Result:
    raise NotImplementedError


def book_appointment(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, schedule: Scheduler) -> Result:
    raise NotImplementedError


def reconcile_attempt(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, schedule: Scheduler) -> Result:
    raise NotImplementedError


def change_appointment(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, schedule: Scheduler) -> Result:
    raise NotImplementedError


def get_appointment_history(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError
