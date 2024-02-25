from ..app.interfaces import Context
from .interfaces import UI


class Center(UI):
    def __init__(self, context: Context, child: UI, *args, **kwargs):
        super().__init__(context=context, *args, **kwargs)
        self.child = child

    def __repr__(self) -> str: ...


class Row(UI):
    def __init__(self, context: Context, children: list[UI], *args, **kwargs):
        super().__init__(context=context, *args, **kwargs)
        self.children = children

    def __repr__(self) -> str: ...


class Column(UI):
    def __init__(self, context: Context, children: list[UI], *args, **kwargs):
        super().__init__(context=context, *args, **kwargs)
        self.children = children

    def __repr__(self) -> str: ...
