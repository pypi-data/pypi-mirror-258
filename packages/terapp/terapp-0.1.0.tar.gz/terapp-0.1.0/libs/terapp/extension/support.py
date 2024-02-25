from ..app import Ter


class ImportSupport:
    def __init__(self):
        self.current_app: Ter = None

    def set_app(self, app: Ter):
        if not isinstance(app, Ter):
            raise TypeError("App must be an instance of Ter")
        self.current_app = app


# Instance of ImportSupport
import_support = ImportSupport()
