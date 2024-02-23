from contextvars import ContextVar
import inspect

from agoku.uitls.singleton import Singleton

if hasattr(inspect, 'Parameter') and hasattr(inspect.Parameter, 'empty'):
    # 使用新版本的写法（Python 3.10+）
    empty_value = inspect.Parameter.empty
else:
    # 使用旧版本的写法
    empty_value = inspect._empty

from types import MappingProxyType
from typing import Dict, Any, Mapping, Iterator
from contextlib import contextmanager



class GokuContextRepo(Singleton):
    """一个用于表示上下文存储器的类。"""
    _global_context: Dict[str, Any]  # 全局上下文字典，存储键值对数据,类似全局变量
    _scope_context: Dict[str, ContextVar[Any]]  # 范围上下文字典，存储键值对数据，其中值为ContextVar对象

    def __init__(self) -> None:
        # 创建一个字典，键为"context"，值为self
        self._global_context = {"context": self}
        # 创建一个空字典
        self._scope_context = {}
        # 使用self._global_context创建一个MappingProxyType对象，并将其赋值给self._read_only_global_context
        # 你想要保护一个字典，防止它被修改，或者当你想要创建一个只读的字典视图时。
        # 例如，你可以使用 MappingProxyType 来包装一个字典，这样对这个字典的所有修改都会被忽略，从而保护里面的数据。
        self._read_only_global_context = MappingProxyType(self._global_context)

    def set_global(self, key: str, v: Any) -> None:
        """设置全局上下文的值。"""
        if key not in self._global_context:
            self._global_context[key] = v

    def reset_global(self, key: str) -> None:
        """重置全局上下文的值。"""
        self._global_context.pop(key, None)

    def set_local(self, key: str, value: Any) -> "ContextVar[Any].Token":
        """设置局部上下文的值。"""
        context_var = self._scope_context.get(key)
        if context_var is None:
            context_var = ContextVar(key, default=None)
            self._scope_context[key] = context_var
        return context_var.set(value)

    def reset_local(self, key: str, token: "ContextVar[Any].Token") -> None:
        """重置局部上下文的值。"""
        self._scope_context[key].reset(token)

    def get_local(self, key: str, default: Any = None) -> Any:
        """获取局部上下文的值。"""
        context_var = self._scope_context.get(key)
        return context_var.get() if context_var is not None else default

    def clear(self) -> None:
        """清空上下文存储器。"""
        self._global_context = {"context": self}
        self._scope_context.clear()

    def get(self, key: str, default: Any = None) -> Any:
        """获取全局上下文的值。,如果没有则获取局部的"""
        return self._global_context.get(key, self.get_local(key, default))

    def resolve(self, argument: str) -> Any:
        """解析复杂键。
        这个函数用于解析一个复杂键，即键中包含点号分隔的多个部分。首先根据点号分割键字符串，获取第一个部分first，
        然后通过self.get方法获取对应的值v。如果v为None，则抛出AttributeError异常。
        接着遍历剩余的部分列表keys，依次获取v的对应值。
        如果在获取值的过程中出现KeyError或AttributeError异常，则抛出AttributeError异常。最后返回解析得到的值v。
        Args:
            argument (str): 复杂键字符串。

        Returns:
            Any: 解析得到的值。

        Raises:
            AttributeError: 当self.get(first, None)返回None时，表示`self.context`不包含`first`键。
            AttributeError: 当v为None时，尝试访问v[i]或getattr(v, i)会引发KeyError或AttributeError。

        """
        first, *keys = argument.split(".")

        v = self.get(first, None)
        if v is None:
            raise AttributeError(f"`{self.context}` does not contain `{first}` key")

        for i in keys:
            try:
                v = v[i] if isinstance(v, Mapping) else getattr(v, i)
            except (KeyError, AttributeError):
                raise AttributeError(f"Attribute `{i}` not found in context")
        return v

    def resolve_context_by_name(self,
                                name: str,
                                default: Any,
                                ) -> Any:
        """动态获取上下文的值。
            #
            # contextIOOI.set_global('config', {'database': {'host': 'localhost', 'port': 3306}})
            # # 解析一个深层嵌套的键
            # db_port = contextIOOI.resolve_context_by_name(name='config.database.port',default=2)  # 输出: 3306
        """
        value: Any = empty_value

        try:
            value = self.resolve(name)

        except (KeyError, AttributeError):
            if default is not empty_value:
                value = default
                self.set_global(name, value)
        return value

    def __getattr__(self, __name: str) -> Any:
        """动态获取上下文的值。"""
        return self.get(__name)

    @property
    def context(self) -> Mapping[str, Any]:
        """获取上下文映射。
        这个函数返回一个上下文映射，它包含全局上下文和作用域上下文。全局上下文是一个只读的字典，作用域上下文是一个字典，其中的值是可调用的对象。
        函数使用字典解包来合并这两个上下文，形成最终的上下文映射。
        """
        return {**self._read_only_global_context, **{i: j.get() for i, j in self._scope_context.items()}}

    @contextmanager
    def scope(self, key: str, value: Any) -> Iterator[None]:
        """创建一个上下文作用域。"""
        token = self.set_local(key, value)
        try:
            yield
        finally:
            self.reset_local(key, token)


from typing import cast

# cast 函数在这里的作用是将 GokuContextRepo() 的实例强制转换为 GokuContextRepo 类型。
# 这样做是为了解决静态类型检查器无法推断 FastAppContextRepo() 的类型的问题。
# 使用 cast 函数可以显式地告诉类型检查器我们希望将其视为 FastAppContextRepo 类型。
goku_app_context: GokuContextRepo = cast(GokuContextRepo, GokuContextRepo())  # type: ignore[redundant-cast]

#
# contextIOOI.set_global('config', {'database': {'host': 'localhost', 'port': 3306}})
# # 解析一个深层嵌套的键
# db_port = contextIOOI.resolve_context_by_name(name='config.database.port',default=2)  # 输出: 3306
# print(db_port)
# # 使用上下文管理器在作用域内设置局部变量
# with contextIOOI.scope('key3', 'value3'):
#     scoped_value = contextIOOI.get('key3')  # 输出: 'value3'
#     print("aasaas",scoped_value)
# # 作用域结束后，key3会被自动重置
# # 设置全局上下文
# # 通过属性访问全局上下文
# # app_name = contextIOOI.app_name  # 输出: 'MyApp'
# # print("app_name",app_name.name,app_name.age)
#
