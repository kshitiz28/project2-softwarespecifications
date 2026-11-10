# CarePath test plan

Table refinement of the numbered acceptance checks in spec.md. Each unique test ID extends its original AC identifier.

Frozen clock: 2026-11-10T10:00:00Z unless a step changes it. Fixture data is fictional. Expected domain values were derived from the spec; HTTP status, field names and deterministic identifiers come from contracts.md. Tests use an isolated state per case. Controls change only the invalid input, caller, initial state, or external result under test. **Unchanged [*]** means no persisted state changed or was created. Suppression and unresolved attempts can record the bookkeeping explicitly allowed by the plan.

All executable cases below are included because no subset of AC IDs was specified. The fixture credential-to-identity mapping is in contracts.md and tests/support.py; the JSON catalog is a test fixture, not implementation code. Where relevant, scheduler calls use a 10-second budget; reminder sends check the channel/destination and omit clinical data.

| ID | Requirement | Cases | Inside/outside | Control |
|---|---|---|---|---|
| AC-P01.1 | FR-P01 / AC-P01 | **AC-P01-1-summary**: Show status, last update, requests, task and active appointment. Seed F1. GET /patients/p1/care-summary; credential=patient → HTTP 200, JSON contains {"patient_id":"p1","referrals":[{"id":"r1","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","outstanding_requests":[{"id":"req1","item":"Summary PDF"}],"guidance":"Bring your existing report."}],"appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}],"tasks":[{"id":"t1","status":"Open","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z"}]}; unchanged tables ["*"] (* = full snapshot) | — | — |
| AC-P01.2 | FR-P01 / AC-P01 | **AC-P01-2-none**: No outstanding actions. Seed F2. GET /patients/p1/care-summary; credential=patient → HTTP 200, JSON contains {"patient_id":"p1","tasks":[],"next_action":"No action currently required"}; unchanged tables ["*"] (* = full snapshot) | — | — |
| AC-P01.3 | FR-P01 / AC-P01 | **AC-P01-3-guidance**: Use recorded guidance only. Seed F1. GET /patients/p1/care-summary; credential=patient → HTTP 200, JSON contains {"referrals":[{"id":"r1","guidance":"Bring your existing report."}]}; unchanged tables ["*"] (* = full snapshot) | — | — |
| AC-P02.1 | FR-P02 / AC-P02 | **AC-P02-1-appointment**: Appointment reminder uses email preference. Seed F3. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":1,"skipped":0,"failed":0}; final row counts {"notifications":1}; stored rows contain [["notifications","notification-1",{"patient_id":"p1","channel":"email","status":"Submitted","object_id":"a1","scheduled_at":"2026-11-10T10:00:00Z"}]]; external calls {"send":1}; provider payload includes {"channel":"email","destination":"p1@example.invalid","object_id":"a1"}<br><br>**AC-P02-1-task**: Task reminder uses text preference. Seed F4. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":1,"skipped":0,"failed":0}; final row counts {"notifications":1}; stored rows contain [["notifications","notification-1",{"patient_id":"p1","channel":"text","status":"Submitted","object_id":"t1","scheduled_at":"2026-11-10T10:00:00Z"}]]; external calls {"send":1}; provider payload includes {"channel":"text","destination":"+15550100001","object_id":"t1"} | — | — |
| AC-P02.2 | FR-P02 / AC-P02 | **AC-P02-2-deduplicate**: Rerun produces no second send. Seed F3. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":1,"skipped":0,"failed":0}; final row counts {"notifications":1}; stored rows contain [["notifications","notification-1",{"patient_id":"p1","channel":"email","status":"Submitted","object_id":"a1","scheduled_at":"2026-11-10T10:00:00Z"}]]; external calls {"send":1}; provider payload includes {"channel":"email","destination":"p1@example.invalid","object_id":"a1"}; then POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"skipped":1,"failed":0}; unchanged tables ["*"] (* = full snapshot); external calls {"send":0} | — | — |
| AC-P02.3 | FR-P02 / AC-P02 | **AC-P02-3-canceled**: Suppress Canceled reminder. Seed F5. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"skipped":1,"failed":0}; final row counts {"notifications":0}; external calls {"send":0}<br><br>**AC-P02-3-completed**: Suppress Completed reminder. Seed F6. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"skipped":1,"failed":0}; final row counts {"notifications":0}; external calls {"send":0} | — | AC-P02-3-canceled → AC-P02-1-appointment; AC-P02-3-completed → AC-P02-1-task |
| AC-P02.4 | FR-P02 / AC-P02 | **AC-P02-4-reschedule**: Old unsent reminder is replaced at new time. Seed F7. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"failed":0}; stored rows contain [["notifications","old",{"status":"Superseded"}]]; external calls {"send":0}; then POST /reminders/run; credential=reminder-service; JSON {}; set clock 2026-11-11T10:00:00Z → HTTP 200, JSON contains {"submitted":1,"failed":0}; stored rows contain [["notifications","notification-1",{"scheduled_at":"2026-11-11T10:00:00Z","object_id":"a1","status":"Submitted"}]]; external calls {"send":1}; provider payload includes {"channel":"email","destination":"p1@example.invalid","object_id":"a1"} | — | — |
| AC-P02.5 | FR-P02 / AC-P02 | **AC-P02-5-missing_contact**: No send when missing contact. Seed F8. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"skipped":1,"failed":0}; stored rows contain [["notifications","notification-1",{"status":"Suppressed","reason":"missing_contact"}]]; external calls {"send":0}<br><br>**AC-P02-5-missing_timing**: No send when missing timing. Seed F9. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"skipped":1,"failed":0}; stored rows contain [["notifications","notification-1",{"status":"Suppressed","reason":"missing_timing"}]]; external calls {"send":0} | — | AC-P02-5-missing_contact → AC-P02-1-appointment; AC-P02-5-missing_timing → AC-P02-1-appointment |
| AC-P02.6 | FR-P02 / AC-P02 | **AC-P02-6-failure**: Record failure without claiming receipt. Seed F3. External replies {"send":{"outcome":"failed"}}. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"skipped":0,"failed":1}; stored rows contain [["notifications","notification-1",{"status":"Failed","delivered":false}]]; external calls {"send":1}; provider payload includes {"channel":"email","destination":"p1@example.invalid","object_id":"a1"} | — | AC-P02-6-failure → AC-P02-1-appointment |
| AC-P03.1 | FR-P03 / AC-P03 | **AC-P03-1-authority**: Representative with valid scoped authority. Seed F10. GET /patients/p1/care-summary; credential=rep → HTTP 200, JSON contains {"patient_id":"p1","referrals":[{"id":"r1","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","outstanding_requests":[{"id":"req1","item":"Summary PDF"}],"guidance":"Bring your existing report."}],"appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}],"tasks":[{"id":"t1","status":"Open","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z"}]}; unchanged tables ["*"] (* = full snapshot) | — | — |
| AC-P03.2 | FR-P03 / AC-P03 | **AC-P03-2-appt-only**: Only appointment category returned. Seed F11. GET /patients/p1/care-summary; credential=rep → HTTP 200, JSON contains {"patient_id":"p1","appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}]}; absent fields ["referrals","tasks","next_action"]; unchanged tables ["*"] (* = full snapshot) | — | — |
| AC-P03.3 | FR-P03 / AC-P03 | **AC-P03-3-expired**: Reject expired authority. Seed F12. GET /patients/p1/care-summary; credential=rep → HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; absent fields ["patient_id","referrals","tasks","appointments","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P03-3-expired-control**: Control: Reject expired authority. Seed F13. GET /patients/p1/care-summary; credential=rep → HTTP 200, JSON contains {"patient_id":"p1","appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}]}; absent fields ["referrals","tasks","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P03-3-revoked**: Reject revoked authority. Seed F14. GET /patients/p1/care-summary; credential=rep → HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; absent fields ["patient_id","referrals","tasks","appointments","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P03-3-revoked-control**: Control: Reject revoked authority. Seed F11. GET /patients/p1/care-summary; credential=rep → HTTP 200, JSON contains {"patient_id":"p1","appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}]}; absent fields ["referrals","tasks","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P03-3-missing**: Reject missing authority. Seed F15. GET /patients/p1/care-summary; credential=rep → HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; absent fields ["patient_id","referrals","tasks","appointments","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P03-3-missing-control**: Control: Reject missing authority. Seed F11. GET /patients/p1/care-summary; credential=rep → HTTP 200, JSON contains {"patient_id":"p1","appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}]}; absent fields ["referrals","tasks","next_action"]; unchanged tables ["*"] (* = full snapshot) | Expiry one second before request denied; future expiry accepted | AC-P03-3-expired → AC-P03-3-expired-control; AC-P03-3-revoked → AC-P03-3-revoked-control; AC-P03-3-missing → AC-P03-3-missing-control |
| AC-P04.1 | FR-P04 / AC-P04 | **AC-P04-1**: Reject unauthorized direct read. Seed F16. GET /patients/p1/care-summary; credential=none → HTTP 401, JSON contains {"error":"unauthenticated"} and nonempty message; absent fields ["patient_id","referrals","tasks","appointments","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P04-1-control**: Control: Reject unauthorized direct read. Seed F16. GET /patients/p1/care-summary; credential=patient → HTTP 200, JSON contains {"patient_id":"p1","referrals":[{"id":"r1","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","outstanding_requests":[{"id":"req1","item":"Summary PDF"}],"guidance":"Bring your existing report."}],"appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}],"tasks":[{"id":"t1","status":"Open","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z"}]}; unchanged tables ["*"] (* = full snapshot) | — | AC-P04-1 → AC-P04-1-control |
| AC-P04.2 | FR-P04 / AC-P04 | **AC-P04-2**: Reject unauthorized direct read. Seed F16. GET /patients/p1/care-summary; credential=other-patient → HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; absent fields ["patient_id","referrals","tasks","appointments","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P04-2-control**: Control: Reject unauthorized direct read. Seed F16. GET /patients/p1/care-summary; credential=patient → HTTP 200, JSON contains {"patient_id":"p1","referrals":[{"id":"r1","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","outstanding_requests":[{"id":"req1","item":"Summary PDF"}],"guidance":"Bring your existing report."}],"appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}],"tasks":[{"id":"t1","status":"Open","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z"}]}; unchanged tables ["*"] (* = full snapshot) | — | AC-P04-2 → AC-P04-2-control |
| AC-P04.3 | FR-P04 / AC-P04 | **AC-P04-3**: Reject unauthorized direct read. Seed F16. GET /patients/p2/care-summary; credential=patient → HTTP 403, JSON contains {"error":"forbidden"} and nonempty message; absent fields ["patient_id","referrals","tasks","appointments","next_action"]; unchanged tables ["*"] (* = full snapshot)<br><br>**AC-P04-3-control**: Control: Reject unauthorized direct read. Seed F16. GET /patients/p1/care-summary; credential=patient → HTTP 200, JSON contains {"patient_id":"p1","referrals":[{"id":"r1","status":"Accepted","updated_at":"2026-11-10T09:59:59Z","outstanding_requests":[{"id":"req1","item":"Summary PDF"}],"guidance":"Bring your existing report."}],"appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}],"tasks":[{"id":"t1","status":"Open","instructions":"Upload summary","due_at":"2026-11-11T10:00:00Z"}]}; unchanged tables ["*"] (* = full snapshot) | — | AC-P04-3 → AC-P04-3-control |
| AC-P02-extra-early | FR-P02 / AC-P02 | **AC-P02-extra-early**: **Extra.** FR-P02: one second before configured send time. Seed F3. POST /reminders/run; credential=reminder-service; JSON {}; set clock 2026-11-10T09:59:59Z → HTTP 200, JSON contains {"submitted":0,"failed":0}; unchanged tables ["*"] (* = full snapshot); external calls {"send":0} | 09:59:59 no send; 10:00:00 eligible (AC-P02-1-appointment). | — |
| AC-P02-extra-uncertain | FR-P02 / AC-P02 | **AC-P02-extra-uncertain**: **Extra.** NFR-P03: uncertain provider outcome. Seed F3. External replies {"send":{"outcome":"timeout"}}. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"failed":0}; stored rows contain [["notifications","notification-1",{"status":"Uncertain","delivered":false}]]; external calls {"send":1}; provider payload includes {"channel":"email","destination":"p1@example.invalid","object_id":"a1"}; then POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"failed":0}; unchanged tables ["*"] (* = full snapshot); external calls {"send":0} | — | — |
| AC-P02-extra-concurrent | FR-P02 / AC-P02 | **AC-P02-extra-concurrent**: **Extra.** NFR-P03: concurrent scans claim one reminder. Seed F3. Submit concurrently; expected effects apply to the batch. POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":1,"failed":0}; final row counts {"notifications":1}; external calls {"send":1}; then POST /reminders/run; credential=reminder-service; JSON {} → HTTP 200, JSON contains {"submitted":0,"failed":0}; final row counts {"notifications":1}; external calls {"send":1} | — | — |
| AC-P01-extra-freshness | FR-P01 / AC-P01 | **AC-P01-extra-freshness**: **Extra.** NFR-P04: next read reflects committed cancellation. Seed F1. GET /patients/p1/care-summary; credential=patient → HTTP 200, JSON contains {"appointments":[{"id":"a1","starts_at":"2026-11-11T10:00:00Z","status":"Scheduled","provider_id":"receiver","location":"Clinic A"}]}; unchanged tables ["*"] (* = full snapshot); then GET /patients/p1/care-summary; credential=patient; fixture change [["appointments","a1",{"id":"a1","referral_id":"r1","patient_id":"p1","provider_id":"receiver","status":"Canceled","starts_at":"2026-11-11T10:00:00Z","location":"Clinic A","external_booking_id":"ext1"}]] → HTTP 200, JSON contains {"appointments":[]}; unchanged tables ["*"] (* = full snapshot) | — | — |

## Fixture records

The shared identity catalog, configured urgencies and clock are applied to each fixture. All other starting tables are empty.

**F1**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F2**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": []
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Completed",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F3**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {},
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F4**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {},
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "text",
      "address": "+15550100001"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F5**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Canceled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {},
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F6**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {},
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Completed",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F7**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-12T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {},
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  },
  "notifications": {
    "old": {
      "id": "old",
      "patient_id": "p1",
      "object_id": "a1",
      "channel": "email",
      "scheduled_at": "2026-11-10T10:00:00Z",
      "status": "Pending"
    }
  }
}
```

**F8**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {},
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {},
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F9**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {},
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {}
}
```

**F10**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    },
    "r2": {
      "id": "r2",
      "patient_id": "p2",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    },
    "a2": {
      "id": "a2",
      "referral_id": "r2",
      "patient_id": "p2",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    },
    "t2": {
      "id": "t2",
      "patient_id": "p2",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r2"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F11**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F12**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments"
      ],
      "expires_at": "2026-11-10T09:59:59Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F13**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments"
      ],
      "expires_at": "2026-11-10T10:00:01Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F14**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": true
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F15**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {},
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```

**F16**

```json
{
  "referrals": {
    "r1": {
      "id": "r1",
      "patient_id": "p1",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1,
      "guidance": "Bring your existing report.",
      "outstanding_requests": [
        {
          "id": "req1",
          "item": "Summary PDF"
        }
      ]
    },
    "r2": {
      "id": "r2",
      "patient_id": "p2",
      "referring_provider_id": "sender",
      "receiving_provider_id": "receiver",
      "service": "Cardiology",
      "reason": "Consultation",
      "urgency": "Urgent",
      "status": "Accepted",
      "updated_at": "2026-11-10T09:59:59Z",
      "version": 1
    }
  },
  "appointments": {
    "a1": {
      "id": "a1",
      "referral_id": "r1",
      "patient_id": "p1",
      "provider_id": "receiver",
      "status": "Scheduled",
      "starts_at": "2026-11-11T10:00:00Z",
      "location": "Clinic A",
      "external_booking_id": "ext1"
    }
  },
  "tasks": {
    "t1": {
      "id": "t1",
      "patient_id": "p1",
      "nurse_id": "nurse",
      "instructions": "Upload summary",
      "due_at": "2026-11-11T10:00:00Z",
      "status": "Open",
      "document_required": true,
      "referral_id": "r1"
    }
  },
  "authority": {
    "rep:p1": {
      "categories": [
        "appointments",
        "referrals",
        "tasks"
      ],
      "expires_at": "2026-11-11T10:00:00Z",
      "revoked": false
    }
  },
  "preferences": {
    "p1": {
      "channel": "email",
      "address": "p1@example.invalid"
    }
  },
  "reminder_settings": {
    "default": {
      "offset_seconds": 86400
    }
  }
}
```


## Gap checklist and environment checks

Returned fields and freshness: AC-P01. Timing, suppression, provider failures, and concurrent claims: AC-P02. Authority scope/expiry and direct identifier access: AC-P03/04. Reminder requests have no client-supplied timing field. Multiple-invalid-input precedence remains unspecified.

| NFR | Validation | Execution scope |
|---|---|---|
| NFR-P01 | Test another patient identifier and authority that expires or is revoked between reads. Target: Check identity and patient access on every request, including direct record identifiers. Recheck representative scope and validity on each read. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-P02 | Inspect actual reminder payloads and logs using fictional clinical records. Target: Use HTTPS outside local development. Email/text reminders and ordinary logs must contain no clinical findings or supporting documents. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-P03 | Use a controlled clock, repeated scans, concurrent scans, and a delivery timeout. Target: While the application and delivery service are available, submit an eligible reminder within 60 seconds after its configured time. Repeated scans must not submit the same scheduled reminder twice. Record uncertain delivery without claiming success. With a controlled clock and both services available, check submission elapsed 59s meets the bound and 61s misses it; this is a timing verdict, not a rule to discard late reminders. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-P04 | Change a booking/task before a read or send and check the resulting view or suppression. Target: Read committed care records on each page request. Immediately before reminder submission, recheck appointment/task status and time against the latest committed records. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-P05 | Measure summary reads at the stated test load. Target: For 20 simultaneous users and 10,000 combined care records, 95% of care-summary reads must return within 2 seconds, excluding external delivery time. Use 200 measured eligible requests at the specified 20-user, 10,000-record load; sort durations and check the 190th is at most 2,000 ms. Exercise 1,999 and 2,001 ms in the threshold check. | Implemented environment / deployment check; not a 501 skeleton test. |
| NFR-P06 | Use keyboard-only navigation and inspect labels, focus, status text, and an empty-action example. Target: Status/next-action views must work with keyboard navigation, visible focus, and labeled controls. Status must not be conveyed by color alone. Show a clear no-action message when appropriate. | Implemented environment / deployment check; not a 501 skeleton test. |

## Spec gaps

- FR-P01 through FR-P04 all have criteria; AC-P01 through AC-P04 all have requirements.
- Exact authority-expiry equality, valid-from handling, and authority provisioning are not specified. Tests use expired and unexpired records away from equality.
- Provider idempotency, how to reconcile a timeout, and catch-up after downtime are unspecified. Test only the documented local claim and uncertain result; no exactly-once external delivery claim.
- The draft does not define hard ordering between a cancellation and a send already in progress. Test a committed cancellation before the send check, not a stronger guarantee.
- If several inputs are invalid, the spec does not specify error precedence. Rejection tests deliberately isolate one invalid condition. Pagination, maximum response sizes, and error message wording are unspecified.
- NFRs have Validation entries rather than separate AC IDs. API-addressable parts are covered by the extra cases above; deployment and UI checks remain environment tests.
