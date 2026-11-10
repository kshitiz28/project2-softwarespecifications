# CarePath test plan

Table refinement of the numbered acceptance checks in spec.md. Each unique test ID extends its original AC identifier.

Frozen clock: 2026-11-10T10:00:00Z unless a step changes it. Fixture data is fictional. Expected domain values were derived from the spec; HTTP status, field names and deterministic identifiers come from contracts.md. Tests use an isolated state per case. Controls change only the invalid input, caller, initial state, or external result under test. **Unchanged [*]** means no persisted state changed or was created. Suppression and unresolved attempts can record the bookkeeping explicitly allowed by the plan.

All executable cases below are included because no subset of AC IDs was specified. The fixture credential-to-identity mapping is in contracts.md and tests/support.py; the JSON catalog is a test fixture, not implementation code. Where relevant, scheduler calls use a 10-second budget; reminder sends check the channel/destination and omit clinical data.

| ID | Requirement | Cases | Inside/outside | Control |
|---|---|---|---|---|
| AC-A01.1 | FR-A01 / AC-A01 | **AC-A01-1-slots**: List offered future slots. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. GET /referrals/r1/appointment-slots; credential=staff → HTTP 200, JSON contains {"items":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}]}; unchanged tables ["*"] (* = full snapshot); external calls {"slots":1} | — | — |
| AC-A01.2 | FR-A01 / AC-A01 | **AC-A01-2-book**: Confirm and link appointment. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","referral_id":"r1","patient_id":"p1","status":"Scheduled","starts_at":"2026-11-11T10:00:00Z","external_booking_id":"ext1"}; final row counts {"appointments":1}; stored rows contain [["appointments","appointment-1",{"referral_id":"r1","patient_id":"p1","status":"Scheduled"}]]; external calls {"book":1} | — | — |
| AC-A01.3 | FR-A01 / AC-A01 | **AC-A01-3-unavailable**: Unavailable slot. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"unavailable"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 409, JSON contains {"error":"slot_unavailable"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"book":1}<br><br>**AC-A01-3-unavailable-control**: Control: Unavailable slot. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","referral_id":"r1","patient_id":"p1","status":"Scheduled","starts_at":"2026-11-11T10:00:00Z","external_booking_id":"ext1"}; final row counts {"appointments":1}; stored rows contain [["appointments","appointment-1",{"referral_id":"r1","patient_id":"p1","status":"Scheduled"}]]; external calls {"book":1} | — | AC-A01-3-unavailable → AC-A01-3-unavailable-control |
| AC-A01.4 | FR-A01 / AC-A01 | **AC-A01-4-timeout**: Timeout, blocked retry, then reconcile. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"timeout","elapsed_ms":10001},"lookup":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 202, JSON contains {"attempt_id":"attempt-1","outcome":"unresolved"}; absent fields ["appointment"]; unchanged tables ["appointments","history"] (* = full snapshot); final row counts {"booking_attempts":1}; stored rows contain [["booking_attempts","attempt-1",{"status":"Unresolved","referral_id":"r1"}]]; external calls {"book":1}; then POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 409, JSON contains {"error":"attempt_unresolved"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"book":0}; then POST /booking-attempts/attempt-1/reconcile; credential=staff; JSON {} → HTTP 200, JSON contains {"attempt_id":"attempt-1","outcome":"confirmed","status":"Scheduled"}; final row counts {"appointments":1}; stored rows contain [["appointments","appointment-1",{"status":"Scheduled","referral_id":"r1"}]]; external calls {"lookup":1}<br><br>**AC-A01-4-control**: Control: booking completes before deadline. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A","elapsed_ms":9999}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","referral_id":"r1","patient_id":"p1","status":"Scheduled","starts_at":"2026-11-11T10:00:00Z","external_booking_id":"ext1"}; final row counts {"appointments":1}; stored rows contain [["appointments","appointment-1",{"referral_id":"r1","patient_id":"p1","status":"Scheduled"}]]; external calls {"book":1} | 9.999s confirmed; 10.001s unresolved. Adapter must receive a 10-second timeout. | AC-A01-4-timeout → AC-A01-4-control |
| AC-A01.5 | FR-A01 / AC-A01 | **AC-A01-5-concurrent**: At most one booking survives concurrent calls. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. Submit concurrently; expected effects apply to the batch. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","referral_id":"r1","patient_id":"p1","status":"Scheduled","starts_at":"2026-11-11T10:00:00Z","external_booking_id":"ext1"}; final row counts {"appointments":1,"history":1}; stored rows contain [["appointments","appointment-1",{"referral_id":"r1","patient_id":"p1","status":"Scheduled"}]]; external calls {"book":1}; then POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 409, JSON contains {"error":"booking_conflict"} and nonempty message; final row counts {"appointments":1,"history":1}; stored rows contain [["appointments","appointment-1",{"status":"Scheduled","referral_id":"r1"}]]; external calls {"book":1}<br><br>**AC-A01-5-extra-active**: **Extra.** FR-A01: second booking rejected after first is committed. Seed F2. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 409, JSON contains {"error":"booking_conflict"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"book":0}<br><br>**AC-A01-5-extra-active-control**: **Extra.** Control: FR-A01: second booking rejected after first is committed. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","referral_id":"r1","patient_id":"p1","status":"Scheduled","starts_at":"2026-11-11T10:00:00Z","external_booking_id":"ext1"}; final row counts {"appointments":1}; stored rows contain [["appointments","appointment-1",{"referral_id":"r1","patient_id":"p1","status":"Scheduled"}]]; external calls {"book":1} | One active appointment allowed; second rejected. | AC-A01-5-concurrent → AC-A01-2-book; AC-A01-5-extra-active → AC-A01-5-extra-active-control |
| AC-A02.1 | FR-A02 / AC-A02 | **AC-A02-1-reschedule**: Confirmed replacement retains referral link. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"reschedule","slot_id":"s2","reason":"Patient requested another time"} → HTTP 200, JSON contains {"id":"a1","status":"Scheduled","starts_at":"2026-11-12T10:00:00Z","referral_id":"r1"}; final row counts {"history":1}; stored rows contain [["appointments","a1",{"starts_at":"2026-11-12T10:00:00Z","referral_id":"r1","external_booking_id":"ext2"}]]; external calls {"reschedule":1} | — | — |
| AC-A02.2 | FR-A02 / AC-A02 | **AC-A02-2-rejected**: Rejected replacement preserves original. Seed F2. External replies {"reschedule":{"outcome":"unavailable"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"reschedule","slot_id":"s2","reason":"Patient requested another time"} → HTTP 409, JSON contains {"error":"slot_unavailable"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"reschedule":1}<br><br>**AC-A02-2-rejected-control**: Control: Rejected replacement preserves original. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"reschedule","slot_id":"s2","reason":"Patient requested another time"} → HTTP 200, JSON contains {"id":"a1","status":"Scheduled","starts_at":"2026-11-12T10:00:00Z","referral_id":"r1"}; final row counts {"history":1}; stored rows contain [["appointments","a1",{"starts_at":"2026-11-12T10:00:00Z","referral_id":"r1","external_booking_id":"ext2"}]]; external calls {"reschedule":1} | — | AC-A02-2-rejected → AC-A02-2-rejected-control |
| AC-A02.3 | FR-A02 / AC-A02 | **AC-A02-3-cancel**: Cancel without canceling referral. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 200, JSON contains {"id":"a1","status":"Canceled","requested_by":"staff","reason":"Patient canceled"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["appointments","a1",{"status":"Canceled"}]]; external calls {"cancel":1} | — | — |
| AC-A02.4 | FR-A02 / AC-A02 | **AC-A02-4-reason**: Reason missing. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel"} → HTTP 422, JSON contains {"error":"validation_error","field":"reason"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"cancel":0}<br><br>**AC-A02-4-reason-control**: Control: Reason missing. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 200, JSON contains {"id":"a1","status":"Canceled","requested_by":"staff","reason":"Patient canceled"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["appointments","a1",{"status":"Canceled"}]]; external calls {"cancel":1} | — | AC-A02-4-reason → AC-A02-4-reason-control |
| AC-A02.5 | FR-A02 / AC-A02 | **AC-A02-5-completed**: Cannot change Completed. Seed F3. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 409, JSON contains {"error":"invalid_appointment_state"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"cancel":0}<br><br>**AC-A02-5-completed-control**: Control: Cannot change Completed. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 200, JSON contains {"id":"a1","status":"Canceled","requested_by":"staff","reason":"Patient canceled"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["appointments","a1",{"status":"Canceled"}]]; external calls {"cancel":1}<br><br>**AC-A02-5-canceled**: Cannot change Canceled. Seed F4. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 409, JSON contains {"error":"invalid_appointment_state"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"cancel":0}<br><br>**AC-A02-5-canceled-control**: Control: Cannot change Canceled. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 200, JSON contains {"id":"a1","status":"Canceled","requested_by":"staff","reason":"Patient canceled"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["appointments","a1",{"status":"Canceled"}]]; external calls {"cancel":1}<br><br>**AC-A02-5-no-show**: Cannot change No-show. Seed F5. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 409, JSON contains {"error":"invalid_appointment_state"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"cancel":0}<br><br>**AC-A02-5-no-show-control**: Control: Cannot change No-show. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 200, JSON contains {"id":"a1","status":"Canceled","requested_by":"staff","reason":"Patient canceled"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["appointments","a1",{"status":"Canceled"}]]; external calls {"cancel":1} | Scheduled is changeable; Completed is not.; Scheduled is changeable; Canceled is not.; Scheduled is changeable; No-show is not. | AC-A02-5-completed → AC-A02-5-completed-control; AC-A02-5-canceled → AC-A02-5-canceled-control; AC-A02-5-no-show → AC-A02-5-no-show-control |
| AC-A03.1 | FR-A03 / AC-A03 | **AC-A03-1-history**: Confirmed change adds actor/time/reason and before/after. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"reschedule","slot_id":"s2","reason":"Patient requested another time"} → HTTP 200, JSON contains {"id":"a1","status":"Scheduled","starts_at":"2026-11-12T10:00:00Z","referral_id":"r1"}; final row counts {"history":1}; stored rows contain [["appointments","a1",{"starts_at":"2026-11-12T10:00:00Z","referral_id":"r1","external_booking_id":"ext2"}]]; external calls {"reschedule":1}; then GET /appointments/a1/history; credential=staff → HTTP 200, JSON contains {"items":[{"actor_id":"staff","at":"2026-11-10T10:00:00Z","reason":"Patient requested another time","old":{"starts_at":"2026-11-11T10:00:00Z","status":"Scheduled"},"new":{"starts_at":"2026-11-12T10:00:00Z","status":"Scheduled"}}]}; unchanged tables ["*"] (* = full snapshot) | — | — |
| AC-A03.2 | FR-A03 / AC-A03 | **AC-A03-2-append**: Later cancellation does not replace history. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"reschedule","slot_id":"s2","reason":"Patient requested another time"} → HTTP 200, JSON contains {"id":"a1","status":"Scheduled","starts_at":"2026-11-12T10:00:00Z","referral_id":"r1"}; final row counts {"history":1}; stored rows contain [["appointments","a1",{"starts_at":"2026-11-12T10:00:00Z","referral_id":"r1","external_booking_id":"ext2"}]]; external calls {"reschedule":1}; then PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"}; set clock 2026-11-10T10:00:01Z → HTTP 200, JSON contains {"id":"a1","status":"Canceled","requested_by":"staff","reason":"Patient canceled"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["appointments","a1",{"status":"Canceled"}]]; external calls {"cancel":1}; then GET /appointments/a1/history; credential=staff → HTTP 200, JSON contains {"items":[{"actor_id":"staff","at":"2026-11-10T10:00:00Z","reason":"Patient requested another time","old":{"starts_at":"2026-11-11T10:00:00Z","status":"Scheduled"},"new":{"starts_at":"2026-11-12T10:00:00Z","status":"Scheduled"}},{"actor_id":"staff","at":"2026-11-10T10:00:01Z","reason":"Patient canceled","old":{"starts_at":"2026-11-12T10:00:00Z","status":"Scheduled"},"new":{"starts_at":"2026-11-12T10:00:00Z","status":"Canceled"}}]}; unchanged tables ["*"] (* = full snapshot) | — | — |
| AC-A03.3 | FR-A03 / AC-A03 | **AC-A03-3-no-false-history**: Failed change does not create history. Seed F2. External replies {"reschedule":{"outcome":"unavailable"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"reschedule","slot_id":"s2","reason":"Patient requested another time"} → HTTP 409, JSON contains {"error":"slot_unavailable"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"reschedule":1}<br><br>**AC-A03-3-no-false-history-control**: Control: Failed change does not create history. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"reschedule","slot_id":"s2","reason":"Patient requested another time"} → HTTP 200, JSON contains {"id":"a1","status":"Scheduled","starts_at":"2026-11-12T10:00:00Z","referral_id":"r1"}; final row counts {"history":1}; stored rows contain [["appointments","a1",{"starts_at":"2026-11-12T10:00:00Z","referral_id":"r1","external_booking_id":"ext2"}]]; external calls {"reschedule":1} | — | AC-A03-3-no-false-history → AC-A03-3-no-false-history-control |
| AC-A01-extra-role | FR-A01 / AC-A01 | **AC-A01-extra-role**: **Extra.** NFR-A01: patient cannot book as staff. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=patient; JSON {"slot_id":"s1"} → HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"book":0}<br><br>**AC-A01-extra-role-control**: **Extra.** Control: NFR-A01: patient cannot book as staff. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","referral_id":"r1","patient_id":"p1","status":"Scheduled","starts_at":"2026-11-11T10:00:00Z","external_booking_id":"ext1"}; final row counts {"appointments":1}; stored rows contain [["appointments","appointment-1",{"referral_id":"r1","patient_id":"p1","status":"Scheduled"}]]; external calls {"book":1} | — | AC-A01-extra-role → AC-A01-extra-role-control |
| AC-A02-extra-type | FR-A02 / AC-A02 | **AC-A02-extra-type**: **Extra.** FR-A02: reason type. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":42} → HTTP 422, JSON contains {"error":"validation_error","field":"reason"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"cancel":0}<br><br>**AC-A02-extra-type-control**: **Extra.** Control: FR-A02: reason type. Seed F2. External replies {"reschedule":{"outcome":"confirmed","external_booking_id":"ext2","starts_at":"2026-11-12T10:00:00Z","provider_id":"receiver","location":"Clinic A"},"cancel":{"outcome":"confirmed"}}. PATCH /appointments/a1; credential=staff; JSON {"action":"cancel","reason":"Patient canceled"} → HTTP 200, JSON contains {"id":"a1","status":"Canceled","requested_by":"staff","reason":"Patient canceled"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["appointments","a1",{"status":"Canceled"}]]; external calls {"cancel":1} | — | AC-A02-extra-type → AC-A02-extra-type-control |
| AC-A01-extra-referral-state | FR-A01 / AC-A01 | **AC-A01-extra-referral-state**: **Extra.** FR-A01: referral must be accepted. Seed F6. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 409, JSON contains {"error":"invalid_referral_state"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"book":0}<br><br>**AC-A01-extra-referral-state-control**: **Extra.** Control: FR-A01: referral must be accepted. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","referral_id":"r1","patient_id":"p1","status":"Scheduled","starts_at":"2026-11-11T10:00:00Z","external_booking_id":"ext1"}; final row counts {"appointments":1}; stored rows contain [["appointments","appointment-1",{"referral_id":"r1","patient_id":"p1","status":"Scheduled"}]]; external calls {"book":1} | — | AC-A01-extra-referral-state → AC-A01-extra-referral-state-control |
| AC-A01-extra-slot-boundary | FR-A01 / AC-A01 | **AC-A01-extra-slot-boundary**: **Extra.** FR-A01: slot must be in the future. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-10T10:00:00Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-11T10:00:00Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 422, JSON contains {"error":"invalid_slot"} and nonempty message; unchanged tables ["*"] (* = full snapshot); external calls {"book":0}<br><br>**AC-A01-extra-slot-boundary-control**: **Extra.** Control: FR-A01: slot must be in the future. Seed F1. External replies {"slots":[{"id":"s1","starts_at":"2026-11-10T10:00:01Z","provider_id":"receiver","location":"Clinic A"}],"book":{"outcome":"confirmed","external_booking_id":"ext1","starts_at":"2026-11-10T10:00:01Z","provider_id":"receiver","location":"Clinic A"}}. POST /referrals/r1/appointments; credential=staff; JSON {"slot_id":"s1"} → HTTP 201, JSON contains {"id":"appointment-1","status":"Scheduled","starts_at":"2026-11-10T10:00:01Z","referral_id":"r1","patient_id":"p1"}; final row counts {"appointments":1}; external calls {"book":1} | Starts exactly now rejected; starts one second later accepted. | AC-A01-extra-slot-boundary → AC-A01-extra-slot-boundary-control |

## Fixture records

The shared identity catalog, configured urgencies and clock are applied to each fixture. All other starting tables are empty.

**F1**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  }
}
```

**F2**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  }
}
```

**F3**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Completed",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  }
}
```

**F4**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Canceled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  }
}
```

**F5**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "No-show",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  }
}
```

**F6**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Under review",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  }
}
```


## Gap checklist and environment checks

Future-slot boundary, role, referral state, timeout and concurrent claims: AC-A01. Reason input type and allowed appointment state: AC-A02. Returned history and failed-change preservation: AC-A03. Exact timeout equality and ordering for multiple invalid inputs are unresolved.

| NFR | Validation | Execution scope |
|---|---|---|
| NFR-A01 | Try signed-out, wrong-role, and unrelated-patient booking requests; verify denial and no external call. Target: Verify staff identity, scheduling permission, and patient access on every booking or change request. Unauthorized requests must make no booking or return patient details. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-A02 | Run two simultaneous bookings and force a local transaction failure. Target: At most one confirmed active appointment or unresolved booking attempt may reserve a referral at a time. Save each confirmed local change and history entry together. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-A03 | Delay the scheduling response beyond 10 seconds and check unresolved status and blocked retry. Target: Use a finite 10-second external-call timeout. A timeout must leave a visible unresolved attempt rather than a successful booking. Block another change until the result is reconciled. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-A04 | Inspect deployed transport and logs for booking and cancellation attempts. Target: Use HTTPS outside local development and omit patient and booking details from ordinary diagnostic logs. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-A05 | Measure local read responses at the stated test load. Target: For 20 simultaneous users and 10,000 appointments, 95% of local appointment reads must return within 2 seconds, excluding scheduling-service time. Use 200 measured eligible requests at the specified 20-user, 10,000-record load; sort durations and check the 190th is at most 2,000 ms. Exercise 1,999 and 2,001 ms in the threshold check. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-A06 | Exercise rejection, timeout, and blank-reason cases and inspect displayed messages. Target: Clearly distinguish confirmed, failed, and unresolved booking results. Keep the entered change reason after a validation error. | Implemented environment / deployment check; not a 501 skeleton test. |

## Spec gaps

- FR-A01 through FR-A03 all have criteria; AC-A01 through AC-A03 all have requirements.
- The external scheduler API, attempt lookup, atomic replacement, slot timezone policy and terminal status updates are not specified. Tests use the proposed adapter interface and controlled replies, not a real scheduler.
- NFR-A03 gives 10 seconds but does not settle exact equality or later callbacks. The test brackets the limit at 9.999 and 10.001 seconds.
- If several inputs are invalid, the spec does not specify error precedence. Rejection tests deliberately isolate one invalid condition. Pagination, maximum response sizes, and error message wording are unspecified.
- NFRs have Validation entries rather than separate AC IDs. API-addressable parts are covered by the extra cases above; deployment and UI checks remain environment tests.
