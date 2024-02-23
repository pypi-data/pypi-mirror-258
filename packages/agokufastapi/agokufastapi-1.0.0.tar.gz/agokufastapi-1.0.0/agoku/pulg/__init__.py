import abc
from typing import Annotated

from agoku.base.context import goku_app_context
from agoku.base.gokuapp import GokuFastAPI
from fastapi import Request


class PluginException(Exception):
    """查询异常的定义"""


class IBasePlugin(metaclass=abc.ABCMeta):
    """插件基础定义"""

    name: str
    describe: str  # 描述
    app: GokuFastAPI = None
    request: Annotated[Request, goku_app_context.request] = None

    def __init__(self, name=None, describe=None, **options):
        """创建应用的插件"""
        self.name = name or self.name
        self.describe = describe

    def __repr__(self) -> str:
        """输出插件信息"""
        return f"<FastAPI.Exts.Plugin: {self.name}>"

    @property
    def installed(self):
        """检测插件是否已安装"""
        return bool(self.app)

    def setup(self, app: GokuFastAPI, name: str = None, **options):
        self.app= app
        app.on_emitter_event(event_type='on_startup')(lambda: self.on_startup(name))
        app.on_emitter_event(event_type='on_shutdown')(lambda: self.on_shutdown(name))
        app.on_emitter_event(event_type='on_request_start')(lambda req: self.on_request_start(req))
        app.on_emitter_event(event_type='on_request_finished')(lambda req, resp: self.on_request_finished(req, resp))

    @abc.abstractmethod
    def on_startup(self, name):
        pass

    @abc.abstractmethod
    def on_shutdown(self, name):
        pass

    @abc.abstractmethod
    def on_request_start(self, request):
        pass

    @abc.abstractmethod
    def on_request_finished(self, request, response):
        pass
