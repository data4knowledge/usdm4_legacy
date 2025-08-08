from docling.document_converter import DocumentConverter


class ToHTML:
    def __init__(self, full_path: str):
        self._converter = DocumentConverter()
        self._full_path = full_path
        self.html = None
        self.error = None

    def execute(self):
        try:
            result = self._converter.convert(self._full_path)
            self.html = result.document.export_to_html()
            print("HTML", self.html[0:1000])
            return self.html
        except Exception as e:
            self.error = f"Exception '{e}' raised converting document to HTML"
            print("Error", self.error)
            return None