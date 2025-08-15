import re
from simple_error_log.errors import Errors

def errors_clean_all(errors: Errors) -> list[dict]:
    result = errors.dump(0)
    for item in result:
        item = _fix_timestamp(item)
    return result

def error_clean(errors: Errors, index=0) -> dict:
    result = errors._items[index].to_dict()
    return _fix_timestamp(result)

def _fix_timestamp(data: dict) -> dict:
    timestamp_pattern = r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\.(\d{6})"
    if "timestamp" in data:
        data["timestamp"] = re.sub(
            timestamp_pattern, "YYYY-MM-DD HH:MM:SS.nnnnnn", data["timestamp"]
        )
    return data