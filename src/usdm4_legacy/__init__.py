from usdm4_legacy.import_.legacy_import import LegacyImport
from usdm4.api.wrapper import Wrapper
from simple_error_log.errors import Errors
from simple_error_log.error_location import KlassMethodLocation


class USDM4Legacy:
    MODULE = "usdm4_legacy.__init__.USDM4Legacy"

    def __init__(self):
        self._errors = Errors()
        self._import = None

    def from_pdf(self, filepath: str) -> str | None:
        try:
            self._import = LegacyImport(filepath, self._errors)
            return self._import.process()
        except Exception as e:
            location = KlassMethodLocation(self.MODULE, "from_pdf")
            self._errors.exception(
                f"Exception raised converting legacy '.pdf' file '{filepath}'",
                e,
                location,
            )
            return None

    # def extra(self) -> dict | None:
    #     try:
    #         if self._m11_import:
    #             return self._m11_import.extra()
    #         else:
    #             raise RuntimeError
    #     except Exception as e:
    #         location = KlassMethodLocation(self.MODULE, "extra")
    #         self._errors.exception(
    #             "Exception raised obtaining extra information", e, location
    #         )
    #         return None

    @property
    def errors(self):
        return self._errors
