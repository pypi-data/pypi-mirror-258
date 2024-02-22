from dataclasses import dataclass
from typing import Generic, Optional, Type, TypeVar

from dataclasses_json import DataClassJsonMixin

from .models import (
    C,
    Result,
    SchedulerCommand,
    SchedulerCommandResponse,
    StatusInfo,
    WSSchedulerRawMsgType,
    WSToolRawMsgType,
)


class WSSchedulerMsgParser(Generic[C]):
    def __init__(self, command_cls: Type[C]) -> None:
        self.command_cls = command_cls

    def parse_scheduler_msg(self, raw_msg: WSSchedulerRawMsgType):
        if raw_msg["type"] == "command":
            return SchedulerCommand.from_dict(self.command_cls, raw_msg["data"])
        else:
            raise NotImplementedError(raw_msg)


class WSToolMsgParser:
    def parse_tool_msg(self, raw_msg: WSToolRawMsgType):
        if raw_msg["type"] == "status":
            return StatusInfo.from_dict(raw_msg["data"])
        elif raw_msg["type"] == "result":
            return Result.from_dict(raw_msg["data"])
        elif raw_msg["type"] == "response":
            return SchedulerCommandResponse.from_dict(raw_msg["data"])
        else:
            raise NotImplementedError(raw_msg)


RestRespDataType = TypeVar("RestRespDataType", bound=DataClassJsonMixin)


@dataclass
class RestResponse(DataClassJsonMixin, Generic[RestRespDataType]):
    msg: str
    data: Optional[RestRespDataType] = None

    @classmethod
    def dict_from_msg(cls, msg: str, data_raw: dict):
        return {"msg": msg, "data": data_raw}


@dataclass
class FileUploadResponse(DataClassJsonMixin):
    filename_in_storage: str
