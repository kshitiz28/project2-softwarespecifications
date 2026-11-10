from typing import Callable
from .types import Call, Clock, IdFactory, Record, Result, Scheduler, Sender
from .persistence import Persistence
from .access_control import AccessControl

def run_reminders(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, send: Sender) -> Result:
    raise NotImplementedError
