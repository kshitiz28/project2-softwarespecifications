# Sangam — Slice 1: Show an owned care summary

Changed application files: `app/access_control.py`, `app/patient_views.py`.

Full suite: **12 passed, 19 failed**. See pytest_output.txt.

Target tests still failing: none.

Previously passing acceptance tests now failing: none. The unchanged all-501 smoke test is the approved baseline exception; after Slice 1 it remains red.

The route operates with the existing injected dependencies. The default persistence backend and live adapters remain stubs; the application factory can be exercised with the original pytest fixtures.
