# CarePath test plan — Kshitiz

BDD refinement of the Gherkin in spec.md. Each unique test ID extends its original AC identifier.

Frozen clock: 2026-11-10T10:00:00Z unless a step changes it. Fixture data is fictional. Expected domain values were derived from the spec; HTTP status, field names and deterministic identifiers come from contracts.md. Tests use an isolated state per case. Controls change only the invalid input, caller, initial state, or external result under test. **Unchanged [*]** means no persisted state changed or was created. Suppression and unresolved attempts can record the bookkeeping explicitly allowed by the plan.

All executable cases below are included because no subset of AC IDs was specified. The fixture credential-to-identity mapping is in contracts.md and tests/support.py; the JSON catalog is a test fixture, not implementation code. Where relevant, scheduler calls use a 10-second budget; reminder sends check the channel/destination and omit clinical data.

## AC-R01-submit: Submit complete referral

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-submit — Submit complete referral
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 201, JSON contains {"id":"referral-1","status":"Submitted","patient_id":"p1","updated_at":"2026-11-10T10:00:00Z"}; final row counts {"referrals":1,"history":1}; stored rows contain [["referrals","referral-1",{"status":"Submitted","patient_id":"p1"}]]
```

## AC-R01-missing-patient_id: Required field omitted: patient_id

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-patient_id — Required field omitted: patient_id
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"patient_id"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Field present / omitted

**Accepted control:** AC-R01-missing-patient_id-control

## AC-R01-missing-patient_id-control: Control: Required field omitted: patient_id

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-patient_id-control — Control: Required field omitted: patient_id
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 201, JSON contains {"id":"referral-1","status":"Submitted","patient_id":"p1","updated_at":"2026-11-10T10:00:00Z"}; final row counts {"referrals":1,"history":1}; stored rows contain [["referrals","referral-1",{"status":"Submitted","patient_id":"p1"}]]
```

**Inside/outside:** Field present / omitted

## AC-R01-missing-receiving_provider_id: Required field omitted: receiving_provider_id

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-receiving_provider_id — Required field omitted: receiving_provider_id
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"receiving_provider_id"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Field present / omitted

**Accepted control:** AC-R01-missing-receiving_provider_id-control

## AC-R01-missing-receiving_provider_id-control: Control: Required field omitted: receiving_provider_id

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-receiving_provider_id-control — Control: Required field omitted: receiving_provider_id
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 201, JSON contains {"id":"referral-1","status":"Submitted","patient_id":"p1","updated_at":"2026-11-10T10:00:00Z"}; final row counts {"referrals":1,"history":1}; stored rows contain [["referrals","referral-1",{"status":"Submitted","patient_id":"p1"}]]
```

**Inside/outside:** Field present / omitted

## AC-R01-missing-service: Required field omitted: service

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-service — Required field omitted: service
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"service"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Field present / omitted

**Accepted control:** AC-R01-missing-service-control

## AC-R01-missing-service-control: Control: Required field omitted: service

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-service-control — Control: Required field omitted: service
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 201, JSON contains {"id":"referral-1","status":"Submitted","patient_id":"p1","updated_at":"2026-11-10T10:00:00Z"}; final row counts {"referrals":1,"history":1}; stored rows contain [["referrals","referral-1",{"status":"Submitted","patient_id":"p1"}]]
```

**Inside/outside:** Field present / omitted

## AC-R01-missing-reason: Required field omitted: reason

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-reason — Required field omitted: reason
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","urgency":"Urgent"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"reason"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Field present / omitted

**Accepted control:** AC-R01-missing-reason-control

## AC-R01-missing-reason-control: Control: Required field omitted: reason

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-reason-control — Control: Required field omitted: reason
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 201, JSON contains {"id":"referral-1","status":"Submitted","patient_id":"p1","updated_at":"2026-11-10T10:00:00Z"}; final row counts {"referrals":1,"history":1}; stored rows contain [["referrals","referral-1",{"status":"Submitted","patient_id":"p1"}]]
```

**Inside/outside:** Field present / omitted

## AC-R01-missing-urgency: Required field omitted: urgency

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-urgency — Required field omitted: urgency
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"urgency"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Field present / omitted

**Accepted control:** AC-R01-missing-urgency-control

## AC-R01-missing-urgency-control: Control: Required field omitted: urgency

**Requirement:** FR-R01. 

```gherkin
Scenario: AC-R01-missing-urgency-control — Control: Required field omitted: urgency
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 201, JSON contains {"id":"referral-1","status":"Submitted","patient_id":"p1","updated_at":"2026-11-10T10:00:00Z"}; final row counts {"referrals":1,"history":1}; stored rows contain [["referrals","referral-1",{"status":"Submitted","patient_id":"p1"}]]
```

**Inside/outside:** Field present / omitted

## AC-R02-accept: Receiving provider accepts

**Requirement:** FR-R02. 

```gherkin
Scenario: AC-R02-accept — Receiving provider accepts
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"accept","comments":"Accepted for consultation","version":1}
  Then observe HTTP 200, JSON contains {"status":"Accepted","reviewer_id":"receiver","reviewed_at":"2026-11-10T10:00:00Z"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
```

## AC-R02-redirect-missing: Redirect without destination

**Requirement:** FR-R02. 

```gherkin
Scenario: AC-R02-redirect-missing — Redirect without destination
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"redirect","comments":"Accepted for consultation","version":1}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"destination_provider_id"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R02-redirect-missing-control

## AC-R02-redirect-missing-control: Control: Redirect without destination

**Requirement:** FR-R02. 

```gherkin
Scenario: AC-R02-redirect-missing-control — Control: Redirect without destination
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"redirect","comments":"Accepted for consultation","version":1,"destination_provider_id":"other-provider"}
  Then observe HTTP 200, JSON contains {"status":"Redirected","reviewer_id":"receiver","reviewed_at":"2026-11-10T10:00:00Z"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Redirected"}]]
```

## AC-R02-extra-stale: NFR-R02: stale review

**Requirement:** FR-R02. **Extra.** 

```gherkin
Scenario: AC-R02-extra-stale — NFR-R02: stale review
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"accept","comments":"Accepted for consultation","version":0}
  Then observe HTTP 409, JSON contains {"error":"stale_version"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R02-extra-stale-control

## AC-R02-extra-stale-control: Control: NFR-R02: stale review

**Requirement:** FR-R02. **Extra.** 

```gherkin
Scenario: AC-R02-extra-stale-control — Control: NFR-R02: stale review
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"accept","comments":"Accepted for consultation","version":1}
  Then observe HTTP 200, JSON contains {"status":"Accepted","reviewer_id":"receiver","reviewed_at":"2026-11-10T10:00:00Z"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
```

## AC-R02-extra-identity: NFR-R01: wrong receiving provider

**Requirement:** FR-R02. **Extra.** 

```gherkin
Scenario: AC-R02-extra-identity — NFR-R01: wrong receiving provider
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=other-provider; JSON {"decision":"accept","comments":"Accepted for consultation","version":1}
  Then observe HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R02-extra-identity-control

## AC-R02-extra-identity-control: Control: NFR-R01: wrong receiving provider

**Requirement:** FR-R02. **Extra.** 

```gherkin
Scenario: AC-R02-extra-identity-control — Control: NFR-R01: wrong receiving provider
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"accept","comments":"Accepted for consultation","version":1}
  Then observe HTTP 200, JSON contains {"status":"Accepted","reviewer_id":"receiver","reviewed_at":"2026-11-10T10:00:00Z"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
```

## AC-R03-share: Share findings with the referring provider

**Requirement:** FR-R03. 

```gherkin
Scenario: AC-R03-share — Share findings with the referring provider
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/findings; credential=receiver; JSON {"text":"Consultation completed","complete":true}
  Then observe HTTP 200, JSON contains {"status":"Completed","findings":"Consultation completed"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Completed","findings":"Consultation completed"}]]
  When I invoke GET /referrals/r1; credential=sender
  Then observe HTTP 200, JSON contains {"id":"r1","status":"Completed","findings":"Consultation completed"}; unchanged tables ["*"] (* = full snapshot)
```

## AC-R03-extra-blank: FR-R03: blank findings

**Requirement:** FR-R03. **Extra.** 

```gherkin
Scenario: AC-R03-extra-blank — FR-R03: blank findings
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/findings; credential=receiver; JSON {"text":" ","complete":true}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"text"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R03-extra-blank-control

## AC-R03-extra-blank-control: Control: FR-R03: blank findings

**Requirement:** FR-R03. **Extra.** 

```gherkin
Scenario: AC-R03-extra-blank-control — Control: FR-R03: blank findings
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/findings; credential=receiver; JSON {"text":"Consultation completed","complete":true}
  Then observe HTTP 200, JSON contains {"status":"Completed","findings":"Consultation completed"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Completed","findings":"Consultation completed"}]]
```

## AC-R04-filters: Combine all filters and exclude inaccessible referrals

**Requirement:** FR-R04. 

```gherkin
Scenario: AC-R04-filters — Combine all filters and exclude inaccessible referrals
  Given the standard identities, clock, and seeded records {"referrals":{"old":{"id":"old","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-09T09:59:59Z","version":1},"young":{"id":"young","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-09T10:00:01Z","version":1},"answered":{"id":"answered","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-09T09:00:00Z","version":1},"routine":{"id":"routine","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Routine","status":"Under review","updated_at":"2026-11-09T09:00:00Z","version":1},"hidden":{"id":"hidden","patient_id":"p2","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-09T09:00:00Z","version":1}},"information_requests":{"old":{"id":"old","referral_id":"old","status":"Awaiting response"},"young":{"id":"young","referral_id":"young","status":"Awaiting response"},"answered":{"id":"answered","referral_id":"answered","status":"Responded"},"routine":{"id":"routine","referral_id":"routine","status":"Awaiting response"},"hidden":{"id":"hidden","referral_id":"hidden","status":"Awaiting response"}}}
  When I invoke GET /referrals?urgency=Urgent&missing_information=true&age_hours=24; credential=coordinator
  Then observe HTTP 200, JSON contains {"items":[{"id":"old"}]}; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** 23h59m59s excluded; 24h00m01s included. Exact equality is a spec gap.

## AC-R05-roundtrip: Request then link response

**Requirement:** FR-R05. 

```gherkin
Scenario: AC-R05-roundtrip — Request then link response
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/information-requests; credential=coordinator; JSON {"item":"Summary PDF","recipient_id":"patient"}
  Then observe HTTP 201, JSON contains {"id":"request-1","status":"Awaiting response","referral_id":"r1","recipient_id":"patient"}; final row counts {"information_requests":1}
  When I invoke GET /referrals/r1; credential=coordinator
  Then observe HTTP 200, JSON contains {"id":"r1","information_requests":[{"id":"request-1","status":"Awaiting response"}]}; unchanged tables ["*"] (* = full snapshot)
  When I invoke POST /referrals/r1/information-requests/request-1/response; credential=patient; JSON {"filename":"summary.pdf","content_base64":"YWJj"}
  Then observe HTTP 200, JSON contains {"id":"request-1","status":"Responded","sender_id":"patient","responded_at":"2026-11-10T10:00:00Z","document_id":"document-1"}; final row counts {"documents":1}; stored rows contain [["information_requests","request-1",{"status":"Responded","referral_id":"r1","document_id":"document-1","sender_id":"patient","responded_at":"2026-11-10T10:00:00Z"}],["documents","document-1",{"filename":"summary.pdf","referral_id":"r1"}]]; forbidden stored field values [["referrals","r1","status",["Accepted","Completed"]]]
```

## AC-R05-missing-recipient: Recipient omitted

**Requirement:** FR-R05. 

```gherkin
Scenario: AC-R05-missing-recipient — Recipient omitted
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/information-requests; credential=coordinator; JSON {"item":"Summary PDF"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"recipient_id"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R05-missing-recipient-control

## AC-R05-missing-recipient-control: Control: Recipient omitted

**Requirement:** FR-R05. 

```gherkin
Scenario: AC-R05-missing-recipient-control — Control: Recipient omitted
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/information-requests; credential=coordinator; JSON {"item":"Summary PDF","recipient_id":"patient"}
  Then observe HTTP 201, JSON contains {"id":"request-1","status":"Awaiting response","referral_id":"r1","recipient_id":"patient"}; final row counts {"information_requests":1}
```

## AC-R05-extra-recipient: FR-R05: wrong responder

**Requirement:** FR-R05. **Extra.** 

```gherkin
Scenario: AC-R05-extra-recipient — FR-R05: wrong responder
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"information_requests":{"request-1":{"id":"request-1","referral_id":"r1","recipient_id":"patient","status":"Awaiting response"}}}
  When I invoke POST /referrals/r1/information-requests/request-1/response; credential=sender; JSON {"filename":"summary.pdf","content_base64":"YWJj"}
  Then observe HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R05-extra-recipient-control

## AC-R05-extra-recipient-control: Control: FR-R05: wrong responder

**Requirement:** FR-R05. **Extra.** 

```gherkin
Scenario: AC-R05-extra-recipient-control — Control: FR-R05: wrong responder
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"information_requests":{"request-1":{"id":"request-1","referral_id":"r1","recipient_id":"patient","status":"Awaiting response"}}}
  When I invoke POST /referrals/r1/information-requests/request-1/response; credential=patient; JSON {"filename":"summary.pdf","content_base64":"YWJj"}
  Then observe HTTP 200, JSON contains {"id":"request-1","status":"Responded","sender_id":"patient","responded_at":"2026-11-10T10:00:00Z","document_id":"document-1"}; final row counts {"documents":1}; stored rows contain [["information_requests","request-1",{"status":"Responded","referral_id":"r1","document_id":"document-1","sender_id":"patient","responded_at":"2026-11-10T10:00:00Z"}],["documents","document-1",{"filename":"summary.pdf","referral_id":"r1"}]]; forbidden stored field values [["referrals","r1","status",["Accepted","Completed"]]]
```

## AC-R06-history: History captures old/new values and actor

**Requirement:** FR-R06. 

```gherkin
Scenario: AC-R06-history — History captures old/new values and actor
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"accept","comments":"Accepted for consultation","version":1}
  Then observe HTTP 200, JSON contains {"status":"Accepted","reviewer_id":"receiver","reviewed_at":"2026-11-10T10:00:00Z"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
  When I invoke GET /referrals/r1; credential=receiver
  Then observe HTTP 200, JSON contains {"history":[{"actor_id":"receiver","at":"2026-11-10T10:00:00Z","previous_status":"Under review","new_status":"Accepted"}]}; unchanged tables ["*"] (* = full snapshot)
```

## AC-R06-duplicate: Apply once and ignore replay

**Requirement:** FR-R06. 

```gherkin
Scenario: AC-R06-duplicate — Apply once and ignore replay
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"status_mappings":{"trusted:approved":{"status":"Accepted"}}}
  When I invoke POST /referral-events; credential=trusted; JSON {"event_id":"e1","referral_id":"r1","external_status":"approved"}
  Then observe HTTP 200, JSON contains {"outcome":"applied","status":"Accepted"}; final row counts {"external_events":1,"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
  When I invoke POST /referral-events; credential=trusted; JSON {"event_id":"e1","referral_id":"r1","external_status":"approved"}
  Then observe HTTP 200, JSON contains {"outcome":"duplicate","status":"Accepted"}; unchanged tables ["*"] (* = full snapshot)
```

## AC-R06-unmapped: Flag unmapped event without updating referral

**Requirement:** FR-R06. 

```gherkin
Scenario: AC-R06-unmapped — Flag unmapped event without updating referral
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"status_mappings":{"trusted:approved":{"status":"Accepted"}}}
  When I invoke POST /referral-events; credential=trusted; JSON {"event_id":"e1","referral_id":"r1","external_status":"UNKNOWN"}
  Then observe HTTP 202, JSON contains {"outcome":"review_required","status":"Under review"}; unchanged tables ["referrals","history"] (* = full snapshot); final row counts {"review_flags":1}
```

## AC-R06-extra-untrusted: NFR-R01: untrusted event sender

**Requirement:** FR-R06. **Extra.** 

```gherkin
Scenario: AC-R06-extra-untrusted — NFR-R01: untrusted event sender
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"status_mappings":{"trusted:approved":{"status":"Accepted"}}}
  When I invoke POST /referral-events; credential=untrusted; JSON {"event_id":"e1","referral_id":"r1","external_status":"approved"}
  Then observe HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R06-extra-untrusted-control

## AC-R06-extra-untrusted-control: Control: NFR-R01: untrusted event sender

**Requirement:** FR-R06. **Extra.** 

```gherkin
Scenario: AC-R06-extra-untrusted-control — Control: NFR-R01: untrusted event sender
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"status_mappings":{"trusted:approved":{"status":"Accepted"}}}
  When I invoke POST /referral-events; credential=trusted; JSON {"event_id":"e1","referral_id":"r1","external_status":"approved"}
  Then observe HTTP 200, JSON contains {"outcome":"applied","status":"Accepted"}; final row counts {"external_events":1,"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
```

## AC-R06-extra-rollback: NFR-R02: failed commit

**Requirement:** FR-R06. **Extra.** 

```gherkin
Scenario: AC-R06-extra-rollback — NFR-R02: failed commit
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"accept","comments":"Accepted for consultation","version":1}; inject commit failure
  Then observe HTTP 500, JSON contains {"error":"persistence_error"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R06-extra-rollback-control

## AC-R06-extra-rollback-control: Control: NFR-R02: failed commit

**Requirement:** FR-R06. **Extra.** 

```gherkin
Scenario: AC-R06-extra-rollback-control — Control: NFR-R02: failed commit
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}}}
  When I invoke POST /referrals/r1/reviews; credential=receiver; JSON {"decision":"accept","comments":"Accepted for consultation","version":1}
  Then observe HTTP 200, JSON contains {"status":"Accepted","reviewer_id":"receiver","reviewed_at":"2026-11-10T10:00:00Z"}; final row counts {"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
```

## AC-R01-extra-type: FR-R01: reason has wrong input type

**Requirement:** FR-R01. **Extra.** 

```gherkin
Scenario: AC-R01-extra-type — FR-R01: reason has wrong input type
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":42,"urgency":"Urgent"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"reason"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-R01-extra-type-control

## AC-R01-extra-type-control: Control: FR-R01: reason has wrong input type

**Requirement:** FR-R01. **Extra.** 

```gherkin
Scenario: AC-R01-extra-type-control — Control: FR-R01: reason has wrong input type
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /referrals; credential=sender; JSON {"patient_id":"p1","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent"}
  Then observe HTTP 201, JSON contains {"id":"referral-1","status":"Submitted","patient_id":"p1","updated_at":"2026-11-10T10:00:00Z"}; final row counts {"referrals":1,"history":1}; stored rows contain [["referrals","referral-1",{"status":"Submitted","patient_id":"p1"}]]
```

## AC-R06-extra-concurrent: FR-R06: concurrent delivery of one event

**Requirement:** FR-R06. **Extra.** 

```gherkin
Scenario: AC-R06-extra-concurrent — FR-R06: concurrent delivery of one event
  Given the standard identities, clock, and seeded records {"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"status_mappings":{"trusted:approved":{"status":"Accepted"}}}
  When I concurrently request POST /referral-events; credential=trusted; JSON {"event_id":"e1","referral_id":"r1","external_status":"approved"}
  Then observe HTTP 200, JSON contains {"outcome":"applied","status":"Accepted"}; final row counts {"external_events":1,"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
  When I concurrently request POST /referral-events; credential=trusted; JSON {"event_id":"e1","referral_id":"r1","external_status":"approved"}
  Then observe HTTP 200, JSON contains {"outcome":"duplicate","status":"Accepted"}; final row counts {"external_events":1,"history":1}; stored rows contain [["referrals","r1",{"status":"Accepted"}]]
```


## Gap checklist and environment checks

Required fields and input type: AC-R01. Identity, stale versions and errors: AC-R02 extras. Listing and age: AC-R04. Recipient and response state: AC-R05. Duplicate events, history, unmapped status, and rollback: AC-R06. Check access before exposing data; combined-fault error ordering remains unspecified.

| NFR | Validation | Execution scope |
|---|---|---|
| NFR-R01 | Try a signed-out request, a wrong provider, a wrong response recipient, and an untrusted external source; all must be denied. Target: Every request must verify the user and permitted patient/action, or authenticate a configured external source. Unauthorized requests return no patient data and change nothing. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-R02 | Force a save failure and two conflicting reviews; check rollback and rejection of the stale decision. Target: Save referral changes and their history together in one database transaction. A failed save leaves neither a partial change nor a success result. A stale review must be rejected if another user has changed the referral. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-R03 | Check the deployed connection and inspect logs after submission, sharing, and response upload. Target: Use HTTPS outside local development and keep clinical text and documents out of ordinary application logs. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-R04 | Run a load test with those records and users and measure response times. Target: For 20 simultaneous users and 10,000 referral records, 95% of referral-detail and filter requests must return within 2 seconds. Exclude file transfer and external-service time. Use 200 measured eligible requests at the specified 20-user, 10,000-record load; sort durations and check the 190th is at most 2,000 ms. Exercise 1,999 and 2,001 ms in the threshold check. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-R05 | Submit incomplete forms and check labels, errors, and retained values. Target: Show field-specific validation errors and preserve entered referral/request text after a validation failure. Show statuses as readable labels. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-R06 | Run AC-R01 through AC-R06 with fictional records and no external healthcare connection. Target: Referral rules and external-update handling must be testable with a local test database and fixed external test events. | Implemented environment / deployment check; not a 501 skeleton test. |

## Spec gaps

- All six FR sections link to an AC, and all six AC sections have an FR. Decline, complete transition rules and valid redirect handoff have no detailed original AC; only the specified redirect validation and visible Redirected status are tested.
- FR-R04/AC-R04 does not define equality at exactly 24 hours, default ordering, pagination, or empty-filter policy. The age cases bracket equality by one second without choosing it.
- FR-R06/NFR-R06 does not define the production FHIR/BSeR version, trust exchange, mappings, or out-of-order policy. Tests use the fictional trusted:approved mapping.
- Supporting document type/size/retention, the referral transition on information request/response, and identity provisioning are unspecified. The response case uses a small synthetic file and does not choose an upload policy.
- If several inputs are invalid, the spec does not specify error precedence. Rejection tests deliberately isolate one invalid condition. Pagination, maximum response sizes, and error message wording are unspecified.
- NFRs have Validation entries rather than separate AC IDs. API-addressable parts are covered by the extra cases above; deployment and UI checks remain environment tests.
