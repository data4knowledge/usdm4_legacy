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
        return result
