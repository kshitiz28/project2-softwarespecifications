# CarePath — Kshitiz

From this folder:

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal with the environment active:

```sh
python -m pytest -q tests/test_skeleton.py
python -m pytest -q --tb=line tests/test_acceptance.py
```

The smoke check expects 501 from each documented route. Acceptance tests expect the actual future behavior and intentionally fail while it is missing. Use a different port if running several folders at once.

- contracts.md describes module signatures, injections and HTTP routes.
- test_plan.md refines the source acceptance criteria and records unresolved spec gaps.
- tests/cases.json contains the executable fixtures, with controls next to rejection cases.
- tests/support.py is test-only instrumentation. No database or external provider is contacted.