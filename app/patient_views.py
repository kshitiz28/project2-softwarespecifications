from typing import Callable
from .types import Call, Clock, IdFactory, Record, Result, Scheduler, Sender
from .persistence import Persistence
from .access_control import AccessControl

def get_care_summary(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError
