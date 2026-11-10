from pathlib import Path
import json
from .support import run_case

CASES = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))


def test_AC_R01_submit():
    run_case(CASES['AC-R01-submit'])


def test_AC_R01_missing_patient_id():
    run_case(CASES['AC-R01-missing-patient_id'])


def test_AC_R01_missing_patient_id_control():
    run_case(CASES['AC-R01-missing-patient_id-control'])


def test_AC_R01_missing_receiving_provider_id():
    run_case(CASES['AC-R01-missing-receiving_provider_id'])


def test_AC_R01_missing_receiving_provider_id_control():
    run_case(CASES['AC-R01-missing-receiving_provider_id-control'])


def test_AC_R01_missing_service():
    run_case(CASES['AC-R01-missing-service'])


def test_AC_R01_missing_service_control():
    run_case(CASES['AC-R01-missing-service-control'])


def test_AC_R01_missing_reason():
    run_case(CASES['AC-R01-missing-reason'])


def test_AC_R01_missing_reason_control():
    run_case(CASES['AC-R01-missing-reason-control'])


def test_AC_R01_missing_urgency():
    run_case(CASES['AC-R01-missing-urgency'])


def test_AC_R01_missing_urgency_control():
    run_case(CASES['AC-R01-missing-urgency-control'])


def test_AC_R02_accept():
    run_case(CASES['AC-R02-accept'])


def test_AC_R02_redirect_missing():
    run_case(CASES['AC-R02-redirect-missing'])


def test_AC_R02_redirect_missing_control():
    run_case(CASES['AC-R02-redirect-missing-control'])


def test_AC_R02_extra_stale():
    run_case(CASES['AC-R02-extra-stale'])


def test_AC_R02_extra_stale_control():
    run_case(CASES['AC-R02-extra-stale-control'])


def test_AC_R02_extra_identity():
    run_case(CASES['AC-R02-extra-identity'])


def test_AC_R02_extra_identity_control():
    run_case(CASES['AC-R02-extra-identity-control'])


def test_AC_R03_share():
    run_case(CASES['AC-R03-share'])


def test_AC_R03_extra_blank():
    run_case(CASES['AC-R03-extra-blank'])


def test_AC_R03_extra_blank_control():
    run_case(CASES['AC-R03-extra-blank-control'])


def test_AC_R04_filters():
    run_case(CASES['AC-R04-filters'])


def test_AC_R05_roundtrip():
    run_case(CASES['AC-R05-roundtrip'])


def test_AC_R05_missing_recipient():
    run_case(CASES['AC-R05-missing-recipient'])


def test_AC_R05_missing_recipient_control():
    run_case(CASES['AC-R05-missing-recipient-control'])


def test_AC_R05_extra_recipient():
    run_case(CASES['AC-R05-extra-recipient'])


def test_AC_R05_extra_recipient_control():
    run_case(CASES['AC-R05-extra-recipient-control'])


def test_AC_R06_history():
    run_case(CASES['AC-R06-history'])


def test_AC_R06_duplicate():
    run_case(CASES['AC-R06-duplicate'])


def test_AC_R06_unmapped():
    run_case(CASES['AC-R06-unmapped'])


def test_AC_R06_extra_untrusted():
    run_case(CASES['AC-R06-extra-untrusted'])


def test_AC_R06_extra_untrusted_control():
    run_case(CASES['AC-R06-extra-untrusted-control'])


def test_AC_R06_extra_rollback():
    run_case(CASES['AC-R06-extra-rollback'])


def test_AC_R06_extra_rollback_control():
    run_case(CASES['AC-R06-extra-rollback-control'])


def test_AC_R01_extra_type():
    run_case(CASES['AC-R01-extra-type'])


def test_AC_R01_extra_type_control():
    run_case(CASES['AC-R01-extra-type-control'])


def test_AC_R06_extra_concurrent():
    run_case(CASES['AC-R06-extra-concurrent'])
