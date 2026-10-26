# Description

This part of CarePath covers Referral Management and Tracking. Providers submit referrals, review them, and share visit findings. Coordinators find delayed referrals and request missing information. Appointment booking, follow-up tasks, and patient-facing reminders are covered by the other team members. CarePath supports care coordination; it does not make clinical decisions.

# Goals

1. Maintain continuity of care between providers.
2. Help receiving providers deliver referred care.
3. Prevent referrals from becoming delayed or incomplete.

# Domain Model

## Actors

- **Referring provider:** Creates a referral and receives visit findings.
- **Receiving provider:** Reviews the referral and records the outcome.
- **Referral coordinator:** Monitors progress and requests missing information.
- **Patient:** May provide information requested for their referral.

## Objects

- **Referral:** Identifier, patient, referring provider, receiving provider, requested service, reason, urgency, status, and last-update time.
- **Referral review:** Provider decision, comments, reviewer, and review time.
- **Supporting document:** A file linked to the referral and its patient.
- **Information request:** Missing item, recipient, linked referral, response, and status: Awaiting response or Responded.
- **Visit finding:** Provider-entered results linked to a referral and shared with the referring provider.
- **Change history:** Who changed a referral, when, and its previous and new status.

Referral statuses include Submitted, Under review, Information required, Accepted, Declined, Redirected, and Completed. Providers control review decisions. A response to an information request does not automatically accept or complete the referral. Users must be signed in and have permission for the patient and action. Urgency values come from the organization's configured list.

# Functional Requirements

## FR-R01: Submit a referral

As a referring provider, I want to submit a referral in CarePath with the patient, destination provider, reason, urgency, and supporting information, so that I can keep referral information available.

Patient, destination, requested service, reason, and urgency are required. CarePath creates an identifier and sets Submitted. Missing required information produces a field error without creating a submitted referral. Supports Goal 1. Tested by AC-R01.

## FR-R02: Record a review decision

As a receiving provider, I want to review a referral in CarePath and record an acceptance, decline, or redirection with comments, so that I can keep referral decisions and outcomes recorded.

Only the current receiving provider may record the decision. Comments are required; redirection also requires a new destination. CarePath records the reviewer, time, and status change. Supports Goal 2. Tested by AC-R02.

## FR-R03: Share visit findings

As a receiving provider, I want to record visit findings in CarePath and share them with the referring provider, so that I can keep referral decisions and outcomes recorded.

Findings must not be blank. The receiving provider records them for an accepted referral. Final sharing includes confirmation that the service is complete and sets Completed. Supports Goals 1 and 2. Tested by AC-R03.

## FR-R04: Find referrals needing attention

As a referral coordinator, I want to filter referrals in CarePath by urgency, missing information, and time since the last update, so that I can keep referrals moving forward.

Combined filters must match all selected conditions and show only accessible referrals. Missing information means an unanswered information request. Supports Goal 3. Tested by AC-R04.

## FR-R05: Request missing information

As a referral coordinator, I want to send a request for missing information through CarePath to the patient or referring provider and track its response, so that I can keep referrals moving forward.

The missing item and recipient are required. Only the selected recipient may respond. CarePath links the response to the request and referral and records the sender and time. Supports Goal 3. Tested by AC-R05.

## FR-R06: Keep referral updates consistent

CarePath must record referral status changes in history, apply supported updates from trusted connected systems, and ignore duplicate external event identifiers. Unknown status mappings must be flagged for staff review without replacing the current status. Supports Goals 1 and 3. Tested by AC-R06.

# Acceptance Criteria

All scenarios assume the actor is signed in and has permission unless stated otherwise.

## AC-R01: Referral submission

```gherkin
Feature: Submit a referral
  Scenario: Submit a complete referral
    Given a referring provider opens New referral
    When the provider enters all required information and selects Submit
    Then CarePath creates a referral with an identifier and status Submitted
    And shows Referral details

  Scenario: Required information is missing
    When the provider submits without a destination provider
    Then CarePath shows a field error
    And does not create a submitted referral
```

## AC-R02: Review decision

```gherkin
Feature: Review a referral
  Scenario: Accept a referral
    Given the receiving provider is reviewing a referral
    When the provider records acceptance with comments
    Then CarePath sets Accepted and records the reviewer and time

  Scenario: Redirect without a destination
    When the receiving provider redirects a referral without a new destination
    Then CarePath rejects the decision without changing the referral
```

## AC-R03: Visit findings

```gherkin
Feature: Share visit findings
  Scenario: Share final findings
    Given the receiving provider has an Accepted referral
    When the provider enters findings and confirms service completion
    And shares the findings with the referring provider
    Then the referring provider can view the findings
    And the referral becomes Completed
```

## AC-R04: Referral filtering

```gherkin
Feature: Find referrals needing attention
  Scenario: Combine filters
    Given Urgent is a configured urgency value
    When a coordinator filters for Urgent, missing information, and 24 hours since update
    Then results match all three conditions
    And contain only referrals the coordinator can access
```

## AC-R05: Missing information

```gherkin
Feature: Request missing information
  Scenario: Send and track a request
    Given a referral is missing a document
    When the coordinator describes the missing item and selects the patient as recipient
    And sends the request
    Then it appears as Awaiting response in Referral details
    When that patient provides the requested document
    Then CarePath links it to the request and marks it Responded
    And does not automatically accept or complete the referral

  Scenario: Recipient is missing
    When the coordinator sends a request without a recipient
    Then CarePath shows an error and sends nothing
```

## AC-R06: Referral updates

```gherkin
Feature: Keep referral updates consistent
  Scenario: Record a status change
    When an authorized referral status change is saved
    Then its history records the actor, time, previous status, and new status

  Scenario: Duplicate external update
    Given an external event has already been processed
    When the same source sends that event identifier again
    Then CarePath makes no duplicate change

  Scenario: Unknown external status
    When a trusted connected system sends an unmapped status
    Then CarePath flags it for review and keeps the current status
```
