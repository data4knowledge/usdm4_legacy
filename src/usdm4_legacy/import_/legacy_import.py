from simple_error_log.errors import Errors
from simple_error_log.error_location import KlassMethodLocation
from usdm4 import USDM4
from usdm4_legacy.import_.load import LoadPDF
from usdm4_legacy.import_.extract import ExtractStudy
from usdm4_legacy.import_.assemble import AssembleUSDM
from usdm4.api.wrapper import Wrapper
from usdm4_legacy.__info__ import __model_version__ as usdm_version, __package_version__ as system_version


class LegacyImport:
    MODULE = "usdm4.legacy.import_.legacy_import.LegacyImport"

    def __init__(self, file_path: str, errors: Errors):
        self._file_path = file_path
        self._errors = errors
        self._html = None
        self._sections = []
        usdm4 = USDM4()
        self._assembler = usdm4.assembler(errors)

    def process(self) -> Wrapper:
        try:
            loader = LoadPDF(self._file_path, self._errors)
            self._sections = loader.process()
            print(f"Loaded PDF")
            extractor = ExtractStudy(self._sections, self._errors)
            self._study = extractor.process()
            print(f"Extracted content: {self._study}")
            assembler = AssembleUSDM(self._study, self._errors)
            wrapper = self._assembler.wrapper("USDM4 Legacy Protocol Package", system_version)
            print(f"Study built")
            return wrapper
        except Exception as e:
            location = KlassMethodLocation(self.MODULE, "process")
            self._errors.exception(
                f"Exception raised processing legacy '.pdf' file '{self._file_path}'",
                e,
                location,
            )
            return None

    # def extra(self):
    #     return {
    #         "title_page": self._title_page.extra(),
    #         "miscellaneous": self._miscellaneous.extra(),
    #         "amendment": self._amendment.extra(),
    #     }
