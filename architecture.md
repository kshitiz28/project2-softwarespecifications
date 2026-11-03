# 1. Overview

Patient Guidance and Communication in CarePath web application builds authorized care summaries from the other care modules and sends reminders through the existing notification provider using a simple periodic job inside the application.

# 2. Modules

Screen modules run in the browser; the other modules run in the CarePath server. The dependency column lists permitted uses of other CarePath modules, rather than runtime machines or external systems.

| Module | Responsibility | May depend on |
|---|---|---|
| Patient screens | Present accessible care summaries (FR-P01, FR-P03; NFR-P06). | Patient views |
| Access control | Decide which patient information the caller may see (FR-P03, FR-P04). | Persistence |
| Patient views | Assemble the permitted care summary (FR-P01, FR-P03). | Access control, Referral workflow, Appointment workflow, Task workflow |
| Reminder delivery | Coordinate scheduled reminder submissions (FR-P02). | Appointment workflow, Task workflow, Persistence |
| Persistence | Store authority, preferences, and notification attempts consistently (Domain Model; NFR-P03). | None within CarePath |


# 3. Request flow

**Main scenario: View care details (FR-P01, FR-P03, FR-P04; AC-P01, AC-P03, AC-P04).**

1. Patient screens request a summary using the signed-in session and selected patient identifier.
2. Access control verifies identity and patient access. For a representative it reloads the authority, checks time/scope/revocation, and determines permitted categories.
3. Patient views requests only those categories from the care modules. The care modules also honor the permitted patient context; the browser's submitted role or identifier is not trusted.
4. Patient views uses committed records to build the response and determines whether any patient action is outstanding. It generates no medical advice.
5. Patient screens display text status, last-update information, and required actions using labeled controls and keyboard focus. An unauthorized request returns no care information.

# 4. Design decisions

| Decision | Reason |
|---|---|
| Use the same application/database as the care modules. | **Preference:** simple direct access to the committed records needed by NFR-P04. |
| Recheck identity and representative authority at the server on each read. | FR-P03/FR-P04, AC-P03/AC-P04, NFR-P01. Previously loaded page data cannot authorize a later request. |
| Assemble summaries on request rather than maintaining a cache. | NFR-P04 and AC-P01 require current care data; the stated test load does not require a cache. |
| Run one simple periodic reminder function within the application. | FR-P02 and NFR-P03 require time-triggered behavior. No queue or additional deployed worker is needed at the proposed scale. |
| Scan every 30 seconds while running. | **Preference** to meet NFR-P03's 60-second submission target; the spec fixes no scan algorithm. |
| Use UTC server times; show user-facing times with a zone. | **Preference** for reminder comparisons; FR-P02 timing and authority validity require a consistent clock. |
| Atomically claim reminders using object identifier, current due/start time, reminder offset, and channel as the unique key. | AC-P02.2 and NFR-P03 prevent repeated/concurrent scans submitting the same reminder twice. |
| Recheck the latest care state immediately before calling the provider. | AC-P02.3–4 and NFR-P04 require suppression after cancellation/completion and replacement after rescheduling. |
| Keep pending/failed/uncertain delivery distinct from confirmed delivery. | AC-P02.6 and NFR-P03 forbid claiming success after a failure. No automatic retry policy is specified. |
| Use labeled controls, visible focus, and text status. | NFR-P06 makes these required accessibility checks, not optional styling. |

# 5. Constraints and known limits

- The technology-neutral proposal is one browser-based application, one relational database, and the already-required external notification provider.
- The reminder loop needs a continuously running application. A host that sleeps cannot satisfy NFR-P03 while asleep. Its timing target is explicitly conditional on application/provider availability.
- A database claim prevents duplicate local submission attempts. Exactly-once delivery across a provider timeout is not guaranteed without a provider idempotency/result-lookup contract; do not claim it from a local transaction alone.
- Changes committed after the final reminder-state check may race with external sending. Strict cancellation of an already-submitted message is not promised by the spec.
- The spec does not require multi-region availability, offline care data, an additional queue, or automatic recovery of missed reminders.
- The 20-user/10,000-record read target and 60-second reminder bound are proposed acceptance targets, not measured performance.

# 6. Out of scope

- Billing and insurance approval.
- Emergency triage and automated diagnosis.
- Referral decisions, appointment changes, and task assignment or completion are owned by the other CarePath functionalities.

