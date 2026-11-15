from .types import Clock, Record, ContractError
from .persistence import Persistence


class AccessControl:
    def authorize(self, authorization: str | None, action: str,
                  patient_id: str | None, *, store: Persistence, clock: Clock) -> Record:
        """Authorize an appointment action against the configured identity store.

        Identity records and permissions follow the fixture contract in contracts.md;
        no external authentication provider is assumed here.
        """
        if not isinstance(authorization, str) or not authorization.startswith("Bearer "):
            raise ContractError(401, "unauthenticated", "Sign-in is required.")
        token = authorization[len("Bearer "):].strip()
        if not token:
            raise ContractError(401, "unauthenticated", "Sign-in is required.")

        actor = store.get("identities", token)
        if actor is None:
            raise ContractError(401, "unauthenticated", "Invalid sign-in credential.")
        if actor.get("role") != "scheduling_staff":
            raise ContractError(403, "forbidden", "Scheduling permission is required.")
        allowed = actor.get("patient_ids", [])
        if patient_id is not None and patient_id not in allowed:
            raise ContractError(403, "forbidden", "Access to this patient is not permitted.")
        return actor
