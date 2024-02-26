from typing import Any

from .abstract_parser import AbstractParser


class UevtParser(AbstractParser):

    def __init__(self, path: Any) -> None:
        AbstractParser.__init__(self, path)
