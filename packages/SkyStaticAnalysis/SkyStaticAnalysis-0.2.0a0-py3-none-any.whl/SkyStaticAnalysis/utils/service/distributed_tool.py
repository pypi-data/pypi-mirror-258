"""
Make a tool work as a distributed service

Pushing messages proactively

Distributed tool must know the endpoint of the scheduler.
"""
import os
import json
import threading
import time
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)


import uuid

from SkyStaticAnalysis.utils.files import file_to_dataurl

from .states import StateMachine
from .processmgr import SubprocessManager
from ..functional import sky_generator, SkyGenerator, SkyFrozenGenerator
from flask import Flask, abort, make_response, redirect, request, send_from_directory
from flask_sock import Sock, ConnectionClosed as WSConnectionClosed
from .models import (
    C,
    ProcessContext,
    Result,
    SchedulerCommandResponse,
    StatusInfo,
    Status,
    ToolMsgTypes,
    Trigger,
    WSToolMsg,
    WSToolRawMsgType,
    WSSchedulerRawMsgType,
    SchedulerCommand,
)
from .messages import WSSchedulerMsgParser
import requests
import websocket
from dataclasses_json import DataClassJsonMixin
from .log import logger


class DistributedTool(Generic[C]):
    def __init__(
        self,
        cmd_type: Type[C],
        scheduler_addr: str,
        scheduler_port: int,
        name="default",
        root_folder=".skystaticanalysis",
    ) -> None:
        self.root_folder = root_folder
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)
        self._cmd_type: Type[C] = cmd_type
        self.scheduler_endpoint = f"{scheduler_addr}:{scheduler_port}"
        self.name = name
        self._uuid = uuid.uuid4().hex
        self._ws = websocket.WebSocket()

        self._thread_websocket: threading.Thread

        self._thread_status_push = threading.Thread(target=self._task_status_push)
        self._thread_status_push.daemon = True

        self.process_mgr = SubprocessManager(self.on_task_finish)

        self.current_context: Optional[
            ProcessContext
        ] = None  # ProcessContext(self.root_folder)

        self._connect()

    def _connect(self):
        self._ws.connect(
            f"ws://{self.scheduler_endpoint}/api/websocket/{self.name}/{self._uuid}"
        )
        self._thread_websocket = threading.Thread(target=self._task_websocket)
        self._thread_websocket.daemon = True
        self._thread_websocket.start()

    def _task_websocket(self):
        """
        Execute the background task for websocket.
        """
        parser = WSSchedulerMsgParser(self._cmd_type)
        while 1:
            try:
                msg: Union[str, bytes] = self._ws.recv()
            except ConnectionResetError as e:
                # When receiving this error, jump out of this `while` loop
                # then start a new listening thread.
                raise e
            try:
                data: WSSchedulerRawMsgType = json.loads(msg)
                print(data)
                parsed = parser.parse_scheduler_msg(data)
                print("received command", parsed)
                if isinstance(parsed, SchedulerCommand):
                    parsed: SchedulerCommand[C]
                    resp = self.process_command(parsed.uuid, parsed.data)
                    self._send_msg("response", resp)
                else:
                    raise NotImplementedError(parsed)
            except json.JSONDecodeError:
                print("Cannot parse:", msg)
                continue

    def _send_msg(self, type: ToolMsgTypes, data: DataClassJsonMixin):
        raw_msg: WSToolRawMsgType = {"type": type, "data": data.to_dict()}
        try:
            self._ws.send(json.dumps(raw_msg))
        except ConnectionResetError:
            # TODO: Optimize the code for re-connect!
            print("trying to reconnect...")
            try:
                self._connect()
            except ConnectionRefusedError:
                print("connection refused, retrying again...")

    def _task_status_push(self):
        """
        Push status to the server
        """
        while 1:
            status = self.handle_status()
            self._send_msg("status", status)
            time.sleep(1)

    def on_task_finish(self, task_id: str):
        assert self.current_context is not None
        self.current_context.info.status = Status.STOPPED
        self.handle_task_finish()
        self._send_msg("result", self.get_result())

    def handle_task_finish(self):
        return

    def handle_rules(self):
        return self.rules()

    def rules(self):
        return [
            {"type": "input", "field": "goods_name", "title": "商品名称"},
            {"type": "datePicker", "field": "created_at", "title": "创建时间"},
        ]

    def handle_status(self) -> StatusInfo:
        if self.current_context is not None:
            return self.current_context.info
        else:
            return StatusInfo(
                uuid="", start_time=-1, end_time=-1, status=Status.STOPPED
            )

    @sky_generator
    def all_results(self) -> Generator[Tuple[str, StatusInfo], None, None]:
        for folder in os.listdir(self.root_folder):
            folder_abs_path = os.path.join(self.root_folder, folder)
            try:
                with open(
                    os.path.join(folder_abs_path, ".processinfo.json"), encoding="utf8"
                ) as f:
                    yield folder_abs_path, StatusInfo(**json.load(f))
            except Exception:
                import traceback

                traceback.print_exc()

    def results(self) -> SkyFrozenGenerator[Tuple[str, StatusInfo]]:
        """
        Get all results, and sort by start time
        """
        return self.all_results().f.sort(lambda item: item[1].start_time, reverse=True)

    def get_result(self) -> Result:
        """
        Get the result produced during the latest running.
        """
        assert self.current_context is not None
        result_file = self.result_file()
        if not os.path.isabs(result_file):
            result_file = os.path.join(self.current_context.data_folder, result_file)
        return Result(
            info=self.current_context.info,
            problems=self.current_context.found_problems,
            raw_file=file_to_dataurl(result_file),
        )

    def result_file(self) -> str:
        raise NotImplementedError

    def handle_results(self):
        return self.results().map(lambda x: x.to_json()).l

    def task_start(self, cmd: C):
        self.current_context = ProcessContext(self.root_folder, uuid.uuid4().hex)
        self.handle_start_tool(cmd)
        self.current_context.info.status = Status.RUNNING

    def process_command(self, cmd_uuid: str, cmd: C) -> SchedulerCommandResponse:
        """
        问题：如何解决Websocket的响应问题？
        """
        if cmd.type == Trigger.START:
            if (
                self.current_context is not None
                and self.current_context.info.status == Status.RUNNING
            ):
                return SchedulerCommandResponse(
                    cmd_uuid, False, "tool is already running"
                )
            self.current_context = ProcessContext(self.root_folder, uuid.uuid4().hex)
            logger.info(
                f"current tool {self._uuid} status: { self.current_context.info.status}"
            )
            self.handle_start_tool(cmd)
            self.current_context.info.status = Status.RUNNING
            return SchedulerCommandResponse(cmd_uuid, True)

        elif cmd.type == Trigger.STOP:
            if self.current_context is None:
                return SchedulerCommandResponse(
                    cmd_uuid, False, "no process is running"
                )
            self.handle_stop_tool(cmd)
            self.current_context.info.status = Status.STOPPED
            self.current_context.info.end_time = time.time()
            self.current_context.dump()
            return SchedulerCommandResponse(cmd_uuid, True)
        else:
            raise NotImplementedError

    def handle_start_tool(self, cmd: C):
        raise NotImplementedError

    def handle_stop_tool(self, cmd: C):
        raise NotImplementedError

    def _start_tasks(self):
        self._thread_status_push.start()

    def start(self):
        self._start_tasks()
        while True:
            time.sleep(1)

    def start_in_thread(self):
        self._start_tasks()
