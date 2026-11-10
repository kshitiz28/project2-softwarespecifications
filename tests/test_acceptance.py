from pathlib import Path
import json
from .support import run_case

CASES = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))


def test_AC_T01_assign():
    run_case(CASES['AC-T01-assign'])


def test_AC_T01_instructions():
    run_case(CASES['AC-T01-instructions'])


def test_AC_T01_instructions_control():
    run_case(CASES['AC-T01-instructions-control'])


def test_AC_T01_due_at():
    run_case(CASES['AC-T01-due_at'])


def test_AC_T01_due_at_control():
    run_case(CASES['AC-T01-due_at-control'])


def test_AC_T01_due_at_past():
    run_case(CASES['AC-T01-due_at-past'])


def test_AC_T01_due_at_past_control():
    run_case(CASES['AC-T01-due_at-past-control'])


def test_AC_T01_due_at_type():
    run_case(CASES['AC-T01-due_at-type'])


def test_AC_T01_due_at_type_control():
    run_case(CASES['AC-T01-due_at-type-control'])


def test_AC_T02_evidence():
    run_case(CASES['AC-T02-evidence'])


def test_AC_T02_no_document():
    run_case(CASES['AC-T02-no-document'])


def test_AC_T02_no_document_control():
    run_case(CASES['AC-T02-no-document-control'])


def test_AC_T02_size():
    run_case(CASES['AC-T02-size'])


def test_AC_T02_size_control():
    run_case(CASES['AC-T02-size-control'])


def test_AC_T02_type():
    run_case(CASES['AC-T02-type'])


def test_AC_T02_type_control():
    run_case(CASES['AC-T02-type-control'])


def test_AC_T02_repeat():
    run_case(CASES['AC-T02-repeat'])


def test_AC_T03_overdue():
    run_case(CASES['AC-T03-overdue'])


def test_AC_T03_extra_clock_before():
    run_case(CASES['AC-T03-extra-clock-before'])


def test_AC_T03_extra_clock_after():
    run_case(CASES['AC-T03-extra-clock-after'])


def test_AC_T02_extra_identity():
    run_case(CASES['AC-T02-extra-identity'])


def test_AC_T02_extra_identity_control():
    run_case(CASES['AC-T02-extra-identity-control'])


def test_AC_T02_extra_rollback():
    run_case(CASES['AC-T02-extra-rollback'])


def test_AC_T02_extra_rollback_control():
    run_case(CASES['AC-T02-extra-rollback-control'])


def test_AC_T02_extra_concurrent():
    run_case(CASES['AC-T02-extra-concurrent'])


def test_AC_T01_extra_list_empty():
    run_case(CASES['AC-T01-extra-list-empty'])


def test_AC_T02_extra_document_access():
    run_case(CASES['AC-T02-extra-document-access'])


def test_AC_T02_extra_document_access_control():
    run_case(CASES['AC-T02-extra-document-access-control'])


def test_AC_T03_extra_offset():
    run_case(CASES['AC-T03-extra-offset'])
