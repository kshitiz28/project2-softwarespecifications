"""Deterministic test doubles; not imported by the application."""
from collections import Counter
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Barrier, RLock
from fastapi.testclient import TestClient
from app.main import create_app
from app.types import ContractError

IDENTITIES = {
    "sender": {"id":"sender","role":"referring_provider","patient_ids":["p1"]},
    "receiver":{"id":"receiver","role":"receiving_provider","patient_ids":["p1"]},
    "other-provider":{"id":"other-provider","role":"receiving_provider","patient_ids":["p1"]},
    "coordinator":{"id":"coordinator","role":"coordinator","patient_ids":["p1"]},
    "nurse":{"id":"nurse","role":"nurse","patient_ids":["p1"]},
    "staff":{"id":"staff","role":"scheduling_staff","patient_ids":["p1"]},
    "patient":{"id":"patient","role":"patient","patient_id":"p1"},
    "other-patient":{"id":"other-patient","role":"patient","patient_id":"p2"},
    "rep":{"id":"rep","role":"representative"},
    "trusted":{"id":"trusted","role":"external_source","trusted":True},
    "untrusted":{"id":"untrusted","role":"external_source","trusted":False},
    "reminder-service":{"id":"reminder-service","role":"reminder_service"},
}

class FixtureStore:
    def __init__(self, seed):
        self.data = deepcopy({"identities": IDENTITIES, "urgencies":{"Urgent":{"value":"Urgent"},"Routine":{"value":"Routine"}}, **seed})
        self.lock = RLock()
        self.fail = False

    def snapshot(self):
        with self.lock:
            return deepcopy(self.data)

    def get(self, table, key):
        with self.lock:
            return deepcopy(self.data.get(table, {}).get(key))

    def list(self, table):
        with self.lock:
            return deepcopy(list(self.data.get(table, {}).values()))

    def commit(self, writes):
        with self.lock:
            if self.fail:
                raise ContractError(500, "persistence_error", "Injected commit failure")
            candidate = deepcopy(self.data)
            for w in writes:
                current = candidate.get(w.table, {}).get(w.key)
                if (w.require_absent and current is not None) or (w.expected is not None and current != w.expected):
                    raise ContractError(409, "write_conflict", "Record changed")
                if w.value is None:
                    candidate.get(w.table, {}).pop(w.key, None)
                else:
                    candidate.setdefault(w.table, {})[w.key] = deepcopy(w.value)
            self.data = candidate

def subset(actual, expected):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), actual
        for key, val in expected.items():
            assert key in actual, (key, actual)
            subset(actual[key], val)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), (actual, expected)
        remaining = list(actual)
        for item in expected:
            for i, val in enumerate(remaining):
                try:
                    subset(val, item)
                except AssertionError:
                    continue
                remaining.pop(i)
                break
            else:
                raise AssertionError((actual, expected))
    else:
        assert actual == expected, (actual, expected)

def run_case(case):
    store = FixtureStore(case["seed"])
    clock_value = ["2026-11-10T10:00:00Z"]
    lock = RLock()
    counters = Counter()
    calls = []

    def clock():
        return datetime.fromisoformat(clock_value[0].replace("Z", "+00:00"))

    def make_id(kind):
        with lock:
            counters[kind] += 1
            return f"{kind}-{counters[kind]}"

    def schedule(operation, payload, timeout_seconds):
        with lock:
            calls.append((operation, deepcopy(payload), timeout_seconds))
        reply = case["external"].get(operation)
        if operation == "slots":
            return {"items": deepcopy(reply or [])}
        assert reply is not None, f"Unexpected scheduler operation: {operation}"
        if reply.get("outcome") == "timeout":
            raise TimeoutError("Injected scheduler timeout")
        return deepcopy(reply)

    def send(payload):
        with lock:
            calls.append(("send", deepcopy(payload), None))
        reply = case["external"].get("send", {"outcome":"submitted"})
        if reply.get("outcome") == "timeout":
            raise TimeoutError("Injected delivery timeout")
        return deepcopy(reply)

    app = create_app(store=store, clock=clock, id_factory=make_id, schedule=schedule)
    def invoke(client, s):
        headers = {"Authorization": "Bearer "+s["token"]} if s["token"] is not None else {}
        kwargs = {"json":s["body"]} if "body" in s else {}
        return client.request(s["method"],s["url"],headers=headers,**kwargs)

    def check(s, response, before, offset):
        assert response.status_code == s["status"], (
            f"Expected HTTP {s['status']}, got {response.status_code}; body={response.text}"
        )
        body = response.json()
        if "exact" in s:
            assert body == s["exact"]
        subset(body, s.get("fields", {}))
        if s["status"] >= 400:
            assert isinstance(body.get("message"), str) and body["message"]
            assert set(body) <= {"error", "message", "field"}, "Unexpected fields in error response"
        for field in s.get("absent", []):
            assert field not in body
        after = store.snapshot()
        for table in s.get("unchanged", []):
            if table == "*":
                assert after == before, "Rejection/read/replay changed state"
            else:
                assert after.get(table,{}) == before.get(table,{})
        for table, count in s.get("count", {}).items():
            assert len(after.get(table,{})) == count, (table, after.get(table,{}))
        for table, key, record in s.get("records", []):
            assert key in after.get(table,{}), (table,key)
            subset(after[table][key],record)
        for table,key,field,forbidden in s.get("not_values", []):
            assert after[table][key][field] not in forbidden
        for op, count in s.get("external", {}).items():
            assert sum(c[0]==op for c in calls[offset:]) == count, (op,calls[offset:])
        for op,payload,timeout in calls[offset:]:
            if op != "send":
                assert timeout == 10
            else:
                assert isinstance(payload.get("message"),str) and "CarePath" in payload["message"]
                assert not ({"findings","documents","clinical_text","content_base64"} & payload.keys())
                if "send_payload" in s:
                    subset(payload,s["send_payload"])

    if case["concurrent"]:
        barrier = Barrier(len(case["steps"]))
        def worker(s):
            with TestClient(app) as client:
                barrier.wait(timeout=5)
                return invoke(client,s)
        before = store.snapshot()
        with ThreadPoolExecutor(max_workers=len(case["steps"])) as pool:
            responses = list(pool.map(worker,case["steps"]))
        # Match by status and, for two successes, by submitted count if specified.
        assert sorted(r.status_code for r in responses) == sorted(s["status"] for s in case["steps"]), (
            f"Expected concurrent HTTP statuses {[s['status'] for s in case['steps']]}, got {[r.status_code for r in responses]}"
        )
        remaining = list(responses)
        for s in case["steps"]:
            idx = next((i for i,r in enumerate(remaining) if r.status_code==s["status"] and
                ("submitted" not in s.get("fields",{}) or r.json().get("submitted")==s["fields"]["submitted"]) and
                ("outcome" not in s.get("fields",{}) or r.json().get("outcome")==s["fields"]["outcome"])), None)
            assert idx is not None, "No matching concurrent outcome"
            check(s,remaining.pop(idx),before,0)
        return

    with TestClient(app) as client:
        for s in case["steps"]:
            if "clock" in s:
                clock_value[0] = s["clock"]
            for table,key,value in s.get("edit",[]):
                store.data.setdefault(table,{})[key]=deepcopy(value)
            store.fail = s.get("fail_commit",False)
            before,offset = store.snapshot(),len(calls)
            check(s,invoke(client,s),before,offset)
