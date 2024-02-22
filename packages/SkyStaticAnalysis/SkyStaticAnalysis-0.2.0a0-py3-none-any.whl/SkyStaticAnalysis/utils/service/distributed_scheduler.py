"""
Make a tool work as a distributed service

Pushing messages proactively

Distributed tool must know the endpoint of the scheduler.

Each registered tool has a ToolProxy class to store websocket connection 
"""
import logging
import os
import json
import queue
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
    TypedDict,
    Union,
    cast,
)
from SkyStaticAnalysis.third_parties.jsonobject import (
    JsonObject,
    StringProperty,
    DictProperty,
    IntegerProperty,
    FloatProperty,
    ListProperty,
)
import uuid
from SkyStaticAnalysis.third_parties.jsonobject.properties import ObjectProperty
from contextlib import contextmanager
from SkyStaticAnalysis.utils.files import file_to_dataurl

from .states import StateMachine
from .processmgr import SubprocessManager
from ..functional import sky_generator, SkyGenerator, SkyFrozenGenerator
from flask import Flask, abort, make_response, redirect, request, send_from_directory
from flask_sock import Sock, Server as WSServer, ConnectionClosed as WSConnectionClosed
from .models import (
    C,
    BaseCommand,
    ProcessContext,
    Result,
    SchedulerCommand,
    SchedulerCommandDictType,
    SchedulerCommandResponse,
    StatusInfo,
    Status,
    ToolTask,
    Trigger,
    WSSchedulerRawMsgType,
    WSToolRawMsgType,
)
import requests
from .messages import WSToolMsgParser
from .log import logger

class ToolRemoteRef:
    """
    A class containing reference to remote tools
    """

    _scheduler_command_session_queues: Dict[
        str, queue.Queue[SchedulerCommandResponse]
    ] = {}

    def __init__(self, uuid: str, name: str, ws: WSServer) -> None:
        self.name = name
        self.ws = ws
        self.uuid = uuid
        self.status: Optional[StatusInfo] = None

    def send_command(self, cmd_type: Trigger, cmd_data: Dict) -> Tuple[str, bool]:
        """
        Send command to the tool by websocket
        """
        request_uuid: str = uuid.uuid4().hex
        scheduler_cmd = SchedulerCommand.create_dict(
            request_uuid, {"type": cmd_type, "data": cmd_data}
        )
        with self.wait_command_response(scheduler_cmd, request_uuid) as msg:
            if msg is None:
                return "queue wait timeout!", False
            return msg.msg, msg.success

    @contextmanager
    def wait_command_response(
        self, scheduler_cmd: SchedulerCommandDictType, req_uuid: str
    ) -> Generator[Optional[SchedulerCommandResponse], None, None]:
        """
        A context manager to manage the temporary queue.
        """
        scheduler_msg = WSSchedulerRawMsgType(type="command", data=scheduler_cmd)
        self.ws.send(json.dumps(scheduler_msg))
        self._scheduler_command_session_queues[req_uuid] = queue.Queue(1)
        try:
            yield self._scheduler_command_session_queues[req_uuid].get(timeout=5)
        except queue.Empty:
            yield None
        finally:
            self._scheduler_command_session_queues.pop(req_uuid)

    @classmethod
    def put_response(cls, resp: SchedulerCommandResponse):
        """
        The `start_task` and `stop_task` procedure will be blocked until
        the response is put into the corresponding queue.
        """
        cls._scheduler_command_session_queues[resp.uuid].put(resp)

    def update_status_info(self, status_info: StatusInfo):
        self.status = status_info

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"


class RemoteTools:
    def __init__(self) -> None:
        self.tools: Dict[str, ToolRemoteRef] = {}

    def add(self, tool: ToolRemoteRef):
        self.tools[tool.uuid] = tool

    def remove(self, tool: ToolRemoteRef):
        self.tools.pop(tool.uuid)

    def get_tools_by_name(self, name: str) -> List[ToolRemoteRef]:
        """
        Get tools by name
        """
        return list(filter(lambda tool: tool.name == name, self.tools.values()))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.tools}>"


class Scheduler(Generic[C]):
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8681,
        root_folder=".skystaticanalysis",
        scheduler_address: str = "",
    ) -> None:
        self.root_folder = root_folder
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)
        abs_path = lambda f: os.path.abspath(os.path.join(os.path.dirname(__file__), f))

        self.app = Flask(__name__, static_folder=abs_path("./static"))
        self.port = port
        self.host = host

        self.app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}
        sock = Sock(self.app)

        self._ws_recv_msg_queue: queue.Queue[
            Tuple[ToolRemoteRef, WSToolRawMsgType]
        ] = queue.Queue()
        sock.route("/api/websocket/<path:tool_name>/<path:uuid>")(self.handle_websocket)
        self._message_handling_thread = threading.Thread(
            target=self._task_handle_message
        )
        self._message_handling_thread.daemon = True

        self._tasks_scheduling_thread = threading.Thread(
            target=self._task_schedule_tool_tasks
        )
        self._tasks_scheduling_thread.daemon = True

        # Task queue stores the json-serializable dictionaries as data for each task

        self._tasks: List[ToolTask] = []
        self._tools = RemoteTools()
        self._results: queue.Queue[Result] = queue.Queue()

        self.app.add_url_rule(
            "/register", view_func=self.handle_register, methods=["POST"]
        )

    def handle_websocket(self, ws: WSServer, tool_name: str, uuid: str):
        tool_ref = ToolRemoteRef(uuid, tool_name, ws)
        self._tools.add(tool_ref)
        while True:
            try:
                msg: Union[str, bytes] = ws.receive()
                try:
                    data: WSToolRawMsgType = json.loads(msg)
                    self._ws_recv_msg_queue.put((tool_ref, data))
                except json.JSONDecodeError:
                    logger.error(f"Cannot decode message: {msg}")
            except WSConnectionClosed as e:
                self._tools.remove(tool_ref)
                raise e

    def handle_register(self):
        """
        Handle tool registration
        """
        return ""

    def _task_schedule_tool_tasks(self):
        """
        Continuously get tool task from the queue, then dispatch it to corresponding tools by tools' name.
        """
        while 1:
            try:
                for task in self._tasks.copy():
                    task_assigned = False
                    
                    # print(f"all tools:", self._tools.tools.keys())
                    for tool_ref in self._tools.get_tools_by_name(task.tool_name):
                        if tool_ref.status is None:
                            continue
                        elif not tool_ref.status.status in (Status.READY, Status.STOPPED):
                            continue
                        
                        msg, status = tool_ref.send_command(Trigger.START, task.data)
                        if status:
                            task_assigned = True
                            print(f"assigned task {id(task)} to {tool_ref.uuid} succeeded")
                            break
                        else:
                            print(f"trying to assign task {id(task)} to {tool_ref.uuid} failed due to {msg}")
                    if task_assigned:
                        self._tasks.remove(task)
                    else:
                        print(f"all tools for {task.tool_name} are busy, waiting...")

            except Exception as e:
                import traceback

                traceback.print_exc()
            finally:
                time.sleep(1)

    def _task_handle_message(self):
        """
        Handle websocket messages
        """
        while 1:
            msg: WSToolRawMsgType
            tool_ref, msg = self._ws_recv_msg_queue.get()
            tool_msg = WSToolMsgParser().parse_tool_msg(msg)
            if isinstance(tool_msg, StatusInfo):
                tool_ref.update_status_info(tool_msg)
                logger.debug(
                    f"tool {tool_ref.name}#{tool_ref.uuid} status: {tool_ref.status.status if tool_ref.status is not None else "unknown"}!"
                )
            elif isinstance(tool_msg, Result):
                logger.debug(f"tool {tool_ref.name}#{tool_ref.uuid} got result: {tool_msg}")
                self._results.put(tool_msg)
            elif isinstance(tool_msg, SchedulerCommandResponse):
                tool_ref.put_response(tool_msg)
                print(tool_msg, "scheduler-command-resp")
            else:
                raise NotImplementedError(tool_msg)

    def _start_tasks(self):
        self._message_handling_thread.start()
        self._tasks_scheduling_thread.start()

    def start(self, debug=False):
        self._start_tasks()
        self.app.run(host=self.host, debug=debug, port=self.port)

    def start_in_thread(self):
        self.th = threading.Thread(target=self.start)
        self.th.setDaemon(True)
        self.th.start()
        logger.info("scheduler started!")
