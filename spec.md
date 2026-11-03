# Description

This part of CarePath covers Follow-up and Task Management. Nurses assign clear actions to patients, and patients complete them or upload requested documents. Task progress is recorded separately from referral and appointment progress. Reminders are handled by the patient communication functionality.

# Goals

1. Support follow-up care after or between visits.
2. Help patients manage and complete their next steps.
3. Prevent delays caused by unfinished patient tasks.

# Domain Model

## Actors

- **Nurse:** Assigns tasks with instructions and due dates.
- **Patient:** Views and completes their assigned tasks.

## Objects

- **Follow-up task:** Identifier, patient, assigning nurse, instructions, due time, status, and optional referral link.
- **Document requirement:** Indicates whether the patient must upload a document before completion.
- **Supporting document:** Uploaded file, filename, uploader, upload time, and linked task.
- **Task history:** Records assignment, status changes, and completion time.
- **Referral:** Optional care context for the task; its patient must match the task's patient.

Task statuses are Open, Overdue, and Completed. An unfinished task becomes Overdue after its due time. Completing a task does not complete its referral. Users must be signed in and have permission for the patient and action. The organization configures allowed file types and the maximum upload size.

# Functional Requirements

This file uses must statements to keep task behavior direct and testable.

## FR-T01: Assign a follow-up task

CarePath must let an authorized nurse assign a patient a task with instructions, a future due time, and an indication of whether a document is required.

- Instructions must not be blank.
- Record the patient, nurse, due time, and initial status Open.
- Show the task in the patient's task list.

Supports Goals 1 and 3. Tested by AC-T01.

## FR-T02: Complete an assigned task

CarePath must let the assigned patient complete a task and upload a requested document when needed.

- A required document must be uploaded successfully before completion.
- Reject files outside the configured type or size limits.
- Set Completed and record the completion time.
- Repeating completion must not create another completion or change its original time.

Supports Goals 1 and 2. Tested by AC-T02.

## FR-T03: Track task progress

CarePath must show current task status and retain assignment and status-change history. An overdue task may still be completed. Task history must identify the actor and time of each change.

Supports Goals 2 and 3. Tested by AC-T03.

# Acceptance Criteria

All scenarios assume the actor is signed in and has permission unless stated otherwise.

## AC-T01: Task assignment

```gherkin
Feature: Assign a follow-up task
  Scenario: Assign a valid task
    Given a nurse can access a patient
    When the nurse enters instructions and a future due time
    And assigns the task to that patient
    Then CarePath creates an Open task with the nurse and patient recorded
    And shows it in the patient's task list

  Scenario: Invalid task details
    When the nurse submits blank instructions or a due time that is not in the future
    Then CarePath shows a validation error and does not create the task
```

## AC-T02: Task completion

```gherkin
Feature: Complete an assigned task
  Scenario: Complete a task with its document
    Given a patient opens their assigned document task
    When the patient uploads an allowed file and selects Mark complete
    Then the task becomes Completed
    And CarePath shows its completion time

  Scenario: A required document is missing
    Given a patient opens an Open task requiring a document
    When the patient selects Mark complete without the document
    Then CarePath explains that a document is required
    And the task remains Open

  Scenario: Invalid upload
    When a patient uploads an unsupported or oversized file
    Then CarePath rejects it without attaching it to the task

  Scenario: Repeat completion
    Given a task is already Completed
    When its patient repeats the completion action
    Then CarePath keeps the original completion and time
```

## AC-T03: Task progress

```gherkin
Feature: Track task progress
  Scenario: Complete an overdue task
    Given an unfinished task has passed its due time and is shown as Overdue
    When the patient completes it with any required document
    Then it becomes Completed
    And task history records the change, actor, and time
    And the linked referral is not automatically completed
```

# Nonfunctional Requirements

The following list is in priority order: 1 is highest. These are proposed project targets, not measured results. Each item traces to the existing specification and includes a validation check.

| ID | Priority / quality | Requirement | Why it is needed / trace | Validation |
|---|---|---|---|---|
| NFR-T01 | 1. Security | Check patient access and the permitted nurse/patient action on every task or document request. Only the assigned patient can complete the task. | FR-T01, FR-T02; Domain Model access rule. Tasks and documents belong to an identified patient. | Attempt assignment without nurse permission, completion by another patient, and an unauthorized document read. |
| NFR-T02 | 2. Data integrity | Task completion and its history must commit together. Concurrent or repeated completion must retain one original completion time and one completion transition. | FR-T02, FR-T03; AC-T02 repeat completion. Partial or duplicate results would misstate progress. | Send simultaneous completion requests and force a database failure. |
| NFR-T03 | 3. Privacy and upload safety | Use HTTPS outside local development. Enforce configured file size/type limits on the server and deny access to stored documents unless patient access is verified. | FR-T02; AC-T02 invalid upload. Browser-only restrictions cannot protect uploaded evidence. | Bypass browser validation and attempt an invalid upload and an unauthorized download. |
| NFR-T04 | 4. Time accuracy | Use the server clock and UTC instants for due/completion comparisons; display times with their time zone. At or after completion, preserve the original timestamp. | FR-T01 through FR-T03; AC-T03. Due times must not depend on a client clock or ambiguous local time. | Use test clocks before and after a deadline and clients in different time zones. |
| NFR-T05 | 5. Performance | For 20 simultaneous users and 10,000 tasks, 95% of task-list and task-detail requests must return within 2 seconds, excluding file transfer. | FR-T01 and FR-T03. Patients need timely access to assigned work. | Load-test task reads at the stated size and user count. |
| NFR-T06 | 6. Usability | Display instructions, due time, status, and whether a document is required together. Show a clear validation error while keeping entered task instructions. | AC-T01 invalid details and AC-T02 missing document. Users should know how to correct an incomplete task. | Inspect assignment errors and an incomplete document-task screen. |


# Non-goals

- Billing and insurance approval.
- Emergency triage and automated diagnosis.
- Referral decisions, appointment changes, and reminder delivery are owned by the other CarePath functionalities.
