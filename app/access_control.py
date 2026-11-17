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

        if action == "list_tasks":
            allowed = (identity.get("role") == "patient"
                       and patient_id == identity.get("patient_id"))
        elif action == "assign_task":
            allowed = (identity.get("role") == "nurse"
                       and patient_id in identity.get("patient_ids", []))
        else:
            allowed = False

        if not allowed:
            raise ContractError(403, "forbidden", "You are not authorized for this request.")
        return identity
