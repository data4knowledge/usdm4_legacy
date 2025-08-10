# from usdm4.api.wrapper import Wrapper
from simple_error_log.errors import Errors
from usdm4 import USDM4
from usdm4_legacy.import_.to_html import ToHTML
from usdm4_legacy.import_.clean_html import CleanHTML
from usdm4_legacy.import_.split_html import SplitHTML
from usdm4_legacy.import_.title_page import TitlePage

class LegacyImport:
    def __init__(self, file_path: str, errors: Errors):
        self._file_path = file_path
        self._errors = errors
        self._html = None
        self._sections = []
        usdm4 = USDM4()
        self._assembler = usdm4.assembler(errors)

    def process(self) -> None:
        processor = ToHTML(self._file_path, self._errors)
        self._html = processor.process()
        cleaner = CleanHTML(self._html, self._errors)
        self._html = cleaner.process()
        splitter = SplitHTML(self._html, self._errors)
        self._sections = splitter.process()
        print(f"SECTIONS: {self._sections[0:1]}")

    def to_usdm(self) -> str | None:
        title_page = TitlePage(self._sections, self._errors)
        title_page.process()
        # usdm = ToUSDM(
        #     self._builder,
        #     self._errors,
        #     self._title_page,
        #     # self._inclusion_exclusion,
        #     # self._estimands,
        #     # self._amendment,
        #     self._sections,
        # )
        # usdm = usdm.export()
        # return usdm
        return ""

    def extra(self):
        return {
            "title_page": self._title_page.extra(),
            "miscellaneous": self._miscellaneous.extra(),
            "amendment": self._amendment.extra(),
        }
