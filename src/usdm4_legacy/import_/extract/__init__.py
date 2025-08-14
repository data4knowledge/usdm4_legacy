from simple_error_log.errors import Errors
from simple_error_log.error_location import KlassMethodLocation
from usdm4_legacy.import_.extract.title_page import TitlePage


class ExtractStudy:
    MODULE = "usdm4_legacy.import_.extract.__init__.ExtractStudy"

    def __init__(self, sections: list[str], errors: Errors):
        self._sections = sections
        self._errors = errors

    def process(self) -> dict:
        try:
            result = {}
            title_page = TitlePage(self._sections, self._errors)
            tp_result = title_page.process()
            result["identification"] = self._identification(tp_result)
            result["document"] = {
                "document": {
                    "label": "Protocol Document",
                    "version": "",  # @todo
                    "status": "Final",  # @todo
                    "template": "Legacy",
                    "version_date": tp_result["other"]["approval_date"],
                },
                "sections": self._sections,
            }
            result["study_design"] = {
                "label": "Study Design 1",
                "rationale": "",  # @todo
                "trial_phase": tp_result["other"]["phase"],
            }
            result["population"] = {"label": "Default population"}
            result["study"] = {
                "approval_date": tp_result["other"]["approval_date"],
                "version": "1",  # @todo
                "rationale": "Not set",  # @todo
                "name": "STUDY",  # @todo
                "label": "STUDY",  # @todo
            }
            return result
        except Exception as e:
            print(f"Exception: {e}")
            location = KlassMethodLocation(self.MODULE, "process")
            self._errors.exception(
                f"Exception raised extracting study data",
                e,
                location,
            )
            return None

    def _identification(self, tp: dict) -> dict:
        try:
            print(f"\n\nTP: {tp}\n\n")
            result = {"titles": tp["titles"], "identifiers": []}
            for org in ["ct.gov", "fda"]:
                if org in tp:
                    result["identifiers"].append(
                        {
                            "identifier": tp[org]["identifier"],
                            "scope": {"standard": org},
                        }
                    )
            if "sponsor" in tp:
                result["identifiers"].append(
                    {
                        "identifier": tp["sponsor"]["identifier"],
                        "scope": {
                            "non_standard": {
                                "type": "pharma",
                                "name": tp["sponsor"]["label"]
                                .upper()
                                .replace(" ", "-"),
                                "description": "The sponsor organization",
                                "label": tp["sponsor"]["label"],
                                "identifier": "UNKNOWN",
                                "identifierScheme": "UNKNOWN",
                                "legalAddress": tp["sponsor"]["legalAddress"],
                            }
                        },
                    }
                )
            return result
        except Exception as e:
            location = KlassMethodLocation(self.MODULE, "_identification")
            self._errors.exception(
                f"Exception raised building identification data",
                e,
                location,
            )
            return {}
