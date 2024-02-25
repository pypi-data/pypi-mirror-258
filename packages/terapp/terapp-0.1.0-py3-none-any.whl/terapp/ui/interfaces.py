from ..app.interfaces import Context


class UI:
    def __init__(self, context: Context, *args, **kwargs):
        self.context = context
        self.width = None
        self.height = None

    def __repr__(self) -> str: ...

    def set_size(self, width: int, height: int):
        self.width = width
        self.height = height
