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
