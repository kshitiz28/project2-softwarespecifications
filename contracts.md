# CarePath contracts

Proposed Python and HTTP interfaces for the attached specification. HTTP status codes, JSON field names and fictional fixtures are contract choices. The skeleton does not implement acceptance behavior. No new product requirement is added.

## 1. Public Python interfaces

**Types.** `Record` is `dict[str, object]` with JSON-serializable values at the HTTP boundary. `Call` carries `authorization: str | None, path: dict[str, str], query: dict[str, str], body: bytes`. `Result(status: int, body: Record)` is a transport result. `Clock` is an injected zero-argument function returning an aware datetime; `IdFactory` maps an entity-kind string to an identifier. `Write(table: str, key: str, value: Record | None, expected: Record | None = None, require_absent: bool = False)` represents one mutation; a null value deletes a row. The optional expected value compares the prior row and require_absent reserves a key.

**Failure.** Every product-module method is currently a stub raising `NotImplementedError`. Implemented functions will return `Result` or raise `ContractError(status, error, message, field=None)` for the documented outcomes. The server serializes flat error JSON. Adapter timeouts may raise `TimeoutError`.

| Module / signature | Success | Failure | Spec trace | Injected |
|---|---|---|---|---|
| `patient_screens.present(result: Record) -> str` | Render the permitted fields or validation result | NotImplementedError; future presentation handles only supplied result | AC-P01; Domain Model | Already-authorized view data; no storage access |
| `AccessControl.authorize(authorization: str \| None, action: str, patient_id: str \| None, *, store: Persistence, clock: Clock) -> Record` | Authorized actor id, role, patient or permitted categories | 401 unauthenticated; 403 forbidden | Domain Model; NFR-P01 | Persistence and server clock |
| `Persistence.get(table: str, key: str) -> Record \| None` | Stored row or None | 500 persistence_error | Domain Model; NFR-P03 | Database boundary, supplied by application factory |
| `Persistence.list(table: str) -> list[Record]` | Snapshot list; empty list if no rows | 500 persistence_error | Domain Model; NFR-P01 | Database boundary; authorization occurs in workflow |
| `Persistence.commit(writes: Sequence[Write]) -> None` | All mutations committed atomically | 409 write_conflict; 500 persistence_error; no partial writes | NFR-P03 | Database transaction boundary |
| `patient_views.get_care_summary(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result` | 200: patient_id and permitted referrals/appointments/tasks; next_action when permitted; omit restricted categories | 401 unauthenticated; 403 forbidden; no care fields in either error | FR-P01/P03/P04; AC-P01/P03/P04; NFR-P01/P04/P05/P06 | access: AccessControl, store: Persistence, clock: Clock |
| `reminder_delivery.run_reminders(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, send: Sender) -> Result` | 200: submitted, skipped, failed counts; provider outcome persisted, not a claim of receipt | 401 unauthenticated; 403 forbidden; 500 persistence_error | FR-P02; AC-P02; NFR-P02/P03/P04 | access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, send: Sender |
| `create_app(*, store: Persistence \| None = None, clock: Clock \| None = None, id_factory: IdFactory \| None = None, send: Sender \| None = None) -> FastAPI` | FastAPI server with the routes below | Invalid dependency setup is a wiring error, not an acceptance result | Transport scaffolding for the listed FR routes | Persistence, clock, identifiers and optional external callable |

## 2. REST APIs

Routes accept JSON bodies where listed and a Bearer credential. The skeleton hands raw request bytes to its public function so request parsing does not preempt the required 501. Once implemented, the workflow validates types and identifiers before changing state. All listed routes currently return HTTP 501 with `{"error":"not_implemented","message":"CarePath behavior is not implemented."}`.

| Method and path | Public function | Request | Intended result | Spec trace |
|---|---|---|---|---|
| GET `/patients/{patient_id}/care-summary` | patient_views.get_care_summary | Path patient_id: str. Session identity and authority looked up on every read. | 200: patient_id and permitted referrals/appointments/tasks; next_action when permitted; omit restricted categories | FR-P01/P03/P04; AC-P01/P03/P04; NFR-P01/P04/P05/P06 |
| POST `/reminders/run` | reminder_delivery.run_reminders | Empty JSON object; internal service credential only. Clock and provider injected; no caller-provided scheduling time. | 200: submitted, skipped, failed counts; provider outcome persisted, not a claim of receipt | FR-P02; AC-P02; NFR-P02/P03/P04 |

## 3. Test fixtures and transport conventions

The tests only invoke documented HTTP routes and the application factory. They inject a Persistence double with the public get/list/commit signatures, a controlled clock and identifier generator, and external replies where applicable. The fixture can inspect its own records; no test-only application API is needed. A rejection has nonempty message and the listed error code (and field when applicable). Error precedence for multiple invalid conditions is open.

Test identity records are looked up by credential in identities. Each contains an actor id and role, and patient_id or patient_ids where relevant. Representative authority is keyed by representative and patient. Synthetic credentials include sender (referring provider), receiver and other-provider (receiving providers), coordinator, nurse, staff (scheduling staff), patient (p1), other-patient (p2), rep (representative), trusted (configured external source), untrusted (known but unconfigured external source), and reminder-service (internal caller). Staff in the fixtures have access to p1. The seeded records and expected state shapes are shown in test_plan.md and tests/cases.json. Fixture prefixes for generated ids are entity names such as referral, request, appointment, attempt, task, document, history, and notification. Tests set dates in UTC, do not contact real services, and compare only promised fields. List membership assertions do not impose ordering.

Notification injection: `Sender = Callable[[Record], Record]`; payload has channel, destination, object_id and a CarePath message; returns outcome submitted or failed, or raises TimeoutError. Care summaries use supplied care records at this standalone boundary; the combined application should use the existing care workflow interfaces. The internal reminder route must authorize the reminder-service credential before any send.

Nonfunctional requirements reuse these routes or module boundaries. HTTPS, logs, browser behavior and load checks do not introduce REST endpoints. See test_plan.md for environment-dependent validation.
