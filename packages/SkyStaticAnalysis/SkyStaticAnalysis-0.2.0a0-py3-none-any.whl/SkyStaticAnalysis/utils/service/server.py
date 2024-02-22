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
from enum import Enum

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum
import uuid
from SkyStaticAnalysis.third_parties.jsonobject.properties import ObjectProperty

from SkyStaticAnalysis.utils.files import file_to_dataurl

from .states import StateMachine
from .processmgr import SubprocessManager
from ..functional import sky_generator, SkyGenerator, SkyFrozenGenerator
from flask import Flask, abort, make_response, redirect, request, send_from_directory
from flask_sock import Sock


class Status(StrEnum):
    READY = "ready"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
    STOPPED = "stopped"  # stopped manually


class Trigger(str, Enum):
    START = "start"  # 开始分析，需要带有参数
    STOP = "stop"  # 强制杀死进程


class BaseCommand(JsonObject):
    type: Trigger = cast(
        Trigger,
        StringProperty(required=True, choices=list(Trigger.__members__.values())),
    )


C = TypeVar("C", bound=BaseCommand)

# sock = Sock(app)


# @sock.route("/echo")
# def echo(ws):
#     while True:
#         data = ws.receive()
#         ws.send(data)


class ResultInfo(JsonObject):
    uuid: str = cast(str, StringProperty())
    start_time: float = cast(float, FloatProperty())
    end_time: float = cast(float, FloatProperty())
    status: str = cast(
        Trigger, StringProperty(choices=[str(s) for s in Status.__members__.values()])
    )


class Position(JsonObject):
    type = StringProperty(required=True)
    line = IntegerProperty()
    column = IntegerProperty()
    text = StringProperty()  # 对错误位置的文字描述

    @classmethod
    def textual(cls, text):
        return cls(type="text", text=text)

    @classmethod
    def line_col(cls, line, column=-1):
        return cls(type="line_col", line=line, column=column)


class Problem(JsonObject):
    file: str = cast(str, StringProperty())  # 出问题的文件
    description: str = cast(str, StringProperty())  # 出问题的描述
    position: Position = cast(Position, ObjectProperty(Position))


class Result(JsonObject):
    info: ResultInfo = ResultInfo()
    problems = cast(List[Problem], ListProperty(Problem))
    raw_file = cast(str, StringProperty())  # 原始文件，以url的形式


class ProcessContext:
    def __init__(self, root_folder: str, ctx_id: str) -> None:
        self.root_folder = root_folder
        self.info = ResultInfo(
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


class Server(Generic[C]):
    def __init__(
        self,
        cmd_type: Type[C],
        host: str = "0.0.0.0",
        port: int = 8681,
        root_folder=".skystaticanalysis",
    ) -> None:
        self.root_folder = root_folder
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)
        self._cmd_type: Type[C] = cmd_type
        abs_path = lambda f: os.path.abspath(os.path.join(os.path.dirname(__file__), f))

        self.app = Flask(__name__, static_folder=abs_path("./static"))
        self.port = port
        self.host = host
        self.process_mgr = SubprocessManager(self.on_task_finish)

        def handle_root():
            return redirect("/index.html")

        def send_file(filename):
            assert self.app.static_folder is not None
            return send_from_directory(self.app.static_folder, filename)

        self.app.add_url_rule("/", view_func=handle_root)
        self.app.add_url_rule(
            "/<path:filename>",
            view_func=send_file,
        )
        self.app.add_url_rule(
            "/command", view_func=self.handle_command, methods=["POST"]
        )
        self.app.add_url_rule("/status", view_func=self.handle_status, methods=["GET"])
        self.app.add_url_rule("/result", view_func=self.handle_result, methods=["GET"])
        self.app.add_url_rule(
            "/results", view_func=self.handle_results, methods=["GET"]
        )
        self.app.add_url_rule(
            "/rules-edit", view_func=self.handle_rules, methods=["GET"]
        )
        self.current_context: Optional[
            ProcessContext
        ] = None  # ProcessContext(self.root_folder)

    def on_task_finish(self, task_id: str):
        assert self.current_context is not None
        self.current_context.info.status = Status.STOPPED
        self.handle_task_finish()

    def handle_task_finish(self):
        return

    def handle_rules(self):
        return self.rules()

    def rules(self):
        return [
            {"type": "input", "field": "goods_name", "title": "商品名称"},
            {"type": "datePicker", "field": "created_at", "title": "创建时间"},
        ]

    def handle_status(self):
        if self.current_context is not None:
            return self.current_context.info.to_json()
        else:
            return ResultInfo(
                uuid="", start_time=-1, end_time=-1, status=Status.STOPPED
            ).to_json()

    @sky_generator
    def all_results(self) -> Generator[Tuple[str, ResultInfo], None, None]:
        for folder in os.listdir(self.root_folder):
            folder_abs_path = os.path.join(self.root_folder, folder)
            try:
                with open(
                    os.path.join(folder_abs_path, ".processinfo.json"), encoding="utf8"
                ) as f:
                    yield folder_abs_path, ResultInfo(**json.load(f))
            except Exception:
                import traceback

                traceback.print_exc()

    def results(self) -> SkyFrozenGenerator[Tuple[str, ResultInfo]]:
        """
        Get all results, and sort by start time
        """
        return self.all_results().f.sort(lambda item: item[1].start_time, reverse=True)

    def handle_result(self) -> Dict[str, Any]:
        if self.current_context is None:
            return {"id": None, "status": "failed", "message": "no result file now!"}
        result_file = self.result_file()
        if not os.path.isabs(result_file):
            result_file = os.path.join(self.current_context.data_folder, result_file)
        return Result(
            info=self.current_context.info.to_json(),
            problems=self.current_context.found_problems,
            raw_file=file_to_dataurl(result_file),
        ).to_json()

    def result_file(self) -> str:
        raise NotImplementedError

    def handle_results(self):
        return self.results().map(lambda x: x.to_json()).l

    def current_analysis(self):
        pass

    def handle_command(self):
        data = json.loads(request.data)
        cmd: C = self._cmd_type(data)
        if cmd.type == Trigger.START:
            self.current_context = ProcessContext(self.root_folder, uuid.uuid4().hex)
            self.handle_start_tool(cmd)
            self.current_context.info.status = Status.RUNNING
            return {
                "id": self.current_context.info.uuid,
                "status": "success",
                "message": "started!",
            }
        elif cmd.type == Trigger.STOP:
            if self.current_context is None:
                return {
                    "message": "no process is runnings",
                    "status": "failed",
                    "id": self.current_context.info.uuid,
                }
            self.handle_stop_tool(cmd)
            self.current_context.info.status = Status.STOPPED
            self.current_context.info.end_time = time.time()
            self.current_context.dump()
            return {
                "id": self.current_context.info.uuid,
                "status": "failed",
                "message": "cannot ",
            }
        else:
            raise NotImplementedError

    def handle_start_tool(self, data: C):
        pass

    def handle_stop_tool(self, data: C):
        pass

    def start(self, debug=False):
        self.app.run(host=self.host, debug=debug, port=self.port)

    def start_in_thread(self):
        self.th = threading.Thread(target=self.start)
        self.th.setDaemon(True)
        self.th.start()
        print("started!")
