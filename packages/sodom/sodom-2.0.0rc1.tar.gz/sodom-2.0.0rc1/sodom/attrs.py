__license__ = '''
sodom
Copyright (C) 2023  Dmitry Protasov (inbox@protaz.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from keyword import iskeyword
from operator import truth
from typing import Callable, Iterable, Self
from sodom.context import (
    DEFAULT_RENDER_CONTEXT,
    DEFAULT_SEPARATOR,
    RenderContext,
)


_attr_format = '{k}={q}{v}{q}'.format

freeze: Callable[[dict[str, str]], tuple[tuple[str, str], ...]] = \
    lambda self: tuple(self.items())


class Attrs(dict[str, str]):
    def __call__(self: Self) -> None:
        from sodom.elements import CURRENT_ELEMENT

        try:
            parent = CURRENT_ELEMENT.get()
        except LookupError as e:
            raise RuntimeError('Attribute should be called in context of Normal Element.') from e
        else:
            parent.attrs.merge_update(self)

    def merge(
        self: Self,
        other: dict[str, str],
        separator: str = DEFAULT_SEPARATOR,
    ) -> 'Attrs':
        '''Merge attributes into new Attrs instance.'''
        copied_self = Attrs(self)
        copied_self.merge_update(other, separator)
        return copied_self

    def merge_update(
        self: Self,
        other: dict[str, str],
        separator: str = DEFAULT_SEPARATOR,
    ) -> Self:
        '''Merge attributes inplace.'''
        for k, v in other.items():
            self[k] = separator.join(filter(
                truth,
                (
                    self.get(k, ''),
                    v,
                ),
            ))
        return self

    __or__ = merge
    __ior__ = merge_update # type: ignore

def render_attrs(
    frozenattrs: Iterable[tuple[str, str]],
    *,
    ctx: RenderContext = DEFAULT_RENDER_CONTEXT,
) -> str:
    attrs = list[str]()
    attrs_append = attrs.append

    for attr_name, attr_value in frozenattrs:
        if iskeyword(stripped_attr_name := attr_name.strip('_')):
            attr_name = stripped_attr_name

        if ctx.underscore_replacer != '_':
            attr_name = attr_name.replace('_', ctx.underscore_replacer)
        elif attr_name.split('_', 1)[0] in ctx.special_attrs:
            attr_name = attr_name.replace('_', '-', 1)

        if attr_value:  # attribute value must be significant otherwise empty will be rendered.
            attr_content = _attr_format(k=attr_name, q=ctx.quotes, v=attr_value)
        else:
            attr_content = attr_name

        attrs_append(attr_content)

    rendered_attrs = ctx.separator.join(attrs)
    return rendered_attrs
