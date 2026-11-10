# CarePath test plan

BDD refinement of the Gherkin in spec.md. Each unique test ID extends its original AC identifier.

Frozen clock: 2026-11-10T10:00:00Z unless a step changes it. Fixture data is fictional. Expected domain values were derived from the spec; HTTP status, field names and deterministic identifiers come from contracts.md. Tests use an isolated state per case. Controls change only the invalid input, caller, initial state, or external result under test. **Unchanged [*]** means no persisted state changed or was created. Suppression and unresolved attempts can record the bookkeeping explicitly allowed by the plan.

All executable cases below are included because no subset of AC IDs was specified. The fixture credential-to-identity mapping is in contracts.md and tests/support.py; the JSON catalog is a test fixture, not implementation code. Where relevant, scheduler calls use a 10-second budget; reminder sends check the channel/destination and omit clinical data.

## AC-T01-assign: Assign and list task

**Requirement:** FR-T01. 

```gherkin
Scenario: AC-T01-assign — Assign and list task
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T10:00:01Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 201, JSON contains {"id":"task-1","status":"Open","patient_id":"p1","nurse_id":"nurse","due_at":"2026-11-10T10:00:01Z"}; final row counts {"tasks":1,"history":1}
  When I invoke GET /patients/p1/tasks; credential=patient
  Then observe HTTP 200, JSON contains {"items":[{"id":"task-1","status":"Open"}]}; unchanged tables ["*"] (* = full snapshot)
```

## AC-T01-instructions: Reject invalid instructions

**Requirement:** FR-T01. 

```gherkin
Scenario: AC-T01-instructions — Reject invalid instructions
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":" ","due_at":"2026-11-10T10:00:01Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"instructions"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Valid value vs invalid value

**Accepted control:** AC-T01-instructions-control

## AC-T01-instructions-control: Control: Reject invalid instructions

**Requirement:** FR-T01. 

```gherkin
Scenario: AC-T01-instructions-control — Control: Reject invalid instructions
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T10:00:01Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 201, JSON contains {"id":"task-1","status":"Open","patient_id":"p1","nurse_id":"nurse","due_at":"2026-11-10T10:00:01Z"}; final row counts {"tasks":1,"history":1}
```

**Inside/outside:** Valid value vs invalid value

## AC-T01-due_at: Reject invalid due_at

**Requirement:** FR-T01. 

```gherkin
Scenario: AC-T01-due_at — Reject invalid due_at
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T10:00:00Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"due_at"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Now +1s accepted; equal and −1s rejected

**Accepted control:** AC-T01-due_at-control

## AC-T01-due_at-control: Control: Reject invalid due_at

**Requirement:** FR-T01. 

```gherkin
Scenario: AC-T01-due_at-control — Control: Reject invalid due_at
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T10:00:01Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 201, JSON contains {"id":"task-1","status":"Open","patient_id":"p1","nurse_id":"nurse","due_at":"2026-11-10T10:00:01Z"}; final row counts {"tasks":1,"history":1}
```

**Inside/outside:** Now +1s accepted; equal and −1s rejected

## AC-T01-due_at-past: Reject invalid due_at

**Requirement:** FR-T01. 

```gherkin
Scenario: AC-T01-due_at-past — Reject invalid due_at
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T09:59:59Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"due_at"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Now +1s accepted; equal and −1s rejected

**Accepted control:** AC-T01-due_at-past-control

## AC-T01-due_at-past-control: Control: Reject invalid due_at

**Requirement:** FR-T01. 

```gherkin
Scenario: AC-T01-due_at-past-control — Control: Reject invalid due_at
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T10:00:01Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 201, JSON contains {"id":"task-1","status":"Open","patient_id":"p1","nurse_id":"nurse","due_at":"2026-11-10T10:00:01Z"}; final row counts {"tasks":1,"history":1}
```

**Inside/outside:** Now +1s accepted; equal and −1s rejected

## AC-T01-due_at-type: Reject invalid due_at

**Requirement:** FR-T01. **Extra.** 

```gherkin
Scenario: AC-T01-due_at-type — Reject invalid due_at
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":42,"document_required":false,"referral_id":"r1"}
  Then observe HTTP 422, JSON contains {"error":"validation_error","field":"due_at"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Valid value vs invalid value

**Accepted control:** AC-T01-due_at-type-control

## AC-T01-due_at-type-control: Control: Reject invalid due_at

**Requirement:** FR-T01. **Extra.** 

```gherkin
Scenario: AC-T01-due_at-type-control — Control: Reject invalid due_at
  Given the standard identities, clock, and seeded records {"tasks":{},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T10:00:01Z","document_required":false,"referral_id":"r1"}
  Then observe HTTP 201, JSON contains {"id":"task-1","status":"Open","patient_id":"p1","nurse_id":"nurse","due_at":"2026-11-10T10:00:01Z"}; final row counts {"tasks":1,"history":1}
```

**Inside/outside:** Valid value vs invalid value

## AC-T02-evidence: Upload allowed file and complete

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-evidence — Upload allowed file and complete
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks/t1/documents; credential=patient; JSON {"filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA="}
  Then observe HTTP 201, JSON contains {"id":"document-1","task_id":"t1","size_bytes":8}; final row counts {"documents":1}; stored rows contain [["documents","document-1",{"task_id":"t1","filename":"summary.pdf"}]]
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["tasks","t1",{"status":"Completed","completed_at":"2026-11-10T10:00:00Z"}]]
```

**Inside/outside:** Configured fixture max 8 bytes; 8-byte PDF accepted.

## AC-T02-no-document: Required evidence absent

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-no-document — Required evidence absent
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 422, JSON contains {"error":"document_required"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-T02-no-document-control

## AC-T02-no-document-control: Control: Required evidence absent

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-no-document-control — Control: Required evidence absent
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["tasks","t1",{"status":"Completed","completed_at":"2026-11-10T10:00:00Z"}]]
```

## AC-T02-size: Reject oversized allowed PDF

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-size — Reject oversized allowed PDF
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks/t1/documents; credential=patient; JSON {"filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjAK"}
  Then observe HTTP 413, JSON contains {"error":"file_too_large"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** 8 bytes accepted / 9 bytes rejected (fixture policy)

**Accepted control:** AC-T02-size-control

## AC-T02-size-control: Control: Reject oversized allowed PDF

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-size-control — Control: Reject oversized allowed PDF
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks/t1/documents; credential=patient; JSON {"filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA="}
  Then observe HTTP 201, JSON contains {"id":"document-1","task_id":"t1","size_bytes":8}; final row counts {"documents":1}; stored rows contain [["documents","document-1",{"task_id":"t1","filename":"summary.pdf"}]]
```

**Inside/outside:** 8 bytes accepted / 9 bytes rejected (fixture policy)

## AC-T02-type: Reject unsupported media type

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-type — Reject unsupported media type
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks/t1/documents; credential=patient; JSON {"filename":"summary.txt","media_type":"text/plain","content_base64":"YWJjZGVmZ2g="}
  Then observe HTTP 415, JSON contains {"error":"unsupported_file_type"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Inside/outside:** Same eight-byte size; disallowed type vs allowed type

**Accepted control:** AC-T02-type-control

## AC-T02-type-control: Control: Reject unsupported media type

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-type-control — Control: Reject unsupported media type
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke POST /tasks/t1/documents; credential=patient; JSON {"filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA="}
  Then observe HTTP 201, JSON contains {"id":"document-1","task_id":"t1","size_bytes":8}; final row counts {"documents":1}; stored rows contain [["documents","document-1",{"task_id":"t1","filename":"summary.pdf"}]]
```

**Inside/outside:** Same eight-byte size; disallowed type vs allowed type

## AC-T02-repeat: Keep completion timestamp on repeat

**Requirement:** FR-T02. 

```gherkin
Scenario: AC-T02-repeat — Keep completion timestamp on repeat
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["tasks","t1",{"status":"Completed","completed_at":"2026-11-10T10:00:00Z"}]]
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}; set clock 2026-11-10T10:00:01Z
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; unchanged tables ["*"] (* = full snapshot)
```

## AC-T03-overdue: Complete overdue task without changing referral

**Requirement:** FR-T03. 

```gherkin
Scenario: AC-T03-overdue — Complete overdue task without changing referral
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-10T09:59:59Z","status":"Overdue","document_required":false,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke GET /tasks/t1; credential=patient
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Overdue"}
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["tasks","t1",{"status":"Completed","completed_at":"2026-11-10T10:00:00Z"}]]
  When I invoke GET /tasks/t1; credential=patient
  Then observe HTTP 200, JSON contains {"history":[{"actor_id":"patient","at":"2026-11-10T10:00:00Z","new_status":"Completed"}]}; unchanged tables ["*"] (* = full snapshot)
```

## AC-T03-extra-clock-before: NFR-T04: server clock evaluates deadline

**Requirement:** FR-T03. **Extra.** 

```gherkin
Scenario: AC-T03-extra-clock-before — NFR-T04: server clock evaluates deadline
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-10T10:00:01Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke GET /tasks/t1; credential=patient
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Open","due_at":"2026-11-10T10:00:01Z"}
```

**Inside/outside:** Read one second before/after due time.

## AC-T03-extra-clock-after: NFR-T04: server clock evaluates deadline

**Requirement:** FR-T03. **Extra.** 

```gherkin
Scenario: AC-T03-extra-clock-after — NFR-T04: server clock evaluates deadline
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-10T09:59:59Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}}}
  When I invoke GET /tasks/t1; credential=patient
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Overdue","due_at":"2026-11-10T09:59:59Z"}
```

**Inside/outside:** Read one second before/after due time.

## AC-T02-extra-identity: NFR-T01: wrong patient

**Requirement:** FR-T02. **Extra.** 

```gherkin
Scenario: AC-T02-extra-identity — NFR-T01: wrong patient
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke POST /tasks/t1/complete; credential=other-patient; JSON {}
  Then observe HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-T02-extra-identity-control

## AC-T02-extra-identity-control: Control: NFR-T01: wrong patient

**Requirement:** FR-T02. **Extra.** 

```gherkin
Scenario: AC-T02-extra-identity-control — Control: NFR-T01: wrong patient
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["tasks","t1",{"status":"Completed","completed_at":"2026-11-10T10:00:00Z"}]]
```

## AC-T02-extra-rollback: NFR-T02: completion transaction fails

**Requirement:** FR-T02. **Extra.** 

```gherkin
Scenario: AC-T02-extra-rollback — NFR-T02: completion transaction fails
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}; inject commit failure
  Then observe HTTP 500, JSON contains {"error":"persistence_error"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-T02-extra-rollback-control

## AC-T02-extra-rollback-control: Control: NFR-T02: completion transaction fails

**Requirement:** FR-T02. **Extra.** 

```gherkin
Scenario: AC-T02-extra-rollback-control — Control: NFR-T02: completion transaction fails
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; unchanged tables ["referrals"] (* = full snapshot); final row counts {"history":1}; stored rows contain [["tasks","t1",{"status":"Completed","completed_at":"2026-11-10T10:00:00Z"}]]
```

## AC-T02-extra-concurrent: NFR-T02: simultaneous completion preserves one timestamp

**Requirement:** FR-T02. **Extra.** 

```gherkin
Scenario: AC-T02-extra-concurrent — NFR-T02: simultaneous completion preserves one timestamp
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I concurrently request POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}
  When I concurrently request POST /tasks/t1/complete; credential=patient; JSON {}
  Then observe HTTP 200, JSON contains {"id":"t1","status":"Completed","completed_at":"2026-11-10T10:00:00Z"}; final row counts {"history":1}; stored rows contain [["tasks","t1",{"status":"Completed","completed_at":"2026-11-10T10:00:00Z"}]]
```

## AC-T01-extra-list-empty: FR-T01: empty task list

**Requirement:** FR-T01. **Extra.** 

```gherkin
Scenario: AC-T01-extra-list-empty — FR-T01: empty task list
  Given the standard identities, clock, and seeded records {"tasks":{"other":{"id":"other","patient_id":"p2","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}}}
  When I invoke GET /patients/p1/tasks; credential=patient
  Then observe HTTP 200, JSON exact {"items":[]}; unchanged tables ["*"] (* = full snapshot)
```

## AC-T02-extra-document-access: NFR-T03: unauthorized evidence read

**Requirement:** FR-T02. **Extra.** 

```gherkin
Scenario: AC-T02-extra-document-access — NFR-T03: unauthorized evidence read
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke GET /tasks/t1/documents/d1; credential=other-patient
  Then observe HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; unchanged tables ["*"] (* = full snapshot)
```

**Accepted control:** AC-T02-extra-document-access-control

## AC-T02-extra-document-access-control: Control: NFR-T03: unauthorized evidence read

**Requirement:** FR-T02. **Extra.** 

```gherkin
Scenario: AC-T02-extra-document-access-control — Control: NFR-T03: unauthorized evidence read
  Given the standard identities, clock, and seeded records {"tasks":{"t1":{"id":"t1","patient_id":"p1","nurse_id":"nurse","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z","status":"Open","document_required":true,"referral_id":"r1"}},"referrals":{"r1":{"id":"r1","patient_id":"p1","referring_provider_id":"sender","receiving_provider_id":"receiver","service":"Cardiology","reason":"Consultation","urgency":"Urgent","status":"Under review","updated_at":"2026-11-10T09:59:59Z","version":1}},"upload_policy":{"default":{"allowed_types":["application/pdf"],"max_bytes":8}},"documents":{"d1":{"id":"d1","task_id":"t1","patient_id":"p1","filename":"summary.pdf","media_type":"application/pdf","content_base64":"JVBERi0xLjA=","size_bytes":8}}}
  When I invoke GET /tasks/t1/documents/d1; credential=patient
  Then observe HTTP 200, JSON contains {"id":"d1","task_id":"t1","filename":"summary.pdf","content_base64":"JVBERi0xLjA="}; unchanged tables ["*"] (* = full snapshot)
```

## AC-T03-extra-offset: NFR-T04: equivalent UTC instant

**Requirement:** FR-T03. **Extra.** 

```gherkin
Scenario: AC-T03-extra-offset — NFR-T04: equivalent UTC instant
  Given the standard identities, clock, and seeded records {}
  When I invoke POST /tasks; credential=nurse; JSON {"patient_id":"p1","instructions":"Read instructions","due_at":"2026-11-10T04:00:01-06:00","document_required":false,"referral_id":"r1"}
  Then observe HTTP 201, JSON contains {"id":"task-1","status":"Open","due_at":"2026-11-10T10:00:01Z"}; final row counts {"tasks":1,"history":1}
```


## Gap checklist and environment checks

Due-time and input type: AC-T01 and AC-T03 extras. Upload size/type, assigned identity, state, concurrent/repeated completion and rollback: AC-T02. Empty listing: AC-T01 extra. Returned history and referral isolation: AC-T03. Error ordering for several bad fields remains unspecified.

| NFR | Validation | Execution scope |
|---|---|---|
| NFR-T01 | Attempt assignment without nurse permission, completion by another patient, and an unauthorized document read. Target: Check patient access and the permitted nurse/patient action on every task or document request. Only the assigned patient can complete the task. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-T02 | Send simultaneous completion requests and force a database failure. Target: Task completion and its history must commit together. Concurrent or repeated completion must retain one original completion time and one completion transition. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-T03 | Bypass browser validation and attempt an invalid upload and an unauthorized download. Target: Use HTTPS outside local development. Enforce configured file size/type limits on the server and deny access to stored documents unless patient access is verified. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-T04 | Use test clocks before and after a deadline and clients in different time zones. Target: Use the server clock and UTC instants for due/completion comparisons; display times with their time zone. At or after completion, preserve the original timestamp. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-T05 | Load-test task reads at the stated size and user count. Target: For 20 simultaneous users and 10,000 tasks, 95% of task-list and task-detail requests must return within 2 seconds, excluding file transfer. Use 200 measured eligible requests at the specified 20-user, 10,000-record load; sort durations and check the 190th is at most 2,000 ms. Exercise 1,999 and 2,001 ms in the threshold check. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-T06 | Inspect assignment errors and an incomplete document-task screen. Target: Display instructions, due time, status, and whether a document is required together. Show a clear validation error while keeping entered task instructions. | Implemented environment / deployment check; not a 501 skeleton test. |

## Spec gaps

- FR-T01 through FR-T03 all have criteria; AC-T01 through AC-T03 all have requirements.
- Configured type/size values are unspecified. The 8-byte limit and application/pdf policy are test fixtures, not defaults. Content sniffing rules are not defined.
- Reopen, replacement of evidence after completion, and permission provisioning are not defined. No tests choose those policies.
- If several inputs are invalid, the spec does not specify error precedence. Rejection tests deliberately isolate one invalid condition. Pagination, maximum response sizes, and error message wording are unspecified.
- NFRs have Validation entries rather than separate AC IDs. API-addressable parts are covered by the extra cases above; deployment and UI checks remain environment tests.
