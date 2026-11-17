# Slice 1: Read a patient’s empty task list

Changed application files: `app/access_control.py`, `app/task_workflow.py`.

Full suite: **1 passed, 29 failed**. See pytest_output.txt.

Target tests still failing: none.

Previously passing acceptance tests now failing: none. The unchanged all-501 smoke test is the approved baseline exception; after Slice 1 it remains red.

The route operates with the existing injected dependencies. The default persistence backend and live adapters remain stubs; the application factory can be exercised with the original pytest fixtures.
