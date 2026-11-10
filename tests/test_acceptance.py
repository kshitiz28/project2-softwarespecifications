from pathlib import Path
import json
from .support import run_case

CASES = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))


def test_AC_A01_1_slots():
    run_case(CASES['AC-A01-1-slots'])


def test_AC_A01_2_book():
    run_case(CASES['AC-A01-2-book'])


def test_AC_A01_3_unavailable():
    run_case(CASES['AC-A01-3-unavailable'])


def test_AC_A01_3_unavailable_control():
    run_case(CASES['AC-A01-3-unavailable-control'])


def test_AC_A01_4_timeout():
    run_case(CASES['AC-A01-4-timeout'])


def test_AC_A01_4_control():
    run_case(CASES['AC-A01-4-control'])


def test_AC_A01_5_concurrent():
    run_case(CASES['AC-A01-5-concurrent'])


def test_AC_A02_1_reschedule():
    run_case(CASES['AC-A02-1-reschedule'])


def test_AC_A02_2_rejected():
    run_case(CASES['AC-A02-2-rejected'])


def test_AC_A02_2_rejected_control():
    run_case(CASES['AC-A02-2-rejected-control'])


def test_AC_A02_3_cancel():
    run_case(CASES['AC-A02-3-cancel'])


def test_AC_A02_4_reason():
    run_case(CASES['AC-A02-4-reason'])


def test_AC_A02_4_reason_control():
    run_case(CASES['AC-A02-4-reason-control'])


def test_AC_A02_5_completed():
    run_case(CASES['AC-A02-5-completed'])


def test_AC_A02_5_completed_control():
    run_case(CASES['AC-A02-5-completed-control'])


def test_AC_A02_5_canceled():
    run_case(CASES['AC-A02-5-canceled'])


def test_AC_A02_5_canceled_control():
    run_case(CASES['AC-A02-5-canceled-control'])


def test_AC_A02_5_no_show():
    run_case(CASES['AC-A02-5-no-show'])


def test_AC_A02_5_no_show_control():
    run_case(CASES['AC-A02-5-no-show-control'])


def test_AC_A03_1_history():
    run_case(CASES['AC-A03-1-history'])


def test_AC_A03_2_append():
    run_case(CASES['AC-A03-2-append'])


def test_AC_A03_3_no_false_history():
    run_case(CASES['AC-A03-3-no-false-history'])


def test_AC_A03_3_no_false_history_control():
    run_case(CASES['AC-A03-3-no-false-history-control'])


def test_AC_A01_extra_role():
    run_case(CASES['AC-A01-extra-role'])


def test_AC_A01_extra_role_control():
    run_case(CASES['AC-A01-extra-role-control'])


def test_AC_A02_extra_type():
    run_case(CASES['AC-A02-extra-type'])


def test_AC_A02_extra_type_control():
    run_case(CASES['AC-A02-extra-type-control'])


def test_AC_A01_extra_referral_state():
    run_case(CASES['AC-A01-extra-referral-state'])


def test_AC_A01_extra_referral_state_control():
    run_case(CASES['AC-A01-extra-referral-state-control'])


def test_AC_A01_extra_slot_boundary():
    run_case(CASES['AC-A01-extra-slot-boundary'])


def test_AC_A01_extra_slot_boundary_control():
    run_case(CASES['AC-A01-extra-slot-boundary-control'])


def test_AC_A01_5_extra_active():
    run_case(CASES['AC-A01-5-extra-active'])


def test_AC_A01_5_extra_active_control():
    run_case(CASES['AC-A01-5-extra-active-control'])
