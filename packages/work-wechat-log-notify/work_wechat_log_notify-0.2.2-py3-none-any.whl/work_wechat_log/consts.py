from enum import Enum
from typing import Any, Iterable, Mapping, Sequence, TypeAlias
from tabulate import TableFormat

class MessageType(Enum):
    TEXT = "text"
    TABLE = "table"
    MARKDOWN = "markdown"
    IMAGE = "image"
    NEWS = "news"
    FILE = "file"
    TEMPLATE_CARD = "template_card"

TableType: TypeAlias = Mapping[str, Iterable[Any]] | Iterable[Iterable[Any]]
TableHeadersType: TypeAlias = str | dict[str, str] | Sequence[str]
TableFmtType: TypeAlias = str | TableFormat
