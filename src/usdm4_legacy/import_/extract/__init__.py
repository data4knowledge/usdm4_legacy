from usdm4_legacy.import_.extract.title_page import TitlePage
from simple_error_log.errors import Errors

class ExtractStudy():

    def __init__(self, sections: list[str], errors: Errors):
        self._sections = sections
        self._errors = errors

    def process(self) -> dict:
        result = {}
        title_page = TitlePage(self._sections, self._errors)
        result["title_page"] = title_page.process()
        result["document"] = {           
            "label": "Protocol Document",
            "version": "", # @todo
            "status": "Final", # @todo
            "template": "Legacy",
            "version_date": "", # @todo
        },
        result["section"] = self._sections
        result["study_design"] = {
            "label": "Study Design 1",
            "rationale": "", # @todo
            "trial_phase": result["title_page"]["other"]["phase"]
        }
        result["population"] = {
            "label": "Default population"
        }
        result["study"] = {
            "sponsor_approval_date": "" # @todo
        }
        return result
