# 1. Overview

Follow-up and Task Management is part of the CarePath web application. It handles task assignment, document uploads, task completion, access checks, and task history. The system uses a server-side workflow and a relational database to manage this information.

# 2. Modules

The system is divided into modules based on their responsibilities. Task screens run in the browser, while the other modules run on the CarePath server.

| Module | Responsibility | May depend on |
|---|---|---|
| Task screens | Show task forms, task details, validation messages, and results (AC-T01–AC-T03; NFR-T06). | Task workflow |
| Access control | Check whether a user is allowed to view or change a task or document (Domain Model; NFR-T01). | Persistence |
| Task workflow | Handle task assignment, task completion, and task status rules (FR-T01–FR-T03). | Access control, Document validation, Persistence, Referral workflow |
| Document validation | Check whether an uploaded document meets the allowed file type and size limits (FR-T02; AC-T02). | None within CarePath |
| Persistence | Store task information, documents, completion data, and task history (FR-T03; NFR-T02). | None within CarePath |

Access control and Persistence can be used by other CarePath functions. Referral workflow provides referral information when a task is linked to a referral. Document validation uses the file type and size limits already configured by the organization.

# 3. Request flow

**Main scenario: Complete an assigned task (FR-T02; AC-T02).**

1. Task screens send the user's session, task identifier, and uploaded document to Task workflow.
2. Access control checks that the signed-in user is the patient assigned to the task before allowing the user to upload or view a document.
3. Document validation checks the file type and size on the server. If the file is invalid, it is rejected and not attached to the task.
4. If the file is valid, Persistence stores it and links it to the task. Uploading a document does not automatically complete the task.
5. When the patient selects **Mark complete**, Task workflow reloads the task and checks whether any required document has been uploaded.
6. Task workflow also checks the task's current status using the server clock.
7. Persistence then updates the unfinished task to Completed and records the change in task history within the same transaction.
8. If two completion requests happen at the same time, only one request can complete the task. The other request returns the existing completion information.
9. If the task is already Completed, the original completion time is returned and is not changed.
10. If the database transaction fails, the previous task state remains unchanged.

For task assignment, Task workflow checks that the instructions are not blank and that the due time is in the future before creating the task.

# 4. Design decisions

The specification does not require a specific programming language, framework, hosting platform, or authentication system. The following decisions describe how the requirements can be implemented.

| Decision | Reason |
|---|---|
| Store tasks in the CarePath application database. | This keeps task state and task history together and makes it easier to satisfy the atomic update requirement in NFR-T02. |
| Check identity and permissions on the server. | NFR-T01 and NFR-T03 require access checks for tasks and documents. Browser-only checks could be bypassed. |
| Validate task assignment before saving it. | FR-T01 and AC-T01 require nonblank instructions and a future due time. |
| Validate uploaded documents before attaching them to a task. | FR-T02 and AC-T02 require invalid files to be rejected without being attached. |
| Store supporting documents as protected records in the database. | This keeps document storage simple and avoids adding another storage service. |
| Complete a task and record its history in one transaction. | NFR-T02 requires the task state and history to stay consistent. |
| Use UTC and the server clock for task times. | NFR-T04 requires due-time and completion checks to use a reliable server time instead of the user's device clock. |
| Calculate Overdue status when a task is read or changed. | An unfinished task stays stored as Open but is shown as Overdue when the server time reaches or passes the due time. This avoids the need for a separate background process. |
| Check that a linked referral belongs to the same patient as the task. | The Domain Model requires the task patient and referral patient to match. |

# 5. Constraints and known limits

- The specification does not define a programming language, framework, hosting platform, or authentication system.
- Allowed file types and maximum upload size must come from the organization's configuration.
- Overdue status is calculated when the task is accessed. The design does not include continuous background updates, automatic escalation, or clinical action.
- Reminder functionality can read task information through Task workflow.
- If a database operation fails, the system does not confirm the task assignment or completion.
- The specification does not define database failover or recovery-time requirements.
- If document volume becomes large, a different document storage approach may be needed.
- The NFR response-time target applies to task metadata requests and does not include upload or download time.

# 6. Out of scope

- Billing and insurance approval.
- Emergency triage and automated diagnosis.
- Referral decisions.
- Appointment changes.
- Reminder delivery.

# Spec issues

- The specification does not give exact values for allowed upload types or maximum upload size.
- The specification does not say whether a Completed task can be reopened.
- The specification does not say whether an uploaded document can be replaced after task completion.
- The specification does not define how patient and staff identities or permissions are managed.
