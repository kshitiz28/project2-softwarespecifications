# Description

This part of CarePath covers Appointment Management. Administrative staff arrange appointments for accepted referrals and manage changes. Each appointment stays linked to the correct patient and referral.

# Goals

1. Keep care visits organized.
2. Help patients receive the service requested by their referral.
3. Maintain continuity of care through accurate appointment information.

# Domain Model

## Actors

- **Administrative staff member:** Schedules, reschedules and cancels appointments.
- **Patient:** The person attending the appointment.
- **Receiving provider:** The provider delivering the referred service.

## Objects

- **Referral:** Identifies the patient, receiving provider and referral status.
- **Appointment:** Identifier, referral, patient, provider, date, time, location, status and external booking identifier.
- **Available slot:** A future appointment time offered by the scheduling system.
- **Appointment change:** Requester, reason and previous and new booking details.
- **Change history:** A record of confirmed booking changes.

The external scheduling system confirms bookings and changes. An appointment can be Scheduled, Canceled, Completed or No-show. Only Scheduled appointments can be changed. A referral may have at most one active appointment. Users must be signed in and have permission for the patient and action.

# Functional Requirements

## FR-A01: Schedule a linked appointment

CarePath must let authorized administrative staff choose an available slot for an accepted referral and link the confirmed appointment to that referral and patient.

- The referral must have no active appointment.
- Save Scheduled only after the scheduling system confirms the booking.
- If confirmation fails or is uncertain, do not show a confirmed booking. Resolve an uncertain attempt before allowing another attempt.

Supports Goals 1 and 2. Tested by AC-A01.

## FR-A02: Reschedule or cancel an appointment

CarePath must let authorized administrative staff reschedule or cancel a Scheduled appointment and record the requester and reason.

- A change reason is required.
- Keep the original booking until the replacement is confirmed.
- A confirmed cancellation sets Canceled without canceling the referral.

Supports Goals 1 and 3. Tested by AC-A02.

## FR-A03: Keep appointment history

CarePath must retain who changed an appointment, when, the reason and the old and new booking details. Existing history must not be overwritten by a later change.

Supports Goals 1 and 3. Tested by AC-A03.

# Acceptance Criteria

## AC-A01: Schedule an appointment

For FR-A01:

1. With an accepted referral and no active booking, staff can select an available future slot.
2. A confirmed booking appears as Scheduled and links to the correct referral and patient.
3. An unavailable slot produces a conflict message and no saved appointment.
4. A timeout does not appear as a confirmed booking, and another attempt is blocked until its result is resolved.
5. Concurrent booking attempts cannot leave two active appointments for one referral.

## AC-A02: Change an appointment

For FR-A02:

1. A confirmed reschedule shows the new time and keeps the referral link.
2. A rejected reschedule leaves the original confirmed appointment unchanged.
3. A confirmed cancellation sets Canceled and records the requester and reason.
4. A missing reason produces an error without changing the appointment.
5. Completed, Canceled, and No-show appointments cannot be changed through this operation.

## AC-A03: Record appointment history

For FR-A03:

1. After a confirmed change, history shows the actor, time, reason, and old and new details.
2. A later change adds a new entry without replacing the earlier entry.
3. A failed change does not create a history entry claiming that the booking changed.

# Nonfunctional Requirements


| ID | Priority / quality | Requirement | Why it is needed / trace | Validation |
|---|---|---|---|---|
| NFR-A01 | 1. Security | Verify staff identity, scheduling permission, and patient access on every booking or change request. Unauthorized requests must make no booking or return patient details. | Domain Model access rule; FR-A01 and FR-A02. Appointments contain patient information. | Try signed-out, wrong-role, and unrelated-patient booking requests; verify denial and no external call. |
| NFR-A02 | 2. Concurrency and integrity | At most one confirmed active appointment or unresolved booking attempt may reserve a referral at a time. Save each confirmed local change and history entry together. | AC-A01.5 and AC-A03. Concurrent requests and partial history must not produce misleading bookings. | Run two simultaneous bookings and force a local transaction failure. |
| NFR-A03 | 3. Failure handling | Use a finite 10-second external-call timeout. A timeout must leave a visible unresolved attempt rather than a successful booking. Block another change until the result is reconciled. | FR-A01; AC-A01.4. A slow scheduler must not create a false confirmation. The timeout is a proposed project target. | Delay the scheduling response beyond 10 seconds and check unresolved status and blocked retry. |
| NFR-A04 | 4. Privacy | Use HTTPS outside local development and omit patient and booking details from ordinary diagnostic logs. | Domain Model patient and appointment objects. Scheduling should not expose care information. | Inspect deployed transport and logs for booking and cancellation attempts. |
| NFR-A05 | 5. Performance | For 20 simultaneous users and 10,000 appointments, 95% of local appointment reads must return within 2 seconds, excluding scheduling-service time. | FR-A01 and FR-A02. Staff need prompt access while arranging visits. | Measure local read responses at the stated test load. |
| NFR-A06 | 6. Usability | Clearly distinguish confirmed, failed, and unresolved booking results. Keep the entered change reason after a validation error. | AC-A01.3-4 and AC-A02.4. Staff must know whether an action succeeded. | Exercise rejection, timeout, and blank-reason cases and inspect displayed messages. |

# Non-goals

- Billing and insurance approval.
- Emergency triage and automated diagnosis.
- Referral review, task management, and reminder delivery are owned by the other CarePath functionalities.
