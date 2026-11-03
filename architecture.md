# 1. Overview

Appointment Management runs inside the same CarePath web application as the other functionalities. Its server-side workflow owns booking operations, while a small adapter communicates with the external scheduling system and the shared relational database stores local results.

# 2. Modules

| Module | Responsibility | May depend on |
|---|---|---|
| Appointment screens | Present appointment choices and operation results (AC-A01, AC-A02). | Appointment workflow |
| Access control | Decide whether the caller may perform a booking action (Domain Model; NFR-A01). | Persistence |
| Appointment workflow | Coordinate the appointment lifecycle (FR-A01–FR-A03). | Access control, Scheduling adapter, Persistence; Referral workflow for eligible-referral lookup |
| Scheduling adapter | Translate booking requests and scheduler responses (FR-A01, FR-A02). | None within CarePath |
| Persistence | Store booking attempts, appointments, and history consistently (FR-A03; NFR-A02). | None within CarePath |

# 3. Request flow

**Main scenario: Book an appointment (FR-A01; AC-A01).**

1. Appointment screens send the chosen slot, referral identifier, and sign-in session to Appointment workflow.
2. Access control verifies staff identity, scheduling permission, and patient access before any scheduling call.
3. Appointment workflow checks the referral's eligibility through Referral workflow. Persistence atomically reserves a booking attempt against the referral; a uniqueness rule rejects another active booking or unresolved attempt.
4. Scheduling adapter submits the attempt identifier and slot to the external scheduler. No database transaction is held open during the network call.
5. After confirmation, Persistence commits the confirmed appointment and its history together. Only then do Appointment screens show Scheduled.
6. A rejection releases the local reservation and displays a conflict. A timeout or unknown outcome retains an unresolved attempt and blocks another attempt (NFR-A03).
7. Reconciliation queries the scheduler using the attempt identifier before permitting a new attempt. This requires the external contract described in Spec issues; a blind retry is not safe.

# 4. Design decisions

No fixed language, framework, or hosting choice was supplied. Technology choices below are proposed preferences; each behavioral choice refers to its supporting section in spec.md.

| Decision | Reason |
|---|---|
| Share one application and relational database with the other CarePath functionalities. | **Preference:** avoids separate deployments while supporting NFR-A02 transactions and concurrency. |
| Keep identity and patient access decisions in server-side Access control. | Domain Model and NFR-A01; client-side checks would not cover direct requests. A verified server session is a **preference**, pending the identity system choice. |
| Reserve attempts using database uniqueness and atomic updates before contacting the scheduler. | AC-A01.5 and NFR-A02 require protection across concurrent staff requests. A browser-only lock cannot enforce this. |
| Persist an unresolved attempt and use scheduler lookup rather than blindly retrying. | FR-A01 and AC-A01.4; an external timeout does not establish whether booking succeeded. |
| Apply the 10-second network timeout inside Scheduling adapter. | NFR-A03 explicitly sets the proposed limit; the workflow owns its unresolved-result handling. |
| Use database transactions for local changes and history, not a distributed transaction with the scheduler. | NFR-A02 and AC-A03; local transaction choice is a **preference**. The external system must provide lookup/replacement support. |
| Store UTC instants and display the appointment's explicit time zone. | **Preference** for unambiguous booking times; Domain Model date/time and AC-A01 future-slot validation require a comparison basis. |
| Keep the original booking during a failed replacement. | FR-A02 and AC-A02.2. Requires the scheduler operation described under Spec issues. |

# 5. Constraints and known limits

- No implementation language, framework, hosting platform, or scheduling product was supplied. The proposed shape is a browser, one server application, and a relational database.
- Scheduling is externally controlled. Local database constraints prevent duplicate local attempts; they cannot guarantee an external booking contract that the provider does not offer.
- An unavailable scheduler prevents confirmed booking changes. A local pending attempt must not be presented as success.
- If the scheduler confirms a booking but the local save fails, retain the unresolved attempt and reconcile with the scheduler. Local rollback alone cannot undo the external booking.
- The proposed 20-user/10,000-record target is a test workload, not a measured capacity guarantee. Growth would require measurement before adding infrastructure.

# 6. Out of scope

- Billing and insurance approval.
- Emergency triage and automated diagnosis.
- Referral review, task management and reminder delivery

# Spec issues

- The scheduling API contract is missing. It must define stable request identifiers, booking-result lookup, and replacement/cancellation behavior. If it cannot preserve the original booking until replacement confirmation, FR-A02 is not achievable with the assumed operation.
- The spec does not define how completed/no-show states arrive from the scheduler or how out-of-order booking updates are handled.
- Staff/patient permission assignments and the actual identity system are not defined.
