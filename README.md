# CarePath 

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

The smoke check expects 501 from each documented route and is treated as a baseline-only check. The full suite has 10 passing and 20 failing tests. One Slice 2 test fails because its fixture references a missing referral; the other failures are related to unimplemented later slices or the baseline smoke check. See pytest_output.txt for the full run and slice_report.md for details. The default persistence backend is still a stub; working Slice 1 and Slice 2 behavior can be exercised using the injected pytest fixtures. Use a different port if running several folders at once.

- contracts.md describes module signatures, injections and HTTP routes.
- test_plan.md refines the source acceptance criteria and records unresolved spec gaps.
- tests/cases.json contains the executable fixtures, with controls next to rejection cases.
- tests/support.py is test-only instrumentation. No database or external provider is contacted.

Reference: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) and [error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/).
