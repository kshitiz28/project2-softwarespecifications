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
