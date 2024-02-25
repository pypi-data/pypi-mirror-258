from typing import Literal
from .interfaces import UI


class Header(UI):
    def __init__(self, context, title: str, width: int | Literal["auto", "full"] = "auto", style: Literal["box", "strikethrough"] = "box"):
        super().__init__(context=context)
        self.title = title
        self.width = self.__get_width(width)
        self.height = 3
        self.style = style

    def __get_width(self, width):
        if width == "auto":
            return len(self.title) + 4
        elif width == "full" or width > self.context.width:
            return self.context.width
        else:
            return width

    def __box(self):
        title = self.title.center(self.width - 2)
        tline = "┌" + "─" * (self.width - 2) + "┐"
        mline = "│" + title + "│"
        bline = "└" + "─" * (self.width - 2) + "┘"
        return "\n".join([tline, mline, bline])

    def __strikethrough(self):
        title = self.title.center(self.width, "─")
        return "\n" + title + "\n"

    def __repr__(self) -> str:
        if self.style == "box":
            return self.__box()
        elif self.style == "strikethrough":
            return self.__strikethrough()
        else:
            raise ValueError("Invalid style")
