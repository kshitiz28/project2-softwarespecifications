# Description

This part of CarePath covers Appointment Management. Administrative staff arrange appointments for accepted referrals and manage changes. Each appointment stays linked to the correct patient and referral. Referral decisions, patient tasks and reminder delivery are handled by the other team members.

# Goals

1. Keep care visits organized.
2. Help patients receive the service requested by their referral.
3. Maintain continuity of care through accurate appointment information.

# Domain Model

## Actors

- **Administrative staff member:** Schedules, reschedules, and cancels appointments.
- **Patient:** The person attending the appointment.
- **Receiving provider:** The provider delivering the referred service.

## Objects

- **Referral:** Identifies the patient, receiving provider, and referral status.
- **Appointment:** Identifier, referral, patient, provider, date, time, location, status, and external booking identifier.
- **Available slot:** A future appointment time offered by the scheduling system.
- **Appointment change:** Requester, reason and previous and new booking details.
- **Change history:** A record of confirmed booking changes.

The external scheduling system confirms bookings and changes. An appointment can be Scheduled, Canceled, Completed, or No-show. Only Scheduled appointments can be changed. A referral may have at most one active appointment. Users must be signed in and have permission for the patient and action.

# Functional Requirements

This file uses must statements instead of user stories to describe the same appointment functionality.

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

CarePath must retain who changed an appointment, when, the reason, and the old and new booking details. Existing history must not be overwritten by a later change.

Supports Goals 1 and 3. Tested by AC-A03.

# Acceptance Criteria

These criteria use short checklists instead of Gherkin scripts.

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
