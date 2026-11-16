# Implementation plan — Referral Management and Tracking

Member: Kshitiz. Sources: the existing spec.md, architecture.md, contracts.md, test_plan.md, pytest cases and FastAPI skeleton. Planning only; application and test files are unchanged.

## Baseline and failures by criterion

Full run: `pytest_output.txt` (37 failed, 1 passed, 2 warnings). Each acceptance test failed on its expected HTTP result because the route returned 501. The smoke test passed.

| Criterion | Failing tests | Completed by slice |
|---|---:|---:|
| AC-R01 | 13 | 2 |
| AC-R02 | 7 | 4 |
| AC-R03 | 3 | 5 |
| AC-R04 | 1 | 7 |
| AC-R05 | 5 | 6 |
| AC-R06 | 8 | 9 |

Each test is listed once below, grouped under the criterion or scenario it exercises. An AC spanning several scenarios is completed only in its final contributing slice above. Earlier slices implement prerequisites, not a second completion of that AC. Routes and shared functions may recur because later slices extend them.

## Ordered implementation slices

### Slice 1: Submit a valid referral

- **Goal:** Take one authorized submission through validation, storage and HTTP 201.
- **Spec sources:** FR-R01; NFR-R01/R02.
- **Criteria:** AC-R01: complete submission.
- **Skeleton to fill in:** `referral_workflow.submit_referral`, `AccessControl.authorize`, `Persistence.get`, `Persistence.commit`. Existing routes: POST `/referrals`.
- **Depends on:** None.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R01_submit`

### Slice 2: Reject invalid referral input

- **Goal:** Return field errors before writing any referral or history.
- **Spec sources:** FR-R01; NFR-R05.
- **Criteria:** AC-R01: missing required information; wrong-type extra.
- **Skeleton to fill in:** `referral_workflow.submit_referral`. Existing routes: POST `/referrals`.
- **Depends on:** Slice 1.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R01_missing_patient_id`
- `test_AC_R01_missing_patient_id_control`
- `test_AC_R01_missing_receiving_provider_id`
- `test_AC_R01_missing_receiving_provider_id_control`
- `test_AC_R01_missing_service`
- `test_AC_R01_missing_service_control`
- `test_AC_R01_missing_reason`
- `test_AC_R01_missing_reason_control`
- `test_AC_R01_missing_urgency`
- `test_AC_R01_missing_urgency_control`
- `test_AC_R01_extra_type`
- `test_AC_R01_extra_type_control`

### Slice 3: Record a referral decision

- **Goal:** Save an authorized decision and expose its audit history.
- **Spec sources:** FR-R02, FR-R06; NFR-R01/R02.
- **Criteria:** AC-R02: acceptance and missing redirection destination; AC-R06: status-change history.
- **Skeleton to fill in:** `referral_workflow.review_referral`, `referral_workflow.get_referral`, `Persistence.list`. Existing routes: POST `/referrals/{referral_id}/reviews`; GET `/referrals/{referral_id}`.
- **Depends on:** Slice 1.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R02_accept`
- `test_AC_R02_redirect_missing`
- `test_AC_R02_redirect_missing_control`
- `test_AC_R06_history`

### Slice 4: Protect review writes

- **Goal:** Reject unauthorized or stale reviews and roll back a failed commit.
- **Spec sources:** FR-R02, FR-R06; NFR-R01/R02.
- **Criteria:** Extras for AC-R02 and AC-R06: identity, stale version, rollback.
- **Skeleton to fill in:** `referral_workflow.review_referral`, `AccessControl.authorize`, `Persistence.commit`. Existing routes: POST `/referrals/{referral_id}/reviews`.
- **Depends on:** Slice 3.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R02_extra_stale`
- `test_AC_R02_extra_stale_control`
- `test_AC_R02_extra_identity`
- `test_AC_R02_extra_identity_control`
- `test_AC_R06_extra_rollback`
- `test_AC_R06_extra_rollback_control`

### Slice 5: Share visit findings

- **Goal:** Save final findings and let the referring provider read the completed result.
- **Spec sources:** FR-R03; NFR-R03.
- **Criteria:** AC-R03: final findings; blank text extra.
- **Skeleton to fill in:** `referral_workflow.share_findings`, `referral_workflow.get_referral`. Existing routes: POST `/referrals/{referral_id}/findings`; GET `/referrals/{referral_id}`.
- **Depends on:** Slice 3.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R03_share`
- `test_AC_R03_extra_blank`
- `test_AC_R03_extra_blank_control`

### Slice 6: Request missing information

- **Goal:** Create a request, authorize the selected responder and link the response.
- **Spec sources:** FR-R05; NFR-R01/R03/R05.
- **Criteria:** AC-R05: send and track; missing recipient; wrong responder extra.
- **Skeleton to fill in:** `referral_workflow.request_information`, `referral_workflow.respond_to_information_request`, `referral_workflow.get_referral`, `AccessControl.authorize`. Existing routes: POST `/referrals/{referral_id}/information-requests`; POST `/referrals/{referral_id}/information-requests/{request_id}/response`; GET `/referrals/{referral_id}`.
- **Depends on:** Slice 3.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R05_roundtrip`
- `test_AC_R05_missing_recipient`
- `test_AC_R05_missing_recipient_control`
- `test_AC_R05_extra_recipient`
- `test_AC_R05_extra_recipient_control`

### Slice 7: Filter referrals needing attention

- **Goal:** Apply all filters to the coordinator’s accessible referrals.
- **Spec sources:** FR-R04; NFR-R04.
- **Criteria:** AC-R04: combined filters.
- **Skeleton to fill in:** `referral_workflow.list_referrals`. Existing routes: GET `/referrals`.
- **Depends on:** Slice 6.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R04_filters`

### Slice 8: Apply external referral updates

- **Goal:** Apply trusted mapped events and flag unknown mappings without overwriting referral state.
- **Spec sources:** FR-R06; NFR-R01/R02/R06.
- **Criteria:** AC-R06: unmapped status; untrusted source extra.
- **Skeleton to fill in:** `external_updates.apply_external_event`, `AccessControl.authorize`, `Persistence.commit`. Existing routes: POST `/referral-events`.
- **Depends on:** Slice 4.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R06_unmapped`
- `test_AC_R06_extra_untrusted`
- `test_AC_R06_extra_untrusted_control`

### Slice 9: Deduplicate external events

- **Goal:** Keep one state change and history entry across replay and simultaneous delivery.
- **Spec sources:** FR-R06; NFR-R02.
- **Criteria:** AC-R06: duplicate update; concurrency extra.
- **Skeleton to fill in:** `external_updates.apply_external_event`, `Persistence.commit`. Existing routes: POST `/referral-events`.
- **Depends on:** Slice 8.
- **Done when:** All tests below pass and no previously passing test fails. See the smoke-test blocker below.
- **Status:** not started.

**Tests that should turn green:**

- `test_AC_R06_duplicate`
- `test_AC_R06_extra_concurrent`

## Coverage check

- Unassigned acceptance criteria: none.
- Unassigned failing tests: none.
- Unassigned REST routes: none.
- Contract stub outside these slices: `referral_screens.present` has no callable browser path or test in the supplied suite. The app factory and HTTP adapters already run and require no new entry points.
- Environment validation (load, HTTPS, logs and browser usability where applicable) stays in test_plan.md; it is not certified by passing API tests.

## Design questions

- For the default `Persistence` stub, confirm the relational database connection and schema setup supported by the existing contract. The tests inject a store; passing them alone does not make the default server persistent.
- Confirm real identity provisioning without adding endpoints; the thin path uses the documented fixture and existing AccessControl boundary.
- FR-R04: Decide whether an age of exactly 24 hours qualifies; tests only bracket the threshold.
- FR-R02/FR-R05: Confirm the legal transition rules, successful redirection handoff, and whether a request or response changes referral status.
- FR-R06: Confirm the production trust mechanism, mapping and out-of-order event policy before integrating a live source.
- FR-R01/FR-R05: Confirm referral document limits and how supporting-document IDs are provisioned.

## Test issues

- **Blocks the no-regression condition for Slice 1:** `test_all_contract_routes_return_501` asserts every route returns 501. The first green acceptance test must return a different status on that same route. Both cannot pass unchanged on a working skeleton. Before Task 2, ask whether to keep the smoke assertion as a baseline-only check with an explicit exception, or authorize a revised smoke contract that distinguishes implemented routes. Neither change is made in Task 1.
- `test_AC_R02_redirect_missing_control` expects the visible status Redirected. FR-R02 names redirection and its validation, but does not define handoff or a subsequent state; the test is not evidence for either.
- `test_AC_R06_history` compares a one-entry history fixture. FR-R06 requires preserving changes; this test does not establish how a real record with prior history should be ordered.

**Next action:** Start Submit a valid referral — `test_AC_R01_submit` after the smoke-test conflict is resolved.
