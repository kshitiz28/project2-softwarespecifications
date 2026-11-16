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
        if (action != "submit_referral" or identity.get("role") != "referring_provider"
                or patient_id not in identity.get("patient_ids", [])):
            raise ContractError(403, "forbidden", "You are not authorized for this request.")
        return identity
