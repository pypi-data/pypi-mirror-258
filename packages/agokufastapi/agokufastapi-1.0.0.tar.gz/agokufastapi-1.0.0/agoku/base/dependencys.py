from typing import Annotated

from fastapi import Depends, Request, BackgroundTasks
from agoku.base.context import goku_app_context
from agoku.uitls.body_parse import get_body, get_body_json


class GlobalContextRequest:
    """
    全局请求上下文类
    curr_global_dependencies = [Depends(GlobalContextRequest())]

    Attributes:
        dependencie_name (str): 依赖名称
    """

    def __init__(self, *, dependencie_name: str = 'dependencie_name'):
        self.dependencie_name = dependencie_name

    async def __call__(self, request: Request, background_tasks: BackgroundTasks, bodys=Depends(get_body_json)):
        """
        请求上下文管理器
        Args:
            request (Request): 请求对象

        Returns:
            None
        """
        pass
        # 触发请求开始事件
        # goku_app_context.async_emitter.emit('on_request_start', request)
        goku_app_context.sync_emitter.emit('on_request_start', request)
        # 设置请求上下文
        with goku_app_context.scope('request', request):
            with goku_app_context.scope('background_tasks', background_tasks):
                request.state.current_background_tasks = background_tasks
                try:
                    yield
                finally:
                    # 清空当前的请求
                    pass
                # print('goku_app_context',goku_app_context.response)
