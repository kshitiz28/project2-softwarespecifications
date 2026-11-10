from .types import Clock, Record
from .persistence import Persistence

class AccessControl:
    def authorize(self, authorization: str | None, action: str,
                  patient_id: str | None, *, store: Persistence, clock: Clock) -> Record:
        raise NotImplementedError
