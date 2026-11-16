# Implementation plan — Patient Guidance and Communication

Member: Sangam. Sources: the existing spec.md, architecture.md, contracts.md, test_plan.md, pytest cases and FastAPI skeleton. Planning only; application and test files are unchanged.

## Baseline and failures by criterion

Full run: `pytest_output.txt` (30 failed, 1 passed, 2 warnings). Each acceptance test failed on its expected HTTP result because the route returned 501. The smoke test passed.

| Criterion | Failing tests | Completed by slice |
|---|---:|---:|
| AC-P01 | 4 | 2 |
| AC-P02 | 12 | 8 |
| AC-P03 | 8 | 4 |
| AC-P04 | 6 | 3 |

Each test is listed once below, grouped under the criterion or scenario it exercises. An AC spanning several scenarios is completed only in its final contributing slice above. Earlier slices implement prerequisites, not a second completion of that AC. Routes and shared functions may recur because later slices extend them.

## Ordered implementation slices

### Slice 1: Show an owned care summary

- **Goal:** Return a patient’s authorized referral and related care records through one read route.
- **Spec sources:** FR-P01/FR-P04; NFR-P01/P04.
- **Criteria:** AC-P01.1.
- **Skeleton to fill in:** `patient_views.get_care_summary`, `AccessControl.authorize`, `Persistence.get`, `Persistence.list`. Existing routes: GET `/patients/{patient_id}/care-summary`.
- **Depends on:** None.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P01_1_summary`

### Slice 2: Complete recorded guidance

- **Goal:** Show the no-action message, use recorded guidance and reflect committed changes on the next read.
- **Spec sources:** FR-P01; NFR-P04/P06.
- **Criteria:** AC-P01.2–3 and freshness extra.
- **Skeleton to fill in:** `patient_views.get_care_summary`. Existing routes: GET `/patients/{patient_id}/care-summary`.
- **Depends on:** Slice 1.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P01_2_none`
- `test_AC_P01_3_guidance`
- `test_AC_P01_extra_freshness`

### Slice 3: Enforce direct-read authorization

- **Goal:** Deny missing credentials and cross-patient reads without disclosing care data.
- **Spec sources:** FR-P04; NFR-P01.
- **Criteria:** AC-P04.1–3.
- **Skeleton to fill in:** `patient_views.get_care_summary`, `AccessControl.authorize`. Existing routes: GET `/patients/{patient_id}/care-summary`.
- **Depends on:** Slice 2.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P04_1`
- `test_AC_P04_1_control`
- `test_AC_P04_2`
- `test_AC_P04_2_control`
- `test_AC_P04_3`
- `test_AC_P04_3_control`

### Slice 4: Scope representative access

- **Goal:** Reload authority on each request and return only allowed patient categories.
- **Spec sources:** FR-P03/FR-P04; NFR-P01.
- **Criteria:** AC-P03.1–3.
- **Skeleton to fill in:** `patient_views.get_care_summary`, `AccessControl.authorize`. Existing routes: GET `/patients/{patient_id}/care-summary`.
- **Depends on:** Slice 3.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P03_1_authority`
- `test_AC_P03_2_appt_only`
- `test_AC_P03_3_expired`
- `test_AC_P03_3_expired_control`
- `test_AC_P03_3_revoked`
- `test_AC_P03_3_revoked_control`
- `test_AC_P03_3_missing`
- `test_AC_P03_3_missing_control`

### Slice 5: Submit an eligible reminder

- **Goal:** Use the recorded channel at the configured time and record missing contact or timing settings.
- **Spec sources:** FR-P02; NFR-P02/P03.
- **Criteria:** AC-P02.1 and .5; early-timing extra.
- **Skeleton to fill in:** `reminder_delivery.run_reminders`, `AccessControl.authorize`, `Persistence.commit`. Existing routes: POST `/reminders/run`.
- **Depends on:** Slice 4.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P02_1_appointment`
- `test_AC_P02_1_task`
- `test_AC_P02_5_missing_contact`
- `test_AC_P02_5_missing_timing`
- `test_AC_P02_extra_early`

### Slice 6: Claim reminders once

- **Goal:** Make reminder submission safe against repeated and simultaneous scans.
- **Spec sources:** FR-P02; NFR-P03.
- **Criteria:** AC-P02.2 and concurrent-scan extra.
- **Skeleton to fill in:** `reminder_delivery.run_reminders`, `Persistence.commit`. Existing routes: POST `/reminders/run`.
- **Depends on:** Slice 5.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P02_2_deduplicate`
- `test_AC_P02_extra_concurrent`

### Slice 7: Suppress obsolete reminders

- **Goal:** Recheck committed care state before sending and use the replacement time after a reschedule.
- **Spec sources:** FR-P02; NFR-P04.
- **Criteria:** AC-P02.3–4.
- **Skeleton to fill in:** `reminder_delivery.run_reminders`. Existing routes: POST `/reminders/run`.
- **Depends on:** Slice 6.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P02_3_canceled`
- `test_AC_P02_3_completed`
- `test_AC_P02_4_reschedule`

### Slice 8: Record delivery outcomes

- **Goal:** Keep failed and uncertain delivery distinct from confirmed submission.
- **Spec sources:** FR-P02; NFR-P03.
- **Criteria:** AC-P02.6 and uncertain-delivery extra.
- **Skeleton to fill in:** `reminder_delivery.run_reminders`. Existing routes: POST `/reminders/run`.
- **Depends on:** Slice 7.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_P02_6_failure`
- `test_AC_P02_extra_uncertain`

## Coverage check

- Unassigned acceptance criteria: none.
- Unassigned failing tests: none.
- Unassigned REST routes: none.
- Contract stub outside these slices: `patient_screens.present` has no callable browser path or test in the supplied suite. The app factory and HTTP adapters already run and require no new entry points.
- Private stub `_unspecified_sender` is not a contract function. Live delivery requires the documented Sender binding; the test slices use the existing injection.
- Environment validation (load, HTTPS, logs and browser usability where applicable) stays in test_plan.md; it is not certified by passing API tests.

## Design questions

- For the default `Persistence` stub, confirm the relational database connection and schema setup supported by the existing contract. The tests inject a store; passing them alone does not make the default server persistent.
- Confirm real identity provisioning without adding endpoints; the thin path uses the documented fixture and existing AccessControl boundary.
- FR-P03: Confirm expiry equality, validity start, revocation provisioning and the identity mechanism.
- FR-P02/NFR-P03: Confirm provider result lookup, what happens to missed reminders after downtime, and the timing rule when a cancellation races an already submitted send.
- Architecture §2 refers to the care workflow interfaces; the standalone contract provides fixture records. Confirm combined-app integration and the existing sender binding.

## Test issues

- **Blocks the no-regression condition for Slice 1:** `test_all_contract_routes_return_501` asserts every route returns 501. The first green acceptance test must return a different status on that same route. Both cannot pass unchanged on a working skeleton. Before Task 2, ask whether to keep the smoke assertion as a baseline-only check with an explicit exception, or authorize a revised smoke contract that distinguishes implemented routes. Neither change is made in Task 1.
- `test_AC_P02_5_missing_contact` and `test_AC_P02_5_missing_timing` expect persisted Suppressed records. The AC requires recording a reason; its storage shape is a test/contract choice, not a spec guarantee.
- `test_AC_P02_extra_uncertain` expects no second send after an uncertain outcome. The architecture supports that conservative choice, but FR-P02/NFR-P03 do not define when uncertainty may be reconciled.
- `test_AC_P02_extra_concurrent` counts local provider calls. It cannot prove exactly-once external delivery or the 60-second timing target.

**Next action:** Start Show an owned care summary — `test_AC_P01_1_summary` after the smoke-test conflict is resolved.
