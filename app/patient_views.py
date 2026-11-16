from typing import Callable
from .types import Call, Clock, IdFactory, Record, Result, Scheduler, Sender
from .persistence import Persistence
from .access_control import AccessControl

def get_care_summary(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result:
    patient_id = call.path["patient_id"]
    access.authorize(call.authorization, "get_care_summary", patient_id, store=store, clock=clock)
    referrals = [{key: row[key] for key in ("id", "status", "updated_at", "receiving_provider_id",
                                          "outstanding_requests", "guidance") if key in row}
                 for row in store.list("referrals") if row.get("patient_id") == patient_id]
    appointments = [{key: row[key] for key in ("id", "status", "starts_at", "provider_id", "location")}
                    for row in store.list("appointments")
                    if row.get("patient_id") == patient_id and row.get("status") == "Scheduled"]
    tasks = [{key: row[key] for key in ("id", "status", "instructions", "due_at")}
             for row in store.list("tasks")
             if row.get("patient_id") == patient_id and row.get("status") in {"Open", "Overdue"}]
    summary = {"patient_id": patient_id, "referrals": referrals,
               "appointments": appointments, "tasks": tasks}
    if not tasks and not any(ref.get("outstanding_requests") for ref in referrals):
        summary["next_action"] = "No action currently required"
    return Result(200, summary)
