import json
from tests.usdm4_legacy.helpers.uuid import replace_uuid
from tests.usdm4_legacy.helpers.errors_clean import errors_clean_all
from tests.usdm4_legacy.helpers.files import read_json, write_json, write_yaml, read_yaml
from src.usdm4_legacy import USDM4Legacy
from usdm4.api.wrapper import Wrapper
from usdm4 import USDM4

SAVE = False

def _run_test(name):
    filename = f"{name}.pdf"
    filepath = _full_path(name, filename)
    legacy = USDM4Legacy()
    wrapper: Wrapper = legacy.from_pdf(filepath)
    result = wrapper.to_json()
    result = replace_uuid(result)
    pretty_result = json.dumps(json.loads(result), indent=2)
    result_filename = f"{name}_usdm.json"
    error_filename = f"{name}_errors.yaml"
    if SAVE:
        write_json(_full_path(name, result_filename), result)
        write_yaml(_full_path(name, error_filename), errors_clean_all(legacy.errors))
    expected = read_json(_full_path(name, result_filename))
    assert pretty_result == expected
    error_expected = read_yaml(_full_path(name, error_filename))
    assert errors_clean_all(legacy.errors) == error_expected

def _validate(name):
    json_filename = f"{name}_usdm.json"
    result = USDM4().validate(_full_path(name, json_filename))
    print(
        f"RESULT: {[v for k, v in result._items.items() if v['status'] not in ['Not Implemented', 'Success']]}"
    )
    assert result.passed_or_not_implemented()

def _full_path(directory: str, filename: str) -> str:
    return f"tests/usdm4_legacy/test_files/protocols/{directory}/{filename}"

def test_nct01847274():
    _run_test("NCT01847274")

def test_nct03637764():
    _run_test("NCT03637764")

def test_nct04184622():
    _run_test("NCT04184622")

def test_nct04320615():
    _run_test("NCT04320615")

def test_validate():
    _validate("NCT01847274")
    _validate("NCT03637764")
    _validate("NCT04184622")
    _validate("NCT04320615")
