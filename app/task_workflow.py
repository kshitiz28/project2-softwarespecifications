from typing import Callable
from datetime import datetime, timezone
import json
from .types import Call, Clock, ContractError, IdFactory, Record, Result, Scheduler, Sender, Write
from .persistence import Persistence
from .access_control import AccessControl

def assign_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result:
    # Parse the request before attempting a write. Validation errors leave the store untouched.
    try:
        details = json.loads(call.body)
    except (ValueError, UnicodeDecodeError):
        raise ContractError(422, "validation_error", "A JSON object is required.")
    if not isinstance(details, dict):
        raise ContractError(422, "validation_error", "A JSON object is required.")

    patient_id = details.get("patient_id")
    if not isinstance(patient_id, str) or not patient_id.strip():
        raise ContractError(422, "validation_error", "A patient is required.", "patient_id")

    # Nurses may only assign work to patients in their permitted patient list.
    identity = access.authorize(call.authorization, "assign_task", patient_id,
                                store=store, clock=clock)

    instructions = details.get("instructions")
    if not isinstance(instructions, str) or not instructions.strip():
        raise ContractError(422, "validation_error", "Instructions must not be blank.", "instructions")

    raw_due_at = details.get("due_at")
    try:
        if not isinstance(raw_due_at, str):
            raise ValueError("The due time must be a string.")
        due_at = datetime.fromisoformat(raw_due_at.replace("Z", "+00:00"))
        if due_at.tzinfo is None or due_at.utcoffset() is None:
            raise ValueError("The due time must have a time zone.")
        due_utc = due_at.astimezone(timezone.utc)
    except ValueError:
        raise ContractError(422, "validation_error", "A valid due time with a time zone is required.", "due_at")

    if due_utc <= clock().astimezone(timezone.utc):
        raise ContractError(422, "validation_error", "The due time must be in the future.", "due_at")

    document_required = details.get("document_required")
    if not isinstance(document_required, bool):
        raise ContractError(422, "validation_error", "Document requirement must be true or false.", "document_required")

    referral_id = details.get("referral_id")
    if referral_id is not None:
        if not isinstance(referral_id, str) or not referral_id.strip():
            raise ContractError(422, "validation_error", "A valid referral identifier is required.", "referral_id")
        referral = store.get("referrals", referral_id)
        # Do not invent a referral or bypass the patient/referral relationship.
        if referral is None or referral.get("patient_id") != patient_id:
            raise ContractError(422, "validation_error", "The referral must belong to this patient.", "referral_id")

    task_id = id_factory("task")
    history_id = id_factory("history")
    due_string = due_utc.isoformat(timespec="seconds").replace("+00:00", "Z")
    assigned_at = clock().astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    task = {
        "id": task_id,
        "patient_id": patient_id,
        "nurse_id": identity["id"],
        "instructions": instructions.strip(),
        "due_at": due_string,
        "status": "Open",
        "document_required": document_required,
        "referral_id": referral_id,
    }
    event = {
        "id": history_id,
        "task_id": task_id,
        "actor_id": identity["id"],
        "action": "Assigned",
        "at": assigned_at,
    }
    store.commit([
        Write(table="tasks", key=task_id, value=task, require_absent=True),
        Write(table="history", key=history_id, value=event, require_absent=True),
    ])
    return Result(201, task)


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
