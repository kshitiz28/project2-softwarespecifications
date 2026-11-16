from .types import ContractError, Write
from datetime import timezone
import json
from typing import Callable
from .types import Call, Clock, IdFactory, Record, Result, Scheduler, Sender
from .persistence import Persistence
from .access_control import AccessControl

def submit_referral(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    if not call.authorization:
        access.authorize(None, "submit_referral", None, store=store, clock=clock)
    try:
        data = json.loads(call.body)
    except (ValueError, UnicodeError) as exc:
        raise ContractError(422, "validation_error", "A JSON object is required.", "body") from exc
    if not isinstance(data, dict):
        raise ContractError(422, "validation_error", "A JSON object is required.", "body")
    required = ("patient_id", "receiving_provider_id", "service", "reason", "urgency")
    for field in required:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ContractError(422, "validation_error", "A nonblank string is required.", field)
    if "supporting_document_ids" in data:
        identifiers = data["supporting_document_ids"]
        if not isinstance(identifiers, list) or any(not isinstance(key, str) or not key.strip() for key in identifiers):
            raise ContractError(422, "validation_error", "Provide a list of document identifiers.", "supporting_document_ids")
    actor = access.authorize(call.authorization, "submit_referral", data["patient_id"], store=store, clock=clock)
    receiver = store.get("identities", data["receiving_provider_id"])
    if not receiver or receiver.get("role") != "receiving_provider":
        raise ContractError(422, "validation_error", "Select a receiving provider.", "receiving_provider_id")
    if store.get("urgencies", data["urgency"]) is None:
        raise ContractError(422, "validation_error", "Select an available urgency.", "urgency")
    referral_id = id_factory("referral")
    at = clock().astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    record = {**{field: data[field] for field in required},
              "id": referral_id, "referring_provider_id": actor["id"],
              "status": "Submitted", "updated_at": at}
    if "supporting_document_ids" in data:
        record["supporting_document_ids"] = data["supporting_document_ids"]
    history = {"referral_id": referral_id, "actor_id": actor["id"], "at": at,
               "previous_status": None, "new_status": "Submitted"}
    store.commit([Write("referrals", referral_id, record, require_absent=True),
                  Write("history", id_factory("history"), history, require_absent=True)])
    return Result(201, {field: record[field] for field in ("id", "patient_id", "status", "updated_at")})


def review_referral(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def share_findings(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def list_referrals(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError


def request_information(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def respond_to_information_request(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    raise NotImplementedError


def get_referral(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError
