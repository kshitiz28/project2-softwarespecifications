# Implementation plan — Follow-up and Task Management

Sources: the existing spec.md, architecture.md, contracts.md, test_plan.md, pytest cases and FastAPI skeleton. Planning only; application and test files are unchanged.

## Baseline and failures by criterion

Full run: `pytest_output.txt` (29 failed, 1 passed, 2 warnings). Each acceptance test failed on its expected HTTP result because the route returned 501. The smoke test passed.

| Criterion | Failing tests | Completed by slice |
|---|---:|---:|
| AC-T01 | 10 | 2 |
| AC-T02 | 15 | 5 |
| AC-T03 | 4 | 6 |

Each test is listed once below, grouped under the criterion or scenario it exercises. An AC spanning several scenarios is completed only in its final contributing slice above. Earlier slices implement prerequisites, not a second completion of that AC. Routes and shared functions may recur because later slices extend them.

## Ordered implementation slices

### Slice 1: Read a patient’s empty task list

- **Goal:** Return an empty list for an authorized patient who has no tasks.
- **Spec sources:** FR-T01/FR-T03; NFR-T01.
- **Criteria:** AC-T01 extra: empty list.
- **Skeleton to fill in:** `task_workflow.list_tasks`, `AccessControl.authorize`, `Persistence.get`, `Persistence.list`. Existing routes: GET `/patients/{patient_id}/tasks`.
- **Depends on:** None.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_T01_extra_list_empty`

### Slice 2: Assign and list a task

- **Goal:** Validate the assignment and expose the saved Open task to the patient.
- **Spec sources:** FR-T01; NFR-T01/T04/T06.
- **Criteria:** AC-T01: valid assignment and invalid details; type extra; AC-T03 equivalent-offset extra.
- **Skeleton to fill in:** `task_workflow.assign_task`, `task_workflow.list_tasks`, `Persistence.commit`. Existing routes: POST `/tasks`; GET `/patients/{patient_id}/tasks`.
- **Depends on:** Slice 1.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_T01_assign`
- `test_AC_T01_instructions`
- `test_AC_T01_instructions_control`
- `test_AC_T01_due_at`
- `test_AC_T01_due_at_control`
- `test_AC_T01_due_at_past`
- `test_AC_T01_due_at_past_control`
- `test_AC_T01_due_at_type`
- `test_AC_T01_due_at_type_control`
- `test_AC_T03_extra_offset`

### Slice 3: Validate and protect task documents

- **Goal:** Apply configured upload limits and enforce ownership on evidence reads.
- **Spec sources:** FR-T02; NFR-T01/T03.
- **Criteria:** AC-T02: invalid upload; document-access extra.
- **Skeleton to fill in:** `task_workflow.upload_document`, `task_workflow.get_document`, `DocumentValidation.validate_document`, `AccessControl.authorize`. Existing routes: POST `/tasks/{task_id}/documents`; GET `/tasks/{task_id}/documents/{document_id}`.
- **Depends on:** Slice 2.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_T02_size`
- `test_AC_T02_size_control`
- `test_AC_T02_type`
- `test_AC_T02_type_control`
- `test_AC_T02_extra_document_access`
- `test_AC_T02_extra_document_access_control`

### Slice 4: Complete a task with valid evidence

- **Goal:** Check required evidence before completing a task and retain its first completion timestamp.
- **Spec sources:** FR-T02; NFR-T01/T02.
- **Criteria:** AC-T02: completion with document, missing document, repeat completion; identity extra.
- **Skeleton to fill in:** `task_workflow.complete_task`, `AccessControl.authorize`, `Persistence.commit`. Existing routes: POST `/tasks/{task_id}/complete`.
- **Depends on:** Slice 3.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_T02_evidence`
- `test_AC_T02_no_document`
- `test_AC_T02_no_document_control`
- `test_AC_T02_repeat`
- `test_AC_T02_extra_identity`
- `test_AC_T02_extra_identity_control`

### Slice 5: Make completion atomic

- **Goal:** Preserve one completion and history entry under concurrency or transaction failure.
- **Spec sources:** FR-T02/FR-T03; NFR-T02.
- **Criteria:** AC-T02 extras: concurrent completion and rollback.
- **Skeleton to fill in:** `task_workflow.complete_task`, `Persistence.commit`. Existing routes: POST `/tasks/{task_id}/complete`.
- **Depends on:** Slice 4.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_T02_extra_rollback`
- `test_AC_T02_extra_rollback_control`
- `test_AC_T02_extra_concurrent`

### Slice 6: Show and complete overdue tasks

- **Goal:** Use the server clock for status reads and preserve referral state when recording completion.
- **Spec sources:** FR-T03; NFR-T04/T05.
- **Criteria:** AC-T03: overdue completion; before/after deadline extras.
- **Skeleton to fill in:** `task_workflow.get_task`, `task_workflow.complete_task`. Existing routes: GET `/tasks/{task_id}`; POST `/tasks/{task_id}/complete`.
- **Depends on:** Slice 5.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_T03_overdue`
- `test_AC_T03_extra_clock_before`
- `test_AC_T03_extra_clock_after`

## Coverage check

- Unassigned acceptance criteria: none.
- Unassigned failing tests: none.
- Unassigned REST routes: none.
- Contract stub outside these slices: `task_screens.present` has no callable browser path or test in the supplied suite. The app factory and HTTP adapters already run and require no new entry points.
- Environment validation (load, HTTPS, logs and browser usability where applicable) stays in test_plan.md; it is not certified by passing API tests.

## Design questions

- For the default `Persistence` stub, confirm the relational database connection and schema setup supported by the existing contract. The tests inject a store; passing them alone does not make the default server persistent.
- Confirm real identity provisioning without adding endpoints; the thin path uses the documented fixture and existing AccessControl boundary.
- FR-T02/NFR-T03: Confirm production file limits, type detection rules and retention. Fixture limits alone do not define these.
- FR-T03: Confirm how background overdue changes, if any, are materialized and who is recorded as actor. Verify how the existing referral lookup is supplied without adding a new interface.

## Test issues

- **Blocks the no-regression condition for Slice 1:** `test_all_contract_routes_return_501` asserts every route returns 501. The first green acceptance test must return a different status on that same route. Both cannot pass unchanged on a working skeleton. Before Task 2, ask whether to keep the smoke assertion as a baseline-only check with an explicit exception, or authorize a revised smoke contract that distinguishes implemented routes. Neither change is made in Task 1.
- `test_AC_T02_evidence` and `test_AC_T02_size_control` use a short PDF marker as an allowed payload. They exercise type/size policy, but FR-T02 does not say whether full PDF validity is required.
- `test_AC_T03_extra_offset` uses the assignment route although labeled AC-T03. It belongs with assignment because it checks NFR-T04 normalization on write.

**Next action:** Start Read a patient’s empty task list — `test_AC_T01_extra_list_empty` after the smoke-test conflict is resolved.
