# Appointment Management — Implementation Plan

## Implementation slices

### Slice 1: View eligible appointment slots

- **Name:** View eligible appointment slots
- **Goal:** Return available future slots for an authorized staff member and accepted referral.
- **Spec sources:** FR-A01; AC-A01.1; Domain Model; NFR-A01.
- **Criteria:** AC-A01.1.
- **Tests that should turn green:** `test_AC_A01_1_slots`.
- **Skeleton to fill in:** `GET /referrals/{referral_id}/appointment-slots; appointment_workflow.list_slots; AccessControl.authorize (uses the injected Persistence.get boundary)`.
- **Depends on:** None.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** implemented.

### Slice 2: Confirm an appointment

- **Name:** Confirm an appointment
- **Goal:** Book a selected available future slot and persist a confirmed appointment atomically.
- **Spec sources:** FR-A01; AC-A01.2; FR-A03 (initial confirmed record); NFR-A02.
- **Criteria:** AC-A01.2.
- **Tests that should turn green:** `test_AC_A01_2_book`.
- **Skeleton to fill in:** `POST /referrals/{referral_id}/appointments; appointment_workflow.book_appointment (uses injected Persistence.get/list/commit)`.
- **Depends on:** 1.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** implemented.

### Slice 3: Reject unauthorized booking

- **Name:** Reject unauthorized booking
- **Goal:** Enforce staff-only scheduling and patient scope before any external booking.
- **Spec sources:** NFR-A01; FR-A01; Domain Model.
- **Criteria:** extra: NFR-A01 role restriction.
- **Tests that should turn green:** `test_AC_A01_extra_role`, `test_AC_A01_extra_role_control`.
- **Skeleton to fill in:** `POST /referrals/{referral_id}/appointments; AccessControl.authorize; appointment_workflow.book_appointment`.
- **Depends on:** 1, 2.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 4: Validate referral and slot

- **Name:** Validate referral and slot
- **Goal:** Reject ineligible referrals and non-future slots without booking or persistence changes.
- **Spec sources:** FR-A01; NFR-A01.
- **Criteria:** extra: FR-A01 referral eligibility and future slot boundaries.
- **Tests that should turn green:** `test_AC_A01_extra_referral_state`, `test_AC_A01_extra_referral_state_control`, `test_AC_A01_extra_slot_boundary`, `test_AC_A01_extra_slot_boundary_control`.
- **Skeleton to fill in:** `POST /referrals/{referral_id}/appointments; appointment_workflow.book_appointment`.
- **Depends on:** 2, 3.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 5: Unavailable external slot

- **Name:** Unavailable external slot
- **Goal:** Translate a rejected scheduler booking into a conflict with no saved appointment.
- **Spec sources:** FR-A01; AC-A01.3; NFR-A06.
- **Criteria:** AC-A01.3.
- **Tests that should turn green:** `test_AC_A01_3_unavailable`, `test_AC_A01_3_unavailable_control`.
- **Skeleton to fill in:** `POST /referrals/{referral_id}/appointments; appointment_workflow.book_appointment; Persistence.commit`.
- **Depends on:** 2, 4.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 6: Unresolved timeout and reconciliation

- **Name:** Unresolved timeout and reconciliation
- **Goal:** Keep timed-out attempts unresolved, block retries and reconcile using the same attempt identifier.
- **Spec sources:** FR-A01; AC-A01.4; NFR-A03.
- **Criteria:** AC-A01.4.
- **Tests that should turn green:** `test_AC_A01_4_timeout`, `test_AC_A01_4_control`.
- **Skeleton to fill in:** `POST /referrals/{referral_id}/appointments and POST /booking-attempts/{attempt_id}/reconcile; appointment_workflow.book_appointment/reconcile_attempt; Persistence.get/list/commit`.
- **Depends on:** 2, 5.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 7: Active-booking integrity and concurrency

- **Name:** Active-booking integrity and concurrency
- **Goal:** Prevent simultaneous or repeated booking from leaving two active appointments for one referral.
- **Spec sources:** FR-A01; AC-A01.5; NFR-A02.
- **Criteria:** AC-A01.5, extra: AC-A01.5 existing active booking.
- **Tests that should turn green:** `test_AC_A01_5_concurrent`, `test_AC_A01_5_extra_active`, `test_AC_A01_5_extra_active_control`.
- **Skeleton to fill in:** `POST /referrals/{referral_id}/appointments; appointment_workflow.book_appointment (uses injected Persistence.get/list/commit)`.
- **Depends on:** 2, 6.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 8: Confirmed reschedule

- **Name:** Confirmed reschedule
- **Goal:** Change an existing Scheduled appointment only after external replacement confirmation.
- **Spec sources:** FR-A02; AC-A02.1.
- **Criteria:** AC-A02.1.
- **Tests that should turn green:** `test_AC_A02_1_reschedule`.
- **Skeleton to fill in:** `PATCH /appointments/{appointment_id}; appointment_workflow.change_appointment; AccessControl.authorize; Persistence.get/commit`.
- **Depends on:** 2, 7.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 9: Rejected reschedule and no false history

- **Name:** Rejected reschedule and no false history
- **Goal:** Preserve the previous appointment and its history when the replacement is unavailable.
- **Spec sources:** FR-A02; FR-A03; AC-A02.2; AC-A03.3.
- **Criteria:** AC-A02.2, AC-A03.3.
- **Tests that should turn green:** `test_AC_A02_2_rejected`, `test_AC_A02_2_rejected_control`, `test_AC_A03_3_no_false_history`, `test_AC_A03_3_no_false_history_control`.
- **Skeleton to fill in:** `PATCH /appointments/{appointment_id}; appointment_workflow.change_appointment; Persistence.get/commit`.
- **Depends on:** 8.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 10: Cancellation and change reason

- **Name:** Cancellation and change reason
- **Goal:** Require a nonblank reason and confirm a cancellation while preserving its referral.
- **Spec sources:** FR-A02; AC-A02.3; AC-A02.4; NFR-A06.
- **Criteria:** AC-A02.3, AC-A02.4, extra: FR-A02 reason type.
- **Tests that should turn green:** `test_AC_A02_3_cancel`, `test_AC_A02_4_reason`, `test_AC_A02_4_reason_control`, `test_AC_A02_extra_type`, `test_AC_A02_extra_type_control`.
- **Skeleton to fill in:** `PATCH /appointments/{appointment_id}; appointment_workflow.change_appointment; Persistence.get/commit`.
- **Depends on:** 8, 9.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 11: Terminal appointment state protections

- **Name:** Terminal appointment state protections
- **Goal:** Reject edits to Completed, Canceled and No-show appointments without external side effects.
- **Spec sources:** FR-A02; AC-A02.5.
- **Criteria:** AC-A02.5.
- **Tests that should turn green:** `test_AC_A02_5_completed`, `test_AC_A02_5_completed_control`, `test_AC_A02_5_canceled`, `test_AC_A02_5_canceled_control`, `test_AC_A02_5_no_show`, `test_AC_A02_5_no_show_control`.
- **Skeleton to fill in:** `PATCH /appointments/{appointment_id}; appointment_workflow.change_appointment; Persistence.get/list`.
- **Depends on:** 10.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

### Slice 12: Read append-only change history

- **Name:** Read append-only change history
- **Goal:** Return actor, timestamp, reason, old/new booking details and retain subsequent change entries.
- **Spec sources:** FR-A03; AC-A03.1; AC-A03.2; NFR-A02.
- **Criteria:** AC-A03.1, AC-A03.2.
- **Tests that should turn green:** `test_AC_A03_1_history`, `test_AC_A03_2_append`.
- **Skeleton to fill in:** `GET /appointments/{appointment_id}/history and PATCH /appointments/{appointment_id}; appointment_workflow.get_appointment_history/change_appointment; Persistence.get/list/commit`.
- **Depends on:** 9, 10.
- **Done when:** The listed tests pass and no previously passing test fails.
- **Status:** not started.

## Coverage check

- **Unassigned acceptance criteria:** None. All 13 acceptance criteria are assigned to exactly one slice.
- **Unassigned failing tests:** None. All 33 failing acceptance tests are assigned to exactly one slice.
- **Functions or routes with no slice:** `appointment_screens.present` and `SchedulingAdapter.request` are not assigned to an implementation slice. All five API routes and appointment workflow functions are assigned.

## Design questions

1. Which identity service will provide authenticated actors and patient authorization?
2. Which external scheduling service will implement the `SchedulingAdapter.request` contract?
3. Which persistence backend will enforce appointment uniqueness and concurrency guarantees?
4. How will `appointment_screens.present` be connected to the application UI?

## Test issues

- `tests/test_skeleton.py::test_all_contract_routes_return_501` expects all routes to return HTTP 501, which conflicts with implementing those routes.
- The history append test expects a `history` record containing an `items` array; the required storage representation should be confirmed against the contracts.

**Next action:** Slice 1, View eligible appointment slots — `test_AC_A01_1_slots`.
