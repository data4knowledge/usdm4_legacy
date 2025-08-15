import re
import json
from tests.usdm4_legacy.errors.errors_clean import errors_clean_all
from tests.usdm4_legacy.files.files import read_json, write_json, write_yaml, read_yaml
from src.usdm4_legacy import USDM4Legacy
from usdm4.api.wrapper import Wrapper

SAVE = True

# @pytest.fixture
# def anyio_backend():
#     return "asyncio"


def _run_test(dir, name):
    filename = f"{name}.pdf"
    filepath = _full_path(dir, filename)
    legacy = USDM4Legacy()
    wrapper: Wrapper = legacy.from_pdf(filepath)
    print(f"ERRORS: {legacy.errors.dump(0)}")
    result = wrapper.to_json()
    result = replace_uuid(result)
    # print(f"MATCH: {result[10:70]}")
    pretty_result = json.dumps(json.loads(result), indent=2)
    result_filename = filename = f"{name}_usdm.json"
    error_filename = filename = f"{name}_errors.yaml"
    if SAVE:
        write_json(_full_path(dir, result_filename), result)
        write_yaml(_full_path(dir, error_filename), errors_clean_all(legacy.errors))
    expected = read_json(_full_path(dir, result_filename))
    assert pretty_result == expected
    error_expected = read_yaml(_full_path(dir, error_filename))
    assert errors_clean_all(legacy.errors) == error_expected


def _full_path(dir, filename):
    return f"tests/usdm4_legacy/test_files/{dir}/{filename}"


#@pytest.mark.anyio
def test_nct04184622():
    _run_test("protocols", "NCT04184622")


def replace_uuid(result):
    return re.sub(
        r"[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}",
        "FAKE",
        result,
    )
