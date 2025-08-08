# from usdm4.api.wrapper import Wrapper
from simple_error_log.errors import Errors
from usdm4 import USDM4
from usdm4_legacy.import_.to_html import ToHTML

class LegacyImport:
    def __init__(self, file_path: str, errors: Errors):
        self._file_path = file_path
        self._errors = errors
        self._doc = None
        usdm4 = USDM4()
        self._builder = usdm4.builder(errors)
        self._encoder = usdm4.encoder(errors)

    async def process(self) -> None:
        processor = ToHTML(self._file_path)
        self._doc = processor.execute()

    def to_usdm(self) -> str | None:
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
