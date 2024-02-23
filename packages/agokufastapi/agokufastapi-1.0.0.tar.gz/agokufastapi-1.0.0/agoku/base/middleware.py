from starlette.middleware import _MiddlewareClass, P
from starlette.requests import Request
import typing
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from starlette.responses import Response

import json
from typing import Optional
from pydantic import BaseModel, Field

from agoku.base.context import goku_app_context


class ResponseInfo(BaseModel):
    headers: Optional[Headers] = Field(default=None, title="Response header")
    body: str = Field(default="", title="Response body")
    status_code: Optional[int] = Field(default=None, title="Status code")

    class Config:
        arbitrary_types_allowed = True


class GokuMiddleware:

    def __init__(self, *, app: ASGIApp, is_proxy=True):
        self.app = app
        self.is_proxy = is_proxy
        self.request: typing.Optional[Request] = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        # 和上面的判断类似
        if scope["type"] not in ["http", 'websocket']:
            await self.app(scope, receive, send)
            return

        # 解决读取BODY问题
        if self.is_proxy:
            receive_ = await receive()

            async def receive():
                return receive_

        # 这里考虑直接读取一次body然后保存到对应的上下文中
        # 解析当前的请求体
        self.request = Request(scope, receive=receive)
        # 解析报文体内容
        response_info = ResponseInfo()

        # 下一个循环体
        async def _next_send(message: Message) -> None:
            if message.get("type") == "http.response.start":
                print("请求开始")
                response_info.headers = Headers(raw=message.get("headers"))
                response_info.status_code = message.get("status")
            # 解析响应体内容信息
            elif message.get("type") == "http.response.body":
                print("解析响应报文")
                if body := message.get("body"):
                    response_info.body += body.decode("utf8")

                response = Response(content=response_info.body,
                                    status_code=response_info.status_code,
                                    headers=dict(response_info.headers)
                                    )
                with goku_app_context.scope('response', response):
                    pass
                    try:
                        goku_app_context.sync_emitter.emit('on_request_finished',self.request, response)
                    except AttributeError as e:
                        self.request.app.sync_emitter.emit('on_request_finished',self.request, response)


            await send(message)

        try:
            await self.app(scope, receive, _next_send)
        finally:
            pass
