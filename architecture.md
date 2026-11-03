# 1. Overview

CarePath uses one web application with a browser interface, server-side modules, and a shared relational database. This document covers Referral Management and Tracking.

# 2. Modules

Modules are units of implementation. Screen modules run in the browser; the other modules run in the CarePath server. The dependency column lists permitted uses of other CarePath modules, rather than runtime machines or external systems.

| Module            | Responsibility                                                                                    | May depend on                                  |
| ----------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Referral screens  | Present referral forms and results (FR-R01–FR-R05; AC-R01–AC-R05).                                | Referral workflow                              |
| Access control    | Decide whether the authenticated caller may perform the requested action (Domain Model; NFR-R01). | Persistence                                    |
| Referral workflow | Apply the referral lifecycle rules (FR-R01–FR-R05).                                               | Access control, Persistence                    |
| External updates  | Translate trusted external referral events (FR-R06).                                              | Access control, Referral workflow, Persistence |
| Persistence       | Save and retrieve referral records and history consistently (FR-R06; NFR-R02).                    | None within CarePath                           |

Access control and Persistence are shared with the other CarePath functionalities. External updates owns the connection to trusted healthcare systems. Module calls go through public interfaces; screens do not access database records directly.

# 3. Request flow

**Main scenario: Submit a referral (FR-R01; AC-R01).**

1. Referral screens send the submitted fields and the current sign-in session to Referral workflow.
2. Access control verifies the caller, provider role, and patient access before care data is returned or changed.
3. Referral workflow validates required fields and identifiers. On error, Referral screens display field errors and retain input (NFR-R05).
4. Persistence saves the referral and creation/status history in one transaction. The server supplies its identifier and UTC timestamps.
5. After commit, Referral workflow returns the saved result and Referral screens open Referral details. A failed commit returns an error without a partial submitted record.

# 4. Design decisions

| Decision                                                                                                    | Reason                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Use one server application and a relational database.                                                       | **Preference:** a simple way to provide the transactions required by NFR-R02.                                                                  |
| Authenticate through a verified server-side session and apply access checks inside the server.              | NFR-R01 and the Domain Model require identity and patient access checks. The session mechanism is a **preference**; a login/identity provider. |
| Use one transaction for a referral update and its history. Check the record version before saving a review. | NFR-R02; AC-R06 status history. Prevents partial updates and stale decisions.                                                                  |
| Give each external source/event pair a unique database key.                                                 | FR-R06 and AC-R06 duplicate update; avoids duplicate effects even under concurrency.                                                           |
| Use UTC server timestamps; format times in the browser with an explicit zone.                               | **Preference** supporting NFR-R02 history consistency.                                                                                         |
| Put uploaded file contents and metadata behind Persistence and Access control.                              | Domain Model documents and NFR-R03 privacy. Database binary storage is a **preference** suitable for a small project.                          |
| Filter referrals in the database using patient access and all selected conditions.                          | FR-R04 and AC-R04; avoids returning unauthorized records for client-side filtering.                                                            |
| Keep integration mappings in External updates. Use fixed events for tests.                                  | FR-R06 and NFR-R06 require testable supported mappings, not a live healthcare system during testing.                                           |

# 5. Constraints and known limits

- The NFR priorities and numerical targets in the updated spec are proposed targets, not measured results or a compliance certification.
- A real deployment needs organization-approved access assignments and integration/security arrangements (NFR-R01, NFR-R03).
- The single database is a shared failure point. Database failure returns an error; this design promises no automatic failover or quantified recovery time.
- Larger files or substantially higher load may justify different storage or deployment, but the present spec does not require those additions.
- The dependency upon other functionality modules.

# 6. Out of scope

- Billing and insurance approval.
- Emergency triage and automated diagnosis.
- Cross functionalities.
