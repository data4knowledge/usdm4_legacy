from usdm4 import USDM4
from usdm4.assembler.assembler import Assembler
from simple_error_log.errors import Errors

class AssembleUSDM():

    def __init__(self, source_data: dict, errors: Errors):
        self._source_data = source_data
        self._errors = errors
        self._usdm4 = USDM4()
        self._assembler: Assembler = self._usdm4.assembler(self._errors)

    def process(self) -> str:
        usdm_data = {}
        usdm_data['identification'] = self._identification()
        return self._assembler.execute(usdm_data)

    def _identification(self) -> dict:
        tp = self._source_data["title_page"]
        print(f"\n\nTP: {tp}\n\n")
        result = {
            "titles": tp['titles'],
            "identifiers": []
        }
        for org in ["ct.gov", "fda"]:
            if org in tp:
                result['identifiers'].append({"identifier": tp[org]['identifier'],"scope": {"standard": org}}) 
        if "sponsor" in tp:
            result['identifiers'].append(
                {
                    "identifier": tp['sponsor']["identifier"],
                    "scope": {
                        "non_standard": {
                            "type": "pharma",
                            "name": tp['sponsor']["label"].upper().replace(" ", "-"),
                            "description": "The sponsor organization",
                            "label": tp['sponsor']["label"],
                            "identifier": "UNKNOWN",
                            "identifierScheme": "UNKNOWN",
                            "legalAddress": tp['sponsor']["legalAddress"]
                        }
                    }
                }
            )