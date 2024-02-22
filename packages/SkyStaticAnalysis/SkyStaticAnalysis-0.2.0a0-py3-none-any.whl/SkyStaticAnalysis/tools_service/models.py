"""
Shared context for both tool service or tool client.
"""

import json
import os
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generic, List, Literal, Type, TypedDict, TypeVar

from dataclasses_json import DataClassJsonMixin


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
    OFFLINE = "offline"
    INVALID = "invalid"

    def __str__(self):
        return str(self.value)


class BaseCommand(DataClassJsonMixin):
    type: Trigger  # WARNING: This property must be rewritten in subclasses


C = TypeVar("C", bound=DataClassJsonMixin)
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


# @dataclass
# class ToolTask:
#     tool_name: str
#     # Field `data` plays the same role as `BaseCommand.data`, but as a json serializable dict.
#     data: Dict[str, Any]


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
