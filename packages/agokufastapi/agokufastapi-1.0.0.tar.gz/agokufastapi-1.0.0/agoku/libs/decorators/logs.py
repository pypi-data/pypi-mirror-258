"""
这个模块提供了装饰器，旨在为使用的函数提供额外的功能。
"""
import asyncio

import logging
from time import perf_counter
from typing import Any
import functools
from typing import Callable, TypeVar, Awaitable

from typing_extensions import ParamSpec

Params = ParamSpec("Params")
ReturnValue = TypeVar("ReturnValue")

logger: logging.Logger = logging.getLogger(__name__)


def with_logging(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    这个装饰器在函数开始和结束执行时记录日志。
    :param func: 要装饰的函数
    :type func: Callable[..., Any]
    :return: 记录了调用信息的装饰函数
    :rtype: Callable[..., Any]
    """

    @functools.wraps(func)
    def sync_wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        添加日志功能的同步包装函数
        :param args: 传递给装饰函数的位置参数
        :type args: tuple[Any, ...]
        :param kwargs: 传递给装饰函数的关键字参数
        :type kwargs: dict[str, Any]
        :return: 装饰函数执行的结果
        :rtype: Any
        """
        logger.info("调用 %s", func.__name__)
        value = func(*args, **kwargs)
        logger.info("完成 %s", func.__name__)
        return value

    @functools.wraps(func)
    async def async_wrapper(
            *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Any:
        """
        添加日志功能的异步包装函数
        :param args: 传递给装饰函数的位置参数
        :type args: tuple[Any, ...]
        :param kwargs: 传递给装饰函数的关键字参数
        :type kwargs: dict[str, Any]
        :return: 装饰函数执行的结果
        :rtype: Any
        """
        logger.info("调用 %s", func.__name__)
        value = await func(*args, **kwargs)
        logger.info("完成 %s", func.__name__)
        return value

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    通过记录装饰函数的执行时间，提供基准测试的功能
    :param func: 要执行的函数
    :type func: Callable[..., Any]
    :return: 添加了基准测试功能的装饰函数
    :rtype: Callable[..., Any]
    """

    @functools.wraps(func)
    def sync_wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        添加基准测试功能的同步包装函数
        :param args: 传递给装饰函数的位置参数
        :type args: tuple[Any, ...]
        :param kwargs: 传递给装饰函数的关键字参数
        :type kwargs: dict[str, Any]
        :return: 装饰函数执行的结果
        :rtype: Any
        """
        start_time: float = perf_counter()
        value = func(*args, **kwargs)
        end_time: float = perf_counter()
        run_time: float = end_time - start_time
        logger.info("%s的执行需要 %s 秒。", func.__name__, run_time)
        return value

    @functools.wraps(func)
    async def async_wrapper(
            *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Any:
        """
        添加基准测试功能的异步包装函数
        :param args: 传递给装饰函数的位置参数
        :type args: tuple[Any, ...]
        :param kwargs: 传递给装饰函数的关键字参数
        :type kwargs: dict[str, Any]
        :return: 装饰函数执行的结果
        :rtype: Any
        """
        start_time: float = perf_counter()
        value = await func(*args, **kwargs)
        end_time: float = perf_counter()
        run_time: float = end_time - start_time
        logger.info("%s的执行需要 %s 秒。", func.__name__, run_time)
        return value

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def fun_hooks(
        f: Callable[Params, Awaitable[ReturnValue]],
) -> Callable[Params, Awaitable[ReturnValue]]:
    @functools.wraps(f)
    def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> ReturnValue:
        r = f(*args, **kwargs)
        return r

    return wrapper
