from .types import ContractError
from .types import Clock, Record
from .persistence import Persistence

class AccessControl:
    def authorize(self, authorization: str | None, action: str,
                  patient_id: str | None, *, store: Persistence, clock: Clock) -> Record:
        if not authorization or not authorization.startswith("Bearer "):
            raise ContractError(401, "unauthenticated", "A bearer credential is required.")
        identity = store.get("identities", authorization.removeprefix("Bearer "))
        if not identity:
            raise ContractError(401, "unauthenticated", "The credential is not recognized.")
        if action != "get_care_summary" or identity.get("role") != "patient" or patient_id != identity.get("patient_id"):
            raise ContractError(403, "forbidden", "You are not authorized for this request.")
        return identity
