import json
from dataclasses import dataclass
from typing import Generic, Tuple, Type

import requests

from .messages import RestRespDataType, RestResponse


class Request(Generic[RestRespDataType]):
    def __init__(
        self,
        host: str,
        port: int,
        router: str,
        resp_cls: Type[RestRespDataType],
        timeout=5,
        log=False,
    ) -> None:
        self.router = ("/" if not router.startswith("/") else "") + router
        self.url = f"http://{host}:{port}" + self.router
        self.log = log
        self._resp_cls = resp_cls
        self.timeout = timeout
        print("request created to url:", self.url)

    def _convert_response(
        self, response: requests.Response
    ) -> Tuple[int, RestResponse[RestRespDataType]]:
        resp_raw = RestResponse.from_json(response.text)
        if resp_raw.data is not None:
            data_raw: dict = resp_raw.data
            resp: RestResponse[RestRespDataType] = RestResponse(
                resp_raw.msg, self._resp_cls.from_dict(data_raw)
            )
            return (response.status_code, resp)
        else:
            return (response.status_code, resp_raw)

    def get(self, params) -> Tuple[int, RestResponse[RestRespDataType]]:
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            self.url, params=params, timeout=self.timeout, headers=headers
        )
        try:
            return self._convert_response(response)
        except json.JSONDecodeError:
            raise NotImplementedError((response.status_code, response.text))

    def post(self, data: dict) -> Tuple[int, RestResponse[RestRespDataType]]:
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self.url, data=json.dumps(data), timeout=self.timeout, headers=headers
        )

        return self._convert_response(response)

    def upload(self, file_path: str) -> Tuple[int, RestResponse[RestRespDataType]]:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f)}

            response = requests.post(
                self.url,
                files=files,
                timeout=self.timeout,
            )

        return self._convert_response(response)


@dataclass
class RequestFactory(Generic[RestRespDataType]):
    host: str
    port: int

    def create_request(
        self, router: str, resp_cls: Type[RestRespDataType], timeout=5
    ) -> Request[RestRespDataType]:
        return Request(self.host, self.port, router, resp_cls, timeout=timeout)
