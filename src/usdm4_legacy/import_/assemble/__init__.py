from usdm4 import USDM4
from usdm4.assembler.assembler import IdentificationAssembler
from simple_error_log.errors import Errors

class AssembleUSDM():

    def __init__(self, source_data: dict, errors: Errors):
        self._source_data = source_data
        self._errors = errors
        self._usdm4 = USDM4()
        self._assembler = self._usdm4.assembler(self._errors)

    def process(self) -> str:
        usdm_data = {}
        usdm_data['identification'] = self._identification()
        return self._assembler.execute(usdm_data)

    def _identification(self):
        return {
            "titles": self._source_data['titles'],
            "identifiers": [
                {
                    "identifier": self._source_data['ct.gov']['identifier'],
                    "scope": {"standard": "ct.gov"}
                } if "ct.gov" in self._source_data else {},
                {
                    "identifier": self._source_data['fda']['identifier'],
                    "scope": {"standard": "ct.gov"}
                } if "fda" in self._source_data else {},
                {
                    "identifier": self._source_data['sponsor']["sponsor_identifier"],
                    "scope": {
                        "non_standard": {
                            "type": "pharma",
                            "name": self._source_data['sponsor']["label"].upper().replace(" ", "-"),
                            "description": "The sponsor organization",
                            "label": self._source_data['sponsor']["label"],
                            "identifier": "UNKNOWN",
                            "identifierScheme": "UNKNOWN",
                            "legalAddress": self._source_data['sponsor']["legalAddress"]
                        }
                    }
                }
            ]
        }