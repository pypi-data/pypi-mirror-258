from typing import Generator

from clang.cindex import Cursor, CursorKind, Type, TypeKind

from ...utils import sky_generator


@sky_generator
def get_local_var_defs(c: Cursor) -> Generator[Cursor, None, None]:
    """
    Get all local variable definitions from a function
    except variables from parameters
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    child: Cursor
    for child in c.walk_preorder():
        if child.kind == CursorKind.VAR_DECL:
            yield child


@sky_generator
def get_var_refs(c: Cursor, include_funcs=False) -> Generator[Cursor, None, None]:
    """
    Get all variables referenced from one function body
    """
    assert c.kind in (CursorKind.FUNCTION_DECL, CursorKind.CXX_METHOD), c.kind
    child: Cursor
    for child in c.walk_preorder():
        if child.kind == CursorKind.DECL_REF_EXPR:
            type: Type = child.type
            if type.kind == TypeKind.FUNCTIONPROTO and not include_funcs:
                continue
            else:
                yield child


@sky_generator
def get_param_decls(c: Cursor) -> Generator[Cursor, None, None]:
    """
    Extract parameter declarations from function definition
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    child: Cursor
    for child in c.walk_preorder():
        if child.kind == CursorKind.PARM_DECL:
            yield child


@sky_generator
def get_global_refs(c: Cursor) -> Generator[Cursor, None, None]:
    """
    Get all global variables referenced in one function
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    all_var_refs = get_var_refs(c).attributes("spelling").to_set()
    local_var_defs = get_local_var_defs(c).attributes("spelling").to_set()
    param_var_defs = get_param_decls(c).attributes("spelling").to_set()
    vars = all_var_refs - local_var_defs - param_var_defs
    var_ref: Cursor
    for var_ref in get_var_refs(c):
        if var_ref.spelling in vars:
            yield var_ref


@sky_generator
def get_global_ref_names(c: Cursor) -> Generator[str, None, None]:
    """
    Get all global variables referenced in one function
    """
    assert c.kind == CursorKind.FUNCTION_DECL, c
    all_var_refs = get_var_refs(c).attributes("spelling").to_set()
    local_var_defs = get_local_var_defs(c).attributes("spelling").to_set()
    param_var_defs = get_param_decls(c).attributes("spelling").to_set()
    vars = all_var_refs - local_var_defs - param_var_defs
    for v in vars:
        yield v
