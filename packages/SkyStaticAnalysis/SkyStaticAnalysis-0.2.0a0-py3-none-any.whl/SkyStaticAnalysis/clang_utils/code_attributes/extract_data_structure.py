import json
import os
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from clang.cindex import Cursor, CursorKind, SourceLocation, Type, TypeKind

from ...utils import SkyGenerator, sky_generator
from .extract_function_info import get_var_refs
from .extract_globals import all_globals
from .utils import CompilerArgsType, extract_ast, extract_literal_value, parse_file


def extract_call_exprs(node: Cursor) -> List[Cursor]:
    """
    Get all CALL_EXPR from the node
    """
    callings = []

    for c in node.walk_preorder():
        if c.kind == CursorKind.CALL_EXPR:
            callings.append(c)
    return callings


class ReprUtil:
    @classmethod
    def create_empty_instance(cls):
        return cls.__new__(cls)

    @staticmethod
    def from_serializable_dict(serializable_dict: Dict[str, Any]):
        if not isinstance(serializable_dict, Dict):
            return serializable_dict
        elif "class" not in serializable_dict:
            return serializable_dict
        cls: ReprUtil = globals().get(serializable_dict["class"])

        result = cls.create_empty_instance()
        for key, value in serializable_dict.items():
            if isinstance(value, dict):
                setattr(result, key, cls.from_serializable_dict(value))
            elif isinstance(value, list):
                setattr(
                    result, key, [cls.from_serializable_dict(item) for item in value]
                )
            else:
                setattr(result, key, value)
        return result

    def to_serializable_dict(self):
        d = {"class": self.__class__.__name__}

        def conv_single_obj(val: object):
            if isinstance(val, (int, str, float, bool)):
                return val
            elif hasattr(val, "to_serializable_dict"):
                return val.to_serializable_dict()

        for k, v in self.__dict__.items():
            if isinstance(v, list):
                d[k] = [conv_single_obj(item) for item in v]
            elif isinstance(v, tuple):
                d[k] = tuple([conv_single_obj(item) for item in v])
            elif isinstance(v, dict):
                d[k] = {subk: conv_single_obj(subv) for subk, subv in v.items()}
            else:
                d[k] = conv_single_obj(v)
        return d

    def __repr__(self) -> str:
        return f"======== start class {self.__class__.__name__} =============\n<{json.dumps(self.to_serializable_dict(), indent=2)}>\n========= end class =========="


def program_model_unparse(data: Dict[str, Any]) -> ReprUtil:
    """
    Unparse program model data and return the corresponding type.
    """
    return ReprUtil.from_serializable_dict(data)


class TypeWrapper(ReprUtil):
    """
    The wrapper over data type
    """

    def __init__(self, type_: Type) -> None:
        self._type = type_

        #:
        self.spelling = type_.spelling

        #: A string, not CursorKind
        self.kind = str(type_.kind)

        if type_.kind == TypeKind.POINTER:
            pointee_type: Type = type_.get_pointee()
            self.pointee = str(pointee_type.spelling)


class DefModel(ReprUtil):
    """
    Base class of function/class/struct... definitions
    """

    def __init__(self, spelling: str) -> None:
        self.location: Optional[Tuple[str, int, int]] = (None,)
        self.spelling: str = spelling

    @classmethod
    def from_cursor(cls, c: Cursor):
        raise NotImplementedError

    def update_common_info(self, node: Cursor):
        loc: SourceLocation = node.location
        self.location = (loc.file.name, loc.line, loc.column)


class FunctionDefModel(DefModel):
    """
    Model of function definition
    """

    def __init__(
        self,
        spelling: str,
        type: Type,
    ) -> None:
        super().__init__(spelling)
        self.type = TypeWrapper(type)
        self.params: List[ParamDefModel] = []
        self.callings = []
        self.referenced_globals = []

    @property
    def iter_params(self) -> SkyGenerator["ParamDefModel"]:
        """
        Iterate each parameters
        """
        return SkyGenerator(self.params)

    @property
    def iter_callings(self) -> SkyGenerator["ParamDefModel"]:
        """
        Iterate all callings inside this definition
        """
        return SkyGenerator(self.callings)

    @classmethod
    def from_cursor(cls, node: Cursor) -> "FunctionDefModel":
        fdm = cls(node.spelling, node.type)
        fdm.update_common_info(node)
        child: Cursor
        for child in node.get_children():
            if child.kind == CursorKind.PARM_DECL:
                fdm.params.append(ParamDefModel.from_cursor(child))
            elif child.kind == CursorKind.COMPOUND_STMT:
                for call_node in extract_call_exprs(node):
                    fdm.callings.append(call_node.spelling)
        global_refs = (
            get_var_refs(node, False)
            .filter(lambda var_ref: var_ref.spelling in context.global_vars)
            .attributes("spelling")
            .to_set()
        )
        fdm.referenced_globals = list(global_refs)
        # print('var_refs', var_refs)
        return fdm


class FieldDefModel(DefModel):
    def __init__(self, spelling: str, field_type: Type, init_value_text: str) -> None:
        super().__init__(spelling)
        self.type = TypeWrapper(field_type)
        self.init_value_text = init_value_text

    @classmethod
    def from_cursor(cls, node: Cursor):
        assert node.kind == CursorKind.FIELD_DECL
        children: List[Cursor] = list(node.get_children())
        init_value: str = ""
        if len(children) == 1:
            init_value = extract_literal_value(children[0])
        vdm = cls(
            node.spelling,
            node.type,
            init_value,
        )
        vdm.update_common_info(node)
        return vdm


class UnionDefModel(DefModel):
    """
    Definition model of Union
    """

    def __init__(self, spelling: str) -> None:
        super().__init__(spelling)
        self.children: List[FIELD_TYPE] = []

    @property
    def iter_children(self):
        """
        Iterate child fields inside this union
        """
        return SkyGenerator(self.children)

    @classmethod
    def from_cursor(cls, node: Cursor) -> "UnionDefModel":
        assert node.kind == CursorKind.UNION_DECL
        m = cls(node.spelling)
        m.update_common_info(node)
        child: Cursor
        for child in node.get_children():
            m.children.append(parse_field(child))
        return m


class ParamDefModel(DefModel):
    def __init__(self, spelling: str, field_type: Type) -> None:
        super().__init__(spelling)
        self.type = TypeWrapper(field_type)

    @classmethod
    def from_cursor(cls, node: Cursor) -> "ParamDefModel":
        assert node.kind == CursorKind.PARM_DECL
        m = cls(node.spelling, node.type)
        m.update_common_info(node)
        return m


class TypeDefModel(DefModel):
    def __init__(self, spelling: str) -> None:
        super().__init__(spelling)
        self.from_type = None

    @classmethod
    def from_cursor(cls, node: Cursor) -> "TypeDefModel":
        m = cls(node.spelling)
        m.update_common_info(node)
        child: Cursor = list(node.get_children())[0]
        m.from_type = TypeWrapper(child.type)
        return m


class StructDefModel(DefModel):
    """
    The model indicating a structure definition
    """

    def __init__(self, spelling: str) -> None:
        super().__init__(spelling)

        self.fields: List[FIELD_TYPE] = []

    @property
    def iter_fields(
        self,
    ) -> SkyGenerator["Union[FieldDefModel, UnionDefModel, StructDefModel]"]:
        """
        Iterate fields of this struct
        """
        return SkyGenerator(self.fields)

    @classmethod
    def from_cursor(cls, node: Cursor) -> "StructDefModel":
        assert node.kind == CursorKind.STRUCT_DECL, "Expected a STRUCT_DECL cursor"

        m = cls(node.spelling)
        m.update_common_info(node)
        for child in node.get_children():
            m.fields.append(parse_field(child))

        return m


FIELD_TYPE = Union[FieldDefModel, UnionDefModel]


def parse_field(field: Cursor) -> FIELD_TYPE:
    # Dispatchers for fields/unions/sub-structs
    fields_dispatchers: Dict[CursorKind, DefModel] = {
        CursorKind.FIELD_DECL: FieldDefModel,
        CursorKind.UNION_DECL: UnionDefModel,
        CursorKind.STRUCT_DECL: StructDefModel,
    }
    return fields_dispatchers[field.kind].from_cursor(field)


class ClassDefModel(DefModel):
    """
    The model defining class information
    """

    def __init__(self, spelling: str) -> None:
        super().__init__(spelling)
        self.fields: List[FieldDefModel] = []
        self.methods: List[FunctionDefModel] = []

    @property
    def iter_fields(self) -> SkyGenerator[FieldDefModel]:
        """
        Iterate each field in class
        """
        return SkyGenerator(self.fields)

    @property
    def iter_methods(self) -> SkyGenerator[FunctionDefModel]:
        """
        Iterate each method in class
        """
        return SkyGenerator(self.methods)

    @classmethod
    def from_cursor(cls, node: Cursor) -> "ClassDefModel":
        assert node.kind == CursorKind.CLASS_DECL, extract_ast(node)
        m = cls(node.spelling)
        m.update_common_info(node)
        child: Cursor
        for child in node.get_children():
            if child.kind == CursorKind.FIELD_DECL:
                m.fields.append(FieldDefModel.from_cursor(child))

            elif child.kind == CursorKind.CXX_METHOD:
                method_def_model = FunctionDefModel.from_cursor(child)
                m.methods.append(method_def_model)
            else:
                print("cannot parse", [t.spelling for t in child.get_tokens()])
        return m


class _Context:
    def __init__(self) -> None:
        self.global_vars: Set[str] = set()


context = _Context()


@sky_generator
def data_structure_from_file(
    filename: str, args: CompilerArgsType = None
) -> Generator[DefModel, None, None]:
    c = parse_file(filename, args).cursor
    models = {
        CursorKind.FUNCTION_DECL: FunctionDefModel,
        CursorKind.FIELD_DECL: FieldDefModel,
        CursorKind.UNION_DECL: UnionDefModel,
        CursorKind.STRUCT_DECL: StructDefModel,
        CursorKind.TYPEDEF_DECL: TypeDefModel,
        CursorKind.CLASS_DECL: ClassDefModel,
    }
    context.global_vars = all_globals(c).attributes("spelling").to_set()

    for child in c.get_children():
        if os.path.samefile(child.location.file.name, filename):
            print(child.kind, child.spelling, child.location.file.name)
            if child.kind in models:
                try:
                    method = models[child.kind].from_cursor
                    yield method(child)
                except:
                    import traceback

                    traceback.print_exc()
            else:
                continue


@sky_generator
def iter_data_structures(
    folder: str, name_filter: Callable[[str], bool], args: CompilerArgsType = None
) -> Generator[DefModel, None, None]:
    assert os.path.exists(folder)
    for root, _, files in os.walk(folder):
        for file in files:
            abspath = os.path.join(root, file)
            print(abspath)
            if name_filter(abspath):
                yield from data_structure_from_file(abspath, args)
