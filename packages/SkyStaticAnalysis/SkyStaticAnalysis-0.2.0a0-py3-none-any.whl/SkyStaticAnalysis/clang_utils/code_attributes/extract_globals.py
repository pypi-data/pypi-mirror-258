from typing import Generator

from clang.cindex import Cursor, CursorKind

from ...utils import sky_generator


@sky_generator
def all_globals(c: Cursor) -> Generator[Cursor, None, None]:
    """
    Extract all globals from a translation unit.
    """
    assert c.kind == CursorKind.TRANSLATION_UNIT
    child: Cursor
    for child in c.get_children():
        if child.kind == CursorKind.VAR_DECL:
            yield child
