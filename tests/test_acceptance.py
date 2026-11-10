from pathlib import Path
import json
from .support import run_case

CASES = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))


def test_AC_P01_1_summary():
    run_case(CASES['AC-P01-1-summary'])


def test_AC_P01_2_none():
    run_case(CASES['AC-P01-2-none'])


def test_AC_P01_3_guidance():
    run_case(CASES['AC-P01-3-guidance'])


def test_AC_P02_1_appointment():
    run_case(CASES['AC-P02-1-appointment'])


def test_AC_P02_1_task():
    run_case(CASES['AC-P02-1-task'])


def test_AC_P02_2_deduplicate():
    run_case(CASES['AC-P02-2-deduplicate'])


def test_AC_P02_3_canceled():
    run_case(CASES['AC-P02-3-canceled'])


def test_AC_P02_3_completed():
    run_case(CASES['AC-P02-3-completed'])


def test_AC_P02_4_reschedule():
    run_case(CASES['AC-P02-4-reschedule'])


def test_AC_P02_5_missing_contact():
    run_case(CASES['AC-P02-5-missing_contact'])


def test_AC_P02_5_missing_timing():
    run_case(CASES['AC-P02-5-missing_timing'])


def test_AC_P02_6_failure():
    run_case(CASES['AC-P02-6-failure'])


def test_AC_P03_1_authority():
    run_case(CASES['AC-P03-1-authority'])


def test_AC_P03_2_appt_only():
    run_case(CASES['AC-P03-2-appt-only'])


def test_AC_P03_3_expired():
    run_case(CASES['AC-P03-3-expired'])


def test_AC_P03_3_expired_control():
    run_case(CASES['AC-P03-3-expired-control'])


def test_AC_P03_3_revoked():
    run_case(CASES['AC-P03-3-revoked'])


def test_AC_P03_3_revoked_control():
    run_case(CASES['AC-P03-3-revoked-control'])


def test_AC_P03_3_missing():
    run_case(CASES['AC-P03-3-missing'])


def test_AC_P03_3_missing_control():
    run_case(CASES['AC-P03-3-missing-control'])


def test_AC_P04_1():
    run_case(CASES['AC-P04-1'])


def test_AC_P04_1_control():
    run_case(CASES['AC-P04-1-control'])


def test_AC_P04_2():
    run_case(CASES['AC-P04-2'])


def test_AC_P04_2_control():
    run_case(CASES['AC-P04-2-control'])


def test_AC_P04_3():
    run_case(CASES['AC-P04-3'])


def test_AC_P04_3_control():
    run_case(CASES['AC-P04-3-control'])


def test_AC_P02_extra_early():
    run_case(CASES['AC-P02-extra-early'])


def test_AC_P02_extra_uncertain():
    run_case(CASES['AC-P02-extra-uncertain'])


def test_AC_P02_extra_concurrent():
    run_case(CASES['AC-P02-extra-concurrent'])


def test_AC_P01_extra_freshness():
    run_case(CASES['AC-P01-extra-freshness'])
