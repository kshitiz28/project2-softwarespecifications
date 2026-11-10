# CarePath contracts

These are proposed Python and HTTP interfaces for the attached specification. HTTP status codes, JSON field names and fictional fixtures are contract choices. The skeleton does not implement acceptance behavior. No new product requirement is added.

## 1. Public Python interfaces

**Types.** `Record` is `dict[str, object]` with JSON-serializable values at the HTTP boundary. `Call` carries `authorization: str | None, path: dict[str, str], query: dict[str, str], body: bytes`. `Result(status: int, body: Record)` is a transport result. `Clock` is an injected zero-argument function returning an aware datetime; `IdFactory` maps an entity-kind string to an identifier. `Write(table: str, key: str, value: Record | None, expected: Record | None = None, require_absent: bool = False)` represents one mutation; a null value deletes a row. The optional expected value compares the prior row and require_absent reserves a key.

**Failure.** Every product-module method is currently a stub raising `NotImplementedError`. Implemented functions will return `Result` or raise `ContractError(status, error, message, field=None)` for the documented outcomes. The server serializes flat error JSON. Adapter timeouts may raise `TimeoutError`.

| Module / signature | Success | Failure | Spec trace | Injected |
|---|---|---|---|---|
| `task_screens.present(result: Record) -> str` | Render the permitted fields or validation result | NotImplementedError; future presentation handles only supplied result | AC-T01; Domain Model | Already-authorized view data; no storage access |
| `AccessControl.authorize(authorization: str \| None, action: str, patient_id: str \| None, *, store: Persistence, clock: Clock) -> Record` | Authorized actor id, role, patient or permitted categories | 401 unauthenticated; 403 forbidden | Domain Model; NFR-T01 | Persistence and server clock |
| `Persistence.get(table: str, key: str) -> Record \| None` | Stored row or None | 500 persistence_error | Domain Model; NFR-T02 | Database boundary, supplied by application factory |
| `Persistence.list(table: str) -> list[Record]` | Snapshot list; empty list if no rows | 500 persistence_error | Domain Model; NFR-T01 | Database boundary; authorization occurs in workflow |
| `Persistence.commit(writes: Sequence[Write]) -> None` | All mutations committed atomically | 409 write_conflict; 500 persistence_error; no partial writes | NFR-T02 | Database transaction boundary |
| `DocumentValidation.validate_document(data: bytes, media_type: str, policy: Record) -> None` | Accepted decoded bytes | 413 file_too_large or 415 unsupported_file_type | FR-T02; NFR-T03 | Configured allowed_types and max_bytes |
| `task_workflow.assign_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result` | 201: id, status, patient_id, nurse_id, due_at | 422 validation_error + field; 401 unauthenticated; 403 forbidden; 500 persistence_error | FR-T01; AC-T01; NFR-T01/T04/T06 | access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory |
| `task_workflow.list_tasks(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result` | 200: items list of authorized task records | 401 unauthenticated; 403 forbidden | FR-T01/T03; AC-T01; NFR-T01/T05 | access: AccessControl, store: Persistence, clock: Clock |
| `task_workflow.upload_document(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, validate_document: Callable[[bytes, str, Record], None]) -> Result` | 201: id, task_id, size_bytes | 413 file_too_large; 415 unsupported_file_type; 422 validation_error + field; 401 unauthenticated; 403 forbidden | FR-T02; AC-T02; NFR-T01/T03 | access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory, validate_document: Callable[[bytes, str, Record], None] |
| `task_workflow.get_document(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result` | 200: id, task_id, filename, content_base64 | 401 unauthenticated; 403 forbidden; 404 not_found after authorization | FR-T02; NFR-T01/T03 | access: AccessControl, store: Persistence, clock: Clock |
| `task_workflow.complete_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory) -> Result` | 200: id, status, completed_at (same for successful replay) | 422 document_required; 401 unauthenticated; 403 forbidden; 500 persistence_error | FR-T02/T03; AC-T02/T03; NFR-T01/T02/T04 | access: AccessControl, store: Persistence, clock: Clock, id_factory: IdFactory |
| `task_workflow.get_task(call: Call, *, access: AccessControl, store: Persistence, clock: Clock) -> Result` | 200: id, status, due_at, history; completed_at when completed | 401 unauthenticated; 403 forbidden; 404 not_found after authorization | FR-T03; AC-T03; NFR-T04/T05/T06 | access: AccessControl, store: Persistence, clock: Clock |
| `create_app(*, store: Persistence \| None = None, clock: Clock \| None = None, id_factory: IdFactory \| None = None, validate_document: Callable[[bytes, str, Record], None] \| None = None) -> FastAPI` | FastAPI server with the routes below | Invalid dependency setup is a wiring error, not an acceptance result | Transport scaffolding for the listed FR routes | Persistence, clock, identifiers and optional external callable |

## 2. REST APIs

Routes accept JSON bodies where listed and a Bearer credential. The skeleton hands raw request bytes to its public function so request parsing does not preempt the required 501. Once implemented, the workflow validates types and identifiers before changing state. All listed routes currently return HTTP 501 with `{"error":"not_implemented","message":"CarePath behavior is not implemented."}`.

| Method and path | Public function | Request | Intended result | Spec trace |
|---|---|---|---|---|
| POST `/tasks` | task_workflow.assign_task | JSON patient_id: str, instructions: str, due_at: ISO 8601 str with offset, document_required: bool; optional referral_id: str. | 201: id, status, patient_id, nurse_id, due_at | FR-T01; AC-T01; NFR-T01/T04/T06 |
| GET `/patients/{patient_id}/tasks` | task_workflow.list_tasks | Path patient_id: str. | 200: items list of authorized task records | FR-T01/T03; AC-T01; NFR-T01/T05 |
| POST `/tasks/{task_id}/documents` | task_workflow.upload_document | JSON filename: str, media_type: str, content_base64: str. Limits apply to decoded bytes. | 201: id, task_id, size_bytes | FR-T02; AC-T02; NFR-T01/T03 |
| GET `/tasks/{task_id}/documents/{document_id}` | task_workflow.get_document | Path task_id and document_id: str. | 200: id, task_id, filename, content_base64 | FR-T02; NFR-T01/T03 |
| POST `/tasks/{task_id}/complete` | task_workflow.complete_task | Empty JSON object; use already attached evidence. | 200: id, status, completed_at (same for successful replay) | FR-T02/T03; AC-T02/T03; NFR-T01/T02/T04 |
| GET `/tasks/{task_id}` | task_workflow.get_task | Path task_id: str. | 200: id, status, due_at, history; completed_at when completed | FR-T03; AC-T03; NFR-T04/T05/T06 |

## 3. Test fixtures and transport conventions

The tests only invoke documented HTTP routes and the application factory. They inject a Persistence double with the public get/list/commit signatures, a controlled clock and identifier generator, and external replies where applicable. The fixture can inspect its own records; no test-only application API is needed. A rejection has nonempty message and the listed error code (and field when applicable). Error precedence for multiple invalid conditions is open.

Test identity records are looked up by credential in identities. Each contains an actor id and role, and patient_id or patient_ids where relevant. Representative authority is keyed by representative and patient. Synthetic credentials include sender (referring provider), receiver and other-provider (receiving providers), coordinator, nurse, staff (scheduling staff), patient (p1), other-patient (p2), rep (representative), trusted (configured external source), untrusted (known but unconfigured external source), and reminder-service (internal caller). Staff in the fixtures have access to p1. The seeded records and expected state shapes are shown in test_plan.md and tests/cases.json. Fixture prefixes for generated ids are entity names such as referral, request, appointment, attempt, task, document, history, and notification. Tests set dates in UTC, do not contact real services, and compare only promised fields. List membership assertions do not impose ordering.

Validation injection: `Callable[[bytes, str, Record], None]`; production uses Document validation, and upload-policy fixture supplies the allowed_types and max_bytes. Optional referral linkage uses supplied referral records at this standalone boundary, with Referral workflow in the combined app.

Nonfunctional requirements reuse these routes or module boundaries. HTTPS, logs, browser behavior and load checks do not introduce REST endpoints. See test_plan.md for environment-dependent validation.
