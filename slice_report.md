# Slice 2: Assign and list a task

Changed application files: `app/access_control.py`, `app/task_workflow.py`.

Full suite: **10 passed, 20 failed**. See pytest_output.txt.

Target tests still failing: `test_AC_T03_extra_offset`. The test expects HTTP 201 but references referral `r1`, which is missing from its fixture. The implementation returns 422 because the referral must belong to the assigned patient. The scenario passed in a separate run with a matching referral seeded in memory. No test files were changed.

Previously passing acceptance tests now failing: none. The unchanged all-501 smoke test is the approved baseline exception; after Slice 2 it remains red. The remaining 18 failures relate to later slices that are not implemented.

The routes operate with the existing injected dependencies. An authorized nurse can assign a task with valid instructions and a future due date, and the patient can view the saved task. The default persistence backend and live adapters remain stubs; the application factory can be exercised with the original pytest fixtures.
