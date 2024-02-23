#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import abc

from fastapi import FastAPI
import logging


class IApplicationBuilder():
    """IApplicationBuilder接口类"""

    @classmethod
    @abc.abstractmethod
    def with_environment_settings(cls) -> 'IApplicationBuilder':
        """
        创建一个新的IApplicationBuilder实例用于设置环境参数

        Returns:
            IApplicationBuilder: IApplicationBuilder实例
        """
        raise NotImplemented

    @abc.abstractmethod
    def _instance_app(self) -> FastAPI:
        """
        创建FastAPI实例

        Returns:
            FastAPI: FastAPI实例
        """
        raise NotImplemented

    def _register_health_checks(self, app: FastAPI):
        """
        注册健康检查路由

        Args:
            app (FastAPI): FastAPI实例
        """
        pass

        @app.get("/health_checks", tags=['健康检查模块'], summary='健康检查接口')
        async def health_checks():
            return "ok"

    @abc.abstractmethod
    def _register_loguru_log_client(self, app: FastAPI) -> None:
        """
        注册自定义的日志配置插件

        Args:
            app (FastAPI): FastAPI实例
        """
        raise NotImplemented

    @abc.abstractmethod
    def _register_global_request(self, app: FastAPI) -> None:
        """
        注册全局请求

        Args:
            app (FastAPI): FastAPI实例
        """
        raise NotImplemented

    @abc.abstractmethod
    def _register_exception_handlers(self, app: FastAPI) -> None:
        """
        注册异常处理中间件

        Args:
            app (FastAPI): FastAPI实例
        """
        raise NotImplemented

    @abc.abstractmethod
    def _register_plugins(self, app: FastAPI) -> None:
        """
        注册插件

        Args:
            app (FastAPI): FastAPI实例
        """
        raise NotImplemented

    @abc.abstractmethod
    def _register_routes(self, app: FastAPI) -> None:
        """
        注册路由

        Args:
            app (FastAPI): FastAPI实例
        """
        raise NotImplemented

    @abc.abstractmethod
    def _register_middlewares(self, app: FastAPI) -> None:
        """
        注册中间件

        Args:
            app (FastAPI): FastAPI实例
        """
        raise NotImplemented

    def build(self) -> FastAPI:
        """
        构建项目

        Returns:
            FastAPI: FastAPI实例
        """
        try:
            # 约束注册流程-避免错误
            logging.critical(f'约束注册流程')
            # 创建实例对象
            app = self._instance_app()
            # 执行错误注册
            # 执行自定义的日志配置插件放在最后执行，以便获取到上下文的实例对象
            self._register_loguru_log_client(app)
            self._register_exception_handlers(app)
            # 执行插件的注册----优先于路由注册，避免部分的全局对象加载问题
            self._register_plugins(app)
            # 执行中间件的注册
            self._register_middlewares(app)
            # 注册全局请求，最外层进行注册
            self._register_global_request(app)
            # 注册路由
            self._register_routes(app)
            # 健康检查路由
            self._register_health_checks(app)
            return app
        except Exception as e:
            logging.critical(f'项目启动失败:{e}')
            raise e
