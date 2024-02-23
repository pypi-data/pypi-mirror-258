import asyncio
import typing
from contextlib import asynccontextmanager
from typing import Callable, Annotated

import aiojobs
from fastapi import FastAPI
from fastapi.types import DecoratedCallable
from pyee import EventEmitter, AsyncIOEventEmitter

from agoku.base.context import goku_app_context
from agoku.base.dependencys import GlobalContextRequest
from fastapi import Depends

from agoku.base.middleware import GokuMiddleware



class GokuFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):

        # 创建事件发射器--用户同步执行逻辑的时候的事件处理
        self.sync_emitter = EventEmitter()
        # 创建异步事件发射器--可用户类似后台异步任务的处理，单仅限于在异步事件循环中执行相关发布任务
        self.async_emitter = AsyncIOEventEmitter()
        self.async_background_aiojobs = None

        # 设置全局的依赖注入项
        curr_global_dependencies = [Depends(GlobalContextRequest())]
        if kwargs.get('dependencies'):
            curr_global_dependencies += kwargs.get('dependencies')
            kwargs.pop('dependencies')
        # 设置生命周期回调
        curr_lifespan = self.lifespan
        super().__init__(*args, **kwargs, lifespan=curr_lifespan, dependencies=curr_global_dependencies)
        # self.add_middleware(GokuMiddleware, is_proxy=True)
        self.add_middleware(GokuMiddleware,is_proxy=True)

    def init_global_goku_app_context(self,app: "GokuFastAPI"):
        # 设置全局的依赖注入项-sync_emitter
        goku_app_context.set_global('sync_emitter', self.sync_emitter)
        #  设置全局的依赖注入项- async_emitter
        goku_app_context.set_global('async_emitter', self.async_emitter)
        goku_app_context.set_global('async_background_aiojobs', self.async_background_aiojobs)

    @asynccontextmanager
    async def lifespan(self,app: "GokuFastAPI"):
        # 启动事件
        app.emit_startup_server()
        # 创建异步任务调度器--用于异步任务调度
        app.async_background_aiojobs = aiojobs.Scheduler()
        # 创建异步任务调度器--用于异步任务调度
        app.init_global_goku_app_context(app)
        #  设置全局的依赖注入项- async_background_aiojobs
        goku_app_context.set_global('async_background_aiojobs', app.async_background_aiojobs)
        # 生命周回调
        yield
        # 关闭事件
        app.emit_shutdown_server()

    def add_plugin(self, plugin_class, name, *args, **kwargs) -> None:
        # 创建插件实例，并使用提供的参数
        plugin_instance = plugin_class(name=name, *args, **kwargs)
        # 调用插件实例的 setup 方法，传入当前应用实例（self）
        plugin_instance.setup(app=self)


    def on_emitter_event(
            self, event_type: Annotated[str, ...] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            # 判断函数是否是异步函数
            if asyncio.iscoroutinefunction(func):
                # 若是异步函数，则使用async_emitter对象的on方法注册事件和函数
                self.async_emitter.on(event_type if event_type else func.__name__, func)
            else:
                # 若不是异步函数，则使用sync_emitter对象的on方法注册事件和函数
                self.sync_emitter.on(event_type if event_type else func.__name__, func)
            return func

        return decorator

    def emit_request_start_sync(self, request):
        """
        同步地发出请求开始事件。

        参数：
        - self：当前对象的引用
        - request：请求对象
        """
        self.sync_emitter.emit('on_request_start', request)

    def emit_request_finished_sync(self, request, response):
        """
        同步地发出请求完成事件。

        参数：
        - self：当前对象的引用
        - request：请求对象
        - response：响应对象
        """
        self.sync_emitter.emit('on_request_finished', request, response)

    def emit_startup_server(self):
        """
        同步地发出请求开始事件。

        参数：
        - self：当前对象的引用
        - request：请求对象
        """
        self.sync_emitter.emit('on_startup', self)

    def emit_shutdown_server(self):
        """
        同步地发出请求开始事件。

        参数：
        - self：当前对象的引用
        - request：请求对象
        """
        self.sync_emitter.emit('on_shutdown', self)



