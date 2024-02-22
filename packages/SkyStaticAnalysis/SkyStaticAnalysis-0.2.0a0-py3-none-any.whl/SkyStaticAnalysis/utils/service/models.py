"""
Shared context for both tool service or tool client.
"""
import os
import json
import time
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Literal,
    Type,
    TypeVar,
    TypedDict,
    cast,
)

from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin
from enum import Enum


class JSONBase:
    names_map = {}

    @classmethod
    def from_dict(cls, d: dict):
        """
        Create
        """
        assert "type" in d
        self = cls(Trigger.INVALID)
        for k, v in d.items():
            setattr(self, k, v)

    def to_dict(self) -> Dict[str, Any]:
        d = {}
        for k, v in self.__dict__.items():
            k = k if k not in self.__class__.names_map else self.__class__.names_map[k]
            if k.startswith("_"):
                continue
            elif hasattr(v, "to_json"):
                d[k] = v.to_json()
            elif isinstance(v, dict):
                new_dict = {}
                for new_k, new_v in v.items():
                    if hasattr(new_v, "to_json"):
                        new_dict[new_k] = new_v.to_json()
                    else:
                        new_dict[new_k] = new_v
                d[k] = new_dict
            elif isinstance(v, (list, tuple)):
                new_list = []
                for new_v in v:
                    if hasattr(new_v, "to_json"):
                        new_list.append(new_v.to_json())
                    else:
                        new_list.append(new_v)
                d[k] = new_list
            else:
                d[k] = v
        return d


@dataclass
class WSToolMsg(DataClassJsonMixin):
    pass


SchedulerMsgTypes = Literal["command"]
ToolMsgTypes = Literal["status", "result", "response"]


class Trigger(str, Enum):
    START = "start"  # 开始分析，需要带有参数
    STOP = "stop"  # 强制杀死进程
    INVALID = "invalid"

    def __str__(self):
        return str(self.value)


class Status(str, Enum):
    READY = "ready"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
    STOPPED = "stopped"  # stopped manually
    INVALID = "invalid"

    def __str__(self):
        return str(self.value)


class BaseCommand(DataClassJsonMixin):
    type: Trigger  # WARNING: This property must be rewritten in subclasses


C = TypeVar("C", bound=BaseCommand)
T = TypeVar("T")


class WSSchedulerRawMsgType(TypedDict):
    type: SchedulerMsgTypes
    data: Dict[str, Any]


class WSToolRawMsgType(TypedDict):
    type: ToolMsgTypes
    data: Dict[str, Any]


class SchedulerCommandDictType(TypedDict):
    uuid: str
    data: Dict


@dataclass
class SchedulerCommand(Generic[C]):
    """
    The context for blocking service in websocket services.
    """

    uuid: str  # The uuid of the blocking context
    data: C

    @classmethod
    def create_dict(cls, uuid: str, data: Dict) -> SchedulerCommandDictType:
        return {"uuid": uuid, "data": data}

    @classmethod
    def from_dict(cls, cmd_cls: Type[C], data: dict):
        return cls(data["uuid"], cmd_cls.from_dict(data["data"]))

    def to_dict(self) -> SchedulerCommandDictType:
        return {"uuid": self.uuid, "data": self.data.to_dict()}


@dataclass
class SchedulerCommandResponse(DataClassJsonMixin):
    uuid: str
    success: bool
    msg: str = ""


@dataclass
class ToolTask:
    tool_name: str
    # Field `data` plays the same role as `BaseCommand.data`, but as a json serializable dict.
    data: Dict[str, Any]


@dataclass
class StatusInfo(DataClassJsonMixin):
    uuid: str
    start_time: float
    end_time: float
    status: Status


class Position(DataClassJsonMixin):
    type: str
    line: int
    column: int
    text: int  # 对错误位置的文字描述

    @classmethod
    def textual(cls, text):
        return cls(type="text", text=text)

    @classmethod
    def line_col(cls, line, column=-1):
        return cls(type="line_col", line=line, column=column)


@dataclass
class Problem(DataClassJsonMixin):
    file: str
    description: str
    position: Position


@dataclass
class Result(DataClassJsonMixin):
    info: StatusInfo
    problems: List[Problem]
    raw_file: str  # 原始文件，以url的形式


class ProcessContext:
    def __init__(self, root_folder: str, ctx_id: str) -> None:
        self.root_folder = root_folder
        self.info = StatusInfo(
            uuid=ctx_id, start_time=time.time(), end_time=-1, status=Status.READY
        )
        self.data_folder = os.path.join(root_folder, ctx_id)
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self.info_json = os.path.join(self.data_folder, ".processinfo.json")
        self.found_problems: List[Problem] = []
        self.dump()

    def dump(self):
        with open(self.info_json, "w") as f:
            json.dump(
                self.info.to_json(),
                f,
                indent=2,
                ensure_ascii=False,
            )
