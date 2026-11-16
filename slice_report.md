# Kshitiz — Slice 2: Reject invalid referral input

Changed application files: `app/referral_workflow.py`.

Full suite: **13 passed, 25 failed**. See pytest_output.txt.

Target tests still failing: none.

Previously passing acceptance tests now failing: none. The unchanged all-501 smoke test is the approved baseline exception; after Slice 1 it remains red.

The route operates with the existing injected dependencies. The default persistence backend and live adapters remain stubs; the application factory can be exercised with the original pytest fixtures.
