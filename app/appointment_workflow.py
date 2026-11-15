"""Appointment management: the first two slices from plan.md.

Later actions (reconciliation, changes, and history reads) are deliberately
left as contract skeletons for the remaining slices.
"""
import json
from datetime import datetime

from .types import Call, Clock, IdFactory, Record, Result, Scheduler, ContractError, Write
from .persistence import Persistence
from .access_control import AccessControl


def list_slots(call: Call, *, access: AccessControl, store: Persistence,
               clock: Clock, schedule: Scheduler) -> Result:
    """Slice 1: list future appointment slots for an eligible referral."""
    referral = store.get("referrals", call.path["referral_id"])
    if referral is None:
        raise ContractError(409, "invalid_referral_state", "Referral is not available for scheduling.")
    access.authorize(call.authorization, "schedule", referral.get("patient_id"), store=store, clock=clock)
    if referral.get("status") != "Accepted":
        raise ContractError(409, "invalid_referral_state", "Referral must be accepted.")

    reply = schedule("slots", {
        "referral_id": referral["id"],
        "patient_id": referral["patient_id"],
        "provider_id": referral["receiving_provider_id"],
    }, 10)
    future = []
    for slot in reply["items"]:
        try:
            start = datetime.fromisoformat(slot["starts_at"].replace("Z", "+00:00"))
        except (KeyError, AttributeError, ValueError):
            continue
        if start.tzinfo is not None and start > clock():
            future.append(slot)
    return Result(200, {"items": future})


def book_appointment(call: Call, *, access: AccessControl, store: Persistence,
                     clock: Clock, id_factory: IdFactory, schedule: Scheduler) -> Result:
    """Slice 2: save a booking only after the scheduler confirms it.

    Rejected slots, timeout reconciliation and concurrent requests are planned
    separately. This slice never reports a nonconfirmed booking as Scheduled.
    """
    referral = store.get("referrals", call.path["referral_id"])
    if referral is None:
        raise ContractError(409, "invalid_referral_state", "Referral is not available for scheduling.")
    actor = access.authorize(call.authorization, "schedule", referral.get("patient_id"), store=store, clock=clock)
    if referral.get("status") != "Accepted":
        raise ContractError(409, "invalid_referral_state", "Referral must be accepted.")

    try:
        body = json.loads(call.body)
    except (ValueError, UnicodeDecodeError):
        raise ContractError(422, "invalid_slot", "A JSON slot_id is required.", "slot_id")
    if not isinstance(body, dict) or not isinstance(body.get("slot_id"), str) or not body["slot_id"].strip():
        raise ContractError(422, "invalid_slot", "A slot_id is required.", "slot_id")
    slot_id = body["slot_id"]

    # The no-active-booking requirement is checked here; a race-free atomic
    # uniqueness guarantee across workers belongs to Slice 7.
    if any(a.get("referral_id") == referral["id"] and a.get("status") == "Scheduled"
           for a in store.list("appointments")):
        raise ContractError(409, "booking_conflict", "Referral already has an active appointment.")

    slots_reply = schedule("slots", {
        "referral_id": referral["id"],
        "patient_id": referral["patient_id"],
        "provider_id": referral["receiving_provider_id"],
    }, 10)
    selected = next((s for s in slots_reply["items"] if s.get("id") == slot_id), None)
    try:
        start = datetime.fromisoformat(selected["starts_at"].replace("Z", "+00:00"))
        valid = start.tzinfo is not None and start > clock()
    except (TypeError, KeyError, AttributeError, ValueError):
        valid = False
    if not valid:
        raise ContractError(422, "invalid_slot", "The chosen slot must be in the future.", "slot_id")

    attempt_id = id_factory("attempt")
    pending = {"id": attempt_id, "referral_id": referral["id"],
               "slot_id": slot_id, "status": "Pending"}
    # Reserve locally before requesting an external booking; do not hold a
    # database transaction open during the external call.
    store.commit([Write("booking_attempts", attempt_id, pending, require_absent=True)])
    try:
        reply = schedule("book", {
            "attempt_id": attempt_id,
            "slot_id": slot_id,
            "referral_id": referral["id"],
            "patient_id": referral["patient_id"],
            "provider_id": referral["receiving_provider_id"],
        }, 10)
    except TimeoutError as exc:
        # The incomplete timeout path must not return a confirmed appointment.
        raise NotImplementedError("Timeout reconciliation belongs to Slice 6") from exc
    if reply.get("outcome") != "confirmed":
        raise NotImplementedError("Booking rejection handling belongs to Slice 5")

    appointment_id = id_factory("appointment")
    record = {
        "id": appointment_id,
        "referral_id": referral["id"],
        "patient_id": referral["patient_id"],
        "provider_id": reply.get("provider_id", referral["receiving_provider_id"]),
        "slot_id": slot_id,
        "starts_at": reply["starts_at"],
        "location": reply.get("location", selected.get("location")),
        "status": "Scheduled",
        "external_booking_id": reply["external_booking_id"],
    }
    initial_history = {
        "actor_id": actor["id"],
        "at": clock().isoformat().replace("+00:00", "Z"),
        "reason": "Initial confirmed booking",
        "old": {},
        "new": {"starts_at": record["starts_at"], "status": "Scheduled"},
    }
    # Appointment and initial history are committed in the same local update.
    store.commit([
        Write("appointments", appointment_id, record, require_absent=True),
        Write("history", appointment_id, {"appointment_id": appointment_id, "items": [initial_history]}, require_absent=True),
        Write("booking_attempts", attempt_id, None, expected=pending),
    ])
    return Result(201, record)


def reconcile_attempt(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, schedule: Scheduler) -> Result:
    raise NotImplementedError


def change_appointment(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, schedule: Scheduler) -> Result:
    raise NotImplementedError


def get_appointment_history(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    raise NotImplementedError
