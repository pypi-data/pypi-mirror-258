from dataclasses import dataclass, field
from typing import Optional, Sequence

DEFAULT_NEWLINE = '\n'
DEFAULT_TABULATION = '  '
DEFAULT_LEVEL = 0
DEFAULT_QUOTES = '"'
DEFAULT_UNDERSCORE_REPLACER = '-'
DEFAULT_SEPARATOR = ' '
DEFAULT_SPECIAL_ATTRS = [
    'data',
    'aria',
    'x',
    'v',
    'hx',
]

DEFAULT_ELEM_CONTEXT = (
    DEFAULT_NEWLINE,
    DEFAULT_TABULATION,
    DEFAULT_LEVEL,
)

DEFAULT_ATTR_CONTEXT = (
    DEFAULT_QUOTES,
    DEFAULT_UNDERSCORE_REPLACER,
    DEFAULT_SEPARATOR,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RenderContext:
    ##### ELEMS #####
    newline: str
    tabulation: str
    level: int

    ##### ATTRS #####
    quotes: str
    underscore_replacer: str
    separator: str
    special_attrs: tuple[str, ...]

    def with_next_level(self) -> 'RenderContext':
        copied_self = ctx(
            newline=self.newline,
            tabulation=self.tabulation,
            level=self.level + 1,
            quotes=self.quotes,
            underscore_replacer=self.underscore_replacer,
            separator=self.separator,
            special_attrs=self.special_attrs,
        )
        return copied_self


def ctx(
    *,
    ##### ELEMS #####
    newline: Optional[str] = None,
    tabulation: Optional[str] = None,
    level: Optional[int] = None,

    ##### ATTRS #####
    quotes: Optional[str] = None,
    underscore_replacer: Optional[str] = None,
    separator: Optional[str] = None,
    special_attrs: Optional[tuple[str, ...]] = None,
) -> RenderContext:
    result = RenderContext(
        newline=newline if newline is not None else DEFAULT_NEWLINE,
        tabulation=tabulation if tabulation is not None else DEFAULT_TABULATION,
        level=level if level is not None else DEFAULT_LEVEL,
        quotes=quotes if quotes is not None else DEFAULT_QUOTES,
        underscore_replacer=underscore_replacer if underscore_replacer is not None else DEFAULT_UNDERSCORE_REPLACER,
        separator=separator if separator is not None else DEFAULT_SEPARATOR,
        special_attrs=special_attrs if special_attrs is not None else tuple(DEFAULT_SPECIAL_ATTRS),
    )
    return result

DEFAULT_RENDER_CONTEXT = ctx()
