import asyncio
import inspect
from threading import Thread
import logging


# 异步编程相关模块
class Worker(Thread):
    """
    工作线程类

    Args:
        name (str, optional): 工作线程的名称，默认为 "Worker"。 Defaults to "Worker".

    # 使用示例
    from goku.libs.worker import Worker
    class AlertsGather1115555(Worker):
        async def work(self):
            while True:
                print("AlertsGather1115555循环一直输出")

    class AlertsGather111(Worker):
       async def work(self):
            while True:
                pass
                print("AlertsGather111循环一直输出")

    if __name__ == '__main__':
        AlertsGather111().begin()
        AlertsGather1115555.begin()
    """

    def __init__(self, name: str = "Worker", *args, **kwargs) -> None:
        """
        工作线程的初始化方法

        Args:
            name (str, optional): 工作线程的名称，默认为 "Worker"。 Defaults to "Worker".
            *args: 可变参数列表。
            **kwargs: 可变关键字参数列表。
        """
        super().__init__(name=name, *args, **kwargs)
        self.logger = logging.getLogger("Worker")


    def run(self):
        # 启动线程时执行的方法
        self.logger.info(f"Starting worker {self.name}")
        # 使用inspect.iscoroutinefunction(self.work)检查self.work是否定义为异步函数。
        # 如果self.work是异步函数，那么：
        # 创建一个新的 asyncio 事件循环（loop = asyncio.new_event_loop()）。
        # 设置这个新创建的事件循环为当前活动的事件循环（asyncio.set_event_loop(loop)）。
        # 在日志中记录“Asynchronous”，表示即将执行异步操作。
        # 使用asyncio.Task(self.work())将异步函数封装为一个任务，并通过add_done_callback添加回调函数，当任务完成后调用loop.shutdown_asyncgens()清理生成器。
        # 调用loop.run_until_complete(task)来运行并等待此异步任务完成。
        # 完成任务后关闭事件循环（loop.close()）。
        # 如果self.work不是异步函数（即同步函数），直接调用并执行self.work()。
        try:
            # 检查工作方法是否为异步函数
            if inspect.iscoroutinefunction(self.work):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                self.logger.info("Asynchronous")
                # 运行异步函数，添加了异常处理
                task = asyncio.Task(self.work())
                task.add_done_callback(lambda t: loop.shutdown_asyncgens())
                loop.run_until_complete(task)
                loop.close()
            else:
                # 运行同步函数
                self.work()
        except Exception as e:
            self.logger.error(f"An error occurred in worker {self.name}: {e}")

    @classmethod
    def begin(cls, name: str = "Worker", *args, **kwargs) -> 'Worker':
        # 创建并返回一个 Worker 实例
        instance = cls(name=name, *args, **kwargs)
        instance.start()
        # instance.join()
        return instance

    def work(self) -> None:
        # 占位符
        pass

if __name__ == '__main__':
    class AlertsGather1115555(Worker):
        async def work(self):
            while True:
                print("AlertsGather1115555循环一直输出")


    class AlertsGather111(Worker):
        async def work(self):
            while True:
                pass
                print("AlertsGather111循环一直输出")


    if __name__ == '__main__':
        AlertsGather111().begin()
        AlertsGather1115555.begin()