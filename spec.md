# Description

CarePath supports Patient Guidance and Communication. Patients see referral progress and next steps and receive care reminders. Personal representatives can view information within their recorded authority. The other functionalities provide the referral, appointment, and task information. It presents provider-entered guidance and does not generate medical advice.

# Goals

1. Help patients manage their care and understand next steps.
2. Help personal representatives support the patient.
3. Support follow-up care through timely reminders.

# Domain Model

## Actors

- **Patient:** Views their care information and receives reminders.
- **Personal representative:** Views permitted information for a patient within recorded authority.
- **Healthcare staff:** Maintain the referral, appointment, and task information shown to patients.

## Objects

- **Referral summary:** Current status, last-update time, destination provider, and outstanding information requests.
- **Appointment details:** Confirmed time, provider, location, and status.
- **Task summary:** Instructions, due time, status, and required action.
- **Representative authority:** Patient, representative, permitted information, and validity period.
- **Notification:** Recipient, appointment or task, delivery channel, scheduled time, and delivery result.
- **Contact preference:** The patient's recorded communication channel and contact details.

Users must be signed in before viewing care details. Patients see only their own records. Representatives may view only information covered by active authority; this does not grant permission to change records. Reminder timing is configured by the organization, and contact details come from the patient's recorded preference.

# Functional Requirements

## FR-P01: View referral status and next steps

As a patient, I want to view my referral status and next required action in CarePath, so that I can know and complete my next steps.

Show current status, last update, outstanding requests, unfinished tasks, and any active appointment. If no patient action is needed, say so clearly. Supports Goal 1. Tested by AC-P01.

## FR-P02: Receive care reminders

As a patient, I want to receive CarePath reminders for upcoming appointments and due tasks, so that I can know and complete my next steps.

Use the organization's configured timing and the patient's preferred channel. Record delivery results. Do not send reminders for canceled appointments or completed tasks, or send the same scheduled reminder twice. Email and text messages direct patients to CarePath without including clinical findings or documents. Supports Goals 1 and 3. Tested by AC-P02.

## FR-P03: View authorized care details

As a personal representative, I want to view the patient's referral status, appointments, and pending tasks in CarePath within my recorded authority, so that I can know the patient's next steps.

Check authority on every request. Expired, revoked, or missing authority must not grant access. Supports Goal 2. Tested by AC-P03.

## FR-P04: Apply access checks

CarePath must verify the signed-in user's role and patient access before showing care details. Denied requests must return no patient information. These checks also apply to direct requests using record identifiers.

Supports Goals 1 and 2. Tested by AC-P04.

# Acceptance Criteria

These criteria use short checks instead of Gherkin scripts.

## AC-P01: View status and next steps

For FR-P01:

1. A patient viewing their referral sees its current status, last-update time, outstanding requests, unfinished tasks, and active appointment.
2. If no request or task needs the patient's action, the screen says no action is currently required.
3. The screen uses recorded care information and does not invent medical instructions.

## AC-P02: Receive reminders

For FR-P02:

1. At a configured reminder time, an eligible appointment or task reminder uses the patient's recorded contact preference.
2. Running the same reminder process again does not send the same scheduled reminder twice.
3. A cancellation or task completion before sending suppresses the reminder.
4. A confirmed reschedule replaces unsent reminders based on the old appointment time.
5. Missing timing or contact settings prevents sending and records the reason.
6. A delivery failure is recorded without claiming that the patient received the message.

## AC-P03: Representative access

For FR-P03:

1. A representative with active authority sees only the permitted patient's information and permitted information categories.
2. A representative with appointment-only authority cannot view referral or task details.
3. Expired, revoked, or missing authority results in no patient information being returned.

## AC-P04: Access checks

For FR-P04:

1. A request made without signing in returns no patient information.
2. A patient requesting another patient's record is denied access.
3. Changing a record identifier in a direct request does not bypass the access check.

# Nonfunctional Requirements

The following list is in priority order: 1 is highest. These are proposed project targets, not measured results. Each item traces to the existing specification and includes a validation check.

| ID | Priority / quality | Requirement | Why it is needed / trace | Validation |
|---|---|---|---|---|
| NFR-P01 | 1. Security | Check identity and patient access on every request, including direct record identifiers. Recheck representative scope and validity on each read. | FR-P03, FR-P04; AC-P03 and AC-P04. A role or cached page must not grant unrestricted access. | Test another patient identifier and authority that expires or is revoked between reads. |
| NFR-P02 | 2. Privacy | Use HTTPS outside local development. Email/text reminders and ordinary logs must contain no clinical findings or supporting documents. | FR-P02 and the Domain Model. Reminders leave the patient portal and need limited content. | Inspect actual reminder payloads and logs using fictional clinical records. |
| NFR-P03 | 3. Reminder reliability | While the application and delivery service are available, submit an eligible reminder within 60 seconds after its configured time. Repeated scans must not submit the same scheduled reminder twice. Record uncertain delivery without claiming success. | FR-P02; AC-P02.1-2 and AC-P02.6. Reminders must be timely and their delivery status honest. The 60-second bound is a proposed project target. | Use a controlled clock, repeated scans, concurrent scans, and a delivery timeout. |
| NFR-P04 | 4. Data freshness | Read committed care records on each page request. Immediately before reminder submission, recheck appointment/task status and time against the latest committed records. | AC-P01 and AC-P02.3-4. Cached state could show incorrect next steps or produce obsolete reminders. | Change a booking/task before a read or send and check the resulting view or suppression. |
| NFR-P05 | 5. Performance | For 20 simultaneous users and 10,000 combined care records, 95% of care-summary reads must return within 2 seconds, excluding external delivery time. | FR-P01 and FR-P03. Patients and representatives need usable access to next steps. | Measure summary reads at the stated test load. |
| NFR-P06 | 6. Usability and accessibility | Status/next-action views must work with keyboard navigation, visible focus, and labeled controls. Status must not be conveyed by color alone. Show a clear no-action message when appropriate. | FR-P01; AC-P01.2. Patients need understandable and accessible guidance. | Use keyboard-only navigation and inspect labels, focus, status text, and an empty-action example. |

# Non-goals

- Billing and insurance approval.
- Emergency triage and automated diagnosis.
- Referral decisions, appointment changes, and task assignment or completion are owned by the other CarePath functionalities.